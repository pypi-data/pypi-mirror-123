================
text-scrambler
================

Using the Unicode confusable characters and other tricks, we can transform a text into another that looks exactly like it but remains different from a machine view.


Examples
~~~~~~~~

Replacing randomly the Latin characters by Greek or Cyrillic letters and adding the ZW(N)J.

**Original text:**

`Herman Melville (August 1, 1819 – September 28, 1891) was an American novelist, short story writer, and poet of the American Renaissance period. Among his best-known works are Moby-Dick (1851), Typee (1846), a romanticized account of his experiences in Polynesia, and Billy Budd, Sailor, a posthumously published novella. Although his reputation was not high at the time of his death, the centennial of his birth in 1919 was the starting point of a Melville revival and Moby-Dick grew to be considered one of the great American novels.`

**Srambled text (looking the same but totally different):**

`Неrman Μelvillе (Аugust 1, 1819 – Sерtеmbеr 28, 1891) waѕ аn Amerіcan nοvеliѕt, shοrt stоry wrіtеr, and рoеt οf thе Amеriсаn Rеnaissаnсе реrіοd. Amοng his bеѕt-knοwn works arе Мoby-Diсk (1851), Τyрee (1846), а romаntiсized aсcοunt of his ехperienсеs in Pоlynеѕіа, and Віlly Βudd, Sаilоr, а роѕthumοuѕly рublіshed nοvella. Аlthοugh hiѕ rеputatiоn wаs nоt hіgh аt the tіme оf hіѕ dеath, thе centеnnіаl οf hіѕ bіrth іn 1919 was thе startіng pοint οf a Мelvillе rеvіval аnd Mοby-Dісk grеw to be cоnsіdеrеd оne οf thе grеаt Αmerican novеls.`


It is worth to notice that search engines can't find the original webpage (as free online plagiarism checkers). Searching for **Μelvillе** (copy-paste it) on Google doesn't return any match, though the original word **Melville** does.


Using all of the confusable characters of unicode (see [the unicode confusable characters][1]), we can generate weird looking text worthy of old spam messages:

