# py-10 魔术方法与运算符重载 — 记忆编码

> **📍 本章导航**：前置 → [py-09 面向对象](py-09-oop.md) ｜ 相关 → [py-11 迭代与生成器](py-11-iterators-generators.md)·[py-12 异常](py-12-exceptions.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~12min（约 8k tokens）
>
> 本章逻辑链：py-09 的对象只会用自己的普通方法 → 本篇解决"对象怎么接进 `+`、`len()`、`with` 这些语言原生动作" → 引出 py-11 的头号协议：`for` 背后的迭代器。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 协议即遥控器按键排布 | PY-10-01 | 语法糖背后全是双下划线方法 |
| 两张面孔＋长度真值 | PY-10-02~05 | repr 给程序员、str 给观众、len 数格子、bool 判开演 |
| 比较哈希裁判组 | PY-10-06~08 | eq 判等、lt 比序、hash 定键位 |
| 下标与按钮幕布 | PY-10-09~12 | getitem 取、setitem 写删、call、enter/exit |
| 运算符重载三连 | PY-10-13~15 | add 正向、radd 反向、iadd 原地 |
| 描述符与 property 真身 | PY-10-16~19 | 三键装机、包厢特权、语音键真身、代客挂衣 |

## 一、协议即遥控器按键排布（总纲）
### PY-10-01 魔术方法与协议 Magic Method & Protocol
- **是什么**：魔术方法（magic method，双下划线方法/dunder）是 Python 预留的接线口；一组接线口的约定叫协议（protocol）。
- **为什么**：痛点是自定义对象接不进 `len()`、`+`、`for` 等原生语法 → 机制是解释器把 `len(x)` 翻译成 `x.__len__()`、`a + b` 翻译成 `a.__add__(b)` → 行为是实现约定方法即融入语法 → 边界是方法名写错（如 `__len`）不报错，只是静默失效。
- **怎么写**：
  ```python
  class Balance:
      def __init__(self, w): self.w = w
      def __add__(self, other): return Balance(self.w + other.w)   # 接线口
  a, b = Balance(2), Balance(3)
  print((a + b).w, a.__add__(b).w)    # + 号与直调完全等价
  ```
  → 运行输出：`5 5`
- **何时用/不用**：想让对象"像内置类型一样被语法操作"时用；只做内部功能就写普通方法，不必碰魔术方法。
- **锚点**：万能遥控器——按键排布（协议）是行业约定，同一套按键能开任何牌子的电视；对象=电视，魔术方法=机身背后的接线口。
- **易错**：双下划线两边都要有（`__len__` 不是 `_len_`）；手调只是等价写法，正常应让语法自动触发。
- **关联**：`→ PY-10-02~15：本篇把常用接线口逐个插上` / `→ PY-11-01：迭代协议是协议观的第一个完整实例`

## 二、两张面孔＋长度真值（repr/str/len/bool）
### PY-10-02 __repr__ 开发者视角字符串
- **是什么**：`__repr__`（representation）返回给开发者看的字符串，目标是"照着能重新造出这个对象"。
- **为什么**：痛点是 print 一个对象只见内存地址没法调试 → 机制是容器、交互式解释器、repr() 一律调 `__repr__` 拼装 → 行为是调试信息清晰可复现 → 边界是别在里面做耗时计算，它可能被频繁触发。
- **怎么写**：
  ```python
  class Program:
      def __init__(self, name, minute): self.name, self.minute = name, minute
      def __repr__(self): return f"Program({self.name!r}, {self.minute})"
  p = Program("新闻联播", 30)
  print(repr(p)); print(p, [p])   # 无 __str__ 时回落 repr；容器内部统一用 repr
  ```
  → 运行输出：`Program('新闻联播', 30)` ｜ `Program('新闻联播', 30) [Program('新闻联播', 30)]`
- **何时用/不用**：自定义类几乎必写（调试刚需）；只想给用户看一句话时另写 `__str__`，别用 repr 凑合。
- **锚点**：舞台后台的节目单——工作人员照着它能把整台节目原样重排（可复现）。
- **易错**：忘了 `!r` 会丢失引号层次，字符串/数字分不清；只写 `__str__` 不写 `__repr__`，列表里的元素仍是内存地址。
- **关联**：`→ PY-10-03：str 缺席时回落到 repr`
### PY-10-03 __str__ 用户视角字符串
- **是什么**：`__str__` 返回给最终用户看的字符串，供 `print()`、f-string、`str()` 调用。
- **为什么**：痛点是同一对象"精确调试格式"与"友好展示格式"不能混 → 机制是 print/f-string 走 `__str__`，缺了才回落 `__repr__` → 行为是两张面孔各司其职 → 边界是 `%r`、`{x!r}`、日志 repr 仍强制走 repr。
- **怎么写**：
  ```python
  class Program:
      def __init__(self, name, minute): self.name, self.minute = name, minute
      def __repr__(self): return f"Program({self.name!r}, {self.minute})"
      def __str__(self): return f"{self.name}（{self.minute}分钟）"   # 观众看的预告牌
  p = Program("新闻联播", 30)
  print(p); print(str(p), "|", repr(p))   # print → str
  ```
  → 运行输出：`新闻联播（30分钟）` ｜ `新闻联播（30分钟） | Program('新闻联播', 30)`
- **何时用/不用**：对象要打印给人看就写；仅内部调试的类只写 repr 即可。
- **锚点**：舞台前方的预告牌——观众抬头看的大字（友好），与后台节目单（精确）一前一后。
- **易错**：`print(f"{p!r}")` 和日志 `%r` 会绕过 str 直奔 repr，别以为 str 覆盖了一切。
- **关联**：`→ PY-10-02：两者的调用链与回落关系`
### PY-10-04 __len__ 元素个数
- **是什么**：`__len__` 让 `len(obj)` 生效，返回对象的元素个数。
- **为什么**：痛点是自定义容器在 `len()` 面前哑火 → 机制是 `len(x)` 等价 `x.__len__()` → 行为是容器获得长度能力 → 边界是必须返回非负 int，负数触发 `ValueError: __len__() should return >= 0`。
- **怎么写**：
  ```python
  class Channels:
      def __init__(self, names): self.names = names
      def __len__(self): return len(self.names)   # 频道数量

  print(len(Channels(["CCTV1", "湖南", "东方"])))   # len() 触发 __len__
  ```
  → 运行输出：`3`
- **何时用/不用**：对象是"一批东西"就写；单值对象（坐标点）别硬套 len，语义不成立。
- **锚点**：数遥控器上的频道——按住"频道＋"要按几次才数得完，就是 len。
- **易错**：`__len__` 返回 0 会让对象在 `if obj:` 里变假（见 PY-10-05 的回落规则），不是"没定义"那么简单。
- **关联**：`→ PY-10-05：bool 缺席时由 len 接管真值`
### PY-10-05 __bool__ 真值测试
- **是什么**：`__bool__` 定义对象在 `if`、`and`、`not` 中的真假。
- **为什么**：痛点是"有效/无效"的判断不该只看长度 → 机制是真值测试先找 `__bool__`，没有才回落 `__len__`（0 为假），再没有一律为真 → 行为是可自定义"开演=真、空台=假" → 边界是必须返回 bool，返回其他类型会 TypeError。
- **怎么写**：
  ```python
  class Stage:
      def __init__(self, ps): self.ps = ps
      def __bool__(self): return len(self.ps) > 0     # 有节目=开演
  class Channels:                 # 无 __bool__ 时回落 __len__：len()==0 → 假
      def __init__(self, n): self.n = n
      def __len__(self): return self.n
  print(bool(Stage(["春晚"])), bool(Stage([])))
  print(bool(Channels(0)), bool(Channels(2)))
  ```
  → 运行输出：`True False` ｜ `False True`
- **何时用/不用**：对象有"有效/无效"语义就写；只按个数定真假靠 len 回落即可，不必重复实现。
- **锚点**：舞台开演灯——亮着就算开演（真），灭了就是空台（假）。
- **易错**：`__bool__` 忘记 return 会返回 None → TypeError；只想空容器为假，直接靠 `__len__` 更省事。
- **关联**：`→ PY-10-04：真值回落链 __bool__ → __len__ → 恒真`

## 三、比较哈希裁判组（eq/lt/hash）
### PY-10-06 __eq__ 相等判定
- **是什么**：`__eq__` 定义 `==` 的比较规则；未定义时 `==` 退化为 `is`（同一对象）。
- **为什么**：痛点是两个内容相同的对象 `==` 却是 False → 机制是 `a == b` 先试 `a.__eq__(b)`，返回 NotImplemented 再试 `b.__eq__(a)` → 行为是可按业务字段判等 → 边界是自定义 `__eq__` 会连带改变 dict/set 行为（见 hash）。
- **怎么写**：
  ```python
  class Channel:
      def __init__(self, no): self.no = no
      def __eq__(self, other):
          return isinstance(other, Channel) and self.no == other.no   # 按台号判等
  c1, c2, c3 = Channel(7), Channel(7), Channel(8)
  print(c1 == c2, c1 == c3, c1 != c3, c1 == "CCTV7")
  ```
  → 运行输出：`True False True False`
- **何时用/不用**：对象有"值相等"语义（金额、台号）就写；单例/资源句柄保持默认身份比较更安全。
- **锚点**：两台电视调到同一频道号——画面一样就算"同台"（值相等），不必是同一台机器。
- **易错**：比较时漏写 isinstance 会让 `c1 == "任意字符串"` 悄悄返回 True；py3 的 `!=` 自动取反 `__eq__`，但 numpy 数组等第三方类型可能返回数组而非 bool。
- **关联**：`→ PY-10-08：eq 相等则 hash 必须相等` / `→ PY-10-07：eq 是排序比较的地基`
### PY-10-07 __lt__ 与排序比较
- **是什么**：`__lt__` 定义 `<`；配合 `__eq__` 可用 `functools.total_ordering` 自动补齐 `<= > >=`。
- **为什么**：痛点是 `sorted()` 对自定义对象报 `'<' not supported` → 机制是 sorted/min/max 内部只依赖 `<` → 行为是定义一个 `<` 即可入列 → 边界是 total_ordering 生成的方法较慢，性能敏感处手写全套。
- **怎么写**：
  ```python
  import functools
  @functools.total_ordering
  class Program:
      def __init__(self, m, name): self.m, self.name = m, name
      def __eq__(self, o): return self.m == o.m
      def __lt__(self, o): return self.m < o.m      # 按时长比大小
  ps = [Program(30, "新闻"), Program(5, "天气"), Program(90, "晚会")]
  print([p.name for p in sorted(ps)], ps[1] < ps[0], ps[0] >= ps[1])
  ```
  → 运行输出：`['天气', '新闻', '晚会'] True True`
- **何时用/不用**：对象要进 sorted/min/max/堆就写；只需判等就停在 `__eq__`，别顺手全重写。
- **锚点**：按频道号排队——号小的排前面，`<` 就是比号大小。
- **易错**：只定义 `__gt__` 不定义 `__lt__` 会让 sorted 失败；`__eq__` 与 `__lt__` 比较字段必须一致，否则排序自相矛盾。
- **关联**：`→ PY-10-06：total_ordering 需要 eq 配合`
### PY-10-08 __hash__ 与哈希键
- **是什么**：`__hash__` 返回整数哈希值，决定对象能否当 dict 键/set 元素，并决定落到哪个桶。
- **为什么**：痛点是自定义对象当字典键报 `unhashable type` → 机制是 dict/set 先比 hash 定桶、再用 `__eq__` 确认 → 行为是"eq 相等的两对象必须 hash 相等"→ 边界是类中定义 `__eq__` 而不定义 `__hash__` 时，Python 自动把 `__hash__` 置 None（可变对象借此自我保护）。
- **怎么写**：
  ```python
  class Channel:
      def __init__(self, no): self.no = no
      def __eq__(self, o): return isinstance(o, Channel) and self.no == o.no
      def __hash__(self): return hash(self.no)   # eq 相等 → hash 必须相等
  print({Channel(7): "CCTV7"}[Channel(7)], hash(Channel(7)) == hash(Channel(7)))
  class NoHash:
      def __eq__(self, o): return True           # 有 eq 无 hash → 自动置 None
  try: hash(NoHash())
  except TypeError as e: print("TypeError:", e)
  ```
  → 运行输出：`CCTV7 True` ｜ `TypeError: unhashable type: 'NoHash'`
- **何时用/不用**：不可变值对象（台号、坐标）做键时写；会变的字段进了 hash，字典查找会"键丢了"。
- **锚点**：遥控器按键位——hash 是按键编号定位格子，eq 是确认格子里确实是那台。
- **易错**：把列表等可变字段塞进 `hash()` 直接 TypeError；eq 相等但 hash 不同的两对象会被 dict 存成两份，查找时好时坏。
- **关联**：`→ PY-10-06：hash/eq 一致性契约`

## 四、下标与按钮幕布（getitem/setitem/call/enter-exit）
### PY-10-09 __getitem__ 下标取值
- **是什么**：`__getitem__` 让 `obj[i]`、切片 `obj[a:b]` 生效，i 会原样传入（int 或 slice 对象）。
- **为什么**：痛点是自定义容器不能用括号取元素 → 机制是 `obj[i]` 翻译成 `obj.__getitem__(i)`，切片时 i 是 slice → 行为是对象获得序列体验 → 边界是越界应抛 IndexError，这也是 for 旧式迭代停止的信号（`in` 也会依次回落 `__contains__`→`__iter__`→`__getitem__`）。
- **怎么写**：
  ```python
  class ChannelList:
      def __init__(self, names): self.names = names
      def __getitem__(self, i): return self.names[i]   # i 可能是 int 或 slice
  chs = ChannelList(["CCTV1", "湖南", "东方", "北京"])
  print(chs[0], chs[1:3], chs[-1])
  for name in chs: print(name, end=" ")   # 无 __iter__ 时 for 退回 __getitem__
  print()
  ```
  → 运行输出：`CCTV1 ['湖南', '东方'] 北京` ｜ `CCTV1 湖南 东方 北京`
- **何时用/不用**：语义是"按位置/键取东西"就写；只想被 for 遍历，实现 `__iter__` 更规范。
- **锚点**：按频道号换台——`遥控器[7]` 一下跳到 7 号台，切片就是连着扫一串台。
- **易错**：忘了处理 slice 对象，`obj[1:3]` 会把 slice 传给下标直接 TypeError；越界不抛 IndexError 而抛别的，for 会把异常当真炸出来。
- **关联**：`→ PY-10-10：写入侧的同族协议` / `→ PY-11-04：for 的旧式迭代退回机制`
### PY-10-10 __setitem__/__delitem__ 下标写删
- **是什么**：`__setitem__` 定义 `obj[k] = v`，`__delitem__` 定义 `del obj[k]`。
- **为什么**：痛点是只读的下标体验割裂（能查不能改）→ 机制是赋值/删除语法同样翻译成魔术方法调用 → 行为是查/写/删三动作齐活 → 边界是三者应共享同一套键校验，否则出现"删得掉却查不到"的裂缝。
- **怎么写**：
  ```python
  class Remote:
      def __init__(self): self.keys = {}
      def __setitem__(self, k, v): self.keys[k] = v
      def __getitem__(self, k): return self.keys[k]
      def __delitem__(self, k): del self.keys[k]
  r = Remote()
  r[1] = "CCTV1"; print(r[1]); del r[1]   # 依次调 __setitem__/__getitem__/__delitem__
  print(r.keys)
  ```
  → 运行输出：`CCTV1` ｜ `{}`
- **何时用/不用**：需要"像字典一样管理"的封装就写；只读视图只实现 `__getitem__`，改删靠公开方法显式暴露。
- **锚点**：给遥控器按键位存台/删台——按位号写入、按位号清除。
- **易错**：只写 `__getitem__` 不写 `__setitem__`，用户看到的是 `TypeError: object does not support item assignment`，完全看不出你的设计意图。
- **关联**：`→ PY-10-09：查写删三件套成套实现`
### PY-10-11 __call__ 可调用对象
- **是什么**：`__call__` 让对象像函数一样被调用：`obj()` 等价 `obj.__call__()`。
- **为什么**：痛点是"带状态的函数"（换台器、限流器）用裸函数难封装 → 机制是对象名后跟括号走 `__call__` → 行为是状态与行为打包成可调用体 → 边界是别把普通类硬改成可调用，`callable(obj)` 为真会误导调用者。
- **怎么写**：
  ```python
  class Remote:
      def __init__(self, channels): self.channels, self.i = channels, 0
      def __call__(self):        # 对象名() 直接当函数：按一下换一台
          self.i += 1
          return self.channels[self.i % len(self.channels)]
  r = Remote(["CCTV1", "湖南", "东方"])
  print(r(), r(), r(), callable(r))
  ```
  → 运行输出：`湖南 东方 CCTV1 True`
- **何时用/不用**：需要"记住状态的回调"（计数、缓存器）时用；一次性动作写普通方法 `obj.run()` 更直白。
- **锚点**：遥控器上那颗大按钮——拿整个遥控器当按钮按，一下换一台。
- **易错**：`__call__` 里递归调用 `self()` 会无限递归；装饰器类靠 `__call__` 接管函数调用，签名写错会连累被包装函数。
- **关联**：`→ PY-08（见装饰器篇）：装饰器类靠 __call__ 接管调用`
### PY-10-12 __enter__/__exit__ with 协议
- **是什么**：`__enter__`/`__exit__` 构成上下文管理器协议（context manager），驱动 `with` 语法的进入与退出。
- **为什么**：痛点是资源开了一定要关，异常路径容易漏 → 机制是 `with obj:` 先调 `__enter__`，离开代码块无论是否异常都调 `__exit__` → 行为是收尾被语法强制执行 → 边界是 `__exit__` 返回真会吞掉该异常（拦截报警要谨慎）。
- **怎么写**：
  ```python
  class Curtain:
      def __init__(self, name): self.name = name
      def __enter__(self): print(f"幕布拉开：{self.name}"); return self
      def __exit__(self, t, e, tb): print(f"幕布拉上：{self.name}，异常={t}"); return True  # 真=吞异常
  with Curtain("主舞台"):
      print("演出中")
  with Curtain("主舞台"):
      raise ValueError("道具倒塌")
  print("散场后程序继续")
  ```
  → 运行输出：`幕布拉开：主舞台` ｜ `演出中` ｜ `幕布拉上：主舞台，异常=None` ｜ `幕布拉开：主舞台` ｜ `幕布拉上：主舞台，异常=<class 'ValueError'>` ｜ `散场后程序继续`
- **何时用/不用**：有"开-用-关"结构（文件、锁、连接）就用 with；不想写这两个方法可用 `contextlib.contextmanager` 把生成器包成上下文管理器。
- **锚点**：舞台幕布——开演拉开（`__enter__`），散场必拉上（`__exit__`），哪怕台上塌了（异常）也得闭幕。
- **易错**：`__exit__` 默认返回 None（假），异常会继续传播——想吞异常必须显式 return True；吞异常会毁掉排错线索，工程上极少这么做。
- **关联**：`→ PY-12-15：异常路径下 with 仍保证收尾` / `→ PY-11-07：contextmanager 借生成器实现同一协议`

## 五、运算符重载三连（add/radd/iadd）
### PY-10-13 算术运算符重载 __add__/__mul__
- **是什么**：`__add__ __sub__ __mul__ __truediv__` 等分别对应 `+ - * /`，一符一方法。
- **为什么**：痛点是"频道表合并、金额相乘"这类语义用 `a.add(b)` 不如 `a + b` 直觉 → 机制是二元运算符优先问左操作数的对应方法 → 行为是对象获得数学运算体验 → 边界是返回类型要保持直觉，`a + b` 返回怪类型会坑用户。
- **怎么写**：
  ```python
  class ChannelList:
      def __init__(self, names): self.names = list(names)
      def __add__(self, o): return ChannelList(self.names + o.names)  # 合并频道表
      def __mul__(self, n): return ChannelList(self.names * n)        # 重复 n 轮
      def __repr__(self): return f"ChannelList({self.names})"
  print(ChannelList(["CCTV1"]) + ChannelList(["湖南", "东方"]))
  print(ChannelList(["CCTV1"]) * 2)
  ```
  → 运行输出：`ChannelList(['CCTV1', '湖南', '东方'])` ｜ `ChannelList(['CCTV1', 'CCTV1'])`
- **何时用/不用**：对象有自然的数学/组合语义才重载；业务对象硬造 `+` 会让代码更难读，写 `merge()` 更好。
- **锚点**：两张频道表叠成一张——加号就是把两张单子叠起来。
- **易错**：`__add__` 里误改 self（加法应产生新对象）；漏写 `__radd__` 时 `内置类型 + 对象` 会 TypeError（见 PY-10-14）。
- **关联**：`→ PY-10-14：左不行时转问右` / `→ PY-10-15：+= 是另一套方法`
### PY-10-14 __radd__ 反向运算
- **是什么**：`__radd__`（right）是"右操作数版"的 `__add__`，在左操作数搞不定时被调用。
- **为什么**：痛点是 `"湖南" + channel` 报错而 `channel + "湖南"` 正常 → 机制是左操作数返回 NotImplemented 或类型不支持时，Python 转问右操作数的 `__radd__` → 行为是自定义对象能与内置类型双向运算 → 边界是内置类型优先尝试自己的规则，子类想强制优先要靠更复杂的技巧。
- **怎么写**：
  ```python
  class Channel:
      def __init__(self, name): self.name = name
      def __add__(self, o): return f"{self.name}+{o}"
      def __radd__(self, o): return f"{o}+{self.name}"   # 左边不支持时转问右边
  c = Channel("CCTV7")
  print(c + "湖南")    # 调 __add__
  print("湖南" + c)    # str 不认 Channel → 调 __radd__
  ```
  → 运行输出：`CCTV7+湖南` ｜ `湖南+CCTV7`
- **何时用/不用**：运算符一侧可能来自外部类型时必须补；两侧都是自己的类时可省。
- **锚点**：客串顶替——主角（左）不认识这位演员，导演就问替补（右）能不能顶上。
- **易错**：左右都实现却结果不一致（`a+b` 与 `b+a` 拼序不同不报错，但语义打架）；漏实现时报 `TypeError: unsupported operand type(s)`，看不出缺的是 r 版方法。
- **关联**：`→ PY-10-13：正反两件套`
### PY-10-15 __iadd__ 原地运算
- **是什么**：`__iadd__`（in-place）定义 `+=`；未定义时 `a += b` 退化为 `a = a + b`。
- **为什么**：痛点是大对象 `+=` 不该复制出新对象 → 机制是 `+=` 优先调 `__iadd__`，其必须返回对象（通常是 self）→ 行为是原地修改省内存 → 边界是元组/str 等不可变类型没有 `__iadd__`，`+=` 永远产生新对象。
- **怎么写**：
  ```python
  class ChannelList:
      def __init__(self, names): self.names = list(names)
      def __iadd__(self, o): self.names.extend(o); return self   # 原地改并返回自身
  p = ChannelList(["CCTV1"]); q = p
  p += ["湖南", "东方"]          # 调 __iadd__
  print(p.names, q.names, p is q)
  class NoIadd:
      def __init__(self, v): self.v = v
      def __add__(self, o): return NoIadd(self.v + o)
  x = NoIadd(1); y = x; x += 10   # 无 __iadd__ → 退化为 x = x + 10，产生新对象
  print(x.v, y.v, x is y)
  ```
  → 运行输出：`['CCTV1', '湖南', '东方'] ['CCTV1', '湖南', '东方'] True` ｜ `11 1 False`
- **何时用/不用**：对象大且运算高频（矩阵、缓冲区）时值得实现；小对象让 `+=` 走默认新对象反而简单安全。
- **锚点**：在原节目单上续写——`+=` 是往同一张单子后面接着写，不换新单。
- **易错**：`__iadd__` 忘记 return self，变量会被赋成 None；没有 `__iadd__` 时 `x += 10` 后 x 已不是原来那个对象（上例 y 不变）。
- **关联**：`→ PY-10-13：+= 与 + 是两套方法`

## 六、描述符与 property 真身（口号：三键装机，包厢特权）

### PY-10-16 描述符协议 Descriptor Protocol（`__get__/__set__/__delete__/__set_name__`）
- **是什么**：一个类只要定义了 `__get__`、`__set__`、`__delete__` 三者中任一个，它的实例就叫描述符（descriptor）——属性访问被它接管。
- **为什么**：痛点是"属性存取想加拦截逻辑（校验/懒加载/日志）"但普通属性只有裸存取 → 机制是访问 `obj.x` 时解释器按固定流程找 `type(obj).__mro__` 里的描述符并调用 `__get__`，赋值/删除同理 → 行为是属性的"取存删"全部可编程 → 边界是描述符必须定义在**类**上，定义在实例上不生效。
- **怎么写**：
  ```python
  class Typed:
      def __set_name__(self, owner, name): self.name = name      # 装机登记
      def __get__(self, obj, owner): return None if obj is None else obj.__dict__[self.name]
      def __set__(self, obj, value):
          if not isinstance(value, int): raise TypeError(f"{self.name} 需要 int")
          obj.__dict__[self.name] = value
  class Player:
      level = Typed()                                            # 类上挂描述符
  p = Player(); p.level = 3
  try: p.level = "高"
  except TypeError as e: print("拦截:", e)
  print(p.level)
  ```
  → 运行输出：`拦截: level 需要 int`\n`3`
- **何时用/不用**：属性需要校验/懒加载/统一拦截时用；只存个值就用普通属性，别上大炮打蚊子。
- **锚点**：遥控器背后的**三键接线口**（取/存/删）+装机时登记键位（`__set_name__`）——厂家装机时把键位名字登记好，用户按的每个键都被这三个接线口接管。
- **易错**：描述符写在实例上不生效（必须在类上）；`__get__(self, obj, owner)` 里 obj 为 None 说明是类访问（`Player.level`），要妥善返回描述符自身或报错信息。
- **关联**：→ PY-10-17：三种优先级由"存/删"键是否具备决定 ｜ → PY-09-11 property 就是它 ｜ → PY-08-14 cached_property 的真身也是描述符。

### PY-10-17 数据描述符 vs 非数据描述符（属性查找优先级）
- **是什么**：同时有 `__set__`/`__delete__` 的叫数据描述符，只有 `__get__` 的叫非数据描述符；属性查找顺序：**数据描述符 > 实例字典 > 非数据描述符**。
- **为什么**：痛点是"属性有时被描述符拦截、有时又能被实例字典覆盖"搞不清 → 机制是 `obj.x` 的查找链固定：先看数据描述符，再看实例 `__dict__`，最后才轮到非数据描述符 → 行为是数据描述符能强制管住赋值，非数据描述符可被实例属性盖掉 → 边界是类属性名与实例属性名同名时永远按这条链走。
- **怎么写**：
  ```python
  class DataDesc:                                               # 有 __set__：包厢特权
      def __get__(self, obj, owner): return "数据描述符赢"
      def __set__(self, obj, value): pass
  class NonDataDesc:                                            # 只有 __get__：可被盖掉
      def __get__(self, obj, owner): return "非数据描述符赢"
  class A: x, y = DataDesc(), NonDataDesc()
  a = A(); a.__dict__["x"] = "实例字典"; a.__dict__["y"] = "实例字典"
  print(a.x, a.y)
  ```
  → 运行输出：`数据描述符赢 实例字典`
- **何时用/不用**：想让赋值必须被拦截（校验）→ 必须做成数据描述符；只是懒加载/缓存 → 非数据描述符即可（还能被实例字典缓存结果）。
- **锚点**：剧院**包厢特权**——数据描述符是包厢客，永远优先入座（赋值也被管）；实例字典是普通观众；非数据描述符是站票客，观众先占了座他就没座。
- **易错**：`property` 是数据描述符，所以 `obj.prop = v` 无 setter 时抛 `AttributeError`，不会写进实例字典。
- **关联**：→ PY-10-16：优先级由三键装备情况决定 ｜ → PY-10-18 property 的拦截力来自数据描述符身份。

### PY-10-18 property 的真身（property 就是内置描述符）
- **是什么**：`property` 是 Python 内置的数据描述符，`@x.setter` 等装饰器只是给同一个 property 对象换 `__set__` 的语法糖。
- **为什么**：痛点是"getter/setter 写成方法后调用处得加括号，不像属性" → 机制是 property 把函数包装成描述符，`obj.x` 触发 `__get__` 调 getter、`obj.x = v` 触发 `__set__` 调 setter → 行为是读写像属性、逻辑在函数 → 边界是无 setter 的 property 赋值抛 `AttributeError`（数据描述符特权）。
- **怎么写**：
  ```python
  class Circle:
      def __init__(self, r): self._r = r
      @property
      def area(self): return 3.14 * self._r ** 2
  c = Circle(2)
  print(c.area)                      # 不加括号，像属性
  print(type(Circle.__dict__["area"])) # 揭开真身
  ```
  → 运行输出：`12.56`\n`<class 'property'>`
- **何时用/不用**：想让"算出来的值"用属性语法访问时用；需要复杂校验/懒加载/多字段拦截时自己写描述符更清晰。
- **锚点**：遥控器上那颗**语音键**——看起来是一颗普通键（属性），背后是厂家封装好的三键组合（描述符三接线口）。
- **易错**：property 的 getter 里再访问同名属性会无限递归（内部要存 `_x`）；`Circle.area`（类访问）返回 property 对象本身而非数值。
- **关联**：→ PY-09-11：OOP 篇的 property 用法就是本条的皮 ｜ → PY-10-17：无 setter 的 property 仍拦赋值。

### PY-10-19 描述符实战：懒加载与类型校验
- **是什么**：描述符的两大实战形态：非数据描述符做懒加载（首次访问才计算，缓存进实例字典），数据描述符做类型/范围校验（赋值即拦截）。
- **为什么**：痛点是"贵的计算不想每次访问都跑"和"赋值必须守规矩"两个需求散落在各处 → 机制是非数据描述符 `__get__` 首次算完写进 `obj.__dict__`（下次实例字典直取），数据描述符 `__set__` 里校验不过就抛错 → 行为是属性自动变聪明 → 边界是懒加载类属性被删缓存后会重算。
- **怎么写**：
  ```python
  class lazy:
      def __init__(self, fn): self.fn = fn
      def __set_name__(self, owner, name): self.name = name
      def __get__(self, obj, owner):
          if obj is None: return self
          val = self.fn(obj); obj.__dict__[self.name] = val      # 缓存进实例字典
          return val
  class Report:
      @lazy
      def big_table(self):
          print("(计算中…)")
          return sum(range(10000))
  r = Report(); print(r.big_table); print(r.big_table)           # 只算一次
  ```
  → 运行输出：`(计算中…) 49995000 49995000`
- **何时用/不用**：属性计算贵且不变 → 懒加载；赋值需守规矩 → 数据描述符；两者都要就组合使用（property 的 cached 变体，见 PY-08-14 functools.cached_property）。
- **锚点**：剧院**代客挂衣**——懒加载像衣帽间：客人首次存衣才挂（首次访问才算），之后凭牌直取（实例字典直取）。
- **易错**：懒加载缓存后若依赖的数据变了不会自动失效（要手动删 `__dict__` 项）；校验描述符别忘了 `__set_name__` 登记名字，否则错误信息不知道是哪个字段。
- **关联**：→ PY-10-16：两形态就是三键的不同装备方式 ｜ → PY-08-14：stdlib 的 cached_property 是懒加载的官方现成版。

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| repr vs str | `__repr__` 给开发者 | `__str__` 给用户 | print/str 走 str；容器/repr() 走 repr | 后台精确前台美 |
| == vs is | `__eq__` 值相等 | `is` 同一对象 | 比内容用 ==，比身份用 is | 值等靠 eq 身份靠 is |
| __bool__ vs __len__ | 显式真值 | 回落用长度 | bool 优先，len()==0 为假 | 先问 bool 再数格子 |
| + vs += | `__add__` 出新对象 | `__iadd__` 原地改 | 无 i 版时 += 退化为 + 再绑定 | 加号换新单、加等续旧单 |
| __add__ vs __radd__ | 左优先 | 右兜底 | 左类型不支持时转问右 | 左不行问右边 |
| 数据 vs 非数据描述符 | 有 `__set__`/`__delete__` | 只有 `__get__` | 赋值要不要被拦 | 包厢特权 vs 站票可被占 |
| property vs 普通方法 | 属性语法访问 | 括号调用 | 读起来像值就用 property | 算出来的值不加括号 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-10-01 | 魔术方法/协议 | 万能遥控器按键排布（行业约定） | 按键排布 |
| PY-10-02 | __repr__ | 后台节目单（照着能重排） | 后台节目单 |
| PY-10-03 | __str__ | 台前预告牌（观众看大字） | 台前预告牌 |
| PY-10-04 | __len__ | 数遥控器频道数 | 数频道 |
| PY-10-05 | __bool__ | 舞台开演灯 | 开演灯 |
| PY-10-06 | __eq__ | 同一频道号=同台 | 同台判定 |
| PY-10-07 | __lt__ | 按频道号排队 | 号小排前 |
| PY-10-08 | __hash__ | 按键位编号定格子 | 按键位 |
| PY-10-09 | __getitem__ | 按频道号换台 | 换台下标 |
| PY-10-10 | __setitem__/__delitem__ | 按键位存台/删台 | 存台删台 |
| PY-10-11 | __call__ | 遥控器大按钮一按换台 | 大按钮 |
| PY-10-12 | __enter__/__exit__ | 幕布拉开/拉上 | 开闭幕 |
| PY-10-13 | __add__/__mul__ | 两张频道表叠加 | 叠频道表 |
| PY-10-14 | __radd__ | 客串顶替（问右边） | 客串顶替 |
| PY-10-15 | __iadd__ | 原节目单续写 | 续写旧单 |
| PY-10-16 | 描述符协议 | 遥控器三键接线口＋装机登记 | 三键接线口 |
| PY-10-17 | 数据/非数据描述符 | 包厢特权优先级 | 包厢特权 |
| PY-10-18 | property 真身 | 语音键=封装三键组合 | 语音键 |
| PY-10-19 | 懒加载/校验描述符 | 代客挂衣凭牌直取 | 代客挂衣 |

## ✅ 自测清单（合上本篇，先写再看）
1. （写代码）写一个 `Money` 类，让 `Money(2) + Money(3)` 输出 `Money(5)`，并让 `print(m)` 显示 `￥5`。
   > 答案：`__add__` 返回 `Money(self.yuan + other.yuan)`；`__str__` 返回 `f"￥{self.yuan}"`；建议同时写 `__repr__` 与 `__eq__`。
2. （说机制）为什么只定义了 `__eq__` 的类会报 `unhashable type`？
   > 答案：Python 规定定义 `__eq__` 而未定义 `__hash__` 时自动把 `__hash__` 置 None，对象变为不可哈希（PY-10-08）。
3. （说区别）`a is b` 与 `a == b` 各看什么？
   > 答案：is 比身份（id 相同）；== 走 `__eq__` 比值，默认实现退化为身份比较。
4. （改错）`__len__` 返回 -1 会发生什么？
   > 答案：`len()` 抛 `ValueError: __len__() should return >= 0`；长度必须非负。
5. （说区别）`p += [x]` 与 `p = p + [x]` 何时行为不同？
   > 答案：对象实现了 `__iadd__` 且返回 self 时，前者原地改、p 与旧引用是同一对象；否则两者等价（生成新对象），见 PY-10-15。
6. （说机制）为什么 `obj.x = 1` 有时被拦截抛错，有时又能直接写进实例字典？
   > 答案：`x` 是数据描述符（含 `__set__`，如 property/校验描述符）时赋值被拦截（PY-10-17）；只是非数据描述符或普通属性时写进实例字典，且实例字典优先于非数据描述符。
7. （写代码）不看资料，写一个 `age` 描述符：赋值小于 0 抛 `ValueError`，并让错误信息带字段名。
   > 答案：`__set_name__` 登记 `self.name`；`__set__` 里 `if value < 0: raise ValueError(f"{self.name} 不能为负")` 后存 `obj.__dict__[self.name]`（PY-10-16/19）。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-09 面向对象](py-09-oop.md) ｜ ➡️ 下一篇：[py-11 迭代与生成器](py-11-iterators-generators.md)
