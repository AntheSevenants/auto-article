import argparse
import os.path

parser = argparse.ArgumentParser(
    description='generate-snippets - generate dumb snippets')
parser.add_argument("path")
parser.add_argument("snippets_dir")
parser.add_argument("figures_dir")
args = parser.parse_args()

with open(args.path, "rt") as reader:
    figures = reader.read()

for figure in figures.split("\n"):
    print(figure)
    out = f"\includegraphics[scale=0.4]{{{args.figures_dir}/{figure}.png}}"
    out_path = os.path.join(args.snippets_dir, f"{figure}.tex")

    with open(out_path, "wt") as writer:
        writer.write(out)