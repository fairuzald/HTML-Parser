with open("pda pake komen2.txt", "r") as file:
    lines = file.readlines()

line_indices = {}
for i, line in enumerate(lines, start=1):
    # Skip empty lines
    if line.strip() == "" or line.startswith("#"):
        continue
    if line in line_indices:
        print(f"Duplicate line at lines {line_indices[line]} and {i}: {line.strip()}")
    else:
        line_indices[line] = i
