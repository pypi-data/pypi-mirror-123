import string
import hashlib

from alphabet_detector import AlphabetDetector

alphabet_detector = AlphabetDetector()

CHAR_TO_ENC = {}

for _ in "0123456789":
    CHAR_TO_ENC[_] = "N"

for _ in string.punctuation:
    CHAR_TO_ENC[_] = _

NON_LANG_CHARS = set(CHAR_TO_ENC)


def string_to_word_patterns(x):
    word_patterns = []
    for w in x.split():
        atleast_one_non_lang = False
        p = []
        for c in w:
            if c in NON_LANG_CHARS:
                atleast_one_non_lang = True

            _ = CHAR_TO_ENC.get(c)
            if _ is not None:
                if p and p[-1][0] == _:
                    p[-1] = (p[-1][0], p[-1][1] + 1)
                else:
                    p.append((_, 1))
                continue

            language = list(alphabet_detector.detect_alphabet(c))

            if language:
                language = language[0]
                if c.isupper():
                    language = f"u.{language}"

                CHAR_TO_ENC[c] = hashlib.shake_256(language.encode()).hexdigest(1)
                if p and p[-1][0] == CHAR_TO_ENC[c]:
                    p[-1] = (p[-1][0], p[-1][1] + 1)
                else:
                    p.append((CHAR_TO_ENC[c], 1))

                continue

            CHAR_TO_ENC[c] = "U"
            if p and p[-1][0] == "U":
                p[-1] = (p[-1][0], p[-1][1] + 1)
            else:
                p.append(("U", 1))

        p = [f"{c} {_}" for _, c in p]
        word_patterns += p

    return word_patterns


if __name__ == "__main__":
    print(string_to_word_patterns("Praneeth"))
    assert (
        string_to_word_patterns("Praneeth")
        == string_to_word_patterns("Araneeth")
        == string_to_word_patterns("Vraneeth")
        != string_to_word_patterns("praneeth")
    )

    print(string_to_word_patterns("+91 8011026527"))
    assert string_to_word_patterns("+91 8011026527") == string_to_word_patterns(
        "+10 1234567890"
    )

    print(string_to_word_patterns("praneeth@bpraneeth.com"))
    assert (
        string_to_word_patterns("praneeth@apraneeth.com")
        == string_to_word_patterns("praneeth@apraneeth.com")
        != string_to_word_patterns("praneeth@Ppraneeth.com")
    )
