#!/usr/bin/env python3
"""
Markdown → PDF 全库构建脚本（weasyprint），支持分批渲染与断点续跑。

用法：
    python3 md2pdf_weasy.py                  # 全量生成，默认输出 pdf_output/记忆指南-完整版.pdf
    python3 md2pdf_weasy.py --resume         # 从检查点继续（跳过已缓存批次）
    python3 md2pdf_weasy.py --batch-size 20  # 每批最多 20 个文件（默认 40）
    python3 md2pdf_weasy.py --out out.pdf    # 自定义输出路径

实现方式：
    1. 分批把 md 转成 HTML 片段，缓存到 pdf_output/cache/batch_NNNN.html；
    2. 每完成一批把检查点写入 pdf_output/build_state.json
       （已完成批次 / 文件清单 / 失败清单）；
    3. 最后把所有片段合并，整体渲染成一个完整 PDF。
    中断后加 --resume 重新运行，只会补齐缺失的批次再合并渲染，最终输出仍是完整 PDF。
    单文件转换失败不会中断：记录到 pdf_output/failed_files.txt 并继续。
"""

import argparse
import json
import os
import re
import sys
import time

import markdown
from weasyprint import HTML, CSS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "pdf_output")
CACHE_DIR = os.path.join(OUTPUT_DIR, "cache")           # 每批 HTML 片段缓存
STATE_PATH = os.path.join(OUTPUT_DIR, "build_state.json")  # 断点检查点
FAILED_PATH = os.path.join(OUTPUT_DIR, "failed_files.txt")  # 失败文件清单
HTML_DUMP = os.path.join(OUTPUT_DIR, "记忆指南-完整版.html")  # 合并后中间 HTML（调试用）
DEFAULT_OUT = os.path.join(OUTPUT_DIR, "记忆指南-完整版.pdf")

# Markdown 扩展（保持与旧版一致）
MD_EXTENSIONS = ['tables', 'fenced_code', 'codehilite', 'toc', 'nl2br', 'sane_lists']

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

COVER_HTML = '''
<div class="cover">
    <h1>记忆指南</h1>
    <p class="subtitle">Memory Guide</p>
    <hr style="width:40%;margin:1.5em auto;">
    <p class="desc">
        系统化的记忆训练百科<br>
        涵盖记忆科学原理、核心技巧、实战应用及23个学科专项记忆编码<br>
        全库文档合订（篇数以实际生成为准）
    </p>
    <p class="version">v7.2 完整版</p>
</div>
'''


