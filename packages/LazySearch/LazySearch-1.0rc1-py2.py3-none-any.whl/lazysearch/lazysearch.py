import os
import uuid
import tantivy
import datetime
import diskcache
from collections.abc import MutableMapping

try:
    from . import simple_pattern
except:
    import simple_pattern


def flatten_dict(dictionary, parent_key=(), meta={}):
    items = []
    for key, value in dictionary.items():
        if not isinstance(key, str):
            if key not in meta:
                uid = f"_key.{uuid.uuid4()}"
                meta[uid] = key
                key = uid

        new_key = parent_key + (key,)
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, meta))
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten_dict({k: v}, new_key, meta))
        else:
            items.append((list(new_key), value))

    return items


def get_schema(tokenizer):
    schema = tantivy.SchemaBuilder()

    schema.add_text_field(name="_id", tokenizer_name="raw", stored=True)

    schema.add_text_field(name="key", tokenizer_name="raw", stored=True)

    schema.add_text_field(name="value", tokenizer_name=tokenizer, stored=False)

    schema.add_text_field(name="patterns", tokenizer_name="raw", stored=False)

    schema.add_unsigned_field(name="num", stored=False, fast="single")

    schema = schema.build()

    return schema


class Index:
    def __init__(
        self,
        index_name,
        index_path=None,
        tokenizer="default",
        tantivy_ram_size_in_gb=0.25,
        tantivy_threads=0,
    ):
        if not index_path:
            index_path = os.path.join(
                os.path.expanduser("~"), os.path.join("LazySearch", index_name)
            )

        schema = get_schema(tokenizer)

        index_path = os.path.join(index_path, "index")

        try:
            if not os.path.exists(index_path):
                os.makedirs(index_path)
        except:
            pass

        self.INDEX = tantivy.Index(schema, index_path, reuse=True)
        self.WRITER = self.INDEX.writer(
            heap_size=int(tantivy_ram_size_in_gb * 1073741824),
            num_threads=tantivy_threads,
        )
        self.SEARCHER = self.INDEX.searcher()

        meta_index_path = os.path.join(index_path, "meta")

        try:
            if not os.path.exists(meta_index_path):
                os.makedirs(meta_index_path)
        except:
            pass

        self.META = diskcache.Index(meta_index_path)

    def index(self, in_data):
        if not isinstance(in_data, list):
            in_data = [in_data]

        uuids = []

        for _d in in_data:
            _id = _d.get("_id")
            if _id:
                del _d["_id"]
            else:
                _id = f"{uuid.uuid4()}"

            self.META[f"id.{_id}"] = _d

            _d = flatten_dict(_d, meta=self.META)

            for key, value in _d:
                if isinstance(value, str):
                    self.WRITER.add_document(
                        tantivy.Document.from_dict(
                            {
                                "_id": _id,
                                "key": key,
                                "value": value,
                                "patterns": simple_pattern.string_to_word_patterns(
                                    value
                                ),
                                "num": [],
                            }
                        )
                    )

                elif isinstance(value, datetime.datetime):
                    self.WRITER.add_document(
                        tantivy.Document.from_dict(
                            {
                                "_id": _id,
                                "key": key,
                                "value": [],
                                "patterns": [],
                                "num": value.timestamp(),
                            }
                        )
                    )

                elif isinstance(value, (int, float)):
                    self.WRITER.add_document(
                        tantivy.Document.from_dict(
                            {
                                "_id": _id,
                                "key": key,
                                "value": [],
                                "patterns": [],
                                "num": value,
                            }
                        )
                    )

                else:
                    self.WRITER.add_document(
                        tantivy.Document.from_dict(
                            {
                                "_id": _id,
                                "key": key,
                                "value": json.dumps(value),
                                "patterns": simple_pattern.string_to_word_patterns(
                                    value
                                ),
                                "num": [],
                            }
                        )
                    )

            uuids.append(_id)

        return uuids

    def commit(self):
        self.WRITER.commit()
        self.INDEX.reload()
        self.SEARCHER = self.INDEX.searcher()

    def search(
        self,
        string_query=None,
        int_query=None,
        datetime_query=None,
        pattern_query=None,
        start=0,
        n=20,
    ):

        query = []
        if (
            string_query is None
            and int_query is None
            and datetime_query is None
            and pattern_query is None
        ):
            query.append("value:*")
        else:
            if string_query:
                query.append(f"value:{string_query}")
            if pattern_query:
                query.append(
                    " OR ".join(
                        [
                            f'patterns:"{__}"'
                            for __ in simple_pattern.string_to_word_patterns(
                                pattern_query
                            )
                        ]
                    )
                )

            query = [f"({__})" for __ in query]

        query = " AND ".join(query)

        parsed_query = self.INDEX.parse_query(query, ["value", "patterns"])

        _ = self.SEARCHER.search(parsed_query, limit=n, offset=start, count=True)
        current_results, total_count = _.hits, _.count

        start = start + len(current_results)

        for score, doc_address in current_results:
            _ = self.SEARCHER.doc(doc_address)
            _id = _["_id"][0]
            _found_in_key = [
                self.META[__] if __.startswith("_key.") else __ for __ in _["key"]
            ]

            yield {
                "_id": _id,
                "source": self.META[f"id.{_id}"],
                "score": score,
                "total_count": total_count,
                "found_in_key": _found_in_key,
            }

        while start + n < total_count:
            current_results = self.SEARCHER.search(
                parsed_query, limit=n, offset=start, count=False
            ).hits
            for score, doc_address in current_results:
                _id = self.SEARCHER.doc[doc_address]._id
                yield {
                    "_id": _id,
                    "source": self.META[f"id.{_id}"],
                    "score": score,
                    "total_count": total_count,
                }


if __name__ == "__main__":
    test_index = Index("test", index_path="./test_index")
    print(
        test_index.index(
            [{"_id": "1", "d": ["a b"]}, {"c": "a", "d": [1, 2, {99: 100}]}]
        )
    )

    print(
        test_index.index(
            {
                "_id": "3",
                "pawan": [{"name": "kalyan pawan"}],
                "brother": "chiranjeevi",
                "imp_days": [datetime.datetime.now(), [datetime.datetime.now()]],
            }
        )
    )

    test_index.commit()

    print("-----------------")

    for result in test_index.search(pattern_query="xawan"):
        print(result)
