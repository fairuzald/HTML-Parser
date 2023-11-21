import re

def check_html_tag_validity(html_tag):
    pattern = r'^<([a-zA-Z]+)>$'
    match = re.match(pattern, html_tag)
    
    if match:
        return f"Tag {match.group(1)} valid"
    else:
        return "Tag tidak valid"

# Contoh penggunaan
tag_to_check = "<ASU>"
result = check_html_tag_validity(tag_to_check)
print(result)
