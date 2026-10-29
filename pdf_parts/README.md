# pdf_parts 构建说明

> **📍 本章导航**：前置 → 无 ｜ 相关 → [README](../README.md) ｜ 难度 ⭐⭐ ｜ 阅读 ~5min

全库 PDF 构建脚本的使用说明。构建脚本支持**分批渲染 + 断点续跑**，大任务中断后不必从头再来。

## 安装依赖

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple weasyprint markdown
```

> weasyprint 依赖系统 pango 库（Ubuntu/Debian：`sudo apt install libpango-1.0-0 libpangocairo-1.0-0`）。需 Python 3.8+。

## 用法示例

```bash
# 全量生成（默认输出 pdf_output/记忆指南-完整版.pdf）
python3 md2pdf_weasy.py

# 中断后从检查点继续（跳过已缓存批次）
python3 md2pdf_weasy.py --resume

# 内存不足时调小批次 / 自定义输出路径
python3 md2pdf_weasy.py --batch-size 10 --out pdf_output/我的版本.pdf

# 分组生成（共享转换器，若干 md → 一个 PDF）
python3 pdf_parts/convert.py pdf_output/group1.pdf 01-记忆科学基础.md 02-核心记忆技巧.md
```

## 参数表（md2pdf_weasy.py）

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| （无参数） | — | 全量生成完整 PDF，向后兼容 |
| `--resume` | 关 | 读取检查点从断点继续，跳过已完成批次 |
| `--batch-size N` | `40` | 每批最多渲染的文件数，内存不足时调小 |
| `--out PATH` | `pdf_output/记忆指南-完整版.pdf` | 输出 PDF 路径 |

`pdf_parts/convert.py` 保持原 CLI：`python3 convert.py <output.pdf> <file1.md> ...`，单文件失败不中断、末尾汇总。

## 检查点 / 缓存 / 失败清单位置

| 文件 / 目录 | 作用 |
| --- | --- |
| `pdf_output/build_state.json` | 检查点：已完成批次、文件清单、失败清单 |
| `pdf_output/cache/` | 每批 HTML 片段缓存（`batch_0000.html` …），resume 依据 |
| `pdf_output/failed_files.txt` | 失败文件清单（每行：`路径: 错误`） |
| `pdf_output/记忆指南-完整版.html` | 合并后中间 HTML，便于排查渲染问题 |

## 常见问题

- **中断了怎么办？** 重新执行 `python3 md2pdf_weasy.py --resume`，只会补齐未缓存的批次再合并渲染，最终仍是完整 PDF。
- **失败文件怎么看？** 看结尾汇总、`pdf_output/failed_files.txt`，或检查点 `build_state.json` 的 `failed_files` 字段；失败文件已用占位符排版，不影响其余内容。
- **内存不足 / 太慢？** 调小 `--batch-size`（如 `--batch-size 10`）。
- **想彻底重来？** 删除 `pdf_output/build_state.json` 与 `pdf_output/cache/` 后重新全量执行。
