# Import required libraries
import os
from PDA import PDA
from tokenizer import Tokenize

def main():
    # Open and read the asciiArt.txt file
    with open('asciiArt.txt', 'r') as file:
        ascii_art = file.read()
    print(ascii_art)
    
    while True:
        # Request the user to input the name of the PDA file
        pda_file = input('\033[94m' + "Masukkan nama file PDA: " + '\033[0m')
        # Check if the PDA file exists
        if os.path.isfile(pda_file):
            break
        print('\033[91m' + f"PDA file {pda_file} not found." + '\033[0m')

    while True:
        # Request the user to input the name of the HTML file
        input_file = input('\033[94m' + "Masukkan nama file HTML: " + '\033[0m')
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, '../test/', input_file)
        # Check if the HTML file exists
        if os.path.isfile(full_path):
            pda = PDA(pda_file)

            try:
                # Open and read the HTML file
                with open(full_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                print('\033[91m' + f"File {input_file} not found." + '\033[0m')
                print('\033[93m' + "Pastikan file test html ditaruh pada folder test" + '\033[0m')
                continue

            # Create a Tokenize object
            tokenizer = Tokenize()
            tokens_with_line_numbers = []
            # Tokenize each line of the HTML file
            for line_number, code in enumerate(lines, start=1):
                tokens = tokenizer.tokenize(code)
                tokens_with_line_numbers.extend((token, line_number) for token in tokens)

            # Validate the tokens using the PDA
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
            print('\033[93m' + "Pastikan file test html ditaruh pada folder test" + '\033[0m')

if __name__ == "__main__":
    main()
