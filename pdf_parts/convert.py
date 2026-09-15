#!/usr/bin/env python3
"""
Shared converter: list of md files → single PDF via weasyprint.
Usage: python3 convert.py <output_name> <file1.md> <file2.md> ...
"""
import sys, os, re, markdown
from weasyprint import HTML, CSS

STYLE_PATH = os.path.join(os.path.dirname(__file__), "style.css")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def md2html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return f"<p><em>[读取失败 {filepath}: {e}]</em></p>"
    text = re.sub(
        r'!\[([^\]]*)\]\((?!http)([^)]+)\)',
        lambda m: f'![{m.group(1)}](file://{os.path.join(os.path.dirname(filepath), m.group(2))})',
        text
    )
    exts = ['tables', 'fenced_code', 'toc', 'sane_lists', 'nl2br']
    return markdown.markdown(text, extensions=exts)

def build_html(file_list):
    parts = []
    for fpath in file_list:
        fname = os.path.relpath(fpath, BASE_DIR)
        # Section header for subdirectory files
        if '/' in fname:
            parts.append(f'<div style="font-size:13pt;font-weight:bold;color:#34495e;margin:1em 0 0.3em 0;padding-bottom:0.2em;border-bottom:1px dotted #ccc;">{fname}</div>')
        parts.append(md2html(fpath))
    return '\n'.join(parts)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert.py <output.pdf> <file1.md> <file2.md> ...")
        sys.exit(1)

    output_pdf = sys.argv[1]
    file_list = sys.argv[2:]

    print(f"  Converting {len(file_list)} files → {os.path.basename(output_pdf)}")

    body = build_html(file_list)
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"></head>
<body>{body}</body>
</html>"""

    css = CSS(filename=STYLE_PATH)
    HTML(string=full_html, base_url=BASE_DIR).write_pdf(output_pdf, stylesheets=[css])

    size_mb = os.path.getsize(output_pdf) / 1024 / 1024
    print(f"  ✅ {os.path.basename(output_pdf)} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    main()