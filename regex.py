import os
import sys
import re

class Tokenize:
    def __init__(self, definition_folder):
        # Read allowed tags from file
        allowed_tags_file_path = os.path.join(definition_folder, "allowed_tags.txt")
        self.allowed_tags = self.read_allowed_tags(allowed_tags_file_path)

        # Define void elements
        self.void_elements = []

    def read_allowed_tags(self, file_path):
        allowed_tags = {}
        void_elements = []

        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(';')
                    tag = parts[0]
                    if(tag == 'void'):
                        tag = parts[1]
                        void_elements.append(parts[1])
                    attributes = parts[1:]

                    if attributes and attributes[0].lower() == 'void':
                        void_elements.append(attributes[1])
                        allowed_tags[tag] = []
                    else:
                        allowed_tags[tag] = attributes

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)

        # Set void elements in the class
        self.void_elements = void_elements

        return allowed_tags



    def is_valid_tag(self, tag_name):
        return tag_name.lower() in self.allowed_tags

    def tokenize(self, html_code):
        # Remove comments
        html_code = re.sub(r'<!--(.*?)-->', '', html_code, flags=re.DOTALL)

        # Tokenize HTML code
        tags = re.findall(r'<\s*([a-zA-Z0-9]+)\s*[^>]*>|</\s*([a-zA-Z0-9]+)\s*>', html_code)

        # Filter and return tags with attributes based on constraints
        result = []
        stack = []
        for tag_open, tag_close in tags:
            if tag_open:
                tag_name = tag_open.lower()
                if self.is_valid_tag(tag_name):
                    if tag_name not in self.void_elements:
                        stack.append(tag_name)
                    result.append(f"<{tag_name}>")
                else:
                    return []
            elif tag_close:
                tag_name = tag_close.lower()
                if stack and tag_name == stack[-1]:
                    result.append(f"</{stack.pop()}>")

        # Check if all opened tags are closed
        if stack:
            result = []

        return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.html")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, "r") as file:
        html_code = file.read()

    definition_folder = "rules"  # Change this path if necessary
    tokenizer = Tokenize(definition_folder)
    tokens = tokenizer.tokenize(html_code)
    print(tokens)

if __name__ == "__main__":
    main()
