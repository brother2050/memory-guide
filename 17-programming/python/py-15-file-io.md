# py-15 文件 IO — 记忆编码

> **📍 本章导航**：前置 → [py-14 标准库](py-14-stdlib.md) ｜ 相关 → [py-03 字符串](py-03-strings.md)·[py-16 正则](py-16-regex.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~11min（约 7.5k tokens）
>
> 本章逻辑链：py-14 认识了 os/pathlib/json 工具 → 本篇解决"数据怎么安全存进磁盘、再原样取回" → 引出 py-16"从取回的文本里按格式捞信息"。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 开窗点钞三式 | PY-15-01~03 | open 开窗、with 自动关窗、read 三兄弟 |
| 窗口业务牌 | PY-15-04~06 | 模式矩阵 r/w/a/x + b/+ |
| 凭证字迹 | PY-15-07~08 | 编码坑与换行符 |
| 专窗打单 | PY-15-09~11 | csv/json 文件实操 |
| 金库盘点 | PY-15-12~13 | os.walk 与 pathlib 遍历 |

## 一、开窗点钞三式（open / with / read）

### PY-15-01 `open()` 到柜台开窗口 Opening Files
- **是什么**：`open(路径, mode, encoding)` 打开文件返回文件对象（f 是窗口凭证夹）；默认 `mode="r"` 只读，用完必须 `f.close()` 关窗。
- **为什么**：磁盘数据不是内存对象——必须显式"开窗办理"，窗口不关会占系统句柄、缓冲区里的数据可能丢 → 流程：开窗→办理→关窗 → 边界：文件不存在时 `open(不存在, "r")` 抛 `FileNotFoundError`。
- **怎么写**：
```python
f = open("acct.txt", "w", encoding="utf-8")   # 开"存款"窗口
f.write("余额: 100\n")
f.close()
f = open("acct.txt", encoding="utf-8")        # 开"取款"窗口
print("读到:", f.read().strip())
print("窗口已关闭?", f.closed)
f.close()
print("关闭后:", f.closed)
```
→ 运行输出：`读到: 余额: 100` ｜ `窗口已关闭? False` ｜ `关闭后: True`
- **何时用/不用**：几乎总用 `with`（PY-15-02）代替裸 open/close；只有要精确控制关闭时机时才手动管理。
- **锚点**：银行柜台开窗口：取号开窗（open）、递上凭证夹（f）、办完销户（close）；忘了关窗=现金与凭证悬在窗口。
- **易错**：只 `open` 不 `close` → 数据可能没刷进磁盘、句柄泄漏；路径写相对路径依赖"当前工作目录"，换目录就 `FileNotFoundError`。
- **关联**：`→ PY-15-02：with 是标准办卡流程`；`→ PY-15-04：mode 决定办什么业务`。

### PY-15-02 `with` 自动关窗 Context Manager
- **是什么**：`with open(...) as f:` 把文件交给上下文管理器（context manager）：进块自动开、出块（包括抛异常）自动 `close`。
- **为什么**：手动 close 会忘、异常时根本走不到 close → with 保证"无论怎么离开都落锁" → 行为：缩进块结束即关闭 → 边界：`f` 出了 with 就不能再用（`ValueError: I/O operation on closed file`）。
- **怎么写**：
```python
with open("slip.txt", "w", encoding="utf-8") as f:
    f.write("存单\n")
    print("业务中窗口开着:", not f.closed)
print("业务完自动关窗:", f.closed)
```
→ 运行输出：`业务中窗口开着: True` ｜ `业务完自动关窗: True`
- **何时用/不用**：所有文件操作一律 with；一个 with 可同时开多个文件（逗号并列或嵌套）。
- **锚点**：VIP 自动关窗服务：业务办完自动关窗落锁，哪怕客户中途发火摔门（抛异常）也照样锁好。
- **易错**：with 块内 `f` 才有效，块外继续 `f.read()` 报"文件已关闭"；把 `f.read()` 写在 with 外是常见错位。
- **关联**：`→ PY-15-01：open/close 的自动化`；`→ PY-10-11：__enter__/__exit__ 魔术方法`。

### PY-15-03 点钞三式：read / readline / readlines
- **是什么**：三种读取粒度：`read()` 整个文件进一个字符串；`readline()` 每次一行；`readlines()`/直接迭代返回行列表/逐行。
- **为什么**：大文件用 `read()` 一口气吃进内存会爆 → 按行流式读取内存恒定 → 行为：`read()` 返回带 `\n` 的完整文本 → 边界：文件指针读过就到末尾，再读是空串。
- **怎么写**：
```python
with open("notes.txt", encoding="utf-8") as f:
    print("整捆点完:", repr(f.read()))
with open("notes.txt", encoding="utf-8") as f:
    print("一张张点:", repr(f.readline().strip()), repr(f.readline().strip()))
with open("notes.txt", encoding="utf-8") as f:
    print("装订成沓:", [line.strip() for line in f.readlines()])
```
→ 运行输出（文件三行"第一张/第二张/第三张"）：`整捆点完: '第一张\n第二张\n第三张\n'` ｜ `一张张点: '第一张' '第二张'` ｜ `装订成沓: ['第一张', '第二张', '第三张']`
- **何时用/不用**：小文件 `read()`；大文件/逐行处理 `for line in f`（最省内存）；要列表用 `readlines()` 或推导式。
- **锚点**：点钞三式：整捆一次点完（read）、一张张点（readline）、点完装订成沓（readlines）。
- **易错**：文件指针是单行道——同一个 `f` 读两次，第二次拿到空；`readline()` 到末尾返回 `""` 不是报错，循环里要判空。
- **关联**：`→ PY-15-02：读取都在 with 块内做`。

## 二、窗口业务牌（读写模式矩阵）

### PY-15-04 读写模式矩阵 r / w / a / x File Modes
- **是什么**：`mode` 决定业务类型：`r` 只读（默认）、`w` 写（**清空重建**）、`a` 追加、`x` 独占创建（已存在则失败）；加 `+` 表示可读可写，加 `b` 表示二进制。
- **为什么**："打开即清空"是数据丢失重灾区 → 必须按业务选对窗口 → 行为：`w` 先截断文件、`x` 保证不覆盖 → 边界：`r+`/`w+` 混合模式行为微妙，新手先别用。
- **怎么写**：
```python
with open("mode.txt", "x", encoding="utf-8") as f:   # x = 新开户
    f.write("开户行: A\n")
try:
    open("mode.txt", "x")                            # 再开同名户
except FileExistsError as e:
    print("重复开户被拒:", e)
with open("mode.txt", "a", encoding="utf-8") as f:   # a = 续存
    f.write("续存: B\n")
with open("mode.txt", encoding="utf-8") as f:        # r = 只读
    print("账户流水:", f.read().splitlines())
```
→ 运行输出：`重复开户被拒: [Errno 17] File exists: 'mode.txt'` ｜ `账户流水: ['开户行: A', '续存: B']`
- **何时用/不用**：读用 `r`；重建用 `w`；记流水用 `a`；确保不覆盖用 `x`；要"读改写"整个文件，宁可读进来再 `w` 重写。
- **锚点**：窗口业务牌：r 取款、w 销户重开（旧记录清零）、a 续存（流水接着记）、x 新开户（已有户不开）。
- **易错**：`w` 打开已存在文件**立刻清空**（哪怕后面没写任何东西）；`r` 打开不存在的文件抛 `FileNotFoundError`，`w`/`a` 会自动建。
- **关联**：`→ PY-15-05：w 与 a 的对比`；`→ PY-15-06：加 b 变二进制窗口`。

### PY-15-05 `w` 覆盖 vs `a` 追加 Truncate vs Append
- **是什么**：`w` 每次从头写（旧内容全没）、`a` 永远在末尾写（旧内容保留）。
- **为什么**：日志/流水用 `w` 会每天清零只剩最后一笔 → 持久累积数据必须 `a` → 行为：`a` 还会在文件不存在时创建 → 边界：两者都不提供"中间插入"，要改中间内容得整读整写。
- **怎么写**：
```python
with open("flow.txt", "w", encoding="utf-8") as f: f.write("1月\n")
with open("flow.txt", "w", encoding="utf-8") as f: f.write("2月\n")   # 覆盖旧账
with open("flow.txt", encoding="utf-8") as f: print("w 之后只剩:", f.read().splitlines())
with open("flow.txt", "a", encoding="utf-8") as f: f.write("3月\n")   # 接着流水记
with open("flow.txt", encoding="utf-8") as f: print("a 之后流水:", f.read().splitlines())
```
→ 运行输出：`w 之后只剩: ['2月']` ｜ `a 之后流水: ['2月', '3月']`
- **何时用/不用**：配置快照/导出结果用 `w`；日志、账本、csv 累积行用 `a`。
- **锚点**：`w` 是"重开存折"（旧页全撕）、`a` 是"流水账往下记"（旧页留着）。
- **易错**：循环里误用 `w` 每轮清空，最后只剩一轮数据；`a` 模式下 `seek` 到中间写也会强制回到末尾。
- **关联**：`→ PY-15-04：模式矩阵里的两格`；`→ PY-14-11：日志落盘常用追加`。

### PY-15-06 文本模式 vs 二进制模式 Text vs Binary
- **是什么**：文本模式（`r/w/a`）读写 `str`，平台自动换行转换、需 `encoding`；二进制模式（`rb/wb/ab`）读写 `bytes`，逐字节原样进出、不许指定 encoding。
- **为什么**：图片/压缩包/加密数据没有"字符"可言，按文本读写会损坏字节 → 二进制模式把磁盘字节原样搬 → 行为：文本文件用 `rb` 读会得到编码后的字节 → 边界：`str` 与 `bytes` 互转必须显式 encode/decode（→ PY-03-11）。
- **怎么写**：
```python
data = "金额¥100"
with open("cash.bin", "wb") as f: f.write(data.encode("utf-8"))
with open("cash.bin", "rb") as f: raw = f.read()
print("二进制读回:", raw)
print("解码后:", raw.decode("utf-8"))
with open("cash.txt", "w", encoding="utf-8") as f: f.write(data)
with open("cash.txt", "rb") as f: print("文本文件的原始字节:", f.read())
```
→ 运行输出：`二进制读回: b'\xe9\x87\x91\xe9\xa2\x9d\xc2\xa5100'` ｜ `解码后: 金额¥100` ｜ `文本文件的原始字节: b'\xe9\x87\x91\xe9\xa2\x9d\xc2\xa5100'`
- **何时用/不用**：纯文本（配置、csv、日志）用文本模式；图片/音视频/序列化字节用 `rb/wb`。
- **锚点**：柜员手抄汉字（文本模式，认字迹）vs 点钞机过钞（二进制，钞票原样过机不认字）。
- **易错**：文本模式写二进制内容抛 `TypeError: write() argument must be str`；二进制读回的 `b"..."` 要 `.decode()` 才是字符串。
- **关联**：`→ PY-03-11：encode/decode 与 bytes`；`→ PY-15-07：文本模式的编码坑`。

## 三、凭证字迹（编码与换行）

### PY-15-07 编码坑：UnicodeDecodeError Encoding Pitfalls
- **是什么**：文本模式必须按正确 encoding 解码字节；编码不匹配抛 `UnicodeDecodeError`，或用 `errors="replace"` 强读出 `\ufffd` 乱码。
- **为什么**：磁盘上只有字节没有"字符"，utf-8 与 gbk 对同一汉字字节不同 → 用错字迹读凭证=盖错章 → 行为：解码失败立刻报错（Python 默认不悄悄吞）→ 边界：`errors="ignore"` 会静默丢字，慎用。
- **怎么写**（先造一份 gbk 字迹的凭证）：
```python
with open("gbk.txt", "wb") as f:
    f.write("余额100元".encode("gbk"))
try:
    open("gbk.txt", encoding="utf-8").read()
except UnicodeDecodeError as e:
    print("UnicodeDecodeError:", e)
with open("gbk.txt", encoding="gbk") as f:
    print("用对字迹读:", f.read())
with open("gbk.txt", encoding="utf-8", errors="replace") as f:
    print("强读换字:", f.read())
```
→ 运行输出：`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd3 in position 0: invalid continuation byte` ｜ `用对字迹读: 余额100元` ｜ `强读换字: ���100Ԫ`
- **何时用/不用**：打开来源不明的文本一律显式给 encoding（工程默认 utf-8）；处理历史 Windows 文件记得可能是 gbk。
- **锚点**：凭证上的字迹章：utf-8 是行内标准字迹，gbk 是旧式字迹；拿旧凭证盖新章（用错编码）当场对不上账（报错）或字迹糊掉（replace）。
- **易错**：`open()` 不写 encoding 依赖系统默认（跨机器行为不同）；`errors="ignore"` 静默丢字符，比报错更难排查。
- **关联**：`→ PY-03-12：Unicode 与常见编码`；`→ PY-15-08：另一大格式坑是换行符`。

### PY-15-08 换行符与 `newline` 参数 Newline Handling
- **是什么**：Windows 用 `\r\n`、Linux 用 `\n` 表示换行；文本模式默认"通用换行"读入时统一成 `\n`，写入时 `newline=None` 转成平台约定，`newline=""` 原样保留。
- **为什么**：跨系统传的小票（csv/日志）换行符不同，做字节比对、按行 split 会莫名差一个 `\r` → 用 `newline` 控制是否翻译 → 行为：`newline=""` 读写都原样 → 边界：二进制模式无此翻译。
- **怎么写**（用 `newline="\r\n"` 存一张 CRLF 小票）：
```python
with open("nl.txt", "w", encoding="utf-8", newline="\r\n") as f:
    f.write("a\nb\n")
print("原始字节:", open("nl.txt", "rb").read())
with open("nl.txt", encoding="utf-8") as f:              # 默认：统一成 \n
    print("默认读法:", repr(f.read()))
with open("nl.txt", encoding="utf-8", newline="") as f:  # 原样保留
    print("原样读法:", repr(f.read()))
```
→ 运行输出：`原始字节: b'a\r\nb\r\n'` ｜ `默认读法: 'a\nb\n'` ｜ `原样读法: 'a\r\nb\r\n'`
- **何时用/不用**：普通读写就用默认；处理 csv/固定格式小票用 `newline=""`（写 csv 时也建议给）；比对原始字节用 `rb`。
- **锚点**：柜台叫号机小票的"回车+换行"两步走（`\r\n`）：默认点钞时帮你把两步并成一步（`\n`），要验小票原样就得挂"原样"牌（`newline=""`）。
- **易错**：字符串里 `strip()` 没去掉 `\r` 导致 `"a" == line.strip()` 失败；写 csv 不给 `newline=""` 在 Windows 上会多出空行。
- **关联**：`→ PY-15-07：编码是另一半格式坑`；`→ PY-15-09：csv 读写建议配 newline=""`。

## 四、专窗打单（csv / json 文件）

### PY-15-09 csv 读：批量点验票据 `csv.reader` / `DictReader`
- **是什么**：`csv.reader` 把每行解析成格子列表，`csv.DictReader` 用首行当票头、每行成 `{列名: 值}` 字典。
- **为什么**：逗号分隔文本手工 `split(",")` 遇到引号包裹的逗号、字段里有换行就崩 → csv 模块按 RFC 规则正确切格 → 行为：所有值都是字符串（数字要自己转）→ 边界：分隔符/引号可配参数。
- **怎么写**：
```python
import csv
with open("tickets.csv", "w", encoding="utf-8", newline="") as f:
    f.write("日期,金额\n2026-10-06,100\n2026-10-07,200\n")
with open("tickets.csv", encoding="utf-8", newline="") as f:
    print("逐格点票:", list(csv.reader(f)))
with open("tickets.csv", encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        print("带票头点验:", r["日期"], r["金额"])
```
→ 运行输出：`逐格点票: [['日期', '金额'], ['2026-10-06', '100'], ['2026-10-07', '200']]` ｜ `带票头点验: 2026-10-06 100` ｜ `带票头点验: 2026-10-07 200`
- **何时用/不用**：表格数据交换用 csv；嵌套结构用 json（PY-15-11）；行数大到内存放不下用逐行 `for row in reader`。
- **锚点**：批量点验票据：逐格点票（reader）还是每张票带票头点验（DictReader），票头=首行栏目名。
- **易错**：`DictReader` 的列名敲错抛 `KeyError`（不报"列不存在"）；读到的 `"100"` 是字符串，做加法前要 `int()`。
- **关联**：`→ PY-15-10：csv 写是它的逆操作`；`→ PY-15-08：读写 csv 配 newline=""`。

### PY-15-10 csv 写：开票打单 `csv.writer` / `DictWriter`
- **是什么**：`csv.writer(f).writerow(s)` 按行写出格子；`csv.DictWriter` 按 `fieldnames` 票头填字典，`writeheader()` 先打票头。
- **为什么**：手拼 `"a,b\n"` 遇到字段里有逗号/引号就产出坏文件 → writer 自动加引号转义 → 行为：`writerows` 一次写多行 → 边界：DictWriter 字典缺字段抛 `ValueError`。
- **怎么写**：
```python
import csv
with open("out.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows([("日期", "金额"), ("2026-10-06", 100)])
print("writer 打单:", open("out.csv", encoding="utf-8").read().splitlines())
with open("out2.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["日期", "金额"])
    w.writeheader()
    w.writerow({"日期": "2026-10-08", "金额": 300})
print("DictWriter 打单:", open("out2.csv", encoding="utf-8").read().splitlines())
```
→ 运行输出：`writer 打单: ['日期,金额', '2026-10-06,100']` ｜ `DictWriter 打单: ['日期,金额', '2026-10-08,300']`
- **何时用/不用**：导出表格给 Excel 用 csv；要类型保留用 json；追加写把 mode 换 `"a"`。
- **锚点**：开票打单：按格开票（writer）或按票头栏目填单（DictWriter），票头先打印一行（writeheader）。
- **易错**：忘给 `newline=""` 在 Windows 上行距加倍；`DictWriter` 字典键拼错抛 `ValueError: dict contains fields not in fieldnames`。
- **关联**：`→ PY-15-09：读回方式`。

### PY-15-11 json 文件：保险柜存取件 `json.dump` / `json.load`
- **是什么**：`json.dump(对象, f)` 把对象序列化写进文件、`json.load(f)` 从文件反序列化读回；`indent` 让凭条分行打印，`ensure_ascii=False` 保留中文。
- **为什么**：内存对象进程结束就没了 → 存成通用格式才能持久化与交换 → 行为：往返（dump→load）得到等价对象 → 边界：json 只认基础类型，datetime 等要先转字符串。
- **怎么写**：
```python
import json
account = {"户名": "张三", "余额": 100}
with open("vault.json", "w", encoding="utf-8") as f:
    json.dump(account, f, ensure_ascii=False, indent=2)   # 存件、开凭条
with open("vault.json", encoding="utf-8") as f:
    back = json.load(f)                                    # 凭条取件
print("取回:", back, "| 与原件一致:", back == account)
```
→ 运行输出：`取回: {'户名': '张三', '余额': 100} | 与原件一致: True`；凭条内容（真实文件）：
```
{
  "户名": "张三",
  "余额": 100
}
```
- **何时用/不用**：配置、API 结果落盘用 json；人读表格用 csv；超大文件用逐块解析或专用格式。
- **锚点**：保险柜存取件凭条：存件（dump）开一张打印清楚的凭条（indent 分行），取件（load）凭条验货。
- **易错**：`json.load(f)` 和 `json.loads(s)` 只差一个 s（文件 vs 字符串）；手改 json 文件留了尾逗号 → `JSONDecodeError`。
- **关联**：`→ PY-14-04：json 编解码基础`。

## 五、金库盘点（目录遍历）

### PY-15-12 `os.walk`：金库逐层盘点 Directory Walking
- **是什么**：`os.walk(根目录)` 每层产出三元组 `(当前目录路径, 子目录列表, 文件列表)`，默认自顶向下递归整棵树。
- **为什么**：批量处理"目录里所有文件"（重命名、统计、找垃圾）靠手写递归又丑又易错 → walk 把"逐层盘点"做成迭代器 → 行为：边遍历边可改 `dirs` 剪枝 → 边界：目录树巨大时它是惰性的、不爆内存。
- **怎么写**（先造 `vault/2026/10` 三层结构各放一个 .txt）：
```python
import os
for root, dirs, files in os.walk("vault"):
    print(root, "→ 子柜:", dirs, "→ 件:", sorted(files))
```
→ 运行输出：
```
vault → 子柜: ['2026'] → 件: ['a.txt']
vault/2026 → 子柜: ['10'] → 件: ['b.txt']
vault/2026/10 → 子柜: [] → 件: ['c.txt']
```
- **何时用/不用**：全盘扫描/批量改名用 walk；只要一层用 `os.listdir`/`Path.iterdir`；按模式筛选用 `Path.rglob`（PY-15-13）。
- **锚点**：金库逐层盘点：盘点员从大门（根目录）进，每层报"子柜几个、各件几件"（dirs/files），直到最底层小库。
- **易错**：`files` 只是文件名不含路径，要 `os.path.join(root, f)` 才能打开；遍历时删除目录要小心 `dirs[:]` 剪枝写法。
- **关联**：`→ PY-14-01：os 模块基础`；`→ PY-15-13：pathlib 的替代写法`。

### PY-15-13 pathlib 实操：电子流水单 Path I/O
- **是什么**：`Path.write_text/read_text` 一步读写文本，`iterdir` 列一层，`rglob("*.txt")` 按模式全树搜索返回 Path 对象。
- **为什么**：walk+join+open 三件套太啰嗦 → pathlib 把"写、读、找"压缩成链式对象操作 → 行为：rglob 返回生成器可直接 for → 边界：`read_text` 仍是整读，超大文件要 `open`。
- **怎么写**（在 PY-15-12 的 vault 树上加一个 `d.txt`）：
```python
from pathlib import Path
Path("vault/2026/10/d.txt").write_text("流水", encoding="utf-8")
print("read_text:", Path("vault/2026/10/d.txt").read_text(encoding="utf-8"))
print("rglob 全行查询:", sorted(p.name for p in Path("vault").rglob("*.txt")))
print("iterdir 柜面清单:", sorted(p.name for p in Path("vault").iterdir()))
```
→ 运行输出：`read_text: 流水` ｜ `rglob 全行查询: ['a.txt', 'b.txt', 'c.txt', 'd.txt']` ｜ `iterdir 柜面清单: ['2026', 'a.txt']`
- **何时用/不用**：日常文件操作首选 pathlib；要逐行流式读/精细控制仍用 `open`。
- **锚点**：VIP 电子流水单：一张电子单上写（write_text）读（read_text）查（rglob 全行流水查询），不用再一张张翻纸档。
- **易错**：`rglob("*.txt")` 的模式不是正则（是 glob 通配，`*` 跨目录）；`write_text` 每次覆盖全文，追加还得 `open(..., "a")`。
- **关联**：`→ PY-14-03：Path 基础属性`；`→ PY-15-12：os.walk 的等价物`。

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| `w` vs `a` | 打开即清空重写 | 末尾追加 | 旧内容留不留 | 重开存折 vs 流水往下记 |
| `read()` vs `readline()` | 一次整捆 | 一次一行 | 文件多大 | 整捆点钞 vs 一张张点 |
| 文本 vs 二进制模式 | `str`+encoding | `bytes` 原样 | 认不认"字" | 手抄汉字 vs 点钞机过钞 |
| `csv.reader` vs `DictReader` | 行是格子列表 | 行是列名→值字典 | 要不要票头 | 逐格点 vs 带票头点 |
| `json.load` vs `json.loads` | 从文件对象读 | 从字符串解析 | 来源是文件还是文本 | 有 f 管文件，没 f 管字符串 |
| `os.walk` vs `Path.rglob` | 三元组逐层盘点 | 按模式全树匹配 | 要每层信息还是筛结果 | 盘点员 vs 金属探测器 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-15-01 | open() | 柜台开窗口，凭证夹=文件对象 | 开窗口 |
| PY-15-02 | with | VIP 自动关窗落锁 | 自动关窗 |
| PY-15-03 | read 三兄弟 | 点钞三式：整捆/一张张/装订沓 | 点钞三式 |
| PY-15-04 | 模式 r/w/a/x | 窗口业务牌：取款/销户/续存/开户 | 业务牌 |
| PY-15-05 | w vs a | 重开存折 vs 流水往下记 | 存折与流水 |
| PY-15-06 | 文本 vs 二进制 | 手抄汉字 vs 点钞机过钞 | 过钞 |
| PY-15-07 | 编码坑 | 凭证字迹章：盖错章对不上账 | 字迹章 |
| PY-15-08 | 换行符 newline | 小票回车+换行两步走 | 小票换行 |
| PY-15-09 | csv 读 | 批量点验票据（逐格/带票头） | 点验票据 |
| PY-15-10 | csv 写 | 开票打单 | 开票打单 |
| PY-15-11 | json 文件 | 保险柜存取件凭条 | 存取凭条 |
| PY-15-12 | os.walk | 金库逐层盘点单 | 金库盘点 |
| PY-15-13 | pathlib 实操 | VIP 电子流水单 | 电子流水单 |

## ✅ 自测清单（合上本篇，先写再看）
1. 写 3 行代码：把 `["a","b"]` 两行写入 `x.txt`（utf-8），再整读打印。
> 答案：`with open("x.txt","w",encoding="utf-8") as f: f.write("a\nb\n")` 后 `with open("x.txt",encoding="utf-8") as f: print(f.read())` → `a\nb\n`。
2. 为什么 `open("log.txt","w")` 一行没写也会让旧日志消失？想保留旧日志怎么办？
> 答案：`w` 打开即截断清空；用 `"a"` 追加。
3. 文件指针读两次的现象是什么？怎么解决？
> 答案：第二次 `read()` 拿到 `""`（指针已在末尾）；重新 `open` 或 `f.seek(0)`。
4. gbk 文件用 utf-8 读报什么错？给出既能显示又不崩的写法。
> 答案：`UnicodeDecodeError ... invalid continuation byte`；`open(p, encoding="utf-8", errors="replace")`（显示乱码但不崩）或直接 `encoding="gbk"`。
5. 一行代码列出 `vault/` 下所有 `.txt` 的文件名。
> 答案：`[p.name for p in Path("vault").rglob("*.txt")]`。
6. 写 csv 时为什么要 `newline=""`？
> 答案：防止 Windows 上文本模式把 `\n` 翻译成 `\r\n` 导致行距加倍（多出空行）。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-14 标准库](py-14-stdlib.md) ｜ ➡️ 下一篇：[py-16 正则](py-16-regex.md)
