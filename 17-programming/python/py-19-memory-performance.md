# py-19 内存与性能 — 记忆编码

> **📍 本章导航**：前置 → [py-04 容器](py-04-containers.md) ｜ 相关 → [py-11 生成器](py-11-iterators-generators.md)·[py-18 并发](py-18-concurrency.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~12min（约 8k tokens）
>
> 本章逻辑链：py-18 让程序跑得"同时"了 → 本篇解决"东西越堆越多、跑得越来越慢怎么收拾" → 通往 py-20"把收拾流程工程化"。意象域：**房间收纳/断舍离**（行李牌/收纳箱/断舍离三步），锚点不越域。
> 所有计时/内存数字均实测（Python 3.12.3），机器不同数值略有浮动，量级关系稳定。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 谁在管你的行李 | PY-19-01,02 | 行李牌计数 + 保洁队扫环 |
| 收纳改造三件套 | PY-19-03~05 | 装箱法、定格柜、逐件拿 |
| 先测量后动手 | PY-19-06~09 | 拼法、掐表、上秤、拍照 |
| 断舍离清单 | PY-19-10~12 | 门口鞋架、索书号、三步法 |
| 零拷贝与弱引用 | PY-19-13~14 | 免搬箱看货、借钥匙不占房 |

## 一、谁在管你的行李（引用与回收）
### PY-19-01 引用计数 Reference Counting
- **是什么**：CPython 给每个对象记"被几个名字指着"（引用数），计数归零立刻回收。
- **为什么**：痛点：内存是有限房间，东西用完不清走就越堆越满 → 机制：变量赋值是挂"行李牌"（引用），`del` 是摘牌，最后一张牌摘掉对象即销毁 → 行为：`sys.getrefcount(a) - 1` 可查看牌数 → 边界：参数传递/函数调用会临时挂牌，所以要减 1；循环引用归不了零（见 PY-19-02）。
- **怎么写**：
```python
import sys
a = [1, 2, 3]
print("只有 a 一张牌:", sys.getrefcount(a) - 1)
b = a                       # b 只是又挂了一张牌，没有复制列表
print("b 也指向它:", sys.getrefcount(a) - 1)
del b
print("删掉 b 后:", sys.getrefcount(a) - 1)
```
→ 运行输出：`只有 a 一张牌: 1` ／ `b 也指向它: 2` ／ `删掉 b 后: 1`
- **何时用/不用**：排查"对象为何不释放"时先数牌；日常写代码靠直觉赋值即可，不必手管计数。
- **锚点**：**行李牌**——行李上挂的牌就是引用：牌全摘完（计数归零），保洁立刻把行李清走（回收）。
- **易错**：`b = a` 后以为 b 是副本（其实同一件行李多张牌）；`getrefcount` 的返回值要减 1（调用本身挂了临时牌）。
- **关联**：`→ PY-19-02：牌数归零清不掉的情况`　`→ PY-02-08：id/is 判断"是不是同一件行李"`

### PY-19-02 循环引用与 gc 垃圾回收
- **是什么**：`gc` 模块是"保洁队"：定期扫描内存，收走引用计数清不掉的循环引用（garbage collection，分代回收）。
- **为什么**：痛点：两个对象互指对方，牌永远摘不完，引用计数失灵 → 机制：gc 分三代定期标记-清扫，找出"没人要的环"整体回收 → 行为：删掉名字后对象仍在，`gc.collect()` 后被回收 → 边界：带 `__del__` 的循环对象在旧版本曾回收不掉（3.4+ 可以）；gc 有扫描开销。
- **怎么写**：
```python
import gc
class Box:
    def __init__(self, name):
        self.name, self.ref = name, None
    def __del__(self):
        print(f"  [{self.name}] 被回收")
a, b = Box("甲箱"), Box("乙箱")
a.ref, b.ref = b, a            # 互相引用，形成环
del a, b
print("还没听到'被回收' → 环形垃圾卡住了")
n = gc.collect()
print("gc.collect() 回收对象数:", n)
```
→ 运行输出：`还没听到'被回收' → 环形垃圾卡住了` ／ `  [甲箱] 被回收` ／ `  [乙箱] 被回收` ／ `gc.collect() 回收对象数: 2`
- **何时用/不用**：一般不用手动 gc；怀疑内存泄漏时 `gc.collect()` + `gc.get_objects()` 排查。
- **锚点**：**互相绑着的行李牌**——甲箱的牌拴在乙箱上、乙箱的拴在甲箱上，谁的牌都摘不干净，只能请保洁主管（gc）拿剪刀来剪。
- **易错**：把 `gc.collect()` 当"提速按钮"乱调（有开销）；长生命周期对象间互指是内存泄漏的常见源头。
- **关联**：`→ PY-19-01：引用计数的盲区`　`→ PY-09-10：父子对象互持引用要小心成环`

## 二、收纳改造三件套（少占地方）
### PY-19-03 深拷贝 vs 浅拷贝（复习）
- **是什么**：`copy.copy` 浅拷贝只复制最外层容器；`copy.deepcopy` 深拷贝连嵌套内容全部复制（→ 详见 PY-04-12）。
- **为什么**：痛点：搬家想"复制一份"，浅拷贝后改内层原件跟着变 → 机制：浅拷贝共享内层对象（同一批行李），深拷贝递归造新对象 → 行为：改 `shallow[0][0]` 影响 original，改 `deep` 不影响 → 边界：深拷贝慢且费内存，循环引用靠 memo 表处理。
- **怎么写**：
```python
import copy
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)
shallow[0][0] = 99
print("改浅拷贝的内层 → original:", original)
deep[1][0] = 77
print("改深拷贝的内层 → original:", original)
print("外层身份不同:", original is not shallow, "| 内层共享:", original[0] is shallow[0])
```
→ 运行输出：`改浅拷贝的内层 → original: [[99, 2], [3, 4]]` ／ `改深拷贝的内层 → original: [[99, 2], [3, 4]]` ／ `外层身份不同: True | 内层共享: True`
- **何时用/不用**：只读/整体替换用浅拷贝；要独立修改内层才付深拷贝的成本。
- **锚点**：**搬家装箱**——浅拷贝是贴了新箱签但箱里的东西还是同一批；深拷贝是每件东西都重新装一份进新箱。
- **易错**：对"列表的列表"做 `list(orig)` 或 `orig[:]` 以为是深拷贝，其实内层照旧共享（PY-04 消混表同款坑）。
- **关联**：`→ PY-04-12：深浅拷贝的完整对比`　`→ PY-17-07：可变默认值共享同一坑`

### PY-19-04 __slots__ 槽位瘦身
- **是什么**：`__slots__ = ("x",)` 声明实例只允许这些字段，砍掉每实例的 `__dict__`，省内存、禁乱挂属性。
- **为什么**：痛点：百万个小对象每个都带属性字典，内存翻倍 → 机制：slots 用固定偏移量存字段，不建字典 → 行为：实例+属性表 344 字节缩到 40 字节，乱挂属性抛 AttributeError → 边界：slots 类不能动态加字段；多继承受限；别为省几字节牺牲灵活性。
- **怎么写**：
```python
import sys
class Heavy:                       # 默认：每实例带一个属性字典 __dict__
    def __init__(self, x): self.x = x
class Light:
    __slots__ = ("x",)
    def __init__(self, x): self.x = x
h, l = Heavy(1), Light(1)
print("Heavy 有 __dict__:", hasattr(h, "__dict__"), "| Light:", hasattr(l, "__dict__"))
print("实例+属性表字节: Heavy", sys.getsizeof(h) + sys.getsizeof(h.__dict__), "| Light", sys.getsizeof(l))
try:
    l.y = 2
except AttributeError as e:
    print("乱挂属性被拒:", e)
```
→ 运行输出：`Heavy 有 __dict__: True | Light: False` ／ `实例+属性表字节: Heavy 344 | Light 40` ／ `乱挂属性被拒: 'Light' object has no attribute 'y'`
- **何时用/不用**：海量小对象（点/节点/记录）用 slots；普通业务类不必上。
- **锚点**：**定格收纳柜**——柜子只有预定的几格（slots），衣服只能进格子，想塞柜缝（乱挂属性）直接被拒。
- **易错**：slots 类的子类若不声明 slots，又会长回 `__dict__`，瘦身效果丢失。
- **关联**：`→ PY-09-08：slots 与属性机制`　`→ PY-19-05：更省的是干脆不造大对象`

### PY-19-05 生成器惰性求值省内存
- **是什么**：生成器表达式/函数按需产出元素（→ PY-11-05），不一次性把所有值装进内存。
- **为什么**：痛点：百万级数据做列表推导，内存瞬间 800KB+ → 机制：生成器只存"配方"和当前位置，取一个算一个 → 行为：10 万元素列表占 800984 字节，生成器只占 200 字节 → 边界：生成器是一次性的、不能下标索引；要复用先转列表。
- **怎么写**：
```python
import sys
big_list = [x * x for x in range(100_000)]
big_gen = (x * x for x in range(100_000))
print("列表占内存(字节):", sys.getsizeof(big_list))
print("生成器占内存(字节):", sys.getsizeof(big_gen))
print("生成器按需出数:", next(big_gen), next(big_gen))
```
→ 运行输出：`列表占内存(字节): 800984` ／ `生成器占内存(字节): 200` ／ `生成器按需出数: 0 1`
- **何时用/不用**：大数据流、文件逐行读（`for line in f`）用生成器；数据要反复随机访问就用列表。
- **锚点**：**断舍离传送口**——不把整箱东西全倒进房间，而是一个口子一次递一件，房间永远不堆满。
- **易错**：生成器用过一次就空了（`list(gen)` 后再 `list(gen)` 得到 `[]`）；忘记惰性导致"改了代码没生效"的假象。
- **关联**：`→ PY-11-05：yield 的实现机制`　`→ PY-15-02：大文件逐行读同理`

## 三、先测量后动手（计时与盘点）
### PY-19-06 字符串拼接 join vs +
- **是什么**：拼接大量字符串用 `"".join(parts)`，而不是循环 `s += part`。
- **为什么**：痛点：循环拼接每次生成新字符串对象，旧的变垃圾 → 机制：`join` 先算总长一次分配，再批量拷贝（摊还 O(n)）→ 行为：2 万段拼接 join 比循环快两个量级（0.0001s vs 0.0272s）→ 边界：两三段拼接直接 `+` 或 f-string 更清晰。
- **怎么写**：
```python
import time
parts = ["word"] * 20_000
t0 = time.perf_counter()
s = ""
for p in parts:
    s += p
t_plus = time.perf_counter() - t0
t0 = time.perf_counter()
s2 = "".join(parts)
t_join = time.perf_counter() - t0
print(f"循环 += 耗时: {t_plus:.4f}s / join 耗时: {t_join:.4f}s / 一致: {s == s2}")
```
→ 运行输出：`循环 += 耗时: 0.0272s / join 耗时: 0.0001s / 一致: True`（耗时随机器浮动）
- **何时用/不用**：循环内拼接一律 join；固定两三段文本用 f-string 最顺手。
- **锚点**：**一次装箱 vs 来一件搬一次**——join 是量好总长一次装满一箱；`+=` 是每来一件就把整箱倒出来重装一遍。
- **易错**：以为 `+=` 在循环里"就地追加"——字符串不可变，每次都是新对象（PY-03-09）。
- **关联**：`→ PY-03-09：字符串不可变`　`→ PY-19-07：用 timeit 亲自验证`

### PY-19-07 timeit 精确计时
- **是什么**：`timeit.timeit(stmt, setup, number=N)` 专为测小段代码设计：自动多次重复、关垃圾回收、禁用 gc 干扰。
- **为什么**：痛点：`time.time()` 测微秒级代码，噪声比信号大 → 机制：timeit 循环执行 N 次取总时长，首尾预热减少解释器噪声 → 行为：join vs 循环的差距稳定复现 → 边界：测含 IO/全局状态的代码要小心 setup 隔离；超慢代码减小 number。
- **怎么写**：
```python
import timeit
setup = "words = ['记忆'] * 500"
t_join = timeit.timeit("''.join(words)", setup=setup, number=2000)
t_loop = timeit.timeit("s = ''\nfor w in words:\n    s += w", setup=setup, number=2000)
print(f"join 2000 次: {t_join:.4f}s / 循环+= 2000 次: {t_loop:.4f}s")
```
→ 运行输出：`join 2000 次: 0.0086s / 循环+= 2000 次: 0.0295s`（快者：join；耗时随机器浮动）
- **何时用/不用**：两段写法纠结谁快就 timeit；整程序性能用 cProfile（PY-19-08）。
- **锚点**：**厨房计时器**——争论"哪锅水开得快"不用感觉，掐表计时，两次都是同一块表。
- **易错**：测的时候把 setup 里的数据构建也算进 stmt，测的就不是目标代码；number 太小结果全是噪声。
- **关联**：`→ PY-19-06：join 结论的实测来源`　`→ PY-19-08：先找热点再计时微调`

### PY-19-08 cProfile + pstats 找热点
- **是什么**：`cProfile` 给程序全程记账：每个函数调用多少次、花了多少秒；`pstats` 排序出"最胖的函数"。
- **为什么**：痛点：凭直觉优化，改了半天最热的函数没动 → 机制：profiler 在每次函数调用前后记时间戳 → 行为：fib(26) 递归被调 39 万次、耗时占绝对大头，一眼锁定热点 → 边界：profiler 本身有开销（数字偏大），只看相对排序；线程多时统计口径不同。
- **怎么写**（节选，main() 里调用 fib(26)/sum_squares(50_000)，完整实测代码见 test_36.py）：
```python
import cProfile, pstats, io
def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)
def sum_squares(n): return sum(i * i for i in range(n))
def main():
    fib(26)                        # 递归热点
    sum_squares(50_000)
pr = cProfile.Profile()
pr.enable(); main(); pr.disable()
buf = io.StringIO()
pstats.Stats(pr, stream=buf).sort_stats("cumulative").print_stats(3)
print(buf.getvalue())
```
→ 运行输出（路径截短，耗时随机器浮动）：
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.084    0.084 .../demo_profile.py:4(main)
 392835/1    0.074    0.000    0.074    0.074 .../demo_profile.py:2(fib)
        1    0.000    0.000    0.010    0.010 .../demo_profile.py:3(sum_squares)
```
- **何时用/不用**：程序变慢先 cProfile 定位热点，再决定优化谁；几行小代码用 timeit 就够。
- **锚点**：收纳前先**上秤盘点**——把每件行李（函数）放上体重秤，最重的那件才值得动手"断舍离"。
- **易错**：没排序直接看默认输出，热点沉在表底；`sort_stats("cumulative")` 才看累计耗时排行。
- **关联**：`→ PY-19-12：热点定位后走优化三步法`　`→ PY-18-13：并发选型也要先测量`

### PY-19-09 tracemalloc 内存快照
- **是什么**：`tracemalloc` 给内存分配拍照：对比两个快照（snapshot），定位"哪行代码涨了内存"。
- **为什么**：痛点：内存慢慢涨，不知道谁在囤货 → 机制：tracing 记录每次分配的调用行，快照按行聚合统计 → 行为：5 万条记录的列表在分配那行涨了 4123 KiB，删掉后回落到 3 KB → 边界：追踪本身占资源，排查完 `stop()`；只统计 Python 层分配。
- **怎么写**：
```python
import tracemalloc
tracemalloc.start()
before = tracemalloc.take_snapshot()
big = [f"第{i}条记录" for i in range(50_000)]
cur, peak = tracemalloc.get_traced_memory()
print(f"分配后: 当前 {cur/1024:.0f} KB, 峰值 {peak/1024:.0f} KB")
top = tracemalloc.take_snapshot().compare_to(before, "lineno")[:1]
for stat in top: print("增长最多的行:", stat)
```
→ 运行输出（路径截短）：`分配后: 当前 4124 KB, 峰值 4124 KB` ／ `增长最多的行: .../demo_mem.py:4: size=4123 KiB (+4123 KiB), count=50001 (+50001), average=84 B`（文件名/行号随保存情况变化）
- **何时用/不用**：内存泄漏/膨胀用 tracemalloc 定位行号；只想看总量用 `sys.getsizeof`/`gettracemalloc` 之外的粗测即可。
- **锚点**：**收纳前后拍照对比**——搬进来拍一张、收拾完拍一张，两张照片一叠，哪面墙堆多了自动现形。
- **易错**：快照对比忘记取 `before` 基线，看到的是全量不是增量；长驻服务要在稳定期取样。
- **关联**：`→ PY-19-01：谁在占内存的行级视角`　`→ PY-19-05：大列表常是头号囤货者`

## 四、断舍离清单（优化套路）
### PY-19-10 lru_cache 缓存换时间
- **是什么**：`functools.lru_cache` 记住函数的（参数→结果），重复调用直接取缓存（最近最少使用淘汰）。
- **为什么**：痛点：递归/重复计算把同样的答案算了一遍又一遍 → 机制：装饰器包一层字典存结果，命中即返回 → 行为：fib(28) 从 0.03s 量级降到微秒级，`cache_info()` 可查命中率 → 边界：只适合纯函数（同参必同果）；参数要可哈希；缓存占内存。
- **怎么写**：
```python
from functools import lru_cache
@lru_cache(maxsize=None)
def fib_fast(n):
    return n if n < 2 else fib_fast(n-1) + fib_fast(n-2)
print(fib_fast(28), fib_fast.cache_info())
```
→ 运行输出（对比无缓存 0.0317s）：`317811 CacheInfo(hits=26, misses=29, maxsize=None, currsize=29)`，有缓存单次微秒级（耗时随机器浮动）
- **何时用/不用**：重复子问题（递归/查表）用缓存；副作用函数（写文件、改全局）绝不能缓存。
- **锚点**：**门口鞋架**——常穿的鞋（高频参数）摆在门口，出门直接拿，不用每次翻柜子重找。
- **易错**：给带随机数/时间的函数加缓存，结果永远是第一次的值；`maxsize=None` 无限缓存可能吃光内存。
- **关联**：`→ PY-08-02：lru_cache 是装饰器的典型应用`　`→ PY-19-12：算法没救时才用缓存`

### PY-19-11 查找结构：list vs set/dict
- **是什么**：`x in list` 是 O(n) 逐件扫描；`x in set/dict` 是 O(1) 哈希直取。
- **为什么**：痛点：大列表里频繁"在不在"，时间被扫描吃光 → 机制：set/dict 用哈希表定位桶，跳过逐件比较 → 行为：2 万元素 5000 次判断，list 0.6089s vs set 0.0001s（数千倍）→ 边界：set 建表本身要花 O(n)；只需一两次判断不必转 set。
- **怎么写**：
```python
import timeit
setup = "data = list(range(20_000)); s = set(data); d = {k: k for k in data}"
t_list = timeit.timeit("19_999 in data", setup=setup, number=5_000)
t_set = timeit.timeit("19_999 in s", setup=setup, number=5_000)
print(f"list 成员判断: {t_list:.4f}s / set 成员判断: {t_set:.4f}s")
```
→ 运行输出：`list 成员判断: 0.6089s / set 成员判断: 0.0001s`（dict 同为 0.0001s；耗时随机器浮动）
- **何时用/不用**：循环里反复查"在不在"就预转 set/dict；一次两次的查找保持 list 更简单。
- **锚点**：**贴标签收纳箱 vs 散堆逐件翻**——list 是一地散件从头翻到尾找一件；set/dict 是箱子贴好标签，报标签直达那一箱。
- **易错**：`if x in data` 写在双层循环里，不知不觉 O(n²)（PY-19-12 的旧方案实测）。
- **关联**：`→ PY-04-05：set/dict 的哈希机制`　`→ PY-19-12：数据结构换了就能提速`

### PY-19-12 优化三步法：先测量 → 换结构 → 再测量
- **是什么**：性能优化的固定流程：①测量定位（timeit/cProfile）→ ②对症下药（先换数据结构/算法，后抠微优化）→ ③复测确认收益。
- **为什么**：痛点：不测量就优化＝凭感觉断舍离，扔错东西还越整越慢 → 机制：瓶颈往往集中在一两处（二八定律），换算法是数量级收益，微优化只是零头 → 行为：词频统计从 list 线性查换成 dict.get，50 次运行 0.1363s→0.0103s 提速约 13 倍 → 边界：没测量前禁止"顺手优化"；每次只改一处好归因。
- **怎么写**（节选对比，片段不可直接运行：两段各包进 `timeit.timeit(..., number=50)` 计时才是完整可跑版）：
```python
# 旧方案：词频统计用 list 线性找键（内层扫描）
for ch in text:
    for i, (k, v) in enumerate(count):
        if k == ch: ...
# 新方案：dict.get（查键 O(1)）
for ch in text:
    count[ch] = count.get(ch, 0) + 1
```
→ 运行输出：`旧方案(list 线性查) 50 次: 0.1363s` ／ `新方案(dict 查键)  50 次: 0.0103s` ／ `提速约 13 倍`（耗时随机器浮动）
- **何时用/不用**：程序"感觉慢"时走三步法；没测量报告的优化请求先补测量。
- **锚点**：**断舍离三步**——先盘点（上秤/拍照）→ 再改造（换收纳结构）→ 复称（确认真的轻了），不复称等于没收拾。
- **易错**：一次改好几处，变快了不知道是哪招生效；只优化冷代码（占总时长 1% 的部分再快也没用）。
- **关联**：`→ PY-19-07：第①步的秒表`　`→ PY-19-08：第①步的体检秤`　`→ PY-19-11：第②步的常见招`

## 五、零拷贝与弱引用（口号：免搬箱、借钥匙）

### PY-19-13 bytearray 与 memoryview（可变缓冲·零拷贝视图）
- **是什么**：`bytearray` 是可变字节序列（bytes 的可改版）；`memoryview` 是它的零拷贝视图——切片/读写不复制底层数组，直接在原数据上操作。
- **为什么**：痛点是"大二进制数据改一小段却要整块复制"费时费内存 → 机制是 memoryview 只存"起始+长度+格式"的窗口，读写直达缓冲区；bytearray 提供可变底座 → 行为是百万级数据局部修改不产生副本 → 边界是 memoryview 挂着时底层数据不能被收缩/释放；它不能替代文本处理（那是 py-03 的地盘）。
- **怎么写**：
  ```python
  data = bytearray(b"ABCDEFGH")
  mv = memoryview(data)
  print(mv[0:4].tobytes(), mv[0:4].readonly)
  mv[0:4] = b"1234"                      # 通过视图原地改
  print(data)
  ```
  → 运行输出：`b'ABCD' False`\n`bytearray(b'1234EFGH')`
- **何时用/不用**：大二进制缓冲的局部读写/解析（图像、网络包、文件头）必备；小 bytes 操作直接切片，别为省几字节上视图。
- **锚点**：断舍离里的**免搬箱看货**——memoryview 是"不搬箱子就能从窗口看货、换货"；bytearray 是那只可开箱换货的箱子（bytes 是封死的塑封箱）。
- **易错**：`mv[0:4] = b"12"` 长度不匹配直接 `ValueError`（视图赋值不能改长度）；`memoryview(bytes(...))` 是只读视图，赋值抛 `TypeError`。
- **关联**：→ PY-03-15：文本编码在 bytes 层的底层就是这套缓冲 ｜ → PY-19-12：性能优化时先想到"能不能免复制"。

### PY-19-14 weakref 弱引用（借钥匙不占房）
- **是什么**：`weakref.ref(obj)` 创建弱引用：能拿到对象但**不增加引用计数**，对象被回收后弱引用自动变 `None`（或触发回调）。
- **为什么**：痛点是缓存/观察者持有对象导致对象永远无法回收（内存泄漏） → 机制是弱引用不计入引用计数与循环 GC 的强引用边，最后一个强引用消失时对象照常回收 → 行为是"想用时还在，没人用时自动消失" → 边界是 list/dict/int/str 等部分内置类型不支持弱引用（要包一层自定义类）。
- **怎么写**：
  ```python
  import weakref
  class Big: pass
  b = Big()
  r = weakref.ref(b)                       # 借钥匙：不占房
  print(r() is b)
  del b                                    # 主人退房
  print(r())                               # 钥匙失效
  ```
  → 运行输出：`True`\n`None`
- **何时用/不用**：做缓存/注册表/观察者列表怕"拿着不放"时用（或直接用 `WeakKeyDictionary/WeakValueDictionary`）；需要保活的普通持有别用（对象会提前消失）。
- **锚点**：断舍离里的**借钥匙不占房**——弱引用是借出去的备用钥匙：房子该卖卖（回收），钥匙自然失效；强引用是把房子过户到你名下（永不回收）。
- **易错**：弱引用只是"通行证"不是"保管箱"，期间任何强引用存在对象都不会回收；`r()` 每次调用才取对象，取出后要用变量接住，否则临时值立刻可回收。
- **关联**：→ PY-19-01/02：引用计数与 GC 是它的机制前提 ｜ → PY-19-10：lru_cache 的缓存边界问题可用 weakref 思路缓解。

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| 引用计数 vs gc | 归零即回收 | 收循环引用的环 | 有没有环 | 摘牌即清，成环找 gc |
| 浅拷贝 vs 深拷贝 | 复制外层、共享内层 | 递归全复制 | 改内层会不会波及原件 | 只换箱签是浅，全重装是深 |
| 列表 vs 生成器 | 一次全装进内存 | 按需逐个产 | 要不要随机访问/复用 | 全屋堆放 vs 传送口递件 |
| += 拼接 vs join | 每次造新串 | 一次分配批量拷 | 拼接段数 | 少量 +，大量 join |
| timeit vs cProfile | 测两段代码快慢 | 找全程最热函数 | 问题大小 | 比快慢掐表，找病灶体检 |
| lru_cache vs 换算法 | 记答案省重复算 | 改流程降复杂度 | 先换算法还是先缓存 | 算法先行，缓存补漏 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-19-01 | 引用计数 | 行李牌 | 行李牌 |
| PY-19-02 | gc 回收 | 互相绑着的行李牌→保洁剪牌 | 剪牌保洁 |
| PY-19-03 | 深浅拷贝 | 搬家装箱两种装法 | 装箱搬家 |
| PY-19-04 | __slots__ | 定格收纳柜 | 定格柜 |
| PY-19-05 | 生成器 | 断舍离传送口 | 传送口 |
| PY-19-06 | join 拼接 | 一次装箱 vs 来一件搬一次 | 一次装箱 |
| PY-19-07 | timeit | 厨房计时器 | 掐表 |
| PY-19-08 | cProfile | 上秤盘点找最重 | 上秤盘点 |
| PY-19-09 | tracemalloc | 收纳前后拍照对比 | 前后拍照 |
| PY-19-10 | lru_cache | 门口鞋架 | 门口鞋架 |
| PY-19-11 | set/dict 查找 | 贴标签收纳箱直取 | 标签直取 |
| PY-19-12 | 优化三步法 | 盘点→改造→复称 | 复称 |
| PY-19-13 | bytearray/memoryview | 免搬箱看货换货 | 免搬箱 |
| PY-19-14 | weakref 弱引用 | 借钥匙不占房 | 借钥匙 |

## ✅ 自测清单（合上本篇，先写再看）
1. `a = []; b = a` 后 `del b`，列表会被回收吗？为什么？
> 答案：不会，a 还挂着一张引用牌；两个名字都删掉（且不成环）才回收。
2. 两个对象互指、名字都删了，靠什么回收？写出命令。
> 答案：循环引用靠 gc：`gc.collect()`。
3. 写出一行生成器表达式，产生 0~9 的平方，并说明内存优势。
> 答案：`(x*x for x in range(10))`；只存配方不存全部值。
4. 循环拼接 1 万段字符串，正确写法是什么？
> 答案：先收集进列表再 `"".join(parts)`。
5. 程序整体变慢，第一步做什么？第二步的常见大招是什么？
> 答案：先测量定位热点（cProfile）；第二步优先换数据结构/算法（如 list→dict）。

6. （说区别）`memoryview` 切片赋值能改变数据长度吗？
   > 答案：不能，右侧字节长度必须与视图切片一致，否则 `ValueError`（PY-19-13）；要增删长度用 bytearray 本身。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-18 并发](py-18-concurrency.md) ｜ ➡️ 下一篇：[py-20 工程与测试](py-20-engineering-testing.md)
