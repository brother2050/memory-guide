#!/usr/bin/env python3
"""
Shared converter: list of md files → single PDF via weasyprint.
Usage: python3 convert.py <output.pdf> <file1.md> <file2.md> ...

单文件读取/转换失败不会中断整体构建：错误记入 stderr，并在末尾统一汇总。
"""
import sys, os, re, markdown
from weasyprint import HTML, CSS

STYLE_PATH = os.path.join(os.path.dirname(__file__), "style.css")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def md2html(filepath):
    """把单个 md 文件转成 HTML；失败时返回占位 HTML 与错误信息（不抛异常）。"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        # 修复相对图片路径：转成 file:// 绝对路径
        text = re.sub(
            r'!\[([^\]]*)\]\((?!http)([^)]+)\)',
            lambda m: f'![{m.group(1)}](file://{os.path.join(os.path.dirname(filepath), m.group(2))})',
            text
        )
        exts = ['tables', 'fenced_code', 'toc', 'sane_lists', 'nl2br']
        return markdown.markdown(text, extensions=exts), None
    except Exception as e:
        return f"<p><em>[转换失败 {filepath}: {e}]</em></p>", str(e)

def build_html(file_list):
    """逐个转换文件并输出进度；返回 (HTML, 成功数, 失败清单[(文件, 错误)])。"""
    parts = []
    failed = []
    ok = 0
    total = len(file_list)
    for i, fpath in enumerate(file_list, 1):
        fname = os.path.relpath(fpath, BASE_DIR)
        # 进度打印
        print(f"  [{i}/{total}] {fname}")
        # Section header for subdirectory files
        if '/' in fname:
            parts.append(f'<div style="font-size:13pt;font-weight:bold;color:#34495e;margin:1em 0 0.3em 0;padding-bottom:0.2em;border-bottom:1px dotted #ccc;">{fname}</div>')
        html, err = md2html(fpath)
        if err:
            failed.append((fname, err))
            print(f"    ⚠️ 转换失败（已跳过并继续）: {err}", file=sys.stderr)
        else:
            ok += 1
        parts.append(html)
    return '\n'.join(parts), ok, failed

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert.py <output.pdf> <file1.md> <file2.md> ...")
        sys.exit(1)

    output_pdf = sys.argv[1]
    file_list = sys.argv[2:]

    print(f"  Converting {len(file_list)} files → {os.path.basename(output_pdf)}")

    body, ok, failed = build_html(file_list)
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"></head>
<body>{body}</body>
</html>"""

    css = CSS(filename=STYLE_PATH)
    HTML(string=full_html, base_url=BASE_DIR).write_pdf(output_pdf, stylesheets=[css])

    size_mb = os.path.getsize(output_pdf) / 1024 / 1024
    print(f"  ✅ {os.path.basename(output_pdf)} ({size_mb:.1f} MB)")

    # 末尾汇总：成功/失败数量与失败清单
    print(f"  📊 共 {len(file_list)} 个文件：成功 {ok} 个，失败 {len(failed)} 个")
    for fname, err in failed:
        print(f"    ❌ {fname}: {err}")
    if ok == 0:
        print("  ❌ 没有任何文件转换成功", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
