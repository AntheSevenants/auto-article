import argparse
import re
import os.path

parser = argparse.ArgumentParser(
    description='clean-tikz - remove fluff from tikz files')
parser.add_argument("path")
args = parser.parse_args()

print(args.path)

with open(args.path, encoding="UTF-8") as reader:
    content = reader.read()

buffer = []
allow_output = False
for line in content.split("\n"):
    if line.startswith("\\newdimen"):
        buffer.append(line)
    elif line.startswith("\\usetikzlibrary"):
        buffer.append(line)
    elif line.startswith("\\begin{tikzpicture}"):
        buffer.append("")
        buffer.append(line)
        allow_output = True
    elif line.startswith("\\end{tikzpicture}"):
        buffer.append(line)
        allow_output = False
    else:
        if allow_output:
            buffer.append(line)

content = "\n".join(buffer)

with open(args.path, "wt", encoding="UTF-8") as writer:
    writer.write(content)