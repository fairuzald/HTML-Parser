class PDA:
    def __init__(self, filename):
        self.transitions = {}
        self.start_state = None
        self.start_stack = None
        self.accept_states = set()
        self.accepts_empty_stack = False
        self.current_state = None
        self.stack = []
        self.parse_pda_file(filename)

    def parse_pda_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            self.start_state = lines[3].strip()
            self.start_stack = lines[4].strip()
            self.accept_states = set(lines[5].strip().split())
            self.accepts_empty_stack = lines[6].strip() == "F"
            for line in lines[7:]:
                state, symbol, stack_top, new_state, to_push = line.strip().split()
                self.transitions[(state, symbol, stack_top)] = (new_state, to_push)

    def transition(self, symbol):
        if (
            self.current_state,
            symbol,
            len(self.stack) > 0 and self.stack[-1] or None,
        ) in self.transitions:
            self.current_state, to_push = self.transitions[
                (
                    self.current_state,
                    symbol,
                    len(self.stack) > 0 and self.stack[-1] or None,
                )
            ]
            if to_push != "e" and to_push != "idem":
                self.stack.append(to_push)
            elif to_push == "idem":
                pass
            elif self.stack:
                self.stack.pop()
        else:
            self.current_state = None

    def in_accept_state(self):
        return self.current_state in self.accept_states and (
            not self.stack or self.accepts_empty_stack
        )

    def validate(self, tokens):
        self.current_state = self.start_state
        self.stack = [self.start_stack]
        for token in tokens:
            self.transition(token)
            print(token, self.current_state, self.stack)
            if not self.current_state:
                return False
        return self.in_accept_state()