def md2html(filepath):
    """把单个 md 文件转成 HTML；失败时返回占位 HTML 与错误信息（不抛异常）。"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        # 修复相对图片路径：转成 file:// 绝对路径
        text = re.sub(r'!\[([^\]]*)\]\((?!http)([^)]+)\)',
                       lambda m: f'![{m.group(1)}](file://{os.path.join(os.path.dirname(filepath), m.group(2))})',
                       text)
        html = markdown.markdown(text, extensions=MD_EXTENSIONS)
        return html, None
    except Exception as e:
        return f"<p><em>[转换失败 {filepath}: {e}]</em></p>", str(e)


def collect_documents(base):
    """枚举全库文档，返回有序条目列表。

    条目类型：
      {"kind": "html", "html": ...}   封面 / 分部标题 / 小节标题等静态片段
      {"kind": "file", "path": ...}   需要转换的 md 文件
    """
    items = []

    def add_part(title, subtitle=""):
        sub_html = f'<p class="part-sub">{subtitle}</p>' if subtitle else ''
        items.append({"kind": "html",
                      "html": f'<div class="part-title"><h1>{title}</h1>{sub_html}</div>'})

    def add_section(title):
        items.append({"kind": "html",
                      "html": f'<div class="section-title">{title}</div>'})

    def add_file(path):
        items.append({"kind": "file", "path": path})

    # ── 封面 ──
    items.append({"kind": "html", "html": COVER_HTML})

    # ── Part 1: 开篇 ──
    add_part("📖 开篇", "快速入门 · 编码规则")
    for f in ["README.md", "QUICKSTART.md", "MEMORY-ENCODING-RULES.md"]:
        p = os.path.join(base, f)
        if os.path.exists(p):
            add_file(p)

    # ── Part 2: 核心章节 ──
    add_part("📘 核心章节", "55篇专题 · 从记忆科学到影视台词")
    for f in sorted(os.listdir(base)):
        if f.endswith('.md') and re.match(r'^\d{2}-', f):
            add_file(os.path.join(base, f))

    # ── Part 3: 专项目录 ──
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
        # INDEX 放最前
        idx = os.path.join(dpath, "INDEX.md")
        if os.path.exists(idx):
            add_file(idx)
        for f in sorted(os.listdir(dpath)):
            if f.endswith('.md') and f != 'INDEX.md':
                add_section(f"{dirname}/{f}")
                add_file(os.path.join(dpath, f))
        # 二级目录（如 17-programming/python/）
        for sub in sorted(os.listdir(dpath)):
            subpath = os.path.join(dpath, sub)
            if os.path.isdir(subpath):
                add_part(f"📗 {dirname}/{sub}", sub)
                for f in sorted(os.listdir(subpath)):
                    if f.endswith('.md'):
                        add_section(f"{dirname}/{sub}/{f}")
                        add_file(os.path.join(subpath, f))

    # ── Part 4: 实战训练 ──
    pdpath = os.path.join(base, "24-practice")
    if os.path.isdir(pdpath):
        add_part("📙 实战训练", "24-practice · 10个学科实战")
        for f in sorted(os.listdir(pdpath)):
            if f.endswith('.md'):
                add_file(os.path.join(pdpath, f))

    # ── Part 5: 实操练习 ──
    edpath = os.path.join(base, "exercises")
    if os.path.isdir(edpath):
        add_part("📕 实操练习", "exercises · 14个练习")
        for f in sorted(os.listdir(edpath)):
            if f.endswith('.md'):
                add_file(os.path.join(edpath, f))

    # ── Part 6: 实用模板 ──
    tdpath = os.path.join(base, "templates")
    if os.path.isdir(tdpath):
        add_part("📒 实用模板", "templates · 8个模板")
        for f in sorted(os.listdir(tdpath)):
            if f.endswith('.md'):
                add_file(os.path.join(tdpath, f))

    # ── Part 7: Anki ──
    adpath = os.path.join(base, "anki")
    if os.path.isdir(adpath):
        add_part("🃏 Anki 卡片说明", "")
        for f in sorted(os.listdir(adpath)):
            if f.endswith('.md'):
                add_file(os.path.join(adpath, f))

    return items


def plan_batches(items, batch_size):
    """把条目列表切成批次：每批最多 batch_size 个 md 文件，静态条目就近并入所在批。"""
    batches = []
    cur = []
    cur_files = 0
    for it in items:
        # 当前批已满且又遇到新文件时，先封口
        if it["kind"] == "file" and cur_files >= batch_size and cur:
            batches.append(cur)
            cur = []
            cur_files = 0
        cur.append(it)
        if it["kind"] == "file":
            cur_files += 1
    if cur:
        batches.append(cur)
    return batches


def batch_file_list(batch):
    """取出批次内的 md 文件相对路径列表（用于检查点比对）。"""
    return [os.path.relpath(it["path"], BASE_DIR) for it in batch if it["kind"] == "file"]


def render_batch(batch):
    """渲染一个批次为 HTML 片段；返回 (片段, 文件相对路径列表, 失败清单[(路径, 错误)])。"""
    parts = []
    files = []
    failed = []
    for it in batch:
        if it["kind"] == "html":
            parts.append(it["html"])
            continue
        rel = os.path.relpath(it["path"], BASE_DIR)
        files.append(rel)
        html, err = md2html(it["path"])
        if err:
            failed.append((rel, err))
        parts.append(html)
    return '\n'.join(parts), files, failed


def load_state():
    """读取检查点；不存在或损坏时返回 None。"""
    try:
        with open(STATE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def save_state(manifest, completed, failed_map, total_files, batch_size, out_pdf):
    """把检查点原子写入 build_state.json。"""
    completed = sorted(completed)
    state = {
        "version": 1,
        "batch_size": batch_size,
        "out": out_pdf,
        "total_files": total_files,
        # 每批包含的 md 文件清单（断点续跑时用于校验文档树是否变化）
        "manifest": manifest,
        # 已完成的批次序号
        "completed_batches": completed,
        # 已完成的文件清单
        "completed_files": [rel for i in completed if i < len(manifest) for rel in manifest[i]],
        # 失败清单 [{"file": ..., "error": ...}]
        "failed_files": [{"file": k, "error": v} for k, v in sorted(failed_map.items())],
    }
    tmp = STATE_PATH + ".tmp"
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE_PATH)


def write_failed_list(failed_map):
    """把失败清单写入 failed_files.txt（每行：相对路径: 错误）。"""
    with open(FAILED_PATH, 'w', encoding='utf-8') as f:
        for rel, err in sorted(failed_map.items()):
            f.write(f"{rel}: {err}\n")


def count_files(base):
    """统计全库 md 文件数量（含未收录进 PDF 的文档，仅用于提示）。"""
    count = 0
    for root, dirs, files in os.walk(base):
        if '.git' in root or 'pdf_output' in root:
            continue
        for f in files:
            if f.endswith('.md'):
                count += 1
    return count


def build(out_pdf, batch_size, resume):
    """主流程：分批渲染 HTML 片段 → 写检查点 → 合并渲染最终 PDF。"""
    t0 = time.time()
    os.makedirs(CACHE_DIR, exist_ok=True)

    items = collect_documents(BASE_DIR)
    batches = plan_batches(items, batch_size)
    manifest = [batch_file_list(b) for b in batches]
    total_files = sum(len(m) for m in manifest)

    print(f"📚 全库扫描到 {count_files(BASE_DIR)} 个 md 文件，本次收录 {total_files} 篇")
    print(f"📦 分 {len(batches)} 批渲染（每批 ≤ {batch_size} 个文件）")

    # ── 断点续跑：载入检查点 ──
    state = load_state() if resume else None
    if resume and state is None:
        print("⚠️ 未找到检查点（pdf_output/build_state.json），改为全量生成")
    stored_manifest = (state or {}).get("manifest", [])
    completed = set((state or {}).get("completed_batches", [])) if resume else set()
    failed_map = {}
    if resume:
        for d in (state or {}).get("failed_files", []):
            failed_map[d.get("file", "")] = d.get("error", "")

    # ── 分批渲染（每批写缓存 + 检查点）──
    done_count = 0
    for i, batch in enumerate(batches):
        frag_path = os.path.join(CACHE_DIR, "batch_%04d.html" % i)
        can_skip = (resume
                    and i in completed
                    and i < len(stored_manifest)
                    and stored_manifest[i] == manifest[i]
                    and os.path.exists(frag_path))
        if not can_skip:
            if resume and i in completed:
                print(f"⚠️ 批 {i+1} 文件清单与检查点不一致或缓存缺失，重新渲染")
            fragment, files, failed = render_batch(batch)
            with open(frag_path, 'w', encoding='utf-8') as f:
                f.write(fragment)
            for rel, err in failed:
                failed_map[rel] = err
                print(f"    ⚠️ 转换失败（已跳过并记录）: {rel}: {err}", file=sys.stderr)
            completed.add(i)
            save_state(manifest, completed, failed_map, total_files, batch_size, out_pdf)
            write_failed_list(failed_map)
        done_count += len(manifest[i])
        skip_note = "（跳过已缓存）" if can_skip else ""
        print(f"[批 {i+1}/{len(batches)}] 已完成 {done_count}/{total_files} 个文件{skip_note}")

    # ── 合并片段，整体渲染最终 PDF ──
    print("📝 合并 HTML 片段...")
    fragments = []
    for i in range(len(batches)):
        frag_path = os.path.join(CACHE_DIR, "batch_%04d.html" % i)
        with open(frag_path, 'r', encoding='utf-8') as f:
            fragments.append(f.read())
    body_html = '\n'.join(fragments)
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

    # 保存中间 HTML 便于调试
    with open(HTML_DUMP, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"💾 中间 HTML 已保存 ({os.path.getsize(HTML_DUMP)/1024/1024:.1f} MB)")

    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    print("📄 渲染最终 PDF... (大库可能需要几分钟)")
    try:
        html_doc = HTML(string=full_html, base_url=BASE_DIR)
        css = CSS(string=CSS_STYLE)
        html_doc.write_pdf(out_pdf, stylesheets=[css])
    except Exception as e:
        print(f"❌ 最终渲染失败: {e}", file=sys.stderr)
        print("提示: 各批 HTML 片段已缓存，用 --resume 重跑可跳过已缓存批次、直接重试合并渲染",
              file=sys.stderr)
        sys.exit(1)

    # ── 汇总 ──
    elapsed = time.time() - t0
    success = total_files - len(failed_map)
    size_mb = os.path.getsize(out_pdf) / 1024 / 1024
    print(f"\n{'='*60}")
    print("✅ 完成!")
    print(f"📄 文件: {out_pdf}")
    print(f"💾 大小: {size_mb:.1f} MB")
    print(f"📊 成功 {success} 篇 / 失败 {len(failed_map)} 篇 / 耗时 {elapsed:.1f} 秒")
    if failed_map:
        print(f"⚠️ 失败清单: {FAILED_PATH}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="记忆指南全库 Markdown → PDF 构建（weasyprint，支持分批与断点续跑）")
    parser.add_argument("--resume", action="store_true",
                        help="从 pdf_output/build_state.json 检查点继续，跳过已缓存批次")
    parser.add_argument("--batch-size", type=int, default=40, metavar="N",
                        help="每批最多渲染的文件数（默认 40，内存不足时调小）")
    parser.add_argument("--out", default=DEFAULT_OUT, metavar="PATH",
                        help=f"输出 PDF 路径（默认 {DEFAULT_OUT}）")
    args = parser.parse_args()

    if args.batch_size < 1:
        parser.error("--batch-size 必须 ≥ 1")

    print("=" * 60)
    print("🧠 记忆指南 → 完整 PDF (weasyprint)")
    print("=" * 60)

    build(args.out, args.batch_size, args.resume)


if __name__ == "__main__":
    main()
