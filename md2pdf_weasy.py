#!/usr/bin/env python3
"""
Complete Markdown → PDF using weasyprint.
All 286 files, no content truncation, proper CJK rendering.
"""

import os
import re
import markdown
from weasyprint import HTML, CSS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE_DIR, "pdf_output", "记忆指南-完整版.pdf")

CSS_STYLE = """
@font-face {
    font-family: 'NotoSansCJK';
    src: url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');
    font-weight: normal;
}
@font-face {
    font-family: 'NotoSansCJK';
    src: url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc');
    font-weight: bold;
}
@page {
    size: A4;
    margin: 2cm 1.8cm 2cm 1.8cm;
    @top-center {
        content: "记忆指南 Memory Guide";
        font-family: 'NotoSansCJK', sans-serif;
        font-size: 8pt;
        color: #999;
    }
    @bottom-center {
        content: "— " counter(page) " —";
        font-family: 'NotoSansCJK', sans-serif;
        font-size: 8pt;
        color: #999;
    }
}
@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}
body {
    font-family: 'NotoSansCJK', 'Noto Sans CJK SC', sans-serif;
    font-size: 10pt;
    line-height: 1.8;
    color: #333;
}
h1 { font-size: 22pt; margin-top: 0.8em; margin-bottom: 0.4em; color: #222; page-break-before: always; border-bottom: 2px solid #34495e; padding-bottom: 0.3em; }
h2 { font-size: 17pt; margin-top: 0.8em; margin-bottom: 0.3em; color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 0.2em; }
h3 { font-size: 14pt; margin-top: 0.6em; margin-bottom: 0.3em; color: #34495e; }
h4 { font-size: 12pt; margin-top: 0.5em; margin-bottom: 0.2em; color: #34495e; }
h5, h6 { font-size: 11pt; margin-top: 0.4em; margin-bottom: 0.2em; color: #555; }
h1:first-of-type { page-break-before: avoid; }
p { margin: 0.3em 0; text-align: justify; }
blockquote {
    border-left: 3px solid #3498db;
    padding: 0.3em 0.8em;
    margin: 0.5em 0;
    background: #f8f9fa;
    color: #555;
    font-size: 9.5pt;
}
code {
    font-family: 'Noto Sans Mono CJK SC', 'Courier New', monospace;
    background: #f0f0f0;
    padding: 0.1em 0.3em;
    border-radius: 3px;
    font-size: 9pt;
}
pre {
    background: #f6f6f6;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.6em 0.8em;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
}
pre code {
    background: none;
    padding: 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.5em 0;
    font-size: 9pt;
    page-break-inside: auto;
}
th, td {
    border: 1px solid #ddd;
    padding: 0.3em 0.5em;
    text-align: left;
}
th {
    background: #ecf0f1;
    font-weight: bold;
}
tr:nth-child(even) { background: #f9f9f9; }
ul, ol { margin: 0.3em 0; padding-left: 1.5em; }
li { margin: 0.15em 0; }
hr { border: none; border-top: 1px solid #ddd; margin: 1em 0; }
a { color: #2980b9; text-decoration: none; }
img { max-width: 100%; }
.cover {
    text-align: center;
    padding-top: 6cm;
    page-break-after: always;
}
.cover h1 {
    font-size: 36pt;
    border: none;
    color: #222;
    page-break-before: avoid;
    margin-bottom: 0.2em;
}
.cover .subtitle {
    font-size: 16pt;
    color: #666;
    margin-bottom: 0.5em;
}
.cover .desc {
    font-size: 11pt;
    color: #888;
    line-height: 2;
}
.cover .version {
    font-size: 10pt;
    color: #aaa;
    margin-top: 2em;
}
.part-title {
    text-align: center;
    padding-top: 3cm;
    page-break-before: always;
    page-break-after: always;
}
.part-title h1 {
    font-size: 28pt;
    border: none;
    color: #222;
    page-break-before: avoid;
}
.part-title .part-sub {
    font-size: 12pt;
    color: #888;
}
.section-title {
    font-size: 13pt;
    font-weight: bold;
    color: #34495e;
    margin: 1em 0 0.3em 0;
    padding-bottom: 0.2em;
    border-bottom: 1px dotted #ccc;
}
"""


