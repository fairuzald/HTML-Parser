from PDA import PDA
from tokenizer import Tokenize
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py pda.txt input_file.html")
        sys.exit(1)

    pda = PDA(sys.argv[1])
    input_file = sys.argv[2]
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            html_code = file.read()
    except FileNotFoundError:
        print(f"File {input_file} not found.")
        sys.exit(1)

    tokenizer = Tokenize()
    tokens = tokenizer.tokenize(html_code)
    # print(tokens)

    if pda.validate(tokens):
        print("Accepted")
    else:
        print("Syntax Error")

if __name__ == "__main__":
    main()
