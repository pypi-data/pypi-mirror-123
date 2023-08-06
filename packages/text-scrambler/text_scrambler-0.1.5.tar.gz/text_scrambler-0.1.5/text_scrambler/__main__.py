import argparse
import sys

from .text_scrambler import Scrambler


def main(argv):

    parser = argparse.ArgumentParser(
        description="Replace/insert the charaters of the file using the unicode confusable characters",
        usage="Usage : python -m text_scrambler file",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("file", nargs="?", help="encoded in UTF-8")
    parser.add_argument(
        "-l",
        "--level",
        dest="level",
        default=1,
        type=int,
        help="""
        1: insert non printable characters within the text
        2: replace some latin letters to their Greek or Cyrilic equivalent
        3: insert non printable characters and change the some latin  to their Greek or Cyrilic equivalent
        4: insert non printable chraracters change all possible letter to a randomly picked unicode letter equivalent
        default=1""",
    )
    parser.add_argument(
        "-n",
        "--generate",
        dest="n",
        type=int,
        default=1,
        help="""
        Scramble n times the string
        default=1""",
    )
    args = parser.parse_args(argv)

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    with open(args.file) as input_file:
        text = input_file.read()
    scrambler = Scrambler()
    for scrambled_text in scrambler.generate(text, n=args.n, level=args.level):
        print(scrambled_text)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
