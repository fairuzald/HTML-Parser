import re

teks_input = '<div id="tes">'


teks_output = re.sub(r'(?<!\=)"', r'" ', teks_input)

print(teks_output)
