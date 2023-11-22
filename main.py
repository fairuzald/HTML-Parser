from PDA import PDA
from regex import Tokenize


import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py pda.txt input_file.html")
        sys.exit(1)

    pda = PDA(sys.argv[1])
    input_file = sys.argv[2]
    with open(input_file, "r") as file:
        html_code = file.read()

    definition_folder = "rules"
    tokenizer = Tokenize(definition_folder)
    tokens = tokenizer.tokenize(html_code)
    print(tokens)

    print(pda.validate(tokens))


if __name__ == "__main__":
    main()
