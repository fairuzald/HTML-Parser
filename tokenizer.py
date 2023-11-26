import re

class Tokenize:
    def normalize_spaces(self, tag):
        # Replaces multiple spaces between attributes with a single space
        return re.sub(r"\s+", " ", tag)

    def get_content_inside_quotes(s):
        # Returns the content inside quotes if the string is enclosed in double quotes
        if re.match(r'^".*"$', s):
            return s[1:-1]

    def tokenize(self, html_code):
        # Removes spaces, equals signs
        formatting_content_quotes = re.sub(
            r'"([^"]*)"',
            lambda m: m.group(0)
            .replace(" ", "")
            .replace("=", ""),
            html_code,
        )
        # Removes spaces before closing tags and spaces around equals signs
        html_code_cleaned = re.sub(r"\s+(?=>)", "", formatting_content_quotes)
        html_code_cleaned = re.sub(r"\s*=\s*", "=", html_code_cleaned)
        
        # Finds all tags in the cleaned HTML code
        tags = re.findall(r'<[^>]*?(?:"[^"]*?"[^>]*?)*>|<[^>]*>', html_code_cleaned)
        
        # Normalizes spaces in the tags and filters out empty tags
        tags = [self.normalize_spaces(tag) for tag in tags if tag != "<>"]
        result = []
        for tag in tags:
            if re.match(r'^</.*>$', tag):
                # If it's a closing tag, it appends the tag to the result
                tag_name = re.sub(r'</|>', '', tag)
                result.append(f"</{tag_name}>")
            elif re.match(r'^<!--.*-->$', tag):
                # If it's a comment, it appends the comment delimiters to the result
                result.extend(["<!--", "-->"])
            elif re.match(r'^<.*>$', tag):
                # If it's an opening tag, it processes the tag and appends the result
                self.process_opening_tag(tag, result)
        return result

    def process_opening_tag(self, tag, result):
        # This function processes an opening tag
        # It first splits the tag into its name and attributes
        content_tag = re.sub(r'<|>', '', tag).split(" ")
        tag_name = content_tag[0]
        attributes = content_tag[1:]
        # It appends the opening tag to the result
        result.append(f"<{tag_name}")
        # processes each attribute
        for item in attributes:
            if re.search(r'.*?=.*', item):
                # If the attribute has a value, it splits the attribute into its name and value
                split_item = item.split("=")
                if len(split_item) > 1:
                    attribute_name, attribute_value = item.split("=")
                    
                    isQuoteOpen = re.match(r'^".*$', attribute_value)
                    isQuoteClose = re.match(r'^.*"$', attribute_value)
                    attribute_value = re.sub(r'"', '', attribute_value)
                    # It appends the attribute name and equals sign to the result
                    if not isQuoteOpen and not isQuoteClose:
                        result.append(f"{attribute_name}=")
                    else:
                        result.append(f'{attribute_name}="')
                    # If the tag is an input or button and the attribute is type, or if the tag is a form and the attribute is method, it appends the attribute value to the result
                    if (
                    ((tag_name =="input" or tag_name=="button") and attribute_name == "type")
                    or (tag_name == "form" and attribute_name == "method")
                ):
                        result.append(attribute_value)
                    # If the attribute value is enclosed in quotes, it appends a closing quote to the result
                    if len(split_item[1]) > 1 and isQuoteOpen and isQuoteClose:
                        result.append('"')
            else:
                # If the attribute doesn't have a value, it appends the attribute to the result
                result.append(f"{item}")
        result.append(">")
