import argparse

parser = argparse.ArgumentParser(
    description='generate-snippets - generate dumb snippets')
parser.add_argument("path")
args = parser.parse_args()

with open(args.path, "rt") as reader:
    figures = reader.read()

for figure in figures.split("\n"):
    print(figure)
    out = f"\includegraphics[scale=0.4]{{figures/{figure}.png}}"
    out_path = f"snippets/{figure}.tex"

    with open(out_path, "wt") as writer:
        writer.write(out)