import sys

start_input = ""  # input word to be found or not found
found = 0  # stores found state
accepted_config = []  # here we will post end configuration that was accepted


# production rules ("read input", "pop stack", "push stack", "next state")
productions = {}

# all states or non-terminals (not really necessary)
states = []

# list of alphabet symbols or terminals (not really necessary)
symbols = []

# list of stack alphabet symbols (not really necessary)
stack_symbols = []

# start state
start_symbol = ""

# start stack symbol
stack_start = ""

# list of acceptable states
acceptable_states = []

# E - accept on empty stack or F - acceptable state (default is false)
accept_with = ""


def parse_file(filename):
    global productions
    global start_symbol
    global start_stack
    global acceptable_states
    global accept_with

    try:
        lines = [line.rstrip() for line in open(filename)]

    except:
        return 0

    # add start state
    start_symbol = lines[3]

    # add start stack symbol
    start_stack = lines[4]

    # list of acceptable states
    acceptable_states.extend(lines[5].split())

    # E - accept on empty stack or F - acceptable state (default is false)
    accept_with = lines[6]

    # add rules
    for i in range(7, len(lines)):
        production = lines[i].split()

        configuration = [(production[1], production[2], production[4], production[3])]

        if not production[0] in productions.keys():
            productions[production[0]] = []

        configuration = [
            tuple(s if s != "e" else "" for s in tup) for tup in configuration
        ]

        productions[production[0]].extend(configuration)

    print(productions)
    print(start_symbol)
    print(start_stack)
    print(acceptable_states)
    print(accept_with)

    return 1


def main():
    # Mengecek jumlah argumen yang diberikan
    if len(sys.argv) != 3:
        print("Cara penggunaan: python main.py <nama_file_pda> <nama_file_input>")
        return

    # Mengambil nama file dari argumen baris perintah
    pda_file = sys.argv[1]
    input_file = sys.argv[2]

    try:
        parse_file(pda_file)
        print("PDA berhasil dibaca.")

    except FileNotFoundError:
        print("File tidak ditemukan.")


if __name__ == "__main__":
    main()
