import argparse
import os.path

parser = argparse.ArgumentParser(
    description='generate-snippets - generate dumb snippets')
parser.add_argument("path")
parser.add_argument("snippets_dir")
parser.add_argument("figures_dir")
parser.add_argument("--scale", type=float, default=0.4)
args = parser.parse_args()

with open(args.path, "rt") as reader:
    figures = reader.read()

for figure in figures.split("\n"):
    # No empty lines
    if not figure:
        continue

    print(figure)

    valid_extensions = ["png", "pdf"]
    for valid_extension in valid_extensions:
        graphics_path = os.path.join(args.figures_dir, f"{figure}.{valid_extension}")
        if os.path.exists:
            break
    else:
        print(f"No valid figure file: {figure}")

    out = f"\includegraphics[scale={args.scale}]{{{graphics_path}}}"
    out_path = os.path.join(args.snippets_dir, f"{figure}.tex")

    with open(out_path, "wt") as writer:
        writer.write(out)