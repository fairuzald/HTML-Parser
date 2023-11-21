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
                    if tag == 'void':
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
        # Check if tag_name contains only alphanumeric characters and is not empty
        return bool(re.match(r'^[a-zA-Z0-9]+$', tag_name)) and tag_name.lower() in self.allowed_tags
    
    def is_valid_attribute(self, tag_name, attribute_name):
        # Check if tag_name contains only alphanumeric characters and is not empty
        return bool(re.match(r'^[a-zA-Z0-9]+$', attribute_name)) and attribute_name.lower() in self.allowed_tags[tag_name]
    
    
    def normalize_spaces(self, tag):
        # Replace multiple spaces between attributes with a single space
        tag = re.sub(r'\s+', ' ', tag)
        return tag
    
    
    def tokenize(self, html_code):
        # Remove comments
        html_code_cleaned = re.sub(r'\s+(?=>)', '', html_code)

        # Tokenize HTML code with non-greedy regex
        tags = re.findall(r'<[^>]*?(?:"[^"]*?"[^>]*?)*>|<[^>]*>', html_code_cleaned)
        tags = [self.normalize_spaces(tag) for tag in tags if tag != "<>"]

        # Filter and return tags with attributes based on constraints
        result = []
        stack = []
        for tag in tags:
            if tag.startswith("</"):
                tag_name = tag.replace("<", "").replace(">", "").split(" ")[0]
                if stack and tag_name == stack[-1]:
                    result.append(f"</{stack.pop()}>")
                elif len(stack) == 0:
                    return []
                
            elif tag.startswith("<"):
                tag_name = tag.replace("<", "").replace(">", "").split(" ")
                tags = tag_name[0]
                attributes_full = tag_name[1:]

                if self.is_valid_tag(tags):
                    if tag_name not in self.void_elements:
                        stack.append(tag_name)
                    result.append(f"<{tag_name}")
                    
                    for item in attributes_full:
                        # Memisahkan string berdasarkan tanda sama dengan (=)
                        split_item = item.split('=')

                        # Mengambil bagian sebelum tanda sama dengan (=) dan memasukkannya ke dalam array
                        if len(split_item) > 1:
                            isValid = self.is_valid_attribute(tags, split_item[0])
                        
                            if(not isValid):
                                return []
                        
                else:
                    return []
        # Check if all opened tags are closed

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
