import os
import sys
import re


class Tokenize:
    def __init__(self, definition_folder):
        # Read allowed tags from the specified file
        allowed_tags_file_path = os.path.join(definition_folder, "allowed_tags.txt")
        self.void_elements = []
        self.allowed_tags = self.read_allowed_tags(allowed_tags_file_path)

        # Define void elements

    def read_allowed_tags(self, file_path):
        # Initialize dictionaries to store allowed tags and void elements
        allowed_tags = {}
        void_element = []

        try:
            # Read the file containing allowed tags
            with open(file_path, "r") as file:
                for line in file:
                    # Split the line into parts based on the ';' delimiter
                    parts = line.strip().split(";")
                    tag = parts[0]

                    # Check if the tag is a 'void' element
                    if tag == "void":
                        tag = parts[1]
                        void_element.append(parts[1])
                        attributes = parts[2:]
                    else:
                        attributes = parts[1:]

                    # Check if the tag has attributes and if the first attribute is 'void'

                    allowed_tags[tag] = attributes

        except FileNotFoundError:
            # Handle the case where the file is not found
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)

        self.void_elements = void_element

        return allowed_tags

    def is_valid_tag(self, tag_name):
        # Check if tag_name contains only alphanumeric characters and is not empty
        return (
            bool(re.match(r"^[a-zA-Z0-9]+$", tag_name))
            and tag_name.lower() in self.allowed_tags
        )

    def is_valid_attribute(self, tag_name, attribute_name):
        # Check if attribute_name contains only alphanumeric characters and is in the allowed attributes for the tag
        return (
            bool(re.match(r"^[a-zA-Z0-9]+$", attribute_name))
            and attribute_name.lower() in self.allowed_tags[tag_name]
        )

    def normalize_spaces(self, tag):
        # Replace multiple spaces between attributes with a single space
        tag = re.sub(r"\s+", " ", tag)
        return tag

    def get_content_inside_quotes(s):
        # Return the content inside quotes if the string is enclosed in double quotes
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        else:
            return None

    def tokenize(self, html_code):
        # Remove comments and unnecessary spaces within quotes
        html_code_cleaned = re.sub(
            r'"([^"]*)"',
            lambda m: m.group(0)
            .replace(" ", "")
            .replace("=", "")
            .replace("<", "")
            .replace(">", ""),
            html_code,
        )
        html_code_cleaned = re.sub(r"\s+(?=>)", "", html_code_cleaned)

        # Tokenize HTML code with a non-greedy regex
        tags = re.findall(r'<[^>]*?(?:"[^"]*?"[^>]*?)*>|<[^>]*>', html_code_cleaned)
        tags = [self.normalize_spaces(tag) for tag in tags if tag != "<>"]

        # Filter and return tags with attributes based on constraints
        result = []
        stack = []
        for tag in tags:
            if tag.startswith("</"):
                # Closing tag encountered
                tag_name = tag.replace("</", "").replace(">", "")
                if stack and tag_name == stack[-1]:
                    result.append(f"</{stack.pop()}>")
                elif len(stack) == 0:
                    # If the stack is empty, there is a closing tag without a corresponding opening tag
                    return []

            elif tag.startswith("<"):
                # Opening tag encountered
                tag_name = tag.replace("<", "").replace(">", "").split(" ")
                name_tag = tag_name[0]
                attributes_full = tag_name[1:]

                if self.is_valid_tag(name_tag):
                    if name_tag not in self.void_elements:
                        # Add non-void opening name_tag to the stack
                        stack.append(name_tag)
                    result.append(f"<{name_tag}")

                    for item in attributes_full:
                        if "=" in item:
                            split_item = item.split("=")

                            if len(split_item) > 1:
                                # Attribute with a value encountered
                                attribute_name = split_item[0]
                                isQuoteOpen = split_item[1].startswith('"')
                                isQuoteClose = split_item[1].endswith('"')
                                attribute_value = split_item[1].replace('"', "")
                                isValid = self.is_valid_attribute(
                                    name_tag, attribute_name
                                )

                                if not isValid:
                                    # Invalid attribute encountered
                                    return []

                                # Append attribute name and value to the result
                                result.append(attribute_name)
                                result.append("=")
                                if isQuoteOpen:
                                    result.append('"')
                                if (
                                    (name_tag == "img" and attribute_name == "src")
                                    or (
                                        (name_tag == "input" or name_tag == "button")
                                        and attribute_name == "type"
                                    )
                                    or (
                                        name_tag == "form"
                                        and attribute_name == "method"
                                    )
                                ):
                                    result.append(attribute_value)
                                if (
                                    len(split_item[1]) > 1
                                    and isQuoteOpen
                                    and isQuoteClose
                                ):
                                    result.append('"')
                        else:
                            return []

                    result.append(">")
                else:
                    # Invalid opening tag encountered
                    return []
        if stack:
            # Unclosed name_tag exist
            return []

        return result


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
            self.accepts_empty_stack = lines[6].strip() == "E"
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
            self.stack.pop()
            if to_push != "e":
                self.stack.append(to_push)
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
            print(self.current_state, self.stack)
            if not self.current_state:
                return False
        return self.in_accept_state()


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.html")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, "r") as file:
        html_code = file.read()

    definition_folder = "rules"
    tokenizer = Tokenize(definition_folder)
    tokens = tokenizer.tokenize(html_code)
    print(tokens)

    pda = PDA("pda.txt")
    print(pda.validate(tokens))


if __name__ == "__main__":
    main()
