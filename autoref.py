import argparse
import re
import os.path

import helpers.snippets

SNIPPETS_DIR = "snippets/"

parser = argparse.ArgumentParser(
    description='autoref - apply autoref to Quarto output')
parser.add_argument("path")
args = parser.parse_args()

with open(args.path, encoding="UTF-8") as reader:
    content = reader.read()

# Replace normal references with "autoref"
content = re.sub(r"(Figure|Table|Equation|Section)~\\ref", "\\\\autoref", content)

# Now, let's go over all lines and replace tables with my own tables
current_type = None
current_id = None
current_caption = None
current_filename = None
block_output = False
minipage_count = 0
is_true_minipage = False
inner_buffer = []
inner_captions = []

buffer = []
for line in content.split("\n"):
    # print(line)
    if line.startswith("\hypertarget{tbl-"):
        matches = re.search(r"\\hypertarget{(.*?)}", line)
        current_type = "table"
        current_id = matches.group(1)

        block_output = True
    if line.startswith("\\begin{figure}"):
        current_id = "figure"
        minipage_count = 0
        block_output = True
    if line.startswith("\\begin{minipage}[t]"):
        is_true_minipage = True
        # print(line)
    elif line.startswith("\caption") or line.startswith("\subcaption"):
        matches = re.search(r"\\(?:sub)?caption{\\label{(.*?)}(.*)}", line)
        current_id = matches.group(1)
        current_caption = matches.group(2)
    elif "\includegraphics" in line:
        matches = re.search(r"\\includegraphics{(.*?)}", line)
        current_filename = matches.group(1)
    elif line.startswith("\\end"):
        matches = re.search(r"\\end{(.*?)}", line)
        if matches is not None:
            kind = matches.group(1)
        else:
            continue

        if kind not in [ "longtable", "figure", "minipage" ]:
            buffer.append(line)
            continue

        snippets_path = f"{SNIPPETS_DIR}{current_id}.tex"
        if kind == "longtable":
            snippet = helpers.snippets.build_table_snippet(
                snippets_path,
                current_id,
                current_caption)
        elif kind == "figure":
            # if len(inner_buffer) > 0:
            #     current_caption = "\n".join([ current_caption ] + inner_captions).strip(";")

            snippet = helpers.snippets.build_figure_snippet(
                snippets_path,
                current_id,
                current_caption,
                current_filename
            )

            if len(inner_buffer) > 0:
                inner_content = "\n".join(inner_buffer)
                snippet = snippet.replace("__INSERT__", inner_content)

            inner_buffer = []
            inner_captions = []
        elif kind == "minipage":
            if not is_true_minipage:
                continue

            minipage_count += 1
            snippet = helpers.snippets.build_minipage_snippet(
                snippets_path,
                current_id,
                current_caption,
                current_filename,
                minipage_count
            )

            is_true_minipage = False
            inner_buffer.append(snippet)
            continue
        else:
            # print("waluigi")
            continue
            
        buffer.append(snippet)
            
        block_output = False
    else:
        if not block_output:
            buffer.append(line)

output = "\n".join(buffer)

with open("output.tex", "wt", encoding="UTF-8") as writer:
    writer.write(output)