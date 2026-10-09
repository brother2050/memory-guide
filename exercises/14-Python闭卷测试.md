# 🧪 Python 闭卷测试卷（T1 基础 + T2 进阶）

> **📍 本章导航**：前置 → [py-22 复习系统](../17-programming/python/py-22-review-drill.md)（自测四件套 T1/T2 口径）·[py-00 路线图](../17-programming/python/py-00-roadmap.md)（阶段表）｜ 相关 → [17-programming/python/INDEX](../17-programming/python/INDEX.md)（阶段出口检验）·[进度追踪表](../templates/记忆训练进度追踪表.md) ｜ 方法 → [M08](../方法地图.md#m08)·[M30](../方法地图.md#m30)·[M32](../方法地图.md#m32)·[M07-R](../方法地图.md#m07-r) ｜ 难度 ⭐⭐⭐ ｜ 阅读 ~15min（做题另计）
>
> 不是看懂了就算会——**合上资料、限时手写、先写再对答案**。

## 🎯 使用说明（先读这 10 行再开卷）

1. **闭卷铁律**（[M08](../方法地图.md#m08)）：合上 py 篇、INDEX、一切资料，只留空白编辑器/白纸与本卷；**先写/先说，写完才准看答案**。看懂答案不算会，重做全对才算过。
2. **计时**：T1 基础卷 90 分钟、T2 进阶卷 90 分钟，分两次做完；手写代码单题限时约 15 分钟（对齐 [py-22](../17-programming/python/py-22-review-drill.md) T1），改错/排错单题 5 分钟先找错。
3. **通过线怎么判（≥70%）**：①卷面得分 ≥70/100；②手写代码 8 题"一次写对"≥6 题（≈70%，对齐 [INDEX](../17-programming/python/INDEX.md) 阶段 1 出口"T1 闭卷手写一次通过率 ≥70%"）。两条同时满足才算过；只过 ①不过 ② = 代码没过关，回炉手写。
4. **各类题判分线**（沿用 [py-22](../17-programming/python/py-22-review-drill.md) 自测四件套）：手写代码 = 一次运行通过且输出与预期一致；改错/排错 = 找出全部 bug 且改对跑对（改对一半 = 不过）；说区别 = 四要素齐全（定义/判据/反例/口诀）且反例能当场一行写对。
5. **范围**：T1 基础卷 ↔ py-02~py-08（阶段 1~2）；T2 进阶卷 ↔ py-09~py-20（阶段 3~6）。每题标注分值与 PY-ID，错题按 PY-ID 回源篇补。
6. **失败处理**：不过的题一律进错题本，走文末《错题回填指引》。

---

# T1 基础卷（py-02~py-08｜90 分钟｜满分 100）

## 一、手写代码题（8 题 × 7 分 = 56 分）

**T1-1**（7 分｜PY-04-12、PY-04-13）给定 `words = ["apple", "banana", "cherry", "fig"]`：①用**列表推导**生成"长度 ≥5 的词转大写"的列表；②用**字典推导**生成 `{词: 长度}` 字典；③写一行嵌套推导，把 `grid = [["a","b"],["c"]]` 扁平化成一维列表。

**T1-2**（7 分｜PY-03-04、PY-03-07）写两个函数：①`cn_date("2026-10-09")` 返回 `"09.10.2026"`（要求用 split + 解包或 join，不用 replace）；②`reverse("abcde")` 用**一行切片**返回 `"edcba"`。写出 `cn_date` 的返回值。

**T1-3**（7 分｜PY-03-10、PY-02-16）已知 `pi, n, rate, big = 3.14159, 42, 0.25, 1234567`，各写一条 f-string：①两位小数；②右对齐占 6 格后跟一个 `|`；③百分比保留 1 位小数；④千分位分隔。写出四条的输出。

**T1-4**（7 分｜PY-07-06、PY-07-07、PY-07-08、PY-07-10）写函数 `process(a, b=0, *parts, mode, level=1, **extra)`，原样返回六个参数；并预测 `process(1, 2, 3, 4, mode="fast", level=2, tag="X")` 的输出（写出精确值）。

**T1-5**（7 分｜PY-07-12、PY-07-13）手写闭包 `make_counter()`：返回的内层函数每调用一次加 1 并返回当前值；两个计数器互不干扰。写出 `c1, c2 = make_counter(), make_counter()` 后 `c1(), c1(), c2()` 的输出，并说明内层为什么必须写 `nonlocal`。

**T1-6**（7 分｜PY-08-05、PY-08-07、PY-08-08）从零手写带参装饰器 `@retry(times=3)`：被装饰函数抛 `ValueError` 时自动重试，最多 3 次，每次打印第几次返工；要求三层结构、`functools.wraps`、`*a, **kw` 透传并**原样返回**结果。

**T1-7**（7 分｜PY-06-05、PY-06-06）①在单号列表 `["SF001","SF002"]` 中查找目标 `target`，找到打印"找到"并 break，全程没找到时用 **for-else** 打印"全部查验通过"（不用标志位）；②用 `enumerate` 把 `lines = ["1号线","2号线"]` 打印成 `1 1号线; 2 2号线;`（编号从 1 起）。

**T1-8**（7 分｜PY-04-15、PY-04-16）给定 `parcels = [("SF003", 2.0), ("SF001", 1.5), ("SF002", 2.0)]`：①按**重量降序、重量相同按编号升序**排序（元组 key，一次 sorted），写出结果；②用**星号解包**把 `codes = ["SF001","SF002","SF003"]` 拆成"第一个 + 其余"，写出 `first` 与 `rest` 的值和 `rest` 的类型。

## 二、改错题（4 题 × 6 分 = 24 分；每题先找全错，再改正）

**T1-9**（6 分｜PY-07-04）下列函数连续三次调用 `avg_score([])`、`avg_score([80,90,100])`、`avg_score([100])`，第三次结果是 92.5 而不是 100.0，且第一次直接崩。找出全部 bug 并改正：
```python
def avg_score(scores, total=[]):
    for s in scores:
        total.append(s)
    return sum(total) / len(total)
```

**T1-10**（6 分｜PY-02-12、PY-02-05）两处判断写错了，说出哪里不可靠、为什么，并改正：
```python
a, b = int("257"), int("257")
if a is b:
    print("同一对象")            # 期望：值相等就是"同一对象"
x = 0.1 + 0.2
if x == 0.3:
    print("相等")                # 期望：应打印"相等"
```

**T1-11**（6 分｜PY-06-14）想删掉列表里所有 2，结果剩了 `[1, 2, 3]`。找出 bug、解释为什么漏删，并改正（给出两种正确写法之一）：
```python
nums = [1, 2, 2, 3]
for n in nums:
    if n == 2:
        nums.remove(n)
```

**T1-12**（6 分｜PY-08-04、PY-08-06）装饰器有两处埋错，改正后 `add.__name__` 应为 `'add'`、`add(2, 3)` 应返回 `5`：
```python
import functools
def deco(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)          # 只调用
    return wrapper
@deco
def add(a, b):
    "两数相加"
    return a + b
print(add.__name__, add(2, 3))
```

## 三、说区别题（4 题 × 5 分 = 20 分；每题按"定义 / 判据 / 反例一行 / 一句口诀"四要素作答）

**T1-13**（5 分｜PY-02-11、PY-02-12）说区别：`is` 与 `==`。

**T1-14**（5 分｜PY-04-17）说区别：浅拷贝与深拷贝（给出嵌套容器反例）。

**T1-15**（5 分｜PY-07-03、PY-07-04）说区别：可变对象当默认参数 vs `None` 哨兵写法。

**T1-16**（5 分｜PY-04-02）说区别：`append` 与 `extend`（含"传列表"的反例）。

---

# T2 进阶卷（py-09~py-20｜90 分钟｜满分 100）

## 一、手写代码题（8 题 × 7 分 = 56 分）

**T2-1**（7 分｜PY-09-03、PY-09-05、PY-09-06、PY-09-12）设计 `Shape` 基类与 `Circle(Shape)` 子类：`__init__` 登记名字；类变量 `count` 统计实例数（全族共享）；子类用 `super().__init__` 保留父类初始化并重写 `area()`。写出 `c1, c2 = Circle(1), Circle(2)` 后 `c1.area()`（π 取 3.14）与 `Shape.count` 的值。

**T2-2**（7 分｜PY-10-02、PY-10-06、PY-10-07、PY-10-13）写 `Money` 类：`Money(2) + Money(3)` 得到 `Money(5)`（返回**新对象**）；`print(m)` 显示 `￥5`（另写 `__repr__`）；`==` 按金额判等（带 isinstance 防御）；可被 `sorted` 排序。

**T2-3**（7 分｜PY-10-16、PY-10-19）写一个**描述符** `TypedField(typ)`：登记字段名、赋值类型不符抛 `TypeError`（错误信息带字段名）、取值走实例字典；写出 `class Player: level = TypedField(int)` 中 `p.level = "高"` 的报错文本。

**T2-4**（7 分｜PY-11-07、PY-11-11）写生成器 `flatten(rows)`：用 `yield from` 把 `[[1,2],[3]]` 扁平成 `1,2,3`（惰性产出，不要先转列表）。写出 `list(flatten([[1,2],[3]]))` 的结果，并说明为什么它是惰性的。

**T2-5**（7 分｜PY-11-01、PY-11-05）手写迭代器类 `Fib(n)`：产前 n 个斐波那契数 `1,1,2,3,5…`，实现 `__iter__`/`__next__`，耗尽抛 `StopIteration`。写出 `list(Fib(5))`，并指出它能否被 for 遍历两遍、为什么。

**T2-6**（7 分｜PY-12-05、PY-12-06、PY-12-08、PY-12-11）①自定义异常 `ParseError(Exception)`（带消息，命名规范）；②`parse_age(s)` 解析失败时 `raise ParseError(...) from e` 保留原始原因；③调用方写 `try/except ParseError/else/finally` 完整结构。说明 else 与 finally 各自的执行时机。

**T2-7**（7 分｜PY-16-08、PY-16-10、PY-16-12）日志行 `line = "2026-10-09 08:09 ERROR 磁盘满"`：①用**命名分组 + search** 提取日期、级别、消息（写出 `m.group("level")` 的值）；②用 `sub` 把日期换成 `09/10/2026` 格式（写出替换后的整行）。

**T2-8**（7 分｜PY-18-06、PY-18-09、PY-18-13）并发选型与骨架：100 个 URL 下载（IO 密集）与大矩阵运算（CPU 密集）分别选线程/协程/进程中的哪种？为什么？写出 IO 密集版骨架（ThreadPoolExecutor 或 asyncio.gather 二选一）。

## 二、机制问答题（4 题 × 6 分 = 24 分）

**T2-9**（6 分｜PY-09-12、PY-09-13）`class A`，`class B(A)`，`class C(A)`，`class D(B, C)`。写出 `D.__mro__` 的顺序，说明 MRO 按什么算法排、`super()` 沿什么查找；`class D(C, B)` 会怎样？

**T2-10**（6 分｜PY-18-01、PY-18-13）什么是 GIL？为什么 CPU 密集任务开多线程不提速、IO 密集却有效？怎么绕开 GIL？

**T2-11**（6 分｜PY-10-17、PY-10-18）数据描述符、实例字典、非数据描述符的查找优先级是什么？为什么无 setter 的 `property` 赋值会抛 `AttributeError` 而不会写进实例字典？

**T2-12**（6 分｜PY-11-01、PY-11-04、PY-11-06）可迭代对象与迭代器差在哪？把 `for x in obj` 展开成协议三步；为什么同一个生成器第二遍遍历是空的？要复用该怎么做？

## 三、排错题（4 题 × 5 分 = 20 分；指出病因 + 改正）

**T2-13**（5 分｜PY-10-06、PY-10-08）`Point` 定义了 `__eq__` 后 `{Point(1): "A"}[Point(1)]` 抛 `TypeError: unhashable type: 'Point'`。为什么？怎么修？

**T2-14**（5 分｜PY-12-06、PY-12-08、PY-12-16）下面函数有两处异常处理坏味道，指出来并改正：
```python
def load(cfg):
    try:
        return parse(cfg)
    except Exception:
        pass
    finally:
        return "ok"
```

**T2-15**（5 分｜PY-11-04、PY-11-06）`it = (x for x in range(3))` 后 `print(list(it), list(it))` 实际输出 `[0, 1, 2] []`，作者期望两遍都是 `[0, 1, 2]`。为什么第二遍是空的？给两种修法。

**T2-16**（5 分｜PY-18-02、PY-18-03）8 个线程各执行 `for _ in range(100000): counter += 1`，结果远小于 800000。作者辩解"有 GIL 所以不用加锁"。错在哪？`counter += 1` 实际是几步？怎么改？

---

# 参考答案与评分标准（做完再看！）

## T1 基础卷答案

**T1-1**（7 分）
> ① `[w.upper() for w in words if len(w) >= 5]` → `['APPLE', 'BANANA']`；② `{w: len(w) for w in words}` → `{'apple': 5, 'banana': 6, 'cherry': 6, 'fig': 3}`；③ `[x for row in grid for x in row]` → `['a','b','c']`。
> 得分点：①结果在前、for 居中、if 收尾且输出对 3 分；②键值构造对 2 分；③嵌套推导外层 for 在前 2 分。

**T1-2**（7 分）
> ① `def cn_date(s): y, m, d = s.split("-"); return f"{d}.{m}.{y}"`（或 `".".join(reversed(s.split("-")))`）→ `09.10.2026`；② `def reverse(s): return s[::-1]`。
> 得分点：split 拆分 2 分；解包/拼回正确 3 分；切片 `[::-1]` 反转一行 2 分。

**T1-3**（7 分）
> `f"{pi:.2f}"` → `3.14`；`f"{n:>6}|"` → 42 右对齐占 6 格再跟 `|`；`f"{rate:.1%}"` → `25.0%`；`f"{big:,}"` → `1,234,567`。
> 得分点：四种规格符 `:.2f` / `:>6` / `:.1%` / `:,` 各 1.5 分（写对符号即可），输出全对再 1 分。

**T1-4**（7 分）
> 签名次序：位置/默认 → `*args` → keyword-only（`mode`、`level`）→ `**kwargs`；`mode` 必须点名传。
> 输出：`(1, 2, (3, 4), 'fast', 2, {'tag': 'X'})`（a=1、b=2、parts=(3,4) 元组、mode/level 点名、extra 收字典）。
> 得分点：签名合法且次序对 3 分；*args 收元组/**kwargs 收字典 2 分；输出精确预测 2 分。

**T1-5**（7 分）
> `def make_counter(): n = 0; def plus(): nonlocal n; n += 1; return n; return plus`；输出 `1 2 1`（c1/c2 各自独立环境）。
> `nonlocal`：不声明时内层对 n 赋值会新建本地变量（改不到外层，读取报 UnboundLocalError）；`nonlocal` 声明改最近外层函数的名字。
> 得分点：闭包结构与返回内层函数 2 分；nonlocal + 自增返回 2 分；输出 `1 2 1` 2 分；解释 nonlocal 1 分。

**T1-6**（7 分）
> 三层：`def retry(times): def deco(func): @wraps(func) def wrapper(*a, **kw): for i in range(times): try: return func(*a, **kw) except ValueError as e: print(f"第{i+1}次返工: {e}"); return wrapper; return deco`。
> 得分点：三层结构（参数层返回 deco、deco 返回 wrapper）2 分；`@functools.wraps(func)` 1 分；`*a, **kw` 透传且 `return func(...)` 2 分；重试循环只捕 `ValueError` 2 分。

**T1-7**（7 分）
> ① `for code in codes: if code == target: print("找到"); break` 后接 `else: print("全部查验通过")`——else 是"没被 break 才执行"，不是"没进循环"；② `for i, name in enumerate(lines, 1): print(i, name, end="; ")`。
> 得分点：for-else 结构 2 分；语义（没 break 才走 else）2 分；enumerate 带 start=1 且输出对 3 分。

**T1-8**（7 分）
> ① `sorted(parcels, key=lambda p: (-p[1], p[0]))` → `[('SF002', 2.0), ('SF003', 2.0), ('SF001', 1.5)]`（元组 key 逐位比，负号实现降序）；② `first, *rest = codes` → `first='SF001'`、`rest=['SF002', 'SF003']`，rest 是 **list**（星号永远收列表）。
> 得分点：元组 key + 降序写法 3 分；结果对 1 分；星号解包正确 2 分；rest 是 list 1 分。

**T1-9**（6 分）
> 埋错①：`total=[]` 是可变默认参数，def 时创建一次、所有调用共享，前两次成绩污染第三次；埋错②：空列表未防御，`sum([])/len([])` 抛 `ZeroDivisionError`。
> 改正：`def avg_score(scores): if not scores: raise ValueError("scores 不能为空"); return sum(scores) / len(scores)`，或 `total=None` 哨兵 + `if total is None: total = []`。
> 得分点：指出共享默认累积 2 分；指出空序列崩溃 2 分；改成 None 哨兵/现造列表并防御空输入 2 分。

**T1-10**（6 分）
> ① `a is b` 不可靠：`is` 比身份（id），257 超出小整数缓存时是两个对象（缓存是实现细节，不能当规律）；比值应写 `a == b`。② `0.1 + 0.2 == 0.3` 为 False：0.1 二进制只能近似存储，累加得 `0.30000000000000004`；改用 `math.isclose(x, 0.3)` 或 `round(x - 0.3, 10) == 0`。
> 得分点：is/== 分工说清 2 分；浮点近似原因 2 分；两处改正各 1 分。

**T1-11**（6 分）
> 病因：for 按下标推进，`remove` 让后元素前移，下一轮跳过一个 2（实测留下 `[1, 2, 3]`）。
> 改正：遍历副本 `for n in nums[:]:` 或重建 `nums = [n for n in nums if n != 2]`（→ `[1, 3]`）。
> 得分点：解释"下标与元素移动打架导致跳元素"3 分；改正写法（副本或推导式重建）且结果 `[1, 3]` 3 分。

**T1-12**（6 分）
> 埋错①：`wrapper` 忘 `return func(*args, **kwargs)`，返回值变 None（`add(2,3)` 得 None）；埋错②：没加 `@functools.wraps(func)`，`add.__name__` 变 `'wrapper'`、`__doc__` 变 None（丢身份）。
> 改正：wrapper 里 `return func(*args, **kwargs)`；wrapper 上加 `@functools.wraps(func)`（注意写 `(func)`）。
> 得分点：两处埋错各 2 分；改正（return + wraps）2 分。

**T1-13**（5 分）
> 定义：`is` 比身份（id 是否同一对象），`==` 比值（默认走 `__eq__` 比内容）。判据：判 None/True/False 等单例用 `is`，比内容用 `==`。反例：`x = int("257"); y = int("257")` → `x == y` 为 True、`x is y` 为 False。口诀：值等靠 eq，身份靠 is。
> 得分点：定义 1 分、判据 1 分、反例一行写对 2 分、口诀 1 分。

**T1-14**（5 分）
> 定义：浅拷贝只复制最外层（`copy()`/`list()`/`[:]`），深拷贝（`copy.deepcopy`）递归复制所有层。判据：嵌套内部是否共享。反例：`d = {"k": ["A"]}; s = d.copy(); de = copy.deepcopy(d); d["k"].append("B")` → `s["k"] == ['A','B']`、`de["k"] == ['A']`。口诀：浅拷外层，深拷全套。
> 得分点：定义 1 分、判据 1 分、反例一行写对 2 分、口诀 1 分。

**T1-15**（5 分）
> 定义：`def f(bucket=[])` 的默认箱在 def 时造一次、所有调用共享且数据残留；`bucket=None` 哨兵每次调用现造新箱。判据：默认值是不是可变对象（list/dict/set）。反例：`add("螺丝")` 后再 `add("螺母")` 得 `['螺丝', '螺母']`（应各是 `['螺丝']`、`['螺母']`）。口诀：默认可变全厂共箱，None 占位每次新箱。
> 得分点：定义 1 分、判据 1 分、反例一行写对 2 分、口诀 1 分。

**T1-16**（5 分）
> 定义：`append` 加一件（传列表会套一层），`extend` 一批逐件上架。判据：传的是单件还是可迭代。反例：`bad = ["A"]; bad.append(["B","C"])` → `['A', ['B','C']]`（len 只 +1）；`extend` 传字符串会按字符拆开。口诀：append 一件，extend 一批。
> 得分点：定义 1 分、判据 1 分、反例一行写对 2 分、口诀 1 分。

## T2 进阶卷答案

**T2-1**（7 分）
> `class Shape: count = 0; def __init__(self, name): self.name = name; Shape.count += 1; def area(self): return 0`；`class Circle(Shape): def __init__(self, r): super().__init__("圆"); self.r = r; def area(self): return 3.14 * self.r ** 2`。
> 输出：`c1.area() == 3.14`；`Shape.count == 2`（类变量全族共享；经实例赋值才会遮蔽）。
> 得分点：__init__ 登记且返回 None 2 分；super() 调父类初始化 2 分；类变量 count 共享 2 分；重写 area 输出 1 分。

**T2-2**（7 分）
> `__add__` 返回 `Money(self.yuan + other.yuan)`（新对象）；`__str__` 返回 `f"￥{self.yuan}"`；`__repr__` 返回 `f"Money({self.yuan})"`（开发者可复现）；`__eq__` 用 `isinstance(other, Money) and self.yuan == other.yuan`；`__lt__` 比 `self.yuan < other.yuan`（与 eq 同字段）。
> 得分点：__add__ 返回新 Money 2 分；str/repr 分工 2 分；__eq__ 带 isinstance 2 分；__lt__ 可排序 1 分。

**T2-3**（7 分）
> `class TypedField: def __set_name__(self, owner, name): self.name = name; def __get__(self, obj, owner): return None if obj is None else obj.__dict__[self.name]; def __set__(self, obj, value): if not isinstance(value, self.typ): raise TypeError(f"{self.name} 需要 {self.typ.__name__}"); obj.__dict__[self.name] = value`；描述符必须定义在**类**上。
> 报错文本：`level 需要 int`（TypeError）。
> 得分点：`__set_name__` 登记 2 分；`__get__` 走实例字典 1 分；`__set__` 校验+报错带字段名 3 分；指出必须挂在类上 1 分。

**T2-4**（7 分）
> `def flatten(rows): for row in rows: yield from row`；`list(flatten([[1,2],[3]]))` → `[1, 2, 3]`。
> 惰性：含 yield 的函数调用后只返回生成器，逐个取值时才执行到 yield（不预先把数据装进内存）；`yield from` 把子可迭代的值逐个转发并透传 send/throw。
> 得分点：生成器函数结构 2 分；yield from 转发 2 分；结果正确 1 分；惰性解释 2 分。

**T2-5**（7 分）
> `class Fib: def __init__(self, n): self.n, self.i, self.a, self.b = n, 0, 0, 1; def __iter__(self): return self; def __next__(self): if self.i >= self.n: raise StopIteration; self.i += 1; self.a, self.b = self.b, self.a + self.b; return self.a`。
> `list(Fib(5))` → `[1, 1, 2, 3, 5]`。**不能**遍历两遍：它既是可迭代对象又是迭代器（`__iter__` 返回 self），状态记在实例里、取完即废。
> 得分点：__iter__ 返回 self 2 分；__next__ 推进+StopIteration 3 分；结果+一次性的解释 2 分。

**T2-6**（7 分）
> `class ParseError(Exception): pass`（命名 Error 结尾、挂 Exception 下；带字段就 `super().__init__(msg)`）；`raise ParseError(f"年龄非法: {s}") from e`（`__cause__` 指向原异常，traceback 显示因果链）；`try: n = parse_age(s) except ParseError as e: ... else: print("解析成功", n) finally: print("收尾")`。
> else 只在 try 无异常时执行；finally 无论是否出错/return 都执行。
> 得分点：自定义异常规范 2 分；raise from 显式异常链 2 分；try/except/else/finally 结构 2 分；else/finally 时机 1 分。

**T2-7**（7 分）
> ① `m = re.search(r"(?P<y>\d{4})-(?P<mo>\d{2})-(?P<d>\d{2}) (?P<time>\S+) (?P<level>\w+) (?P<msg>.+)", line)`；`m.group("level")` → `ERROR`（`groupdict()` 拿全部字段）。② `re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", line)` → `09/10/2026 08:09 ERROR 磁盘满`。
> 得分点：命名分组 `(?P<name>...)` 2 分；search 全场找 1.5 分；sub 反向引用 `r"\3/\2/\1"` 2.5 分；用原始字符串 r"" 1 分。

**T2-8**（7 分）
> IO 密集（下载）→ 多线程或协程：IO 等待时让出 GIL，可并发等网络；CPU 密集（矩阵）→ 多进程（ProcessPoolExecutor）：每进程一把 GIL，真并行；协程里跑 CPU 任务要 `run_in_executor` 丢进程池，否则堵死事件循环。
> 骨架：`from concurrent.futures import ThreadPoolExecutor` + `with ThreadPoolExecutor(8) as ex: results = list(ex.map(download, urls))`（或 `await asyncio.gather(*(fetch(u) for u in urls))`）。
> 得分点：两场景选型各 1.5 分（共 3）；理由扣 GIL 2 分；骨架可用 2 分。

**T2-9**（6 分）
> `D.__mro__` = `[D, B, C, A, object]`。MRO 用 C3 线性化：子类在前、保持基类列表相对顺序（先 B 后 C）；`super()` 不是"调父类"，而是沿 MRO 链找**下一个**类的实现。`class D(C, B)` 则变为 `[D, C, B, A, object]`（悄悄换优先级）；MRO 无法线性化时创建类抛 TypeError。
> 得分点：MRO 顺序写对 2 分；C3 两条原则 2 分；super 沿 MRO 1 分；写反基类顺序的后果 1 分。

**T2-10**（6 分）
> GIL：CPython 全局解释器锁，同一时刻只允许一个线程执行 Python 字节码（为保护引用计数）。CPU 密集：线程轮流排队拿锁，还多付切换开销，不提速甚至更慢；IO 密集：线程在 IO 等待时让出 GIL，其他线程可继续跑。绕开：多进程（每进程一锁）或把计算交给 NumPy 等原生扩展。
> 得分点：定义 1.5 分；CPU 不提速的原因 1.5 分；IO 有效的原因 1.5 分；绕开方式 1.5 分。

**T2-11**（6 分）
> 优先级：**数据描述符（定义了 `__set__`/`__delete__`）> 实例字典 `__dict__` > 非数据描述符（只有 `__get__`）**。property 是内置**数据描述符**，赋值必走它的 `__set__`；没给 setter 时 `__set__` 直接抛 `AttributeError`，因此永远轮不到实例字典（不会被悄悄覆盖）。懒加载等非数据描述符则可被实例字典缓存盖掉。
> 得分点：优先级链条 3 分；数据/非数据判据 1 分；property 无 setter 抛 AttributeError 的机制 2 分。

**T2-12**（6 分）
> 可迭代对象实现 `__iter__`，能反复遍历；迭代器额外实现 `__next__`（`__iter__` 返回自身），是"一次性取货口"，取完抛 StopIteration。for 三步：`iter(obj)` 得迭代器 → 反复 `next()` → 捕获 `StopIteration` 结束。生成器/迭代器遍历消耗的是自身状态，第二遍自然为空；要复用就每次重新创建生成器，或实现"可迭代但非迭代器"（`__iter__` 每次返回新迭代器，如 list）。
> 得分点：两者区别 2 分；for 三步展开 2 分；耗尽原因+复用做法 2 分。

**T2-13**（5 分）
> 病因：类里定义 `__eq__` 而未定义 `__hash__` 时，Python 自动把 `__hash__` 置 None，对象变为不可哈希（可变对象的自我保护），进 dict/set 直接 `TypeError: unhashable type`。
> 修：补 `def __hash__(self): return hash(self.x)`，并保证 `__eq__` 相等则 `__hash__` 相等（否则 dict 会存两份、查找忽好忽坏）。
> 得分点：说清 __eq__ 连带置 __hash__ 为 None 3 分；补 __hash__ 且契约一致 2 分。

**T2-14**（5 分）
> 坏味道①：`except Exception: pass` 吞异常——故障被捂住，调用方拿到半成品，排错靠猜；② `finally` 里 `return "ok"` 吞掉正在传播的异常并覆盖 try 的返回值（反面教材）。
> 改正：except 里记录并重新抛出/转换（`raise RuntimeError("配置解析失败") from e` 保留因果链）；finally 只做清理不 return。
> 得分点：指出吞异常 1.5 分；指出 finally return 吞异常/覆盖返回值 1.5 分；改正（记录+raise from + finally 不 return）2 分。

**T2-15**（5 分）
> 病因：`(x for x in range(3))` 是生成器（迭代器），遍历消耗其内部状态、取完即废，第二次 `list()` 时已耗尽所以为空；for 的每次遍历并不重置迭代器。
> 修法：①每次遍历重建生成器（`list(gen())`）或先把数据存成 list；②把类改造成"可迭代但非迭代器"（`__iter__` 每次返回新迭代器），即可反复遍历。
> 得分点：一次性/耗尽机制 3 分；两种修法 2 分。

**T2-16**（5 分）
> 错在：GIL 只保证"单条字节码"的原子性，`counter += 1` 是**读→改→写三步**，线程在中间被切走就丢更新（实测 8×10 万丢七成）；"有 GIL 所以不用锁"混淆了 GIL 的作用（它解决的是内存管理安全，不解决竞争条件）。
> 改：`with lock:`（`threading.Lock()`）包住临界区，或不共享数据改用 `queue.Queue` 传值。
> 得分点：拆解三步+丢更新 2 分；纠正 GIL 误解 1.5 分；锁/队列改法 1.5 分。

---

# 📋 错题回填指引（配合 [py-22](../17-programming/python/py-22-review-drill.md) §四 错题反向提取，M32 五步）

1. **记录错误现场**：原错误答案/报错原文一行 + 题源 PY-ID（如 `T1-9 avg_score 越算越肥 → PY-07-04`），别抄整篇。
2. **反推漏洞类型**（四选一）：编码模糊 / 干扰混淆 / 提取失败 / 理解断层。
3. **定向修补**：编码模糊 → 回源篇重做锚点；干扰混淆 → 进 py-21 消混表加对比；提取失败 → 加密 R1 自测；理解断层 → 补"为什么"因果链后费曼讲一遍。
4. **变式再测**：换角度出题（改参数/反过来问），24 小时内做。
5. **转 SRS**：错题纳入 R1→R30（第 1/2/7/15/30 天），连续两次全对才出师（[M07-R](../方法地图.md#m07-r)）。

**回填去向**：T1 错题集中在 py-02~py-08 → 对应 30 天计划 D2~D13 重排；T2 错题集中在 py-09~py-20 → 对应 D14~D27。错题本模板与判读基准（通过率 <70% 砍一半新学量）见 py-22 §四、§五，每日训练记入[进度追踪表](../templates/记忆训练进度追踪表.md)。

**月维护**：本卷出师后每月做一次混合抽查（T1/T2 各抽 4 题，60 分钟）即可维持。

## 📍 导航
> [返回 exercises/README](README.md) ｜ 配套：[py-22 复习系统](../17-programming/python/py-22-review-drill.md) ｜ [py-00 路线图](../17-programming/python/py-00-roadmap.md) ｜ [python/INDEX](../17-programming/python/INDEX.md)
