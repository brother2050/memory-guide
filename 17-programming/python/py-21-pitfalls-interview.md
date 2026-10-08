# py-21 易错点与面试高频 — 记忆编码

> **📍 本章导航**：前置 → [py-00 路线图](py-00-roadmap.md) ｜ 相关 → py-01~py-20（消混对象）·[py-22 复习系统](py-22-review-drill.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M08](../../方法地图.md#m08) ｜ 难度 ⭐⭐⭐ ｜ 阅读 ~15min（约 10k tokens）
>
> 本章逻辑链：py-01~py-20 已完成篇内消混 → 本篇做**跨篇全局消混**（13 组）+ **面试高频 30 问** → [py-22](py-22-review-drill.md) 把 30 问练成肌肉记忆。
> **本篇不新建锚点**：锚点在各源篇，本篇只引用 PY-ID（`PY-模块号-序号` 规则见 [INDEX.md](INDEX.md)；消混表引用精确 PY-xx-xx，未定稿篇暂以模块级 PY-xx 占位；问题的（→ PY-xx）为答案所在模块的指引）。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 消混十三组 | G1~G13 | 跨篇撞车点，一组一张对比卡 |
| 基础十问 | Q01~Q10 | 语法级：张口就来 |
| 进阶十问 | Q11~Q20 | 机制级：说出因果链 |
| 高级十问 | Q21~Q30 | 架构级：给出权衡与边界 |

## 一、全局易混消混表（13 组）
> 统一格式：**定义 / 判据 / 反例 / 一句口诀 / → PY-ID**。判据 = 二选一时的判断规则；反例 = 一行复现的翻车现场（代码均经 Python 3.12 实测）。
### G1 `is` vs `==` —— 身份 vs 相等
| 项 | 内容 |
|---|---|
| 定义 | `is` 比身份（`id()` 同一对象否）；`==` 比值（走 `__eq__`） |
| 判据 | 判单例（None/True/False）、问"是不是同一个" → `is`；问"内容等不等" → `==` |
| 反例 | `[1,2] == [1,2]` 为 True，二者 `is` 为 False |
| 一句口诀 | 身份用 is，内容用 ==；判空 None 要用 is |
| → PY-ID | PY-02-11 id() 与对象身份 · PY-02-12 is 与 == 的分工 → 见 [py-02](py-02-variables-types.md) |
```python
a, b = [1, 2], [1, 2]
print("值等:", a == b, "| 同一对象:", a is b)
x, y = 256, 256
print("小整数 256 is 256:", x is y)
print("跨表达式 257:", int("257") is int("257"))
```
→ 运行输出：`值等: True | 同一对象: False` ／ `小整数 256 is 256: True` ／ `跨表达式 257: False`
### G2 赋值 vs 浅拷贝 vs 深拷贝
| 项 | 内容 |
|---|---|
| 定义 | 赋值=贴同一标签；浅拷贝 `copy.copy()`=只拷外壳一层、嵌套层共享；深拷贝 `copy.deepcopy()`=递归全拷、完全独立 |
| 判据 | 只改顶层 → 浅拷贝；会改嵌套层且互不牵连 → 深拷贝；刻意共享同一份 → 赋值 |
| 反例 | 浅拷贝后 `orig[0][0]=99`，拷贝品内层跟着变（以为是备份，实际共用器官） |
| 一句口诀 | 赋值贴标签，浅拷换外壳，深拷连内脏 |
| → PY-ID | PY-04-19 浅拷贝与深浅拷贝 · PY-19（引用计数）→ 见 [py-04](py-04-containers.md)·[py-19](py-19-memory-performance.md) |
```python
import copy
orig = [[1, 2], [3]]
assign, shallow, deep = orig, copy.copy(orig), copy.deepcopy(orig)
orig[0][0] = 99              # 改嵌套层，看三者谁跟着变
print("赋值 :", assign); print("浅拷:", shallow); print("深拷:", deep)
```
→ 运行输出：`赋值 : [[99, 2], [3]]` ／ `浅拷: [[99, 2], [3]]` ／ `深拷: [[1, 2], [3]]`
### G3 可变默认参数
| 项 | 内容 |
|---|---|
| 定义 | `def f(x, bucket=[])` 的默认值在 **def 执行时只创建一次**，多次调用共享同一个 list |
| 判据 | 默认值是 list/dict/set → 必换 `None` 哨兵；int/str/tuple 等不可变 → 可放心写 |
| 反例 | `add(1)` 得 `[1]`，`add(2)` 得 `[1, 2]`——第二次"继承"第一次的残留 |
| 一句口诀 | 默认可变是共享，None 哨兵函数里建 |
| → PY-ID | PY-07-04 可变默认参数陷阱 · PY-07-03 默认参数 → 见 [py-07](py-07-functions.md) |
```python
def add(x, bucket=[]):       # 反例：默认参数在 def 时只创建一次
    bucket.append(x)
    return bucket
print(add(1), add(2))        # -> [1, 2] [1, 2]（两次其实是同一个脏列表）
def add2(x, bucket=None):    # 正解：None 哨兵 + 调用时新建
    bucket = [] if bucket is None else bucket
    bucket.append(x)
    return bucket
print(add2(1), add2(2))      # -> [1] [2]
```
→ 运行输出：`[1, 2] [1, 2]` ／ `[1] [2]`（第一行两次返回同一个脏列表）
### G4 闭包延迟绑定
| 项 | 内容 |
|---|---|
| 定义 | 闭包（closure）捕获**变量本身**而非定义时的值，调用时才读"最新值"——延迟绑定（late binding） |
| 判据 | 循环批量生成函数后统一调用、结果全是"最后一个值" → 延迟绑定坑；要定格当场值 → 默认参数 `lambda i=i: i` |
| 反例 | `[lambda: i for i in range(3)]` 全部返回 `2` |
| 一句口诀 | 闭包记名字不记值，要定格用默认参数 |
| → PY-ID | PY-07-13 闭包 Closure → 见 [py-07](py-07-functions.md) |
```python
fns = [lambda: i for i in range(3)]          # 反例：捕获变量 i，循环结束才取值
print([f() for f in fns])                    # -> [2, 2, 2]
fns2 = [lambda i=i: i for i in range(3)]     # 正解：默认参数在定义时定格
print([f() for f in fns2])                   # -> [0, 1, 2]
```
→ 运行输出：`[2, 2, 2]` ／ `[0, 1, 2]`
### G5 小整数缓存与字符串驻留（interning）
| 项 | 内容 |
|---|---|
| 定义 | CPython 把 **-5~256 整数**做成常驻对象（小整数缓存），把标识符合法的字符串**驻留（intern）**复用——这些对象"碰巧"`is` 相等 |
| 判据 | 判"值相等"永远用 `==`；`is` 只留给 None 等单例。拿 `is` 当相等 = 把实现细节当语言保证 |
| 反例 | `256 is 256` 为 True，`int("257") is int("257")` 为 False——同一数字两种命运 |
| 一句口诀 | 缓存驻留是巧合，相等判定用等号 |
| → PY-ID | PY-02-04 int 整数 · PY-02-12 is 与 == 的分工 → 见 [py-02](py-02-variables-types.md) |
```python
x, y = 256, 256
print(x is y, int("1000") is int("1000"))   # 小整数缓存 vs 运行时新建
s1, s2 = "".join(["hel", "lo"]), "".join(["hel", "lo"])
print(s1 is s2, s1 == s2)                   # 运行时拼接不驻留：False True
import sys
print(sys.intern(s1) is sys.intern(s2))     # 显式驻留后才是同一对象
```
→ 运行输出：`True False` ／ `False True` ／ `True`
### G6 可变 vs 不可变
| 项 | 内容 |
|---|---|
| 定义 | 不可变（immutable）：int/str/tuple/frozenset，创建后不能改内容；可变（mutable）：list/dict/set，可原地增删改。不可变锁的是**槽位**，不锁槽位里的货 |
| 判据 | 要当 dict 键/集合元素 → 必须可哈希 → 不可变；要原地增删 → 可变 |
| 反例 | `t = ([1], 2)` 是 tuple，但 `t[0].append(99)` 成功——不可变壳里藏着可变 list |
| 一句口诀 | 不可变锁的是槽位，锁不住槽位里的货 |
| → PY-ID | PY-02-13 可变与不可变 · PY-04-05 元组 tuple → 见 [py-02](py-02-variables-types.md)·[py-04](py-04-containers.md) |
```python
t = ([1], 2)
t[0].append(99)              # tuple 槽位不可换，但里面的 list 可变
print(t)
try:
    t[0] = [0]
except TypeError as e:
    print("TypeError:", e)
```
→ 运行输出：`([1, 99], 2)` ／ `TypeError: 'tuple' object does not support item assignment`
### G7 `*args` vs `**kwargs`
| 项 | 内容 |
|---|---|
| 定义 | `*args` 把多余**位置参数**收进元组；`**kwargs` 把多余**关键字参数**收进字典；反过来 `f(*seq)`/`f(**dict)` 是解包 |
| 判据 | 传参看"有没有名字"：无名走 `*args`，有名走 `**kwargs`。签名顺序固定：普通参数→`*args`→仅关键字参数→`**kwargs` |
| 反例 | `f(1, 2, name="张三")` 中 `args=(1,2)`、`kwargs={"name":"张三"}` |
| 一句口诀 | 一星收位置成元组，两星收键值成字典 |
| → PY-ID | PY-07-06 *args 位置可变参数 · PY-07-07 **kwargs 关键字可变参数 → 见 [py-07](py-07-functions.md) |
```python
def f(*args, **kwargs):
    print(type(args).__name__, args, "|", type(kwargs).__name__, kwargs)
f(1, 2, name="张三")
```
→ 运行输出：`tuple (1, 2) | dict {'name': '张三'}`
### G8 类变量 vs 实例变量
| 项 | 内容 |
|---|---|
| 定义 | 类变量（class variable）在 class 体内、全实例共享；实例变量（instance variable）在 `__init__` 用 `self.x` 赋值、各实例独有 |
| 判据 | 读取顺序：实例 `__dict__` → 类 → 基类（沿 MRO）；实例上赋同名值 = **遮蔽**，不是修改类变量 |
| 反例 | `d1.kind = "宠物"` 后 d1 变了 d2 没变——给 d1 新建了实例变量，类变量毫发无损 |
| 一句口诀 | 实例赋值是遮蔽，改类变量用类名 |
| → PY-ID | PY-09（类变量vs实例变量）→ 见 [py-09](py-09-oop.md) |
```python
class Dog:
    kind = "犬科"            # 类变量：全实例共享
d1, d2 = Dog(), Dog()
d1.kind = "宠物"             # 反例：实例变量遮蔽类变量
Dog.kind = "哺乳类"          # 改类变量，未遮蔽者跟着变
print(d1.kind, d2.kind, Dog.kind)
```
→ 运行输出：`宠物 哺乳类 哺乳类`
### G9 `staticmethod` vs `classmethod`
| 项 | 内容 |
|---|---|
| 定义 | `@staticmethod`：无绑定普通函数，只"挂"在类里；`@classmethod`：首参收 **cls**（类本身），可被子类继承定制 |
| 判据 | 要用类本身（工厂方法/替代构造）→ classmethod；纯工具与类无关 → staticmethod；要实例状态 → 普通方法 |
| 反例 | 工厂方法写成 staticmethod，子类调用永远构造出父类实例——丢了 cls 就丢了多态 |
| 一句口诀 | classmethod 收 cls 管造物，staticmethod 挂名纯工具 |
| → PY-ID | PY-09（类方法/静态方法）→ 见 [py-09](py-09-oop.md) |
```python
class Date:
    def __init__(self, y, m, d):
        self.y, self.m, self.d = y, m, d
    @classmethod
    def from_str(cls, s):               # classmethod 收 cls，可被子类定制
        return cls(*map(int, s.split("-")))
    @staticmethod
    def ok(s):                          # staticmethod 与类无关，纯工具
        return len(s.split("-")) == 3
print(Date.from_str("2026-10-06").y, Date.ok("2026-10-06"))
```
→ 运行输出：`2026 True`
### G10 生成器 vs 列表
| 项 | 内容 |
|---|---|
| 定义 | 列表推导式 `[...]`：一次算完、全入内存、可反复遍历；生成器表达式 `(...)`/`yield`：惰性求值、逐个产出、**耗尽即止** |
| 判据 | 数据大 / 只遍历一次 / 流水线处理 → 生成器；要索引、多次遍历、`len()` → 列表 |
| 反例 | 遍历完生成器再遍历一次是空的——"像列表的括号"其实已耗尽 |
| 一句口诀 | 方括号囤货全算完，圆括号售货按需来 |
| → PY-ID | PY-11（生成器）·PY-04-14 列表推导式 → 见 [py-11](py-11-iterators-generators.md)·[py-04](py-04-containers.md) |
```python
gen = (x * 2 for x in range(3))         # 生成器：按需产出
print(next(gen), next(gen))
lst = [x * 2 for x in range(3)]         # 列表：一次算完、可反复遍历
print(lst, lst)
```
→ 运行输出：`0 2` ／ `[0, 2, 4] [0, 2, 4]`
### G11 迭代器 vs 可迭代对象
| 项 | 内容 |
|---|---|
| 定义 | 可迭代对象（iterable）实现 `__iter__`（list/dict/str/generator…）；迭代器（iterator）实现 `__iter__` **和** `__next__`，是带游标的取货员 |
| 判据 | `iter(x) is x` → 迭代器；`iter(x) is not x` → 仅可迭代。for = `iter()` + 反复 `next()` 直到 `StopIteration` |
| 反例 | `next([10,20])` 报 `TypeError`——list 能 for，但自己不是迭代器 |
| 一句口诀 | 可迭代是货品单，迭代器是取货员 |
| → PY-ID | PY-11（迭代协议）→ 见 [py-11](py-11-iterators-generators.md) |
```python
lst = [10, 20]
it = iter(lst)                 # 可迭代对象 -> 迭代器
print("iter(it) is it:", iter(it) is it)   # 迭代器判据
print(next(it), next(it))
```
→ 运行输出：`iter(it) is it: True` ／ `10 20`
### G12 异常 vs 返回码
| 项 | 内容 |
|---|---|
| 定义 | 返回码风格：函数返回 `(ok, value)`，调用方手动检查；异常风格（Python 惯例）：出错即 `raise`，调用方 `try/except`，正常路径干净 |
| 判据 | Python 首选异常（EAFP"先做再捕"）；返回码适合"错误是常态"的流程（如逐行解析统计失败数） |
| 反例 | `(False, None)` 被忽略 → None 悄悄流入下游，报错点离现场十万八千里 |
| 一句口诀 | Python 出错就报警，返回码要记得查警铃 |
| → PY-ID | PY-12（EAFP/LBYL）→ 见 [py-12](py-12-exceptions.md) |
```python
import json
def parse_rc(text):            # 返回码风格：调用方必须记得检查返回值
    try:
        return True, json.loads(text)
    except json.JSONDecodeError:
        return False, None
print(parse_rc('{"a": 1}'))
print(parse_rc("{bad}"))       # 遗忘检查 ok 标志 -> None 埋雷
```
→ 运行输出：`(True, {'a': 1})` ／ `(False, None)`
### G13 GIL 误解
| 项 | 内容 |
|---|---|
| 定义 | GIL（全局解释器锁）是 CPython 的锁：同一时刻只让**一个线程执行字节码**。两大误解："多线程没用"（错）、"多线程=并行"（也错） |
| 判据 | IO 密集（网络/磁盘/睡眠）→ 多线程**有效**（等待时释放 GIL）；CPU 密集 → 多线程**无效**，换 `multiprocessing`/原生扩展 |
| 反例 | 两个 CPU 密集线程不比一个快（实测略慢）；两个 IO 等待线程总耗时≈一个的耗时 |
| 一句口诀 | 等 IO 时放锁所以快，算数时抢锁所以白搭 |
| → PY-ID | PY-18（GIL/并发模型）→ 见 [py-18](py-18-concurrency.md) |
```python
import threading, time
def io_task():                 # 模拟 IO 等待（等待时释放 GIL）
    time.sleep(0.4)
def run(n):
    ts = [threading.Thread(target=io_task) for _ in range(n)]
    t0 = time.perf_counter()
    for t in ts: t.start()
    for t in ts: t.join()
    return round(time.perf_counter() - t0, 2)
print("IO 1线程:", run(1), "s | 2线程:", run(2), "s")
```
→ 运行输出：`IO 1线程: 0.4 s | 2线程: 0.4 s`（CPU 密集实测：1 线程 0.05s、2 线程 0.07s，不提速还多付切换成本）

## 二、面试高频 30 问（基础 / 进阶 / 高级）
> 用法：遮住"要点"先口答（[M08](../../方法地图.md#m08)），卡壳的进错题本按 [M32](../../方法地图.md#m32) 反向提取，练法见 [py-22](py-22-review-drill.md)。"加分"= 让面试官眼前一亮的下一层。
### 基础档 Q01~Q10（语法级：张口就来）

**Q01 list / tuple / dict / set 怎么区别、怎么选？**（→ PY-04）
- 要点：可变性——list/dict/set 可变、tuple 不可变可哈希；查找——dict/set 哈希 O(1)，list O(n)；顺序——list/tuple 有序、dict **3.7+ 规范保序**、set 无序；set 自动去重。选型：只读记录→tuple，键值索引→dict，去重/交并差→set，有序序列→list。
- 加分：tuple 能作 dict 键，正因不可变可哈希。

**Q02 赋值、浅拷贝、深拷贝的区别？**（→ PY-04·PY-19）
- 要点：赋值=同一对象多标签；浅拷贝 `copy.copy()`/切片/构造只拷一层、嵌套层共享；深拷贝 `copy.deepcopy()` 递归全拷。→ 见 G2。
- 加分：`dict.copy()`、`list()` 也都是浅拷贝。

**Q03 `is` 和 `==` 的区别？**（→ PY-02）
- 要点：`is` 比 `id()` 身份，`==` 比值（`__eq__`）；判 None 用 `is`。→ 见 G1。
- 加分：小整数缓存 -5~256 与字符串驻留，正是 `is` 偶尔"蒙对"的原因。

**Q04 为什么默认参数不能用可变对象？**（→ PY-07）
- 要点：默认值在 def 时求值一次存进函数对象、多次调用共享；表现=第二次调用"继承"残留；修复=None 哨兵+函数内新建。→ 见 G3。
- 加分：函数的 `__defaults__` 里能看到那个被共享的 list。

**Q05 `*args` 和 `**kwargs` 是什么？**（→ PY-07）
- 要点：定义时打包（args=元组、kwargs=字典）、调用时解包；签名顺序：普通参数→`*args`→仅关键字参数→`**kwargs`。→ 见 G7。
- 加分：`def f(*, timeout)` 强制关键字传参，防位置错位。

**Q06 字符串是可变的吗？拼接性能注意什么？**（→ PY-03）
- 要点：不可变，一切"修改"都是新建对象；循环 `s += piece` 是 O(n²)，改用 `"".join(list)`；f-string（3.6+）速度可读性俱佳。
- 加分：str 不可变所以可哈希、可作 dict 键；`replace`/`strip` 都返回新串。

**Q07 Python 怎么实现多态？**（→ PY-09）
- 要点：鸭子类型——不看类型看协议（有 `__len__` 就能 `len()`）；不靠签名重载，靠默认参数与 `*args`；要显式约束用 ABC 或 `typing.Protocol`。
- 加分：`collections.abc` 提供"注册"与"继承"两种承诺方式。

**Q08 `with` 语句做了什么？**（→ PY-10·PY-15）
- 要点：进入调 `__enter__`，退出**无论异常与否**都调 `__exit__` 做清理；文件/锁/连接靠它防泄漏。
- 加分：`__exit__` 返回 True 会吞异常（别这么干）；`contextlib.contextmanager` 用 yield 写装饰器版。

**Q09 列表推导式和生成器表达式怎么选？**（→ PY-04·PY-11）
- 要点：`[...]` 立即全量入内存、可重复遍历；`(...)` 惰性逐个、耗尽即止、省内存；数据大/只走一遍→生成器。→ 见 G10。
- 加分：推导式嵌套超过两层就改回普通循环，可读性优先。

**Q10 `try/except/else/finally` 各自何时执行？**（→ PY-12）
- 要点：`except` 捕匹配异常；`else` 在**无异常**时执行（放"成功才做"）；`finally` **总是**执行（放清理）。
- 加分：except 要窄不要宽，`except Exception` 会连真 bug 一起吞，裸 `except:` 是反模式。

### 进阶档 Q11~Q20（机制级：说出因果链）

**Q11 什么是 GIL？有了它多线程还有用吗？**（→ PY-18）
- 要点：CPython 解释器锁 → 同时刻一个线程执行字节码 → IO 密集仍有效（等待释放 GIL）、CPU 密集无效 → 换多进程/原生扩展。→ 见 G13。
- 加分：`multiprocessing` 用多进程绕锁，代价是通信要序列化。

**Q12 闭包的延迟绑定陷阱是什么？**（→ PY-07）
- 要点：闭包捕获变量而非值、调用时读最新值 → 循环生成的 lambda 全指向同一变量；修复=默认参数定格或 `functools.partial`。→ 见 G4。
- 加分：改外层变量要 `nonlocal`；闭包的 `__closure__` 存的是 cell 对象。

**Q13 装饰器的原理？`functools.wraps` 干什么？**（→ PY-08）
- 要点：`@deco` 等价 `f = deco(f)`，本质高阶函数返回 wrapper；不加 `wraps` 会丢 `__name__`/`__doc__`，被饰函数"身份不明"。
- 加分：带参装饰器=三层嵌套；类装饰器靠 `__call__`。

**Q14 迭代器、可迭代对象、生成器的关系？**（→ PY-11）
- 要点：可迭代=`__iter__`；迭代器=`__iter__`+`__next__`，判据 `iter(x) is x`；生成器是"自动挡迭代器"（yield 自动实现两协议），是迭代器子集。→ 见 G11。
- 加分：生成器另有 `send`/`throw`/`close`（协程前身）；`yield from` 是委托语法糖。

**Q15 类变量和实例变量的查找顺序？**（→ PY-09）
- 要点：读取走 实例 `__dict__` → 类 → 基类（MRO）；实例赋同名=遮蔽；可变类变量（类属性 list 当计数器）是全实例共享的雷。→ 见 G8。
- 加分：用 `vars(d)` 与 `Dog.__dict__` 验证遮蔽。

**Q16 `staticmethod` 和 `classmethod` 的区别？**（→ PY-09）
- 要点：classmethod 收 cls，适合工厂/替代构造、子类定制；staticmethod 无绑定纯工具；实例方法才收 self。→ 见 G9。
- 加分：工厂方法用 classmethod，子类调用才返回子类实例。

**Q17 `super()` 与 MRO 是怎么回事？**（→ PY-09）
- 要点：MRO 用 C3 线性化（`Cls.__mro__` 可查）；`super()` 是"沿 MRO 找**下一个**"而非"父类"；菱形继承下共同祖先只初始化一次。
- 加分：实测 `class D(B, C)` 的 MRO 为 `D→B→C→A→object`，`D().hello()` 输出 `D->B->C->A`。

**Q18 `__new__` 和 `__init__` 的区别？**（→ PY-10）
- 要点：`__new__` 静态方法，**创建并返回**实例（可返回别的对象）；`__init__` **初始化**已创建实例、不能返回值。
- 加分：单例、不可变类型要改 `__new__`；`__init__` 只能"装修"不能"换房"。

**Q19 Python 的内存管理机制？**（→ PY-19）
- 要点：引用计数为主（`sys.getrefcount`）、归零即回收；**循环引用**靠分代 GC（gc 三代）兜底；`__del__` 会阻碍回收。
- 加分：破循环用 `weakref`；定位泄漏用 `tracemalloc`/`gc.get_objects`。

**Q20 dict 的实现原理？为什么 3.7+ 有序？**（→ PY-04）
- 要点：哈希表（开放寻址解决冲突）、键须可哈希（`__hash__`+`__eq__` 一致）；3.6 起紧凑字典按插入序存取、3.7 起写进语言规范。
- 加分：`__eq__` 相等则 `__hash__` 必须相等，否则 dict 找不到键。

### 高级档 Q21~Q30（架构级：给出权衡与边界）

**Q21 asyncio 的事件循环怎么调度？**（→ PY-18）
- 要点：单线程事件循环**协作式**调度——`await` 主动让出、IO 就绪才恢复；适合高并发网络 IO；CPU 阻塞会卡死整个循环，要丢 `asyncio.to_thread`。
- 加分：协程无抢占；`gather`/`TaskGroup` 做并发编排；勿在普通线程里随意 `run_until_complete`。

**Q22 threading / multiprocessing / asyncio 怎么选？**（→ PY-18）
- 要点：IO 密集+少量并发→threading；IO 密集+海量连接→asyncio；CPU 密集→multiprocessing/`ProcessPoolExecutor`（GIL 是根因）；混合负载→进程池+协程分层。
- 加分：说清代价——线程有锁与切换开销、进程有序列化与内存开销、协程要求全链路 async 生态。

**Q23 描述符协议和 property 的原理？**（→ PY-09·PY-10）
- 要点：实现 `__get__`/`__set__`/`__delete__` 即描述符；`property` 是**数据描述符**、优先级高于实例 `__dict__`，故 setter 能拦截赋值；用途=校验、惰性缓存。
- 加分：只实现 `__get__` 是非数据描述符、会被实例字典覆盖；`functools.cached_property` 即惰性缓存。

**Q24 元类（metaclass）解决什么问题？**（→ PY-10·PY-17）
- 要点：元类是"类的类"（默认 `type`）、拦截**类的创建过程**；用途=注册表、字段校验、ORM 字段映射。
- 加分：多数场景类装饰器/类工厂就够，"元类是最后手段"，可读性代价高。

**Q25 `__slots__` 的作用与限制？**（→ PY-09·PY-19）
- 要点：去掉实例 `__dict__` 省内存（实测同结构对象 112 vs 408 字节量级）、属性访问更快；限制=不能动态加属性、继承需注意、默认不支持弱引用。
- 加分：适合海量小对象（点/坐标/消息体）；类变量、property 照常可用。

**Q26 Python 性能优化的一般路径？**（→ PY-19）
- 要点：先**测量**（`cProfile`/`timeit`）再优化；大头是算法与数据结构 → 热路径局部化、`join` 拼接、生成器降内存、`lru_cache` 换时间 → 真瓶颈上 C 扩展/多进程。
- 加分：警惕过早微优化；能给出"优化前后数据"才叫优化。

**Q27 import 机制是什么？循环导入怎么解决？**（→ PY-13）
- 要点：找模块（`sys.path`）→ 查 `sys.modules` 缓存 → 执行模块体 → 绑定名字；循环导入=两模块顶层互相引用、对方名字未绑定完。解决：延迟导入（函数内 import）、抽共享模块、重构依赖方向。
- 加分：`__name__ == "__main__"` 让文件兼任脚本与模块。

**Q28 上下文管理器协议与 `contextlib` 的用法？**（→ PY-10）
- 要点：`__enter__` 返回资源、`__exit__` 清理且异常必达；`@contextmanager` 把"前进场+yield+后清理"写成普通函数；`ExitStack` 动态管理不定量资源、`suppress` 忽略指定异常。
- 加分：对比 try/finally——with 把清理绑在资源定义处，不易漏。

**Q29 异常链（`raise ... from ...`）有什么意义？**（→ PY-12）
- 要点：异常转译时默认 `__context__` 保留原异常；`raise NewErr(...) from e` 显式建立 `__cause__`，排障可见完整因果链；`from None` 主动隐藏噪音。
- 加分：库作者应"转译不吞没"，别 `except: pass`。

**Q30 一个 Python 项目的工程化基线？**（→ PY-17·PY-20）
- 要点：ruff/black 统一风格、mypy 渐进类型、pytest 覆盖核心路径、logging 分级（别用 print）、uv/poetry 锁依赖、CI 三道闸（lint→type→test）。
- 加分：类型注解=文档+IDE+检查三合一；`dataclass`/`Enum`/`Protocol` 是现代 Python 的免费类型安全。

## 三、这张表怎么用（30 秒版）

1. **消混**：G1~G13 每天抽 3 组，遮住口诀复述判据（说区别模板见 [py-22](py-22-review-drill.md)）。
2. **面试**：每天 5 问口答 + 2 问手写（如 G3/G4 的修复代码），答不上进错题本 → [M32](../../方法地图.md#m32)。
3. **冲刺**：考前只看"判据 + 一句口诀"两列，其余交给肌肉记忆。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-20 工程与测试](py-20-engineering-testing.md) ｜ ➡️ 下一篇：[py-22 复习系统](py-22-review-drill.md)
