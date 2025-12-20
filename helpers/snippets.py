import os.path
from pathlib import Path

def get_snippet(snippet_path):
    with open(snippet_path, "rt", encoding="UTF-8") as reader:
        snippet = reader.read()

    return snippet

def build_table_snippet(snippet_path, snippet_id, snippet_caption):
    if not os.path.exists(snippet_path):
        print(f"Missing snippet: {snippet_id}")
        return ""

    snippet = get_snippet(snippet_path)
    snippet = add_caption_labels(snippet, snippet_id, snippet_caption)

    return snippet

def build_figure_snippet(snippet_path, snippet_id, snippet_caption, include_filename):
    return build_table_snippet(snippet_path, snippet_id, snippet_caption)

# def build_minipage_snippet(snippet_path, snippet_id, snippet_caption, include_filename, minipage_count):
#     suffix = "\\hfill"
#     if minipage_count % 2 == 0:
#         suffix = "\\medskip"
    
#     return build_table_snippet(snippet_path, snippet_id, snippet_caption) + suffix

def build_minipage_snippet(snippet_path, snippet_id, snippet_caption, include_filename, minipage_count):
    if not os.path.exists(snippet_path):
        print(f"Missing snippet: {snippet_id}")
        return ""

    suffix = "\\quad"
    if minipage_count % 2 == 0:
        suffix = "\\qquad"

    skeleton = f"""\subfloat[{{{snippet_caption}}} \label{{{snippet_id}}}]{{
{get_snippet(snippet_path)}
}}
{suffix}"""
    
    return skeleton

def build_figure_snippet_rejected(snippet_path, snippet_id, snippet_caption, include_filename):
    filename = include_filename.split("/")[-1]
    path = Path(filename)

    if path.suffix == ".pdf":
        snippet = f"""\\begin{{figure}}
\input{{tikz/{path.stem}.tikz}}
\end{{figure}}
"""
    else:
        print(f"Unsupported filetype: {snippet_id}")
        return ""

    snippet = add_caption_labels(snippet, snippet_id, snippet_caption)

    return snippet

def add_caption_labels(snippet, snippet_id, snippet_caption):
    snippet_lines = snippet.strip().split("\n")
    snippet_lines[-1:-1] = [ f"\\caption{{{snippet_caption}}}", f"\\label{{{snippet_id}}}" ]

    return "\n".join(snippet_lines)