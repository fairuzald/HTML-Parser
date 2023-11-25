import re


class Tokenize:
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
        # Remove = space and open close tag on " "
        html_code_cleaned = re.sub(
            r'"([^"]*)"',
            lambda m: m.group(0)
            .replace(" ", "")
            .replace("=", "")
            .replace("<", "")
            .replace(">", ""),
            html_code,
        )
        # 
        html_code_cleaned = re.sub(r"\s+(?=>)", "", html_code_cleaned)
        html_code_cleaned = re.sub(r"\s*=\s*", "=", html_code_cleaned)
        html_code_cleaned = re.sub(r"(?<!<)<!--.*?-->(?!>)", "", html_code_cleaned)

        # Tokenize HTML code with a non-greedy regex
        tags = re.findall(r'<[^>]*?(?:"[^"]*?"[^>]*?)*>|<[^>]*>', html_code_cleaned)
        tags = [self.normalize_spaces(tag) for tag in tags if tag != "<>"]
        # Filter and return tags with attributes based on constraints
        result = []
        for tag in tags:
            if tag.startswith("</"):
                # Closing tag encountered
                tag_name = tag.replace("</", "").replace(">", "")
                result.append(f"</{tag_name}>")
               

            elif tag.startswith("<"):
                # Opening tag encountered
                tag_name = tag.replace("<", "").replace(">", "").split(" ")
                name_tag = tag_name[0]
                attributes_full = tag_name[1:]
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
                            if (not isQuoteOpen and not isQuoteClose) :
                                result.append(f"{attribute_name}=")


                            else:
                                result.append(f'{attribute_name}="')
                            if (
                                (name_tag == "input" or name_tag == "button")
                                and attribute_name == "type"
                            ) or (
                                name_tag == "form" and attribute_name == "method"
                            ):
                                result.append(attribute_value)
                            if len(split_item[1]) > 1 and (
                                (isQuoteOpen and isQuoteClose)
                            ):
                                result.append('"')
                    else:
                        result.append(f"{item}")
                result.append(">")
            
       
        return result