𝚮‍𝒆‌𝕣‍m‍𝓪‍n‍ ‍𝝡‍ҽ‌𝟙‍∨‍𝘪‍𝘐‌𞺀‍𝓮‍ ‍﴾‍𝓐‍𝞄‍𝓰‍ꞟ‌𑣁‍t‌ ‌1‌,‌ ‍1‍8‌1‍Ⳋ‌ ‍–‍ ‌Ꮥ‌𝖊‍𝞺‌𝐭‍𝖾‌m‍Ƅ‌𝔢‌𝔯‌ ‍Ƨ‍𐌚‌ꓹ‌ ‍1‍ଃ‌𝟿‍1‍］‌ ‍𝘸‍𝐚‍𝚜‍ ‍𝖺‌𝔫‍ ‍Α‍m‌ℯ‌𝔯‌𝓲‌ꮯ‌𝒶‌𝓷‌ ‍n‌ം‍𝝼‍𝔢‍𝙸‌ｉ‌s‌𝖙‍؍‍ ‍𐑈‌𝖍‌ꬽ‍ꭇ‍𝓽‍ ‌𝓼‌𝖙‍ⲟ‌r‌𑣜‍ ‍𝐰‌𝓻‌і‍𝒕‍е‍𝕣‍٫‍ ‍α‌𝒏‌𝕕‍ ‍𝙥‌𝜊‍ｅ‍𝕥‍ ‍ﮨ‍f‌ ‌𝘵‍ｈ‍𝗲‌ ‌Α‌m‍𝐞‍𝐫‌ꙇ‌𝒸‍ａ‍n‌ ‍𖼵‍𝘦‍𝑛‌𝐚‌𝒾‌𝑠‌𑣁‌𝜶‌𝕟‌𝗰‌𝒆‍ ‌𝟈‍𝖾‌r‍⍳‌ﮫ‌ᑯ‌𐩐‌ ‍Α‌m‍ｏ‍𝓃‌𝖌‍ ‌𝓱‌Ꭵ‌𝐬‍ ‌Ꮟ‍𝙚‌𝗌‍𝕥‌۔‍𝖐‌𝖓‌ｏ‌𝑤‍𝐧‍ ‌𑜎‌о‌ꮁ‍𝐤‌𝗌‍ ‌𝜶‍𝗿‍𝖾‌ ‌𝕸‍໐‍Ꮟ‍𝙮‍Ⲻ‍𝖣‍𝑖‍𝔠‌𝒌‌ ‍〔‍1‌𝟪‌5‍1‍〕‌ꓹ‌ ‌𝖳‍𝗒‌𝓹‍𝘦‌𝚎‌ ‌〔‍1‍🯸‌𝟜‌6‍❳‍ꓹ‌ ‍𝖆‍ ‌𝕣‌ꬽ‍m‍⍺‌𝘯‌𝘵‌і‌ꮯ‌𝛊‍𝐳‍ⅇ‍𝙙‍ ‍𝕒‌ｃ‍ᴄ‌ჿ‌𝚞‍𝚗‌𝐭‍ ‍𞹤‍𝔣‍ ‍𝚑‌ӏ‌𝓈‌ ‍𝕖‍𝑥‌𝙥‍𝔢‍𝗿‍ꙇ‌e‌𝓷‍ｃ‌℮‍ꮪ‌ ‌𝖎‍𝚗‍ ‌𝙋‍𝘰‌Ӏ‍γ‌𝓷‍𝖾‍𝔰‍𝚒‌𝗮‌؍‍ ‌𝛼‍𝔫‍𝖉‌ ‍𝔅‌Ꭵ‌𝖑‌l‌𝔂‌ ‌𝓑‍𝐮‌𝖉‌𝒹‌‚‌ ‍Ꮥ‌а‌ꙇ‌𝘭‍𝝈‍𝗋‌,‍ ‌α‍ ‍𝑝‍ꬽ‍𐑈‍𝓽‌һ‍𝛖‍m‍𞺄‌ᴜ‍𝔰‍𝗹‌𝑦‍ ‌𝖕‍ᴜ‍Ꮟ‍𝝞‌𝜄‌s‍ｈ‍𝗲‍ꓒ‌ ‌𝓃‍𝗈‌𝓋‍𝒆‌𐌉‌ו‌𝞪‍꘎‍ ‍𖽀‍𝜤‍𝑡‍һ‍𝙤‍𝑢‌ց‍𝘩‌ ‌𝒉‌ι‍ѕ‌ ‌𝖗‌𝒆‌𝛠‍𝚞‍𝐭‌𝓪‌𝙩‌ɪ‍ﮨ‍𝓷‍ ‌𑜊‍𝖺‍s‌ ‍𝘯‍𞹤‍𝚝‌ ‌𝐡‌𝜄‌ᶃ‍𝕙‍ ‍𝖆‍𝘁‍ ‌𝙩‍ｈ‍ꬲ‌ ‍𝓉‌𝔦‍m‍е‍ ‌𝞼‍ẝ‍ ‍ℎ‌ı‍ƽ‍ ‌𝐝‌𝕖‍𝖆‍𝚝‌𝔥‌ꓹ‌ ‍𝙩‌Ꮒ‌ꬲ‍ ‌𝗰‌ⅇ‌𝗻‌𝔱‍𝖊‌𝖓‌n‍𝛊‍𝙖‌𐌠‌ ‍ﻫ‍𝘧‌ ‌𝒽‍𝖎‍𝘴‍ ‍b‍ı‌𝚛‌𝓽‌𝘩‌ ‌ｉ‌𝐧‍ ‍1‍𑣖‌1‍𝟵‌ ‍𑜏‌α‌𝗌‌ ‌𝗍‌𝐡‌ҽ‍ ‍𝕤‍𝑡‍𝛂‌r‍𝓉‍Ꭵ‌𝚗‍ᶃ‍ ‌𝛒‍ס‌𝜾‍𝗻‌𝖙‌ ‌𝜊‌𝖋‌ ‍𝙖‌ ‍ꓟ‍𝙚‌ⵏ‌𝛎‍˛‍І‍𝘭‍ҽ‌ ‌𝔯‍𝐞‌ｖ‌𝞲‌𝚟‌𝖆‍l‍ ‍ɑ‍𝘯‍𝖽‍ ‍𝑀‌ං‌𝒃‍𝚢‌‐‍𝐷‍ͺ‌𝚌‌𝗸‍ ‌𝓰‌ꭈ‌е‌ᴡ‌ ‍𝓉‌ﮭ‌ ‌ᑲ‍ℯ‍ ‌ｃ‍ℴ‍𝙣‌𝔰‌𑣃‍d‍ⅇ‍𝔯‌℮‌ⅾ‍ ‍ﻬ‌𝓃‌℮‍ ‌੦‌𝙛‌ ‍𝙩‌𝔥‍𝔢‍ ‌𝚐‍ꮁ‌ℯ‍𝜶‍𝙩‍ ‍𝞐‍m‍𝘦‍ᴦ‌𝜾‌𝙘‌𝕒‍𝐧‍ ‍𝓃‌ｏ‌𝓿‌ⅇ‍|‍𝒔‍ꓸ



