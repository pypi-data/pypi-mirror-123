import inspect
import os
import sys
from random import choice
from typing import List


__author__ = "GLNB"
__copyright__ = "GLNB"
__license__ = "mit"


from .dictionaries import invisible_chars, dict_latin

__location__ = os.path.join(
    os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe()))
)


class Scrambler:

    # This is done by parsing the Unicode list of confusable characters.
    """

    .. code:: python

        >>> from text_scrambler import Scrambler
        >>> scr = Scrambler()
        >>> text = "This is an example"
        >>> text_1 = scr.scramble(text, level=1)
        >>> # adding only zwj/zwnj characters
        >>> print(text, text_1)
        This is an example T‍h‍i‍s‍ ‌i‍s‍ ‍a‍n‌ ‍e‌x‍a‌m‍p‍l‍e
        >>> assert text != text_1
        >>> print(text_1)
        T‍h‍i‍s‍ ‌i‍s‍ ‍a‍n‌ ‍e‌x‍a‌m‍p‍l‍e
        >>> print(len(text), len(text_1))
        18 35
        >>> text_2 = scr.scramble(text, level=2)
        >>> # replacing some latin letters by their cyrilic/greek equivalent
        >>> print(text_2)
        Тhіѕ iѕ an еxample
        >>> for char, char_2 in zip(text, text_2):
        ...     if char != char_2:
        ...             print(char, char_2)
        ...
        T Т
        i і
        s ѕ
        s ѕ
        e е
        >>> text_4 = scr.scramble(text, level=4)
        >>> # replacing all characters by any
        >>> unicode looking like character
        >>> print(text_4)
        𝕋‌h‌ⅰ‌𝗌‌ ‌𝝸‍𝘴‍‍ 𝛼‌n‍‍ 𝖊‍𝙭‌𝐚‍m‌𝜌‍Ｉ‌𝐞
        >>> versions = scr.generate(text, 10, level=4)
        >>> for txt in versions:
        ...     print(txt)
        ...
        𝘛‌h‌𝚒‌𝓼‍‌ͺ‌s‌ ‍𝛂‌ո‌ ‍ҽ‍𝕩‌𝚊‍m‍𝒑‌𞣇‍𝒆
        𐊗‍𝘩‍ı‍𝚜‌ ‌𝚒‍𐑈‌ ‌𝚊‌𝓃‌ ‍𝔢‌ᕁ‌𝖺‍m‍𝗉‍𝟣‍𝑒
        𝕿‍𝓱‌𝚒‍ꜱ‌ ‍𝗂‌ꮪ‌ ‌𝗮‌𝙣‍ ‌𝖊‍𝑥‌𝛂‌m‌𝜌‍𝕴‍𝖾
        ⊤‍𝐡‍𝓲‍ｓ‍ ‍𝞲‌𝔰‍ ‌𝐚‍𝚗‍ ‌ҽ‌𝓍‌𝚊‌m‌ρ‌׀‌ꬲ
        𝕿‍𝚑‍і‌s‌ ‌𝜾‌ѕ‌ ‍𝔞‌𝕟‍ ‌𝑒‍𝘹‍𝛼‍m‌𝟈‍ﺍ‌℮
        𝗧‌𝐡‍𝚒‍ｓ‍ ‌𝘪‍𝗌‌ ‍𝔞‍ո‍ ‍𝕖‍𝘹‌𝘢‍m‍𝜌‌𝗅‍ⅇ
        𝕋‍𝗁‍ι‍𝔰‌ ‌𝕚‍𝒔‌ ‍𝓪‍𝘯‌ ‌𝙚‍ᕁ‍𝗮‍m‌𝝔‌۱‌ｅ
        𝖳‍𝖍‌ӏ‌𝗌‍ ‍ι‍𑣁‍ ‍α‌𝒏‌ ‍𝖊‍𝘹‌𝛼‍m‌𝗽‍𝜤‌e
        𝔗‌𝓱‍ɪ‍𑣁‍ ‍𝒾‍𝒔‍ ‌𝛼‍𝓷‌‍𝖾‌𝔵‍𝖺‌m‍𝝔‍𝒍‍e
        𝚻‍𝕙‌ɪ‌𝕤‍ ‍ⅈ‍𝕤‍‌𝛂‌𝔫‍ ‍𝓮‍ｘ‌⍺‍m‌⍴‍𝐈‌𝒆
        >>> versions = scr.generate(text, 1000, level=2)
        >>> assert len(versions) == len(set(versions))
        >>> # all unique

    """

    def __init__(
        self,
        confusables_file=os.path.join(
            __location__, "txt_files", "confusablesSummary.txt"
        ),
    ):
        # The confusables can be found at:
        # https://www.unicode.org/Public/security/13.0.0/confusables.txt
        self.confusables_file = confusables_file
        self.invisible_chars = invisible_chars
        self.dict_latin = dict_latin
        self._parse_unicode_file()

    def __str__(self):
        return str(self.scramble("<__main__.Scrambler object>", level=4))

    __repr__ = __str__

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f"exc_type: {exc_type}", file=sys.stderr)
            print(f"exc_value: {exc_value}", file=sys.stderr)
            print(f"exc_traceback: {exc_traceback}", file=sys.stderr)

    def _parse_unicode_file(self) -> dict:
        """return a dict of the unicode confusable given
        the self.confusables_file"""
        self.unicode_dict = {}
        file = open(self.confusables_file, encoding="utf-8")
        ls_lines_confusable = []
        for _ in range(32):
            file.readline()
        for line in file:
            if line.startswith("#"):
                ls_lines_confusable.append(line[:-1])  # not taking the \n
        file.close()
        ls_lines_confusable = ls_lines_confusable[
            :-1
        ]  # not taking the last line (total)
        for line in ls_lines_confusable:
            _, char, *ls_chars = line.split("\t")
            if len(char) > 1:
                continue
            self.unicode_dict[char] = ls_chars

    def scramble(self, text: str, level: int = 1) -> str:
        """return the text scrambled


        :param text: the text to scramble
        :type text: str
        :param level: default to 1
        :type level: int, optional

        **level**:

        1: insert non printable characters within the text

        2: replace some latin letters to their Greek or Cyrilic equivalent

        3: insert non printable characters and change the some latin letters to their Greek or Cyrilic equivalent

        4: insert non printable chraracters change all possible letter to a randomly picked unicode letter equivalent

        :return: the scrambled string
        :rtype: str
        """
        if level not in range(1, 5):
            raise ValueError(f"level {level} not implemented")

        new_text = ""
        if level == 1:
            for char in text:
                new_text += char + choice(self.invisible_chars)
        elif level == 2:
            for char in text:
                new_text += choice(self.dict_latin.get(char, []) + [char])
            new_text += " "
        elif level == 3:
            for char in text:
                new_text += choice(self.dict_latin.get(char, []) + [char]) + choice(
                    self.invisible_chars
                )
        elif level == 4:
            for char in text:
                new_text += choice(self.unicode_dict.get(char, []) + [char]) + choice(
                    self.invisible_chars
                )
        else:
            raise ValueError(f"level '{level}' not implemented")
        return new_text[:-1]

    def generate(self, text: str, n: int = 1000, level: int = 3) -> List[str]:
        """return a list containing n versions of the text jammed

        :param text: the text to be scrambled
        :type text: str
        :param n: the number of time the text should be scrambled, defaults to 1000
        :type n: int, optional
        :param level: the level of the scrambling, defaults to 3
        :type level: int, optional
        :return: a list of scrambled texts, all differents
        :rtype: List[str]



        .. code:: python

            >>> from text_scrambler import Scrambler
            >>> scr = Scrambler()
            >>> text = "A cranial nerve nucleus is a collection of neurons in the brain stem that is associated with one or more of the cranial nerves."
            >>> texts = scr.generate(text, 1000, level=1)
            >>> assert texts[0] != text
            >>> for scrambled_text in texts:
            ...     assert text != scrambled_text
            ...
            >>> print(texts[0])
            A‍ ‌c‍r‌a‌n‍i‍a‌l‌ ‌n‌e‍r‍v‍e‌ ‍n‌u‌c‍l‌e‌u‌s‌ ‍i‌s‌ ‌a‍ ‌c‍o‌l‍l‌e‍c‌t‌i‌o‍n‍ ‌o‍f‍ ‍n‌e‌u‌r‍o‍n‍s‌ ‍i‌n‌ ‍t‌h‍e‍ ‍b‍r‍a‍i‍n‌ ‌s‍t‍e‌m‍ ‍t‍h‍a‍t‍ ‍i‍s‌ ‌a‌s‍s‍o‌c‌i‌a‌t‌e‍d‍ ‌w‌i‌t‌h‍ ‌o‍n‍e‍ ‍o‍r‍ ‌m‌o‍r‍e‌ ‍o‍f‌ ‍t‍h‌e‌ ‍c‍r‌a‍n‍i‌a‍l‌ ‍n‌e‍r‍v‌e‌s‌.
            >>> # different from the original text


        """
        ls_new_text = []
        num_generated = 0
        while True:
            new_text = self.scramble(text, level=level)
            if new_text not in ls_new_text:
                ls_new_text.append(new_text)
                num_generated += 1
            if num_generated == n:
                break
        return ls_new_text
