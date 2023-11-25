from PDA import PDA
from regex import Tokenize


import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py pda.txt input_file.html")
        sys.exit(1)

    pda = PDA(sys.argv[1])
    input_file = sys.argv[2]
    with open(input_file, "r", encoding="utf-8") as file:
        html_code = file.read()

    tokenizer = Tokenize()
    tokens = tokenizer.tokenize(html_code)
    print(tokens)

    if pda.validate(tokens):
        print("Accepted")
    else:
        print("Rejected")


if __name__ == "__main__":
    main()
