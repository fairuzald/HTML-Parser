import os
from PDA import PDA
from tokenizer import Tokenize

def main():
    with open('asciiArt.txt', 'r') as file:
        ascii_art = file.read()
    print(ascii_art)
    while True:
        # Add blue color to the input text
        pda_file = input('\033[94m' + "Masukkan nama file PDA: " + '\033[0m')
        if os.path.isfile(pda_file):
            break
        print('\033[91m' + f"PDA file {pda_file} not found." + '\033[0m')

    while True:
        # Add blue color to the input text
        input_file = input('\033[94m' + "Masukkan nama file HTML: " + '\033[0m')
        # Dapatkan absolute path sekarang lalu balik ../test/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, '../test/', input_file)
        if os.path.isfile(full_path):
            # Check if pda_file exists
            pda = PDA(pda_file)

            try:
                with open(full_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                print('\033[91m' + f"File {input_file} not found." + '\033[0m')
                # Add yellow color
                print('\033[93m' + "Pastikan file test html ditaruh pada folder test" + '\033[0m')
                continue

            tokenizer = Tokenize()
            tokens_with_line_numbers = []
            for line_number, line in enumerate(lines, start=1):
                tokens = tokenizer.tokenize(line)
                tokens_with_line_numbers.extend((token, line_number) for token in tokens)

            if pda.validate(tokens_with_line_numbers):
                print('\033[92m' + "Accepted" + '\033[0m')
            else:
                print('\033[91m' + "Syntax Error" + '\033[0m')

            # Ask the user if they want to continue
            continue_prompt = input('\033[94m' + "Apakah Anda ingin melanjutkan lagi? (y/n): " + '\033[0m')
            if continue_prompt.lower() == 'n':
                break
            if continue_prompt.lower() == 'y':
                continue
            else:
                print('\033[93m' + "Masukkan tidak valid, program akan berhenti." + '\033[0m')
                break
        else:
            print('\033[91m' + f"Input file {input_file} not found." + '\033[0m')
            # Add yellow color
            print('\033[93m' + "Pastikan file test html ditaruh pada folder test" + '\033[0m')

if __name__ == "__main__":
    main()
