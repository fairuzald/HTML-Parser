import os
import sys
import re

class Tokenize:
    def __init__(self, definition_folder):
        # Read global attributes from file
        global_attributes_file = os.path.join(definition_folder, "global_attributes.txt")
        with open(global_attributes_file, "r") as file:
            self.global_attributes = [line.strip() for line in file.readlines()]

        # Read allowed tags from file
        allowed_tags_file = os.path.join(definition_folder, "allowed_tags.txt")
        with open(allowed_tags_file, "r") as file:
            self.allowed_tags = {}
            for line in file.readlines():
                parts = line.strip().split()
                tag = parts[0]
                attributes = parts[1:]
                self.allowed_tags[tag] = attributes

        # Define void elements
        self.void_elements = ["img", "br", "hr"]

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
