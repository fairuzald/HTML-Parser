class PDA:
    # Constructor method
    def __init__(self, filename):
        # Initialize the transitions dictionary
        self.transitions = {}
        # Initialize the start state
        self.start_state = None
        # Initialize the start stack
        self.start_stack = None
        # Initialize the set of accept states
        self.accept_states = set()
        # Initialize the flag for accepting empty stack
        self.accepts_empty_stack = False
        # Initialize the current state
        self.current_state = None
        # Initialize the stack
        self.stack = []
        # Parse the PDA file
        self.parse_pda_file(filename)

    # Method to parse the PDA file
    def parse_pda_file(self, filename):
        with open(filename, "r") as file:
            # Read all lines from the file
            lines = file.readlines()
            # Set the start state
            self.start_state = lines[3].strip()
            # Set the start stack
            self.start_stack = lines[4].strip()
            # Set the accept states
            self.accept_states = set(lines[5].strip().split())
            # Set the flag for accepting empty stack
            self.accepts_empty_stack = lines[6].strip() == "F"
            # Parse the transitions
            for line in lines[7:]:
                # Split the line into components
                state, symbol, stack_top, new_state, to_push = line.strip().split()
                # Add the transition to the transitions dictionary
                self.transitions[(state, symbol, stack_top)] = (new_state, to_push)

    # Method to perform a transition
    def transition(self, symbol, line_number):
        # Check if the transition is valid
        if (
            self.current_state,
            symbol,
            len(self.stack) > 0 and self.stack[-1] or None,
        ) in self.transitions:
            # Perform the transition
            self.current_state, to_push = self.transitions[
                (
                    self.current_state,
                    symbol,
                    len(self.stack) > 0 and self.stack[-1] or None,
                )
            ]
            # Check the value of to_push and modify the stack accordingly
            if to_push != "e" and to_push != "idem":
                self.stack.append(to_push)
            elif to_push == "idem":
                pass
            elif self.stack:
                self.stack.pop()
        else:
            # If the transition is not valid, set the current state to None and raise a SyntaxError
            self.current_state = None
            raise SyntaxError(f"Syntax error at line {line_number}: unexpected input {symbol}")

    # Method to check if the current state is an accept state
    def in_accept_state(self):
        return self.current_state in self.accept_states and (
            not self.stack or self.accepts_empty_stack
        )

    # Method to validate a sequence of tokens
    def validate(self, tokens_with_line_numbers):
        self.current_state = self.start_state
        self.stack = [self.start_stack]
        for token, line_number in tokens_with_line_numbers:
            try:
                self.transition(token, line_number)
            except SyntaxError as e:
                print(e)
                return False
            if not self.current_state:
                return False
        return self.in_accept_state()
