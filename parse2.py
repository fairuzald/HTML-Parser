with open("pda pake komen.txt", "r") as file:
    lines = file.readlines()

new_lines = []
for line in lines:
    if line.startswith("Nformdiv"):
        continue
    line = line.replace("Nformbody", "Nform")
    new_lines.append(line)

with open("pda pake komen2.txt", "w") as file:
    file.write("".join(new_lines))
