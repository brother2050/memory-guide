# py-14 标准库 — 记忆编码

> **📍 本章导航**：前置 → [py-13 模块与包](py-13-modules-packages.md) ｜ 相关 → [py-15 文件 IO](py-15-file-io.md)·[py-16 正则](py-16-regex.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~13min（约 8.5k tokens）
>
> 本章逻辑链：py-13 学会了"把代码借来用" → 本篇盘点标准工具箱里现成的 15 件工具 → 引出 py-15"用这些工具做文件存取"。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 量具三件先量环境 | PY-14-01~03 | os/sys/pathlib：看清自己站在哪 |
| 出门先打标签 | PY-14-04~05 | json/datetime：数据对换成通用格式 |
| 零件归柜工具拼装 | PY-14-06~08 | collections/itertools/functools |
| 算得准抽得随机 | PY-14-09~10 | math/random |
| 登记派单打铭牌 | PY-14-11~13 | logging/argparse/dataclasses |
| 配钥匙过安检 | PY-14-14~15 | copy / re 概览（细节见 py-16） |

## 一、量具三件先量环境（os / sys / pathlib）

### PY-14-01 os 模块：工作台卷尺 The `os` Module
- **是什么**：操作系统（operating system）接口模块：`getcwd` 量当前工作台、`makedirs` 搭新工作台、`environ` 读车间公告栏、`os.path` 处理路径字符串。
- **为什么**：脚本不能假设"我在哪个目录、有哪些环境变量"——换台机器就崩 → os 让代码主动询问环境 → 行为：路径在 os 里是字符串 → 边界：复杂路径操作 pathlib 更顺手（PY-14-03）。
- **怎么写**：
```python
import os
print("当前工作台:", os.getcwd().rsplit("/", 1)[-1])
print("平台:", os.name)
os.makedirs("bench/inner", exist_ok=True)   # 搭新工作台
print("工作台已搭好:", os.path.isdir("bench/inner"))
print("环境变量条目数:", len(os.environ))
```
→ 运行输出：`当前工作台: myproj`（即运行所在目录名，随环境变化） ｜ `平台: posix`（Windows 上是 `nt`） ｜ `工作台已搭好: True` ｜ `环境变量条目数: 54`（随环境变化）
- **何时用/不用**：环境/目录/权限类操作用 os；纯路径拼接解析用 pathlib；文件读写见 py-15。
- **锚点**：工具箱里的老式卷尺：量工作台位置（getcwd）、搭新台面（makedirs）、看墙上公告栏（environ）。
- **易错**：`makedirs` 不加 `exist_ok=True`，目录已存在时抛 `FileExistsError`；`os.getcwd()` 是"进程当前目录"，不是脚本所在目录。
- **关联**：`→ PY-14-03：pathlib 是同域的万用表`；`→ PY-15-12：os.walk 遍历目录`。

### PY-14-02 sys 模块：工具箱盖内侧参数铭牌 The `sys` Module
- **是什么**：解释器（interpreter）级参数：`argv` 启动参数、`version` 版本、`platform` 平台、`path` 找书路线图、`exit` 退出。
- **为什么**：同一份代码要"知道自己被怎么启动、跑在什么解释器上"才能做出反应（命令行参数、版本兼容判断）→ sys 是解释器的仪表盘 → 边界：它管解释器，不管操作系统（那是 os）。
- **怎么写**：
```python
import sys
print("解释器版本:", sys.version.split()[0])
print("参数条数:", len(sys.argv), "（argv[0] 是脚本名）")
print("实现:", sys.implementation.name)
print("平台标识:", sys.platform)
```
→ 运行输出：`解释器版本: 3.12.3` ｜ `参数条数: 1 （argv[0] 是脚本名）` ｜ `实现: cpython` ｜ `平台标识: linux`
- **何时用/不用**：读启动参数做原型用 `sys.argv`，正式 CLI 用 argparse（PY-14-12）；查路径问题用 `sys.path`（→ PY-13-10）。
- **锚点**：工具箱盖内侧的参数铭牌：刻着型号（version）、出厂设置（platform）、启动旋钮位（argv）。
- **易错**：`sys.argv[0]` 是脚本名不是第一个业务参数；`sys.exit()` 抛 `SystemExit`，被裸 `except` 吞掉会导致退出失败。
- **关联**：`→ PY-13-10：sys.path 是找书路线图`；`→ PY-14-12：argparse 替代手写 argv 解析`。

### PY-14-03 pathlib.Path：路径万用表 Path Objects
- **是什么**：`pathlib.Path` 把路径变成对象：`/` 拼接、`.name/.suffix/.parent` 拆解、`exists()` 探测、`read_text/write_text` 读写。
- **为什么**：字符串路径拼接靠手写 `/`、`split`，跨平台（`\` vs `/`）易错 → Path 用运算符和属性把"拼、拆、查"统一成对象操作 → 边界：与 str 互转要显式 `str(p)`。
- **怎么写**：
```python
from pathlib import Path
p = Path("bench/inner") / "note.txt"
p.write_text("ok", encoding="utf-8")
print("存在:", p.exists(), "| 文件名:", p.name, "| 后缀:", p.suffix)
print("父目录:", p.parent.name, "| 绝对路径是 Path:", isinstance(p.resolve(), Path))
```
→ 运行输出：`存在: True | 文件名: note.txt | 后缀: .txt` ｜ `父目录: inner | 绝对路径是 Path: True`
- **何时用/不用**：新代码路径操作首选 pathlib；老代码/需要字符串给第三方库时 `str(p)` 转换。
- **锚点**：万用表一支探针量遍：通断（exists）、档位（suffix）、来路（parent）——比拉卷尺（os.path）快。
- **易错**：`Path("a", "b")` 拼出 `a/b`，但 `Path("a/b.txt").suffix` 是 `.txt`、`with_suffix` 才换后缀；`read_text` 忘记 `encoding` 会踩编码坑（→ PY-15-07）。
- **关联**：`→ PY-14-01：os 是同域卷尺`；`→ PY-15-13：文件实操展开`。

## 二、出门先打标签（json / datetime）

### PY-14-04 json：数据标签打印机 The `json` Module
- **是什么**：JSON（JavaScript Object Notation）编解码：`dumps/loads` 在对象与字符串间转，`dump/load` 对文件转（→ PY-15-11）；`indent` 缩进、`ensure_ascii` 控制中文转义。
- **为什么**：Python 的 dict 别的程序读不懂 → 转成 JSON 文本这个"通用标签"才能跨语言交换 → 行为：dict↔JSON 有类型映射（tuple→list）→ 边界：不支持的对象（如 datetime）直接抛 `TypeError`。
- **怎么写**：
```python
import json
data = {"name": "螺栓", "qty": 6}
tag = json.dumps(data, ensure_ascii=False, indent=2)   # 打标签
print(tag)
print("还原一致:", json.loads(tag) == data)
```
→ 运行输出：`{` ｜ `  "name": "螺栓",` ｜ `  "qty": 6` ｜ `}` ｜ `还原一致: True`
- **何时用/不用**：配置文件、API 数据用 json；要给人读的表格用 csv（→ PY-15-09）；二进制对象用 pickle（了解即可）。
- **锚点**：零件标签打印机：零件数据（dict）压成标准标签（JSON 文本），扫码（loads）还原回零件。
- **易错**：`ensure_ascii=True`（默认）把中文打成 `\u4e2d` 难读；JSON 键必须双引号字符串，Python 里 `True/None` 到 JSON 变 `true/null`。
- **关联**：`→ PY-15-11：json.dump/load 是它的文件版`。

### PY-14-05 datetime：打卡钟 The `datetime` Module
- **是什么**：日期时间对象：`datetime.now()/构造` 取时刻、`strftime` 按模板输出字符串、`strptime` 从字符串解析、`timedelta` 算时间差。
- **为什么**：时间是字符串就只能按字典序比大小、手工算"三天后" → 变成对象才能加减比较 → 行为：`strftime`/`strptime` 用同一套 `%Y-%m-%d` 模板 → 边界：`timedelta.days` 向下取整。
- **怎么写**：
```python
from datetime import datetime, timedelta
t = datetime(2026, 10, 6, 9, 25)
print("标准格式:", t.strftime("%Y-%m-%d %H:%M"))
print("解析回对象:", datetime.strptime("2026-10-06", "%Y-%m-%d").date())
print("三天后:", (t + timedelta(days=3)).date())
print("两时刻相差:", (t - datetime(2026,10,6)).days, "天")
```
→ 运行输出：`标准格式: 2026-10-06 09:25` ｜ `解析回对象: 2026-10-06` ｜ `三天后: 2026-10-09` ｜ `两时刻相差: 0 天`
- **何时用/不用**：时间计算/比较用 datetime；只要"今天几号"可用 `date.today()`；时区处理用 `zoneinfo`（3.9+）。
- **锚点**：车间打卡钟：now 盖时间戳、strftime 换班次牌显示、strptime 从旧小票补录、timedelta 算工时。
- **易错**：`%m` 是月、`%M` 是分——大小写一错解析出错时间；`(t1-t2).days` 只有整天数（0.9 天也是 0 天），小时差要用 `total_seconds()`。
- **关联**：`→ PY-15-08：换行符之外的另一大格式坑在文件篇`。

## 三、零件归柜工具拼装（collections / itertools / functools）

### PY-14-06 collections：多格收纳柜 The `collections` Module
- **是什么**：容器增强件：`Counter` 计数抽屉、`defaultdict` 缺件自动补默认值、`deque` 双端队列（两头快速进出）、`namedtuple` 带字段名的元组。
- **为什么**：原生 dict/list 组合拳太啰嗦（计数要 `d[k] = d.get(k,0)+1`）→ 专用容器把高频套路固化成一步 → 行为：`defaultdict(int)` 缺键自动给 0 → 边界：它仍是 dict 子类，别忘默认值会"凭空变出"键。
- **怎么写**：
```python
from collections import Counter, defaultdict, deque
print("计数前 2:", Counter("abracadabra").most_common(2))
d = defaultdict(int); d["螺栓"] += 1
print("defaultdict:", dict(d))
q = deque([1, 2, 3]); q.appendleft(0); q.append(4)
print("双端队列:", list(q))
```
→ 运行输出：`计数前 2: [('a', 5), ('b', 2)]` ｜ `defaultdict: {'螺栓': 1}` ｜ `双端队列: [0, 1, 2, 3, 4]`
- **何时用/不用**：统计词频用 Counter，累加分组用 defaultdict，队列/滑窗用 deque；简单场景普通 dict/list 就够。
- **锚点**：多格零件收纳柜：计数格自动报数（Counter）、缺件自动补货格（defaultdict）、两头开的抽屉（deque）。
- **易错**：`most_common(2)` 写成 `top(2)`；`defaultdict` 的 `d[k]` 访问会创建键，别在只读判断里用（改用 `k in d`）。
- **关联**：`→ PY-04-09：dict 基础操作`；`→ PY-14-07：和 itertools 都是"加工零件"工具`。

### PY-14-07 itertools：组合工具钳 The `itertools` Module
- **是什么**：迭代器（iterator）加工工具：`chain` 接长料、`islice` 截一段、`count` 无限计数、`accumulate` 累加——全部惰性、省内存。
- **为什么**：把多个列表接起来、取切片、做滚动累加，写循环又慢又占内存 → itertools 用惰性迭代器一步到位 → 行为：结果是生成器，需 `list()` 才物化 → 边界：`count()` 无限，必须配合截断。
- **怎么写**：
```python
import itertools as it
print("接料 chain:", list(it.chain([1, 2], [3])))
print("截料 islice:", list(it.islice(range(10), 2, 5, 2)))
c = it.count(100)
print("棘轮计数:", [next(c) for _ in range(3)])
print("累加 accumulate:", list(it.accumulate([1, 2, 3, 4])))
```
→ 运行输出：`接料 chain: [1, 2, 3]` ｜ `截料 islice: [2, 4]` ｜ `棘轮计数: [100, 101, 102]` ｜ `累加 accumulate: [1, 3, 6, 10]`
- **何时用/不用**：多序列拼接/截断/笛卡尔积用它；一次性的简单循环别硬套（可读性优先）。
- **锚点**：组合工具钳：一把钳子多个头——接料头（chain）、截断头（islice）、棘轮计数头（count）、累加头（accumulate）。
- **易错**：`chain` 传的是可变参数不是列表的列表（要 `from_iterable`）；迭代器用一次就空，第二次循环拿不到东西。
- **关联**：`→ PY-11-14：生成器的惰性原理`。

### PY-14-08 functools：工具改装店 The `functools` Module
- **是什么**：函数工具：`lru_cache` 给纯函数加缓存（结果登记）、`partial` 预置部分参数造新函数、`reduce` 把序列折叠成一个值。
- **为什么**：递归/慢函数反复算同一输入浪费时间 → 缓存把"算过的结果"登记复用 → 行为：`lru_cache` 按参数值存结果 → 边界：参数必须可哈希，函数必须纯（同输入同输出）。
- **怎么写**：
```python
from functools import lru_cache, partial, reduce
@lru_cache(maxsize=None)
def slow(n):
    print(f"  计算 {n} ...")     # 只打印一次
    return n * n
print(slow(3), slow(3))
print("partial:", partial(lambda a, b: a * b, 2)(5))
print("reduce 累乘:", reduce(lambda a, b: a * b, [1, 2, 3, 4]))
```
→ 运行输出：`  计算 3 ...` ｜ `9 9` ｜ `partial: 10` ｜ `reduce 累乘: 24`
- **何时用/不用**：慢纯函数（递归、调接口）上 `lru_cache`；反复传同一参数用 `partial`；`reduce` 大多可用生成器/`sum` 替代。
- **锚点**：工具改装店：给常用工具贴"借用登记"免重复开仓（lru_cache）、把扳手预置好开口尺寸（partial）、把几节料压成一坨（reduce）。
- **易错**：`lru_cache` 用在有副作用/可变参数函数上会返回脏结果；装饰器顺序（`@lru_cache` 与 `@property`）写反不生效。
- **关联**：`→ PY-08-06：装饰器原理`；`→ PY-19-10：缓存的内存代价`。

## 四、算得准抽得随机（math / random）

### PY-14-09 math：水平仪与直角尺 The `math` Module
- **是什么**：数学常量与函数：`ceil/floor` 上下取整、`sqrt/isqrt` 开方（后者整数）、`gcd` 最大公约数、`pi/inf` 常量。
- **为什么**：`**0.5` 浮点开方有精度毛刺、`int()` 截断方向不对 → math 提供方向明确的取整与精确整数运算 → 边界：math 只算"实数直尺"，复数用 `cmath`、大整数随意。
- **怎么写**：
```python
import math
print("上取整/下取整:", math.ceil(2.1), math.floor(2.9))
print("整数开方:", math.isqrt(17), "| gcd:", math.gcd(12, 18))
print("圆周率前 6 位:", round(math.pi, 6))
```
→ 运行输出：`上取整/下取整: 3 2` ｜ `整数开方: 4 | gcd: 6` ｜ `圆周率前 6 位: 3.141593`
- **何时用/不用**：取整/开方/公约数用 math；简单算术直接运算符；统计（均值/方差）用 `statistics`。
- **锚点**：工具箱里的水平仪与直角尺：往上弹（ceil）、往下压（floor）、对齐直角（isqrt 只认整数刻度）。
- **易错**：`int(-2.7)` 是 `-2`（截断）而 `math.floor(-2.7)` 是 `-3`（向下）——负数方向不一样；`isqrt(17)` 是 4（截尾）不是五入。
- **关联**：`→ PY-02-06：float 精度问题`；`→ PY-14-10：random 管随机，math 管精确`。

### PY-14-10 random：抓阄竹罐 The `random` Module
- **是什么**：伪随机（pseudo-random）工具：`randint` 抽区间整数、`choice` 抓一个、`sample` 抓多个不重复、`shuffle` 洗牌、`seed` 固定随机序列。
- **为什么**：抽样、洗牌、造测试数据都要"不可预测但可复现"的乱数 → 伪随机数发生器按 seed 重放 → 行为：同 seed 同序列 → 边界：不是密码学随机（安全场景用 `secrets`）。
- **怎么写**：
```python
import random
random.seed(42)                 # 固定竹罐摆放
print("抽一个号:", random.randint(1, 10))
print("抓一把:", random.choice(["锤子", "扳手", "卷尺"]))
items = [1, 2, 3, 4]; random.shuffle(items)
print("洗牌:", items)
print("抽签不重复:", random.sample(range(100), 3))
```
→ 运行输出：`抽一个号: 2` ｜ `抓一把: 锤子` ｜ `洗牌: [2, 4, 1, 3]` ｜ `抽签不重复: [17, 94, 13]`
- **何时用/不用**：测试数据/游戏/抽样用 random；密码、令牌用 `secrets`；科学计算用 `numpy.random`。
- **锚点**：工具箱角落的抓阄竹罐：伸手抽一个（randint）、抓一把（sample）、摇一摇重排（shuffle）、竹罐摆位固定结果可复现（seed）。
- **易错**：`random.choice([])` 抛 `IndexError`；`shuffle` 是原地修改不返回新列表（`x = shuffle(y)` 得 None）；测试不设 seed 每次结果不同，难复现 bug。
- **关联**：`→ PY-14-09：math 管精确计算`。

## 五、登记派单打铭牌（logging / argparse / dataclasses）

### PY-14-11 logging：检修登记本 The `logging` Module
- **是什么**：分级日志系统：五个级别 `DEBUG<INFO<WARNING<ERROR<CRITICAL`，`basicConfig` 设格式与门槛，`getLogger` 拿登记本，`exception` 附带 traceback。
- **为什么**：`print` 调试留在上线代码里刷屏且无法按级别开关 → logging 设门槛后低级别自动过滤、可输出到文件 → 行为：默认门槛 WARNING → 边界：`basicConfig` 只对首次调用生效。
- **怎么写**：
```python
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger("toolbox")
log.debug("调试墨水：默认不写进本子")
log.info("登记：今日保养完成")
log.warning("警告：扳手磨损")
log.error("故障：电钻不转")
```
→ 运行输出：`INFO | 登记：今日保养完成` ｜ `WARNING | 警告：扳手磨损` ｜ `ERROR | 故障：电钻不转`（`log.exception("抢修记录")` 在异常里额外附 traceback，含 `ZeroDivisionError: division by zero`）
- **何时用/不用**：项目一律 logging；一次性小脚本 print 无妨；需要配置文件/多输出见 → PY-20-16。
- **锚点**：检修登记本：五种颜色的笔=五个级别，墨水（debug）平时不上本子，故障（error）红笔记一笔还能贴事故单（traceback）。
- **易错**：在 `basicConfig` 之后再调不生效（想改要 `force=True`）；`f-string` 写日志（`log.info(f"...")`）浪费格式化开销，用 `log.info("%s", x)`。
- **关联**：`→ PY-12-14：异常与 exception 的配合`；`→ PY-20-16：logging 工程配置`。

### PY-14-12 argparse：门口工单登记板 The `argparse` Module
- **是什么**：命令行参数解析器：`add_argument` 登记参数（位置参数=必填栏、`-n/--num` 选项栏、`type` 栏位格式），`parse_args` 一次拿好，还自带 `--help`。
- **为什么**：手写 `sys.argv` 解析要自己判类型、拼帮助、报错难看 → argparse 把"登记板"标准化 → 行为：类型不符自动报错退出 → 边界：复杂子命令用 `add_subparsers`。
- **怎么写**（用固定参数列表模拟命令行）：
```python
import argparse
parser = argparse.ArgumentParser(description="五金店派工单")
parser.add_argument("job", help="干什么活（必填栏）")
parser.add_argument("-n", "--num", type=int, default=1, help="数量（可选栏）")
args = parser.parse_args(["修水管", "-n", "3"])
print("工单:", args.job, "数量:", args.num, "类型:", type(args.num).__name__)
```
→ 运行输出：`工单: 修水管 数量: 3 类型: int`
- **何时用/不用**：任何要传参的脚本都用它；交互式输入用 `input()`；更漂亮的 CLI 用第三方（typer/click）。
- **锚点**：门口的工单登记板：必填栏（位置参数）、可选勾（选项）、按栏位格式填（type），填错格式登记员当场退回（自动报错）。
- **易错**：`type=int` 只负责转换，`default=1` 不经过 type；`parse_args()` 里传列表是测试技巧，真实运行读 `sys.argv`。
- **关联**：`→ PY-14-02：sys.argv 是它的原材料`。

### PY-14-13 dataclasses：标准件规格铭牌 The `dataclasses` Module
- **是什么**：`@dataclass` 装饰器自动为类生成 `__init__/__repr__/__eq__`；`field(default_factory=...)` 给可变字段配"自动供货"。
- **为什么**：纯数据类手写 init/repr/eq 十几行样板，写错参数顺序就出 bug → dataclass 把样板自动化 → 行为：字段声明即构造参数 → 边界：可变默认值必须用 `default_factory`。
- **怎么写**：
```python
from dataclasses import dataclass, field, fields
@dataclass
class Bolt:
    size: int
    material: str = "钢"
    tags: list = field(default_factory=list)
b = Bolt(8)
print(b)
print("字段清单:", [f.name for f in fields(b)])
print("可变默认安全:", b.tags, Bolt(9, tags=["镀锌"]).tags)
```
→ 运行输出：`Bolt(size=8, material='钢', tags=[])` ｜ `字段清单: ['size', 'material', 'tags']` ｜ `可变默认安全: [] ['镀锌']`
- **何时用/不用**：配置、记录、DTO 用 dataclass；需要继承层级/行为的用普通 class（→ py-09）；不可变数据加 `@dataclass(frozen=True)`。
- **锚点**：标准件规格铭牌：机器冲压出统一规格（自动 init/repr/eq），附加标注（field）另打一行小字。
- **易错**：`tags: list = []` 直接默认可变对象 → 多实例共享一个列表（经典坑）；有默认值的字段必须排在无默认值字段后面。
- **关联**：`→ PY-09-03：类的基本语法`；`→ PY-17-12：dataclass 与类型注解配合`。

## 六、配钥匙过安检（copy / re 概览）

### PY-14-14 copy：配钥匙摊 The `copy` Module
- **是什么**：`copy.copy` 浅拷贝（外层新、内层共用）、`copy.deepcopy` 深拷贝（整棵结构全新）。
- **为什么**：赋值只是多贴一张标签指向同一对象，改一处全体遭殃 → 拷贝造副本 → 行为：浅拷贝的内层仍是同一对象 → 边界：深拷贝更慢，且要求对象可递归拷贝。
- **怎么写**：
```python
import copy
key = {"齿": [1, 2], "柄": "铜"}
shallow = copy.copy(key)        # 配钥匙坯：柄是新的，齿纹共用
deep = copy.deepcopy(key)       # 连齿纹整套复刻
key["齿"].append(3)
print("原钥匙齿纹 :", key["齿"])
print("浅拷贝齿纹 :", shallow["齿"], "（共用内层）")
print("深拷贝齿纹 :", deep["齿"], "（完全独立）")
```
→ 运行输出：`原钥匙齿纹 : [1, 2, 3]` ｜ `浅拷贝齿纹 : [1, 2, 3] （共用内层）` ｜ `深拷贝齿纹 : [1, 2] （完全独立）`
- **何时用/不用**：只增删顶层键用浅拷贝；嵌套结构要互不干扰用深拷贝；纯不可变元素（数字/字符串）浅拷贝即安全。
- **锚点**：五金店门口配钥匙摊：配钥匙坯（copy，柄新齿纹共用）还是整套锁芯复刻（deepcopy，齿纹全新）。
- **易错**：`b = a.copy()` 对 dict/list 是浅拷贝但对 tuple 是"原样返回"（不可变无需拷贝）；含自引用的对象 deepcopy 能处理，`copy.copy` 也只复制外层。
- **关联**：`→ PY-04-14：深浅拷贝原理对比`；`→ PY-19-05：拷贝的内存代价`。

### PY-14-15 re 概览：按样板挑零件 The `re` Module (Overview)
- **是什么**：正则表达式（regular expression）模块：用模式串从文本里"找、抽、换"。常用五个操作：`match/search/findall/sub/compile`。
- **为什么**：按固定格式抽信息（日期、号码）写字符串切片脆如蛋壳 → 正则用模式描述"长什么样"一次匹配一整类 → 行为：`\d+` 匹配数字串 → 边界：复杂规则可读性差，超过 3 行的正则建议注释或换专用解析器。
- **怎么写**：
```python
import re
print(re.findall(r"\d+", "订单2026-10-06共3件"))
print("校验:", bool(re.match(r"^\d+$", "12345")))
print("替换:", re.sub(r"\d+", "#", "a1b22c"))
```
→ 运行输出：`['2026', '10', '06', '3']` ｜ `校验: True` ｜ `替换: a#b#c`
- **何时用/不用**：格式明确的检索/校验/替换用 re；HTML/JSON 等嵌套格式用专用解析器；正则细节一概不在本篇展开。
- **锚点**：按样板挑零件：一张样板（模式）压在整箱零件上逐一比对，合规格的全挑出来（findall）；换件（sub）也是照样板挑出再替换。
- **易错**：模式不加锚点会"半匹配"（`re.match(r"\d+", "12a")` 也成功，只匹配到 `12`）；反斜杠忘写 `r""` 变转义灾难。
- **关联**：`→ 见 PY-16-01：正则元字符与匹配规则全套`；`→ 见 PY-16-10：match/search/findall/sub/compile 逐个实测`。

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| os.path vs pathlib | 路径是字符串 | 路径是 Path 对象 | 拼接用 `+` 还是 `/` | 卷尺量字符串，万用表量对象 |
| `strftime` vs `strptime` | 对象→字符串（输出） | 字符串→对象（解析） | 谁是源头 | f=format 打出去，p=parse 读进来 |
| `copy` vs `deepcopy` | 外层新内层共用 | 整棵全新 | 改内层谁跟着变 | 钥匙坯 vs 整套锁芯 |
| Counter vs 普通 dict | 自动计数有 most_common | 手动 get/累加 | 要不要排名 | 报数抽屉自己数 |
| logging vs print | 分级可开关可落盘 | 全部照打 | 上线要不要留痕 | 登记本 vs 喇叭 |
| `lru_cache` vs 每次重算 | 首次算完登记 | 每次都算 | 输入重复率高不高 | 借还登记免开仓 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-14-01 | os | 工作台卷尺：量台/搭台/看公告栏 | 老卷尺 |
| PY-14-02 | sys | 工具箱盖内侧参数铭牌 | 参数铭牌 |
| PY-14-03 | pathlib | 一支探针的万用表 | 万用表 |
| PY-14-04 | json | 零件标签打印机 | 标签打印机 |
| PY-14-05 | datetime | 车间打卡钟 | 打卡钟 |
| PY-14-06 | collections | 多格零件收纳柜 | 收纳柜 |
| PY-14-07 | itertools | 多头组合工具钳 | 组合钳 |
| PY-14-08 | functools | 工具改装店 | 改装店 |
| PY-14-09 | math | 水平仪与直角尺 | 水平仪 |
| PY-14-10 | random | 抓阄竹罐 | 抓阄罐 |
| PY-14-11 | logging | 检修登记本（五色笔） | 登记本 |
| PY-14-12 | argparse | 门口工单登记板 | 工单板 |
| PY-14-13 | dataclasses | 标准件规格铭牌 | 规格铭牌 |
| PY-14-14 | copy | 配钥匙摊：钥匙坯/整套锁芯 | 配钥匙 |
| PY-14-15 | re 概览 | 样板挑零件：样板=模式，合规格全挑出 | 样板挑件 |

## ✅ 自测清单（合上本篇，先写再看）
1. 一行代码建目录 `data/2026`（已存在也不报错），并打印它是否存在。
> 答案：`os.makedirs("data/2026", exist_ok=True); print(os.path.isdir("data/2026"))` → `True`。
2. `datetime(2026,10,6,9,25)` 减 `datetime(2026,10,6)` 的 `.days` 是多少？为什么？
> 答案：`0`——差 9 小时 25 分，`.days` 只取整天（向下取整）。
3. `Counter("aab")` 的 `most_common(1)` 输出什么？`defaultdict(int)` 缺键取值后字典多了什么？
> 答案：`[('a', 2)]`；多了值为 0 的新键（访问即创建）。
4. `list(it.count(10))` 能跑吗？怎么安全拿前 3 个？
> 答案：不能（无限迭代内存爆掉）；`[next(c) for _ in range(3)]` 或 `list(it.islice(it.count(10), 3))`。
5. 给定 `d = {"齿": [1,2]}`，写出"改副本内层不影响原字典"的两行代码。
> 答案：`import copy; d2 = copy.deepcopy(d); d2["齿"].append(3)`，`d["齿"]` 仍是 `[1,2]`。
6. 为什么 `re.match(r"\d+", "12a")` 返回成功但不代表整串是数字？怎么改？
> 答案：match 只从头匹配前缀；加尾锚 `re.match(r"^\d+$", "12a")` 或用 `fullmatch`。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-13 模块与包](py-13-modules-packages.md) ｜ ➡️ 下一篇：[py-15 文件 IO](py-15-file-io.md)
