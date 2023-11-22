# with open("pda.txt", "r") as file:
#     lines = file.readlines()

# with open("pdatest.txt", "w") as file:
#     for line in lines:
#         if (
#             line.strip()
#             and not line.startswith("#")
#             and not line.startswith("A")
#             and not line.startswith("E")
#         ):
#             file.write(line)

with open("pdatest.txt", "r") as file:
    lines = file.readlines()

new_lines = []
for line in lines:
    words = line.split()
    if len(words) >= 4 and words[3].startswith("A"):
        words[3] = "F" + words[3][1:]
    new_lines.append(" ".join(words))

with open("pdatest1.txt", "w") as file:
    file.write("\n".join(new_lines))

### PRINT ALL STATES ###
# states = set()
# with open("pda.txt", "r") as file:
#     for line in file:
#         if line.startswith("#"):
#             continue
#         parts = line.split()
#         if len(parts) >= 4:
#             states.add(parts[0])
#             states.add(parts[3])

# states_str = " ".join(states)
# print(states_str)

### PRINT ALL INPUT ###
# states = set()
# with open("pda pake komen.txt", "r") as file:
#     for line in file:
#         parts = line.split()
#         if line.startswith("#"):
#             continue
#         if len(parts) >= 4:
#             states.add(parts[1])

# states_str = " ".join(states)
# print(states_str)

### PRINT ALL STACK ###
# states = set()
# with open("pda pake komen.txt", "r") as file:
#     for line in file:
#         parts = line.split()
#         if line.startswith("#"):
#             continue
#         if len(parts) >= 4:
#             states.add(parts[2])

# states_str = " ".join(states)
# print(states_str)
