import argparse
import re
import os.path

import helpers.snippets

parser = argparse.ArgumentParser(
    description='autoref - apply autoref to Quarto output')
parser.add_argument("path")
parser.add_argument("snippets_dir")
parser.add_argument("--output_file", default="output.tex")
args = parser.parse_args()

SNIPPETS_DIR = args.snippets_dir

with open(args.path, encoding="UTF-8") as reader:
    content = reader.read()

# Replace normal references with "autoref"
content = re.sub(r"(Figure|Table|Equation|Section)~\\ref", "\\\\autoref", content)

content = re.sub(r"https:\/\/github\.com\/AntheSevenants\/([a-z-_])+", "\\\\repoLink", content)
content = re.sub(r"\\\[\s*\\begin{align}", "\\\\begin{align}", content)
content = re.sub(r"\\end{align}\s*\\\]", "\\\\end{align}", content)

content = re.sub("gender-from-name-r", "\\\\genderfromnamer", content)
content = re.sub("ElasticToolsR", "\\\\ElasticToolsR", content)

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
    elif line.startswith("\\begin{longtable}"):
        current_id = "table"
        block_output = True
    elif line.startswith("\\begin{figure}"):
        current_id = "figure"
        minipage_count = 0
        block_output = True
    elif line.startswith("\\begin{minipage}[t]"):
        is_true_minipage = True
        # print(line)
    elif line.startswith("\caption") or line.startswith("\subcaption"):
        matches = re.search(r"\\(?:sub)?caption{\\label{(.*?)}(.*)}", line)
        if matches is not None:
            current_id = matches.group(1)
            current_caption = matches.group(2)
        else:
            matches = re.search(r"\\(?:sub)?caption{(.*?)}\\label{(.*?)}", line)
            current_caption = matches.group(1)
            current_id = matches.group(2)
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

        snippets_path = os.path.join(SNIPPETS_DIR, f"{current_id}.tex")
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

with open(args.output_file, "wt", encoding="UTF-8") as writer:
    writer.write(output)