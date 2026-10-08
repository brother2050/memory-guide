# py-11 迭代器与生成器 — 记忆编码

> **📍 本章导航**：前置 → [py-07 函数](py-07-functions.md)·[py-10 魔术方法](py-10-magic-methods.md) ｜ 相关 → [py-14 标准库](py-14-stdlib.md) ｜ 方法 → [M15](../../方法地图.md#m15)·[M13](../../方法地图.md#m13) ｜ 难度 ⭐⭐ ｜ 阅读 ~12min（约 8k tokens）
>
> 本章逻辑链：py-10 给对象接上了语法的线 → 本篇解决"一批数据怎么逐个取、怎么边算边取不占内存"（`for` 的真面目 + 生成器）→ 引出 py-12"取货出错时怎么报警处置"。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 售货机两个协议 | PY-11-01~06 | 可迭代=整机可反复买，迭代器=一次性取货口 |
| 生成器按钮 yield | PY-11-07~10 | 按一次吐一个，机器只记位置不囤货 |
| 投币口与关门 | PY-11-11~13 | yield from 转发、send 投币、close 拉闸 |
| 流水线接头与选型 | PY-11-14~16 | itertools 组合器 + 何时用生成器 |

## 一、售货机两个协议（iter/next/StopIteration）
### PY-11-01 可迭代对象与迭代器 Iterable & Iterator
- **是什么**：可迭代对象（iterable）实现 `__iter__`，能被 for 反复遍历；迭代器（iterator）额外实现 `__next__`，是"一次性取货口"。
- **为什么**：痛点是"能 for"和"能 next"是两种能力，混用会踩空 → 机制是 for 要求 iterable，next() 要求 iterator，两者协议不同 → 行为是 list 可反复遍历，迭代器取完即止 → 边界是迭代器也是可迭代对象（`__iter__` 返回自身），反之不成立。
- **怎么写**：
  ```python
  shelf = ["可乐", "薯片", "水"]     # 可迭代对象：能反复供货
  print(hasattr(shelf, "__iter__"))
  it = iter(shelf)                  # 迭代器：一次性取货口
  print(hasattr(it, "__next__"), next(it), next(it))
  print(it is iter(it))             # 迭代器的 iter() 返回自己
  ```
  → 运行输出：`True` ｜ `True 可乐 薯片` ｜ `True`
- **何时用/不用**：写框架代码要分清"接受 iterable 还是 iterator"；日常 for 循环只管用 iterable，无需手动区分。
- **锚点**：售货机整机（可反复来买）vs 机身上的取货口（一次取一件，取完就空）。
- **易错**：把 list 直接当迭代器用 `next(list)` 报 `TypeError: 'list' object is not an iterator`；迭代器也是可迭代对象，容易被误当"可反复用"（见 PY-11-06）。
- **关联**：`→ PY-11-02：iter() 负责把可迭代变成迭代器` / `→ PY-10-01：这是协议观的完整实例`
### PY-11-02 iter() 两种用法
- **是什么**：`iter(obj)` 把可迭代对象变成迭代器；`iter(可调用, 哨兵)` 反复调用函数直到返回哨兵值。
- **为什么**：痛点是"取货口从哪来"和"按函数供货到哪停"两件事 → 机制是单参版找 `__iter__`（旧协议退回 `__getitem__`），双参版每次调用取值、命中哨兵即 StopIteration → 行为是文件逐行读、输入流取值等都能统一成迭代 → 边界是双参版必须传可调用对象，且哨兵比较用 `==`。
- **怎么写**：
  ```python
  data = iter("AB")                 # 字符串也实现了迭代协议
  print(next(data), next(data))
  supply = ["苹果汁", "可乐", "STOP", "薯片"]
  fetch = lambda: supply.pop(0)     # 可调用对象当取货函数
  for item in iter(fetch, "STOP"): print(item, end=" ")   # 取到哨兵就停
  print()
  ```
  → 运行输出：`A B` ｜ `苹果汁 可乐`
- **何时用/不用**：流式数据"读到某个值为止"就用双参版（如 `iter(lambda: f.readline(), '')`）；普通容器遍历用单参版即可。
- **锚点**：开取货口——单参版是给售货机开口子；双参版是雇个供货员一直送，送来"STOP"牌子就辞退。
- **易错**：双参版忘写哨兵会无限调用；`iter("STOP")` 这种把哨兵写成可迭代对象的字符串比较，容易与逐字符取值混淆。
- **关联**：`→ PY-11-03：next() 是取货动作本身`
### PY-11-03 next() 与 StopIteration
- **是什么**：`next(it)` 取下一个值；取完抛 `StopIteration`，传第二个参数可给默认值（不抛异常）。
- **为什么**：痛点是"取完了"必须有明确信号，None 会和正常值混淆 → 机制是迭代器耗尽抛 StopIteration，for 靠它收尾 → 行为是逐个取值有终止语义 → 边界是生成器内未捕获的 StopIteration 会被转成 RuntimeError（PEP 479，3.5+）。
- **怎么写**：
  ```python
  it = iter(["可乐"])
  print(next(it))
  try: next(it)                     # 货道空了 → 抛 StopIteration
  except StopIteration as e: print("StopIteration:", repr(e))
  print(next(it, "默认值"))         # 给了默认值就不抛异常
  ```
  → 运行输出：`可乐` ｜ `StopIteration: StopIteration()` ｜ `默认值`
- **何时用/不用**：手动控制取值节奏（如批量取 N 个）时用 next；常规遍历交给 for，不要手工捕获 StopIteration。
- **锚点**：按一次按钮取一件货；货道空了亮"售罄"灯（StopIteration）。
- **易错**：`next(it, 默认值)` 掩盖了耗尽信号，循环里用它容易死循环；在生成器函数里手动 `raise StopIteration` 会变成 RuntimeError，应改用 `return`。
- **关联**：`→ PY-11-04：for 就是自动 next + 捕获 StopIteration`
### PY-11-04 for 循环的真面目
- **是什么**：`for x in obj` 是语法糖：`iter(obj)` 得迭代器 → 反复 `next()` → 捕获 `StopIteration` 结束。
- **为什么**：痛点是"为什么我的对象进不了 for"→ 机制是 for 只认迭代协议，等价展开后一切对象同权 → 行为是自定义类实现协议即入 for → 边界是循环体内 `return`/`break`/异常会中断 next 链，迭代器停在原地。
- **怎么写**：
  ```python
  it = iter(["可乐", "薯片"])       # for 第一步：iter()
  while True:
      try: x = next(it)             # 第二步：反复 next
      except StopIteration: break   # 第三步：喊停即结束
      print(x, end=" ")
  print()
  ```
  → 运行输出：`可乐 薯片`
- **何时用/不用**：理解/调试迭代问题时手动展开；日常写 for 即可，不必展开写。
- **锚点**：自动连按按钮——for 是一台自动手指，按到"售罄"灯亮才停。
- **易错**：迭代器中途被消耗（如两个 for 共用一个迭代器），第二个 for 从剩余处继续甚至直接为空；for 体内再对同一迭代器做 list() 会把它抽干。
- **关联**：`→ PY-10-09：只实现 __getitem__ 的旧式迭代也能进 for`
### PY-11-05 自定义迭代器类
- **是什么**：实现 `__iter__`（返回 self）与 `__next__`（返回值或抛 StopIteration）的类，就是手写迭代器。
- **为什么**：痛点是"按自己的规则逐个产出"（分页、游标）→ 机制是协议两方法即被 for/list/解包接受 → 行为是位置状态存在实例里 → 边界是状态存实例意味着同一对象不能并发遍历。
- **怎么写**：
  ```python
  class VendingShelf:               # 售货机货道
      def __init__(self, items): self.items, self.i = items, 0
      def __iter__(self): return self
      def __next__(self):
          if self.i >= len(self.items): raise StopIteration   # 售罄
          self.i += 1
          return self.items[self.i - 1]
  for x in VendingShelf(["可乐", "薯片", "水"]): print(x, end=" ")
  print()
  ```
  → 运行输出：`可乐 薯片 水`
- **何时用/不用**：需要"可恢复的复杂游标"时手写类；一般产出序列用生成器函数（PY-11-07）代码量减半。
- **锚点**：货道记着"出到第几件"——出货指针就是实例里的 self.i。
- **易错**：`__next__` 忘记移动指针会永远吐同一个值；忘记抛 StopIteration，for 永远停不下来。
- **关联**：`→ PY-11-07：生成器是同功能的懒人写法` / `→ PY-10-18 的迭代门牌见 PY-11-01`
### PY-11-06 可迭代 ≠ 迭代器（耗尽与复用）
- **是什么**：可迭代对象可以反复开新迭代器；迭代器是一次性通道，遍历完即废。
- **为什么**：痛点是"第二遍 for 是空的"这类诡异 bug → 机制是遍历消耗的是迭代器状态，可迭代容器本体不动 → 行为是 list/传送带可复用，货道式迭代器不能 → 边界是把迭代器存起来多次使用 = 只有第一遍有货。
- **怎么写**：
  ```python
  class VendingShelf:               # 自己记位置：可迭代，也是迭代器
      def __init__(self, items): self.items, self.i = items, 0
      def __iter__(self): return self
      def __next__(self):
          if self.i >= len(self.items): raise StopIteration
          self.i += 1; return self.items[self.i - 1]
  class Belt:                       # 传送带：只是可迭代，每次给新迭代器
      def __init__(self, items): self.items = items
      def __iter__(self): return iter(self.items)
  shelf, belt = VendingShelf(["可乐", "薯片"]), Belt(["可乐", "薯片"])
  print(list(shelf), list(shelf))   # 耗尽后第二遍是空的
  print(list(belt), list(belt))     # 传送带可反复遍历
  ```
  → 运行输出：`['可乐', '薯片'] []` ｜ `['可乐', '薯片'] ['可乐', '薯片']`
- **何时用/不用**：要被多处遍历的对象，实现"可迭代但非迭代器"（`__iter__` 每次返回新迭代器）；只想用一次的流式数据才做真迭代器。
- **锚点**：传送带（可反复过货）vs 一罐喝完的可乐（一次性）。
- **易错**：类同时实现两协议又想复用，是设计矛盾；`it = iter(obj)` 后再 `iter(obj)`，两者互相独立，别混用。
- **关联**：`→ PY-11-05：自记位置的迭代器天然一次性`

## 二、生成器按钮 yield（函数/表达式/惰性）
### PY-11-07 生成器函数 Generator Function
- **是什么**：含 `yield` 的函数调用后返回生成器（generator）：函数体不执行，每 next 一次执行到下一个 yield。
- **为什么**：痛点是手写迭代器类太啰嗦 → 机制是 yield 让函数"暂停-恢复"，自动生成 `__iter__`/`__next__` → 行为是几行代码造一个迭代器 → 边界是生成器函数调用不执行函数体，想跑第一行必须先 next/send。
- **怎么写**：
  ```python
  def vending(items):
      for x in items:
          yield x                   # 按一次按钮，吐一个商品
  g = vending(["可乐", "薯片"])
  print(type(g).__name__, next(g), next(g))
  print(list(vending(["水"])))      # 也可交给 list 一次性取空
  ```
  → 运行输出：`generator 可乐 薯片` ｜ `['水']`
- **何时用/不用**：按需产出序列、数据管道用生成器；需要随机访问/多次遍历就用 list。
- **锚点**：自动售货机的按钮——每按一次 `yield` 吐一个商品（与 17-prog-syntax-01 的 yield 售货机意象一致）。
- **易错**：调用生成器函数以为执行了函数体（其实什么都没跑）；在生成器里用 `return 值` 会把值放进 StopIteration.value，for 里看不见。
- **关联**：`→ PY-11-05：生成器=懒人版迭代器类` / `→ PY-10-12：contextmanager 用生成器实现 with`
### PY-11-08 生成器的挂起与状态
- **是什么**：yield 挂起时，局部变量、指令位置全部冻结在原地，下次 next 从断点继续。
- **为什么**：痛点是"递推/状态机"要手动存中间态 → 机制是生成器帧（frame）挂起而非销毁 → 行为是写循环像写同步代码一样自然 → 边界是生成器不能被 pickle（默认）、不能并发恢复同一实例。
- **怎么写**：
  ```python
  def counter():
      n = 0
      while True:
          n += 1
          yield n                   # 挂起：局部变量 n 原封不动留在现场
  g = counter()
  print(next(g), next(g), next(g))
  print(g is iter(g))               # 生成器天然是迭代器
  ```
  → 运行输出：`1 2 3` ｜ `True`
- **何时用/不用**：写递推序列（斐波那契、滑动窗口）时用挂起省掉手写状态机；无状态的一次性变换直接用普通函数。
- **锚点**：售货机断电记忆——货道出到第几件（局部变量 n）来电后原样接着出。
- **易错**：两个 next 之间修改了外部共享状态，重入时行为诡异；生成器耗尽后再 next 永远抛 StopIteration，不会重新执行。
- **关联**：`→ PY-11-07：yield 的暂停/恢复机制`
### PY-11-09 生成器表达式 Generator Expression
- **是什么**：`(表达式 for x in ... if ...)` 是生成器表达式（genexp），小括号版"推导式"，产出惰性生成器。
- **为什么**：痛点是只为一次遍历就建整个列表太费内存 → 机制是小括号生成器、方括号列表、大括号集合/字典，语法同源 → 行为是可直接传给 sum/list/for 等消费方 → 边界是生成器只能遍历一次，且没有列表的索引/切片。
- **怎么写**：
  ```python
  sq = (x * x for x in range(5))         # 小括号=生成器表达式
  print(type(sq).__name__, next(sq), next(sq))
  print(list(sq))                        # 剩下的接着取
  print(sum(x * x for x in range(4)))    # 传参时可省外层括号
  ```
  → 运行输出：`generator 0 1` ｜ `[4, 9, 16]` ｜ `14`
- **何时用/不用**：数据只过一道、体量大时用 genexp；要多次使用/索引切片就用列表推导式。
- **锚点**：出货小票——小括号（小票）上只印配方，货照配方现做现吐。
- **易错**：`sum(x for x in ...)` 能跑，但单参函数外只有一个生成器表达式时括号可省，两个及以上必须加括号（如 `print((x for x in y), (a for a in b))`）；先 `list()` 再遍历两次会第二次为空。
- **关联**：`→ PY-11-10：genexp 的卖点就是惰性` / `→ PY-04（见容器篇）：推导式家族的惰性成员`
### PY-11-10 惰性求值与省内存
- **是什么**：惰性求值（lazy evaluation）指值在被索取时才计算；生成器只存"配方+位置"，不存全部数据。
- **为什么**：痛点是百万级数据 `list()` 直接把内存打爆 → 机制是生成器按需产出一个丢一个（消费者负责丢）→ 行为是内存占用与数据量无关 → 边界是需要聚合（如排序、切片）时仍要落地成列表。
- **怎么写**：
  ```python
  import sys
  lazy = (x for x in range(100000))   # 只存公式
  eager = list(range(100000))         # 10 万个数全装下
  print(sys.getsizeof(lazy), "字节 vs", sys.getsizeof(eager), "字节")
  ```
  → 运行输出：`192 字节 vs 800056 字节`
- **何时用/不用**：大文件逐行、大范围扫描用惰性；数据量小且要复用，直接列表更简单。
- **锚点**：售货机不囤货——仓库里零库存，按配方现做（lazy），对比把 10 万瓶全堆进店里（eager）。
- **易错**：生成器被多个消费者各遍历一次，第二次为空；`sorted(gen)` 会隐式落地为列表，省内存效果失效。
- **关联**：`→ PY-11-09：表达式版惰性` / `→ PY-19（见内存篇）：生成器是省内存头号手段`

## 三、投币口与关门（yield from/send/close）
### PY-11-11 yield from 委托产出
- **是什么**：`yield from 可迭代对象` 把子生成器/可迭代的值逐个转发给外层调用方，并透传 send/throw/close。
- **为什么**：痛点是生成器里套循环逐个 yield 太啰嗦，且嵌套生成器的双向通信会断 → 机制是 `yield from` 建立委托通道，值与异常双向直达子生成器 → 行为是生成器可以组合复用 → 边界是它会耗尽子迭代器，子生成器的返回值可从 `yield from` 表达式拿到。
- **怎么写**：
  ```python
  def belt_a():
      yield from ["可乐", "薯片"]     # 逐个转发子可迭代对象
  def belt_b():
      yield from ["水"]
      yield from belt_a()             # 也能转发另一个生成器
  print(list(belt_b()))
  ```
  → 运行输出：`['水', '可乐', '薯片']`
- **何时用/不用**：组合多个子生成器时用；只转发一个简单循环时 `for ... yield` 也行，但会丢失双向通信。
- **锚点**：传送带接传送带——前一条线的货逐件滑进后一条线，不断流。
- **易错**：`yield from` 后面跟了非可迭代对象直接 TypeError；以为它并行跑两个生成器，其实是顺序耗尽。
- **关联**：`→ PY-11-12：yield from 透传 send/throw`
### PY-11-12 send() 双向通信
- **是什么**：`gen.send(v)` 像 next() 一样恢复生成器，但把 v 作为 `yield 表达式` 的返回值送进去。
- **为什么**：痛点是消费者要给生产者回传数据（协程雏形）→ 机制是 yield 既是产出也是接收点，send 的值赋给 yield 左侧变量 → 行为是双向管道 → 边界是首次必须用 `next()`（或 `send(None)`）启动，直接 send 非 None 会报错。
- **怎么写**：
  ```python
  def vending():
      got = yield "出货口就绪"        # 第一次必须先 next() 启动
      while True:
          got = yield f"吐出：{got}"  # send 的值赋给 got
  g = vending()
  print(next(g))                      # 启动到第一个 yield
  print(g.send("可乐"))               # 投币并恢复执行
  print(g.send("薯片"))
  ```
  → 运行输出：`出货口就绪` ｜ `吐出：可乐` ｜ `吐出：薯片`
- **何时用/不用**：需要回传通道（简单协程、管道控制）才用 send；单向产数据用 next 就够，别过度设计。
- **锚点**：投币口——机器吐货（yield）的同时能收硬币（send），投什么吐什么。
- **易错**：一上来 `g.send("x")` 报 `TypeError: can't send non-None value to a just-started generator`；在 yield 赋值语句前结束生成器，send 的值无处安放。
- **关联**：`→ PY-11-13：close 是反向的关门信号`
### PY-11-13 close() 与 GeneratorExit
- **是什么**：`gen.close()` 向生成器内注入 `GeneratorExit` 异常使其收尾关闭；关闭后再 next 抛 StopIteration。
- **为什么**：痛点是生成器持有资源（文件、锁）中途弃用会泄漏 → 机制是 close 触发挂起点抛 GeneratorExit，生成器可捕获清理（但不能继续 yield）→ 行为是显式关停有保障 → 边界是捕获 GeneratorExit 后仍 yield 会触发 RuntimeError。
- **怎么写**：
  ```python
  def vending():
      try:
          yield "可乐"
          yield "薯片"
      except GeneratorExit:
          print("机器关门，停止出货")   # close() 注入 GeneratorExit
  g = vending()
  print(next(g))
  g.close()
  try: next(g)
  except StopIteration: print("StopIteration：已关闭")
  ```
  → 运行输出：`可乐` ｜ `机器关门，停止出货` ｜ `StopIteration：已关闭`
- **何时用/不用**：手动管理生成器生命周期时才调 close；for 循环中途 break 后由垃圾回收兜底，确定性收尾靠 with/contextlib。
- **锚点**：拉闸关门——卷帘门落下（GeneratorExit），机器停止出货。
- **易错**：在 except GeneratorExit 里 `yield` 会 RuntimeError；close 只在挂起点生效，生成器没跑到 yield 就 close，函数体根本没执行过。
- **关联**：`→ PY-11-12：send/throw/close 是同一组控制阀` / `→ PY-10-12：需要确定性收尾首选 with`

## 四、流水线接头与选型（itertools/惰性管道）
### PY-11-14 itertools 组合器（一）count/chain/accumulate
- **是什么**：itertools 模块提供惰性迭代"流水线接头"：`count` 无限计数、`chain` 串联多序列、`accumulate` 前缀累加。
- **为什么**：痛点是循环套循环、手写累加器代码碎 → 机制是每个工具都是惰性生成器，可任意串联 → 行为是流水线声明式组合 → 边界是 `count`/`cycle` 无限，必须配 `islice` 等截断。
- **怎么写**：
  ```python
  import itertools
  print(list(itertools.islice(itertools.count(1), 3)))   # count 无限，需 islice 截断
  print(list(itertools.chain(["可乐"], ["薯片", "水"])))
  print(list(itertools.accumulate([1, 2, 3, 4])))        # 累计：1, 3, 6, 10
  ```
  → 运行输出：`[1, 2, 3]` ｜ `['可乐', '薯片', '水']` ｜ `[1, 3, 6, 10]`
- **何时用/不用**：多序列串联/无限序列/滚动累加直接用；单层简单循环用 for 更直白，不必引入 itertools。
- **锚点**：流水线接头——count 是无限转盘、chain 是两段传送带对接、accumulate 是沿途累加的秤。
- **易错**：`list(itertools.count(1))` 直接跑飞（无限）；chain 的参数是多个可迭代对象，忘了解包 `*` 会把整个列表当一个序列。
- **关联**：`→ PY-11-15：更多接头` / `→ PY-14（见标准库篇）：itertools 全家桶`
### PY-11-15 itertools 组合器（二）takewhile/groupby/cycle
- **是什么**：`takewhile` 条件一破即停、`groupby` 按连续相同键分组、`cycle` 无限循环供货。
- **为什么**：痛点是"取到条件不满足为止/按段分组/循环轮播"手写又长又易错 → 机制是三者都返回惰性迭代器 → 行为是分段处理数据像流水线分拣 → 边界是 groupby 要求数据已按同一键排序，否则同键被拆成多组。
- **怎么写**：
  ```python
  import itertools
  print(list(itertools.takewhile(lambda x: x < 3, [1, 2, 3, 1])))   # 条件一破就停
  print([(k, list(g)) for k, g in itertools.groupby("AABB")])      # 按连续段分组
  print(list(itertools.islice(itertools.cycle("AB"), 5)))           # 循环供货
  ```
  → 运行输出：`[1, 2]` ｜ `[('A', ['A', 'A']), ('B', ['B', 'B'])]` ｜ `['A', 'B', 'A', 'B', 'A']`
- **何时用/不用**：按段/按条件截流的数据处理用它们；简单过滤用生成器表达式的 if 即可，别为一行过滤引入 takewhile。
- **锚点**：质检闸（takewhile 不合格即全线停）、分拣员（groupby 把同类货并一堆）、循环转盘（cycle 转圈供货）。
- **易错**：groupby 的分组对象是一次性迭代器，出循环后再用为空；cycle 无限，忘配 islice 跑飞。
- **关联**：`→ PY-11-14：itertools 基础接头`
### PY-11-16 惰性管道与选型（生成器 vs 列表）
- **是什么**：把多个生成器首尾相接组成惰性管道（pipeline）：每一步按需从上游取一个值加工后传下游，全程不落地。
- **为什么**：痛点是"读取→变换→筛选→聚合"每步都建列表，内存和耗时双爆 → 机制是生成器之间只传单个值，只有最终消费（如 list/sum）才聚合 → 行为是处理超大文件内存恒定 → 边界是需要多次遍历、随机访问、排序时必须落地。
- **怎么写**：
  ```python
  def double(belt):
      for x in belt: yield x * 2
  def pick(belt):
      for x in belt:
          if x % 3 == 0: yield x
  print(list(pick(double(range(10)))))   # 每环节不落地，消费时才逐个出货
  ```
  → 运行输出：`[0, 6, 12, 18]`
- **何时用/不用**：大数据流/文件逐行处理选生成器管道；要索引、切片、二次遍历或 len() 选列表（选型表见对比消混表）。
- **锚点**：传送带加工线——货件在带上边走边加工（double→pick），只有装箱（list）那一刻才落地。
- **易错**：管道里混入 `sorted()/list()` 等落地操作，惰性白做；忘了最终消费者，生成器根本没执行（什么都没发生）。
- **关联**：`→ PY-11-10：管道的收益就是惰性` / `→ PY-11-09：genexp 是最短的一节管道`

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| 可迭代 vs 迭代器 | iterable 有 `__iter__` | iterator 加 `__next__` | 能否 next()；迭代器可反复用吗 | 整机可反复、取货口一次 |
| 生成器函数 vs 生成器表达式 | `yield` 定义多行流程 | 小括号一行配方 | 逻辑复杂用函数、简单变换用表达式 | 复杂流程简单式 |
| yield vs return | 挂起后可恢复 | 终结函数 | 会不会继续产出 | yield 暂停 return 完 |
| next vs send | 只取值 | 取值并回传 | 要不要送东西进生成器 | next 取货 send 投币 |
| 生成器 vs 列表 | 惰性一次性 | 全量可复用 | 要不要二次遍历/索引 | 大流用生成器、复用用列表 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-11-01 | 可迭代对象/迭代器 | 售货机整机 vs 取货口 | 整机与取货口 |
| PY-11-02 | iter() | 开取货口/供货员送"STOP" | 开取货口 |
| PY-11-03 | next()/StopIteration | 按钮取货/售罄灯 | 售罄灯 |
| PY-11-04 | for 真面目 | 自动手指连按按钮 | 自动手指 |
| PY-11-05 | 自定义迭代器类 | 货道出货指针 | 出货指针 |
| PY-11-06 | 可迭代≠迭代器 | 传送带 vs 喝完的可乐 | 传送带可复用 |
| PY-11-07 | 生成器函数 yield | 售货机按钮吐货 | 售货机按钮 |
| PY-11-08 | 挂起与状态 | 断电记忆货道位置 | 断电记忆 |
| PY-11-09 | 生成器表达式 | 出货小票（小括号） | 出货小票 |
| PY-11-10 | 惰性求值 | 不囤货现做 vs 堆满店 | 不囤货 |
| PY-11-11 | yield from | 传送带接传送带 | 接传送带 |
| PY-11-12 | send() | 投币口投币 | 投币口 |
| PY-11-13 | close()/GeneratorExit | 拉闸关门 | 拉闸 |
| PY-11-14 | count/chain/accumulate | 流水线接头（转盘/对接/累加秤） | 流水线接头 |
| PY-11-15 | takewhile/groupby/cycle | 质检闸/分拣员/循环转盘 | 质检闸分拣员 |
| PY-11-16 | 惰性管道 | 传送带加工线 | 加工线 |

## ✅ 自测清单（合上本篇，先写再看）
1. （说区别）`iter([1,2])` 和 `iter(iter([1,2]))` 各得到什么？为什么 `list(it)` 只能来一遍？
   > 答案：前者是新列表迭代器，后者是同一迭代器（迭代器的 iter 返回自身）；迭代器耗尽即废（PY-11-06）。
2. （写代码）把 `for x in range(5): if x % 2: y = x * 10; print(y)` 改写成生成器表达式并打印所有结果。
   > 答案：`print(list(x * 10 for x in range(5) if x % 2))` → `[10, 30]`。
3. （改错）`def f(): yield 1; raise StopIteration` 在 for 里用会怎样？
   > 答案：生成器内逸出的 StopIteration 被转成 RuntimeError（PEP 479），应写 `return`。
4. （说机制）`g.send("x")` 报 `can't send non-None value to a just-started generator`，为什么？
   > 答案：生成器还没启动到 yield，必须先 `next(g)`（或 `g.send(None)`）启动（PY-11-12）。
5. （写代码）不落地内存，统计一个 100 万行文件里含 "ERROR" 的行数，写出核心一行。
   > 答案：`n = sum(1 for line in open(f) if "ERROR" in line)`，全程惰性不建列表。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-10 魔术方法](py-10-magic-methods.md) ｜ ➡️ 下一篇：[py-12 异常处理](py-12-exceptions.md)
