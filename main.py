import sys


class PDA:
    def __init__(self, definition_file):
        with open(definition_file, "r") as file:
            lines = file.readlines()

        self.states = lines[0].strip().split()
        self.input_symbols = lines[1].strip().split()
        self.stack_symbols = lines[2].strip().split()
        self.start_state = lines[3].strip()
        self.start_stack = lines[4].strip()
        self.accept_states = lines[5].strip().split()
        self.accept_condition = lines[6].strip()

        self.transitions = {}
        for line in lines[7:]:
            (
                current_state,
                input_symbol,
                stack_top,
                next_state,
                new_stack_top,
            ) = line.strip().split()
            self.transitions[(current_state, input_symbol, stack_top)] = (
                next_state,
                new_stack_top,
            )

    def check_input(self, input):
        current_state = self.start_state
        current_stack = [self.start_stack]

        for symbol in input:
            if (current_state, symbol, current_stack[-1]) in self.transitions:
                current_state, new_stack_top = self.transitions[
                    (current_state, symbol, current_stack[-1])
                ]
                if new_stack_top != "e":
                    current_stack.append(new_stack_top)
            elif (current_state, "e", current_stack[-1]) in self.transitions:
                current_state, new_stack_top = self.transitions[
                    (current_state, "e", current_stack[-1])
                ]
                if new_stack_top != "e":
                    current_stack.append(new_stack_top)
            else:
                return False

        if current_state in self.accept_states:
            return True
        else:
            return False


def main():
    pda = PDA(sys.argv[1])

    with open(sys.argv[2], "r") as file:
        html_code = file.read()

    if pda.check_input(html_code):
        print("Accepted")
    else:
        print("Syntax Error")


if __name__ == "__main__":
    main()