API
~~~

Python
------

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

        >>> text = "A cranial nerve nucleus is a collection of neurons in the brain stem that is associated with one or more of the cranial nerves."
        >>> texts = scr.generate(text, 1000, level=1)
        >>> assert texts[0] != text
        >>> for scrambled_text in texts:
        ...     assert text != scrambled_text
        ...
        >>> print(texts[0])
        A‍ ‌c‍r‌a‌n‍i‍a‌l‌ ‌n‌e‍r‍v‍e‌ ‍n‌u‌c‍l‌e‌u‌s‌ ‍i‌s‌ ‌a‍ ‌c‍o‌l‍l‌e‍c‌t‌i‌o‍n‍ ‌o‍f‍ ‍n‌e‌u‌r‍o‍n‍s‌ ‍i‌n‌ ‍t‌h‍e‍ ‍b‍r‍a‍i‍n‌ ‌s‍t‍e‌m‍ ‍t‍h‍a‍t‍ ‍i‍s‌ ‌a‌s‍s‍o‌c‌i‌a‌t‌e‍d‍ ‌w‌i‌t‌h‍ ‌o‍n‍e‍ ‍o‍r‍ ‌m‌o‍r‍e‌ ‍o‍f‌ ‍t‍h‌e‌ ‍c‍r‌a‍n‍i‌a‍l‌ ‍n‌e‍r‍v‌e‌s‌.
        >>> # different from the original text



Command line interface (CLI)
----------------------------

To get words from input words through CLI, run


    .. code:: bash

        $ python -m text_scrambler
        usage: Usage : python -m text_scrambler file

        Replace/insert the charaters of the file using the unicode confusable characters

        positional arguments:
          file                  encoded in UTF-8

        optional arguments:
          -h, --help            show this help message and exit
          -l LEVEL, --level LEVEL

                                        1: insert non printable characters within the text
                                        2: replace some latin letters to their Greek or Cyrilic equivalent
                                        3: insert non printable characters and change the some latin  to their Greek or Cyrilic equivalent
                                        4: insert non printable chraracters change all possible letter to a randomly picked unicode letter equivalent
                                        default=1
          -n N, --generate N
                                        Scramble n times the string
                                        default=1






Links
~~~~~

See https://en.wikipedia.org/wiki/Word_joiner for more info on word joiners

See https://unix.stackexchange.com/questions/469347/using-uniq-on-unicode-text for why in this case the `sort` command wouldn't work well to check the uniqueness of those strings

See http://www.unicode.org/Public/security/revision-03/confusablesSummary.txt for the complete list of confusable.