def build_html(base):
    """Build complete HTML from all 286 md files."""
    parts = []
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'toc', 'nl2br', 'sane_lists']

    def md2html(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except:
            return "<p><em>[读取失败]</em></p>"
        # Fix relative image paths
        text = re.sub(r'!\[([^\]]*)\]\((?!http)([^)]+)\)',
                       lambda m: f'![{m.group(1)}](file://{os.path.join(os.path.dirname(filepath), m.group(2))})',
                       text)
        return markdown.markdown(text, extensions=md_extensions)

    def add_part(title, subtitle=""):
        sub_html = f'<p class="part-sub">{subtitle}</p>' if subtitle else ''
        parts.append(f'<div class="part-title"><h1>{title}</h1>{sub_html}</div>')

    def add_section(title):
        parts.append(f'<div class="section-title">{title}</div>')

    # ── Cover ──
    parts.append('''
    <div class="cover">
        <h1>记忆指南</h1>
        <p class="subtitle">Memory Guide</p>
        <hr style="width:40%;margin:1.5em auto;">
        <p class="desc">
            系统化的记忆训练百科<br>
            涵盖记忆科学原理、核心技巧、实战应用及23个学科专项记忆编码<br>
            共 286 篇文档 · 170+ 篇专题文章
        </p>
        <p class="version">v5.1 完整版</p>
    </div>
    ''')

    # ── Part 1: Intro ──
    add_part("📖 开篇", "快速入门 · 编码规则")
    for f in ["README.md", "QUICKSTART.md", "MEMORY-ENCODING-RULES.md"]:
        p = os.path.join(base, f)
        if os.path.exists(p):
            parts.append(md2html(p))

    # ── Part 2: Core chapters ──
    add_part("📘 核心章节", "55篇专题 · 从记忆科学到影视台词")
    for f in sorted(os.listdir(base)):
        if f.endswith('.md') and re.match(r'^\d{2}-', f):
            parts.append(md2html(os.path.join(base, f)))

    # ── Part 3: Subdirectories ──
    subdir_info = [
        ("01-number", "数字记忆编码"), ("02-card", "扑克牌记忆编码"),
        ("03-vocabulary", "词汇记忆编码"), ("04-history", "历史记忆编码"),
        ("05-chemistry", "化学记忆编码"), ("06-geography", "地理记忆编码"),
        ("07-speech", "演讲记忆编码"), ("08-face-name", "人脸与姓名记忆"),
        ("09-english-word", "英语词汇记忆"), ("10-combo", "组合记忆"),
        ("11-math-physics", "数学与物理"), ("12-bio-medical", "生物与医学"),
        ("13-law", "法律记忆"), ("14-route", "路线记忆"),
        ("15-procedure", "程序记忆"), ("16-music", "音乐记忆"),
        ("17-programming", "编程记忆"), ("18-finance", "金融记忆"),
        ("19-psychology", "心理学"), ("20-astronomy", "天文记忆"),
        ("21-sports", "体育记忆"), ("22-art", "艺术记忆"),
        ("23-language", "语言学习"),
    ]
    for dirname, desc in subdir_info:
        dpath = os.path.join(base, dirname)
        if not os.path.isdir(dpath):
            continue
        add_part(f"📗 {dirname}", desc)
        # INDEX first
        idx = os.path.join(dpath, "INDEX.md")
        if os.path.exists(idx):
            parts.append(md2html(idx))
        for f in sorted(os.listdir(dpath)):
            if f.endswith('.md') and f != 'INDEX.md':
                add_section(f"{dirname}/{f}")
                parts.append(md2html(os.path.join(dpath, f)))

    # ── Part 4: Practice ──
    pdpath = os.path.join(base, "24-practice")
    if os.path.isdir(pdpath):
        add_part("📙 实战训练", "24-practice · 10个学科实战")
        for f in sorted(os.listdir(pdpath)):
            if f.endswith('.md'):
                parts.append(md2html(os.path.join(pdpath, f)))

    # ── Part 5: Exercises ──
    edpath = os.path.join(base, "exercises")
    if os.path.isdir(edpath):
        add_part("📕 实操练习", "exercises · 13个练习")
        for f in sorted(os.listdir(edpath)):
            if f.endswith('.md'):
                parts.append(md2html(os.path.join(edpath, f)))

    # ── Part 6: Templates ──
    tdpath = os.path.join(base, "templates")
    if os.path.isdir(tdpath):
        add_part("📒 实用模板", "templates · 7个模板")
        for f in sorted(os.listdir(tdpath)):
            if f.endswith('.md'):
                parts.append(md2html(os.path.join(tdpath, f)))

    # ── Part 7: Anki ──
    adpath = os.path.join(base, "anki")
    if os.path.isdir(adpath):
        add_part("🃏 Anki 卡片说明", "")
        for f in sorted(os.listdir(adpath)):
            if f.endswith('.md'):
                parts.append(md2html(os.path.join(adpath, f)))

    return '\n'.join(parts)


def count_files(base):
    """Count all md files."""
    count = 0
    for root, dirs, files in os.walk(base):
        if '.git' in root or 'pdf_output' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                count += 1
    return count


def main():
    print("=" * 60)
    print("🧠 记忆指南 → 完整 PDF (weasyprint)")
    print("=" * 60)

    total = count_files(BASE_DIR)
    print(f"📋 共 {total} 个文档")

    print("📝 构建 HTML...")
    body_html = build_html(BASE_DIR)

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>记忆指南 Memory Guide - 完整版</title>
</head>
<body>
{body_html}
</body>
</html>"""

    # Save intermediate HTML for debugging
    html_path = os.path.join(BASE_DIR, "pdf_output", "记忆指南-完整版.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"💾 中间 HTML 已保存 ({os.path.getsize(html_path)/1024/1024:.1f} MB)")

    print("📄 生成 PDF... (可能需要几分钟)")
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    html_doc = HTML(string=full_html, base_url=BASE_DIR)
    css = CSS(string=CSS_STYLE)
    html_doc.write_pdf(OUTPUT, stylesheets=[css])

    size_mb = os.path.getsize(OUTPUT) / 1024 / 1024
    print(f"\n{'='*60}")
    print(f"✅ 完成!")
    print(f"📄 文件: {OUTPUT}")
    print(f"💾 大小: {size_mb:.1f} MB")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()