import sys

with open(sys.argv[1], "r") as f:
    content = f.read()

lines = content.splitlines()

for line in range(len(lines)):
    for credential in sys.argv[2:]:
        if credential.strip() in lines[line]:
            raise Exception(f"Found credentials on line {line + 1}.")