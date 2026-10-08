# py-12 异常处理 — 记忆编码

> **📍 本章导航**：前置 → [py-06 控制流](py-06-control-flow.md)·[py-10 魔术方法](py-10-magic-methods.md) ｜ 相关 → [py-20 工程与测试](py-20-engineering-testing.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~12min（约 8k tokens）
>
> 本章逻辑链：py-11 的迭代管道能稳定供货了 → 本篇解决"取货出错（数据坏、文件缺）时怎么报警、怎么处置、怎么留线索" → 引出 py-13 的模块化：把处置规则装进各自的房间。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 接警与分级 | PY-12-01~04 | try 接警、按警情分级、层级树、警报单 |
| 收尾与抛出 | PY-12-05~10 | else 旁门、finally 总闸、raise/from/断链 |
| 自定义与风格 | PY-12-11~13 | 自家警情类、EAFP、assert 压力表 |
| 速查与坏味道 | PY-12-14~16 | 常见警情表、关电闸、别捂报警器 |

## 一、接警与分级（try/except/层级）

### PY-12-01 try/except 基本语义
- **是什么**：`try` 放可能出错的代码，`except` 捕获指定异常并处置；出错时程序不崩溃，跳到 except 继续。
- **为什么**：痛点是坏数据/缺文件让整个程序当场去世 → 机制是异常沿调用栈向上抛，遇到匹配的 except 被捕获处理 → 行为是错误被局部化，主流程继续 → 边界是 except 没匹配到类型时异常继续向上抛，直到有人接或程序终止。
- **怎么写**：
  ```python
  try:
      int("abc")              # 触发 ValueError
  except ValueError as e:
      print("捕获:", type(e).__name__, "-", e)
  print("程序继续")
  ```
  → 运行输出：`捕获: ValueError - invalid literal for int() with base 10: 'abc'` ｜ `程序继续`
- **何时用/不用**：外部输入/IO/解析等"可能合理地失败"处用 try；自己的逻辑 bug 不该用 except 掩盖，应修代码。
- **锚点**：烟雾报警器——起火（异常）立刻响铃并处置，楼里其他人（主流程）继续上班。
- **易错**：try 里只放可能出错的那几行，包住整个函数会让真正的 bug 被误当"异常"吞掉；`except` 后不写类型等价 `except BaseException`，连 Ctrl+C 都拦（见 PY-12-16）。
- **关联**：`→ PY-12-02：按警情分级处置` / `→ PY-12-16：吞异常的坏味道`

### PY-12-02 多分支捕获与元组捕获
- **是什么**：多个 `except` 按顺序匹配，命中即停；一个 except 可捕获元组里的多种异常。
- **为什么**：痛点是不同错误需要不同处置，全塞一个 except 只能瞎猜 → 机制是 except 从上到下逐个类型匹配（子类可被父类接住）→ 行为是每类警情有专属处置 → 边界是父类写在前面会"罩住"后面的子类分支，永远轮不到。
- **怎么写**：
  ```python
  for job in [lambda: 1 / 0, lambda: {}["k"], lambda: int("x")]:
      try: job()
      except ZeroDivisionError: print("捕获 ZeroDivisionError")
      except (KeyError, ValueError) as e: print("捕获", type(e).__name__)   # 元组：一网多捕
  ```
  → 运行输出：`捕获 ZeroDivisionError` ｜ `捕获 KeyError` ｜ `捕获 ValueError`
- **何时用/不用**：处置逻辑不同就分多个 except；处置完全相同的几种异常才用元组合并。
- **锚点**：分警情处置台——火警走一号台、门禁走二号台；一个警铃罩住多个警情（元组）。
- **易错**：`except (KeyError, ValueError)` 的括号漏写变成语法错误；父类 `except Exception` 写在子类前面，后面的分支成为死代码。
- **关联**：`→ PY-12-03：分支顺序依赖异常层级` / `→ PY-12-04：as 后接异常对象`

### PY-12-03 异常层级
- **是什么**：所有内置异常继承自 `BaseException`，常用根是 `Exception`；`KeyboardInterrupt`/`SystemExit` 是 `BaseException` 直属，不算普通异常。
- **为什么**：痛点是"到底该 catch 谁、except Exception 会不会误伤" → 机制是捕获按继承链匹配，父类能接住全部子类 → 行为是可按粒度选择捕获面 → 边界是 `except Exception` 不会拦 Ctrl+C 与 sys.exit，裸 `except:` 则全拦。
- **怎么写**：
  ```python
  print(issubclass(ZeroDivisionError, ArithmeticError))
  print(issubclass(ArithmeticError, Exception))
  print(issubclass(Exception, BaseException))
  print(issubclass(KeyboardInterrupt, Exception))   # 中断不是普通异常
  ```
  → 运行输出：`True` ｜ `True` ｜ `True` ｜ `False`
- **何时用/不用**：库代码捕获 `Exception` 并记录、上层应用按具体类型精细处置；永远别用裸 `except:`。
- **锚点**：消防警情分类树——"起火"是大树干，烟雾报警、电器火是枝叶；树干能罩住整根枝（父类接子类）。
- **易错**：`except Exception` 以为万能，其实漏掉 KeyboardInterrupt（这通常是好事，但要知道）；自定义异常不继承 `Exception` 会导致 except Exception 接不住。
- **关联**：`→ PY-12-11：自定义异常应挂在 Exception 下` / `→ PY-12-02：分支顺序按层级排`

### PY-12-04 异常对象与 args
- **是什么**：`except ... as e` 把异常对象绑给 e；`e.args` 是构造参数元组，`str(e)` 是给人看的信息，`type(e)` 是具体类型。
- **为什么**：痛点是只知道"出错了"不知道错在哪 → 机制是异常实例携带调用方写的参数与回溯信息 → 行为是日志能记录精确原因 → 边界是 e 只在 except 块内有效，出块后被删除防循环引用。
- **怎么写**：
  ```python
  try:
      raise ValueError("温度过高", 42)    # 异常可带多个参数
  except ValueError as e:
      print("args =", e.args)
      print("str  =", str(e), "| type =", type(e).__name__)
  ```
  → 运行输出：`args = ('温度过高', 42)` ｜ `str  = ('温度过高', 42) | type = ValueError`
- **何时用/不用**：处置要看原因（错误码、字段名）时用 as 绑定；只打一行日志也可用 `except ValueError:` 不绑定。
- **锚点**：警报单——单子上写着警情描述（args）和警种（type），处置完归档。
- **易错**：多参数异常的 `str(e)` 显示整个元组，容易误以为信息重复；在 except 外引用 e 会 `NameError`（已被删除）。
- **关联**：`→ PY-12-07：raise 时把信息写进 args`

## 二、收尾与抛出（else/finally/raise/链）

### PY-12-05 else 子句
- **是什么**：`else` 写在所有 except 之后，只在 try 块"没有发生异常"时执行。
- **为什么**：痛点是"正常路径"混在 try 里，会被误当可能出错的代码 → 机制是 try 没抛异常走 else，抛了走 except → 行为是正常/异常路径一眼分开 → 边界是 else 里的异常不会被同层 except 捕获（它不在 try 的保护范围）。
- **怎么写**：
  ```python
  def check(s):
      try: n = int(s)
      except ValueError: print("格式错误")
      else: print("解析成功:", n)     # try 没出事才走这里
      finally: print("安检收尾")     # 无论如何都走
  check("42")
  check("x")
  ```
  → 运行输出：`解析成功: 42` ｜ `安检收尾` ｜ `格式错误` ｜ `安检收尾`
- **何时用/不用**：成功才执行的后续动作（如解析后入库）放 else；既非出错也非收尾的逻辑根本别进 try 结构。
- **锚点**：检查合格才开的旁门——try 没报警，人员从 else 门放行。
- **易错**：把后续处理写进 try 里，其异常被 except 误捕；以为 else 会"无论如何都跑"（那是 finally）。
- **关联**：`→ PY-12-06：else=平安门、finally=总闸`

### PY-12-06 finally 子句
- **是什么**：`finally` 无论 try 是否出错、是否 return 都会执行，用于收尾。
- **为什么**：痛点是"出错也要关文件/解锁"靠手工补容易漏 → 机制是离开 try 结构前强制执行 finally（含 return/异常路径）→ 行为是收尾动作有保证 → 边界是 finally 里的 return 会覆盖 try 的返回值并吞掉未处理异常——反面教材。
- **怎么写**：
  ```python
  def f():
      try: return "try 的返回值"
      finally: print("finally 先执行")    # finally 在真正返回前执行
  def g():
      try: raise ValueError("警报")
      finally: return "finally 的返回值"  # 反面教材：吞掉异常
  print(f()); print(g())
  ```
  → 运行输出：`finally 先执行` ｜ `try 的返回值` ｜ `finally 的返回值`
- **何时用/不用**：资源清理放 finally（更推荐 with，见 PY-12-15）；绝不要在 finally 里 return/吞异常。
- **锚点**：总电闸——不管有没有火警，离场前必须拉闸（finally 永远执行）。
- **易错**：finally 中 return 会吞掉正在传播的异常（上例 g 的警报无声消失）；finally 里再抛新异常会覆盖原异常，排查时看到的是假现场。
- **关联**：`→ PY-12-05：三子句执行顺序 try→else→finally` / `→ PY-12-15：清理优先用 with`

### PY-12-07 raise 与异常转换
- **是什么**：`raise 异常实例` 主动抛出异常；except 中 `raise 新异常` 把底层错误转换成上层语义。
- **为什么**：痛点是底层 KeyError 对调用方无意义，"配置项缺失"才是真语义 → 机制是 raise 触发正常的异常传播，可在任何层转换类型 → 行为是错误沿层级被翻译 → 边界是裸 `raise`（不带参数）只能用在 except 内，表示"重新抛出当前异常"。
- **怎么写**：
  ```python
  def handle():
      try: raise ValueError("烟雾报警")             # raise 抛出新异常
      except ValueError: raise RuntimeError("启动灭火器")   # except 中转成上层异常
  try:
      handle()
  except RuntimeError as e: print("捕获:", type(e).__name__, "-", e)
  ```
  → 运行输出：`捕获: RuntimeError - 启动灭火器`
- **何时用/不用**：校验失败、语义转换时主动 raise；不要用 raise 做正常分支控制（那是返回值的活）。
- **锚点**：手动报警按钮——发现险情按下它（raise），处置中升级警情再按一次（转换）。
- **易错**：`raise ValueError`（类而非实例）合法但少写括号易误读；except 里转换后不带 from，丢掉原始原因（见 PY-12-08）。
- **关联**：`→ PY-12-08：转换时交代因果` / `→ PY-12-04：raise 的参数进 args`

### PY-12-08 raise from 显式异常链
- **是什么**：`raise 新异常 from 原因` 显式声明因果，异常的 `__cause__` 指向原因。
- **为什么**：痛点是排错只看到最外层错误，找不到根因 → 机制是 from 把原因挂到 `__cause__`，traceback 会打印 "The above exception was the direct cause" → 行为是错误链完整可溯 → 边界是 `from None` 是显式断链（PY-12-10）。
- **怎么写**：
  ```python
  try:
      try: int("x")
      except ValueError as e: raise RuntimeError("解析失败") from e   # 显式指定原因
  except RuntimeError as e:
      print("cause   =", type(e.__cause__).__name__)
      print("context =", type(e.__context__).__name__)
  ```
  → 运行输出：`cause   = ValueError` ｜ `context = ValueError`
- **何时用/不用**：底层异常转译成上层异常时必用，一行成本换整条排查链；直接原样上抛就不用（裸 raise 即可）。
- **锚点**：警报单写明起火原因——新警单（新异常）第一页就贴着起火原因（from 原因）。
- **易错**：from 的原因写成字符串而非异常（`raise X from "原因"`）会 TypeError；`__cause__` 与 `__context__` 同时存在时别看错字段（见消混表）。
- **关联**：`→ PY-12-09：不写 from 也有隐式链` / `→ PY-12-10：from None 刻意断链`

### PY-12-09 隐式异常链 __context__
- **是什么**：在 except 块内再抛新异常而没写 from 时，Python 自动把原异常挂到 `__context__`。
- **为什么**：痛点是"处理中又炸了"的现场最容易丢 → 机制是异常触发时若正在处理另一异常，自动记录 `__context__` → 行为是 traceback 出现 "During handling of the above exception" → 边界是隐式链只是记录，语义上不表示因果（区别于 from）。
- **怎么写**：
  ```python
  try:
      try: {}["火警"]
      except KeyError: raise ValueError("键缺失")   # 未用 from：自动挂隐式链
  except ValueError as e:
      print("context =", type(e.__context__).__name__)
      print("cause   =", e.__cause__)
  ```
  → 运行输出：`context = KeyError` ｜ `cause   = None`
- **何时用/不用**：它自动发生，无需手动维护；想表达"因为所以"请显式 from，想隐藏细节用 from None。
- **锚点**：警报单背面自动贴上一条警情单——没人吩咐，系统自己贴的（隐式）。
- **易错**：把 `__context__` 当因果链给用户看，可能暴露无关底层细节；以为没写 from 就没有链，其实 traceback 里照样有。
- **关联**：`→ PY-12-08：显式因果用 from`

### PY-12-10 raise from None 断链
- **是什么**：`raise 新异常 from None` 刻意切断链路，`__cause__` 为 None 且 `__suppress_context__` 为 True，traceback 不再显示底层异常。
- **为什么**：痛点是底层细节（如 SQL 内部错误）对用户是噪音甚至泄密 → 机制是 from None 抑制上下文显示（属性仍在，只是不展示）→ 行为是对外只报干净的语义错误 → 边界是排错线索也一起没了，库内部日志应另行记录原因。
- **怎么写**：
  ```python
  try:
      try: int("x")
      except ValueError: raise RuntimeError("格式错") from None   # 刻意断链
  except RuntimeError as e:
      print("cause   =", e.__cause__)
      print("suppress =", e.__suppress_context__)   # True：traceback 不显示上下文
  ```
  → 运行输出：`cause   = None` ｜ `suppress = True`
- **何时用/不用**：封装层向用户隐藏实现细节时用；团队内部排错代码慎用，等于把线索烧掉。
- **锚点**：警报单不写前因——内部保密，只对外发布"格式错"一条结论。
- **易错**：以为 from None 删除了 `__context__`（其实属性还在，只是被 suppress）；全项目滥用 from None，线上排错无从下手。
- **关联**：`→ PY-12-08：from 值的第三个选项` / `→ PY-12-09：context 仍在只是不显示`

## 三、自定义与风格（自定义异常/EAFP/assert）

### PY-12-11 自定义异常类
- **是什么**：继承 `Exception`（或其子类）定义自己的异常类，可携带业务字段。
- **为什么**：痛点是内置异常类型表达不了业务语义（"库存不足""火警级别"）→ 机制是自定义类同样走继承匹配，可按族捕获 → 行为是调用方 catch 一个基类即可罩住整族 → 边界是命名以 Error 结尾、模块内定义并导出，别继承 BaseException。
- **怎么写**：
  ```python
  class FireAlarm(Exception):            # 消防报警基类
      def __init__(self, level, msg): super().__init__(msg); self.level = level
  class SmokeAlarm(FireAlarm): pass      # 烟雾报警子类
  try:
      raise SmokeAlarm(2, "三楼烟雾超标")
  except FireAlarm as e:                 # 捕获基类即可罩住整族
      print(type(e).__name__, e.level, "-", e)
  ```
  → 运行输出：`SmokeAlarm 2 - 三楼烟雾超标`
- **何时用/不用**：库/框架对外报错必须自定义（调用方要精确捕获）；一次性脚本用内置异常足够。
- **锚点**：自家消防警情分类牌——自家楼的警情分"烟雾/明火"两级，保安按牌处置。
- **易错**：自定义异常不写 `__init__` 直接 `super().__init__(msg)` 也行，但忘了调 super 会导致 `str(e)` 为空；继承错基类（如 ValueError）会让调用方的 except ValueError 误接。
- **关联**：`→ PY-12-03：挂进异常层级树`

### PY-12-12 EAFP vs LBYL
- **是什么**：EAFP（Easier to Ask Forgiveness than Permission）先做、出错再处理；LBYL（Look Before You Leap）先检查再做。
- **为什么**：痛点是"检查通过却失败"的竞态与重复判断 → 机制是 try/except 一次搞定"判断+执行"，检查与执行之间无空隙 → 行为是 Python 惯用 EAFP，代码更短更稳 → 边界是异常本身开销较大且预期高频出错时，LBYL 的 if 判断更划算。
- **怎么写**：
  ```python
  d = {"火警": 119}
  if "火警" in d: print("LBYL:", d["火警"])     # LBYL：先敲门再进
  try: print("EAFP:", d["急救"])               # EAFP：先进再说，撞了再处理
  except KeyError: print("EAFP: 没有这个键，改用 120")
  ```
  → 运行输出：`LBYL: 119` ｜ `EAFP: 没有这个键，改用 120`
- **何时用/不用**：Python 默认写 EAFP（鸭子类型友好）；并发/远端调用等"检查必然过期"的场景坚决 EAFP。
- **锚点**：先进后补检（EAFP，撞了安检再补手续）vs 先检后进（LBYL，门口排队安检）。
- **易错**：把 EAFP 写成 `except Exception` 全兜底，等于没有安检；LBYL 的 `if key in d: d[key]` 查两次，多线程下可能空。
- **关联**：`→ PY-12-01：try 是 EAFP 的载体`

### PY-12-13 assert 断言
- **是什么**：`assert 条件, "消息"` 在条件为假时抛 `AssertionError`；用于程序员自查的内部不变量。
- **为什么**：痛点是"这里理应成立"的假设需要显式钉住 → 机制是 assert 失败即抛 AssertionError，`python -O` 启动时被整体移除 → 行为是开发期快速暴露逻辑错误 → 边界是不能用 assert 做用户输入校验（-O 下消失），也不能替代异常处理。
- **怎么写**：
  ```python
  def pressure(v):
      assert v < 100, "压力超标"      # 程序员自查，不是用户错误处理
      return v
  try: pressure(120)
  except AssertionError as e: print("AssertionError:", e)
  ```
  → 运行输出：`AssertionError: 压力超标`
- **何时用/不用**：内部前置条件/后置条件用 assert；对外参数校验必须用 `raise ValueError`（永不消失）。
- **锚点**：灭火器压力表自查——指针进红区就报警，是给维保人员（程序员）看的自查表。
- **易错**：`assert x == y, f"..."` 的消息是懒计算的，别在消息函数里放副作用；上线跑 `python -O` 后所有 assert 失效，别放关键校验。
- **关联**：`→ PY-12-07：对外校验用 raise` / `→ PY-20（见工程篇）：测试中断言的用法`

## 四、速查与坏味道（常见异常/清理/吞异常）

### PY-12-14 常见内置异常速查
- **是什么**：高频内置异常各管一段：`TypeError` 类型不对、`ValueError` 类型对值不对、`KeyError` 缺键、`IndexError` 下标越界、`ZeroDivisionError` 除零。
- **为什么**：痛点是"该 except 谁"靠猜 → 机制是 Python 按错误性质抛固定类型，记住五虎将覆盖八成场景 → 行是捕获可以精确到具体类型 → 边界是第三方库有自己的异常族，别都归到 ValueError。
- **怎么写**：
  ```python
  cases = [("1 / 0", lambda: 1 / 0), ("int('a')", lambda: int("a")),
           ("{}['k']", lambda: {}["k"]), ("[][0]", lambda: [][0]),
           ("len(1)", lambda: len(1))]
  for text, fn in cases:
      try: fn()
      except Exception as e: print(f"{text:10} -> {type(e).__name__}")
  ```
  → 运行输出：`1 / 0      -> ZeroDivisionError` ｜ `int('a')   -> ValueError` ｜ `{}['k']    -> KeyError` ｜ `[][0]      -> IndexError` ｜ `len(1)     -> TypeError`
- **何时用/不用**：写 except 前先想清楚"这会抛什么"，按表选型；不确定就先跑一遍看真实类型，别凭感觉写 Exception。
- **锚点**：常见警情速查表贴在消控室墙上——什么响什么铃，一眼对照。
- **易错**：`int("a")` 是 ValueError 不是 TypeError（类型对值不对）；`1/0` 在整数/浮点都是 ZeroDivisionError，但 numpy 里是 inf 不报错。
- **关联**：`→ PY-12-03：完整层级看异常树`

### PY-12-15 异常与资源清理
- **是什么**：出错路径上的资源释放，靠 `finally` 或（更优）`with` 上下文管理器保证。
- **为什么**：痛点是"写到一半炸了，文件句柄/锁没释放"→ 机制是 with/finally 在异常传播前执行收尾 → 行为是异常也不会泄漏资源 → 边界是 with 只管实现了协议的对象（协议见 PY-10-12），其他收尾还得 finally。
- **怎么写**：
  ```python
  path = "alarm_log.txt"; f = open(path, "w")
  try: f.write("09:00 烟雾报警")
  finally: f.close()               # finally 保证关闭
  print("已写入", path)
  with open(path) as f:            # with 自动收尾（协议见 PY-10-12）
      print("读回:", f.read())
  ```
  → 运行输出：`已写入 alarm_log.txt` ｜ `读回: 09:00 烟雾报警`
- **何时用/不用**：文件/锁/连接一律 with；非协议资源（临时目录、事务）用 contextlib 或 finally 补。
- **锚点**：灭火之后关电闸——不管火怎么灭的（异常与否），电闸必须落下来。
- **易错**：只写 `f = open(...)` 后靠"程序结束会关"，长生命周期进程句柄耗尽；with 块内别再手动 close（重复关闭无害但没必要）。
- **关联**：`→ PY-10-12：with 的协议机制` / `→ PY-12-06：finally 的语义`

### PY-12-16 吞异常的坏味道
- **是什么**：`except: pass`、只打日志不上抛、裸 `except:` 全兜底，都会把真实故障藏起来。
- **为什么**：痛点是"程序不报错了"的虚假安全感 → 机制是异常被消化后调用方拿到 None/半成品数据，故障延迟爆发 → 行为是排错只能靠猜 → 边界是"预期中的异常"（如探测式读取）可以吞，但必须注释理由。
- **怎么写**：
  ```python
  def risky():
      try: 1 / 0
      except Exception: pass       # 裸式吞掉：警报被捂住
  risky(); print("看不出这里出过事")   # 反面教材
  def better():
      try: 1 / 0
      except ZeroDivisionError as e: print(f"记录警报: {e}")   # 记录后按需上抛
  better()
  ```
  → 运行输出：`看不出这里出过事` ｜ `记录警报: division by zero`
- **何时用/不用**：吞异常只允许出现在"已知且已注释"的探测场景；其余情况记录并重新抛出或转换（PY-12-07）。
- **锚点**：把报警器捂住——被子盖住烟感（except: pass），火还在烧，只是没人知道了。
- **易错**：`except Exception: pass` 同样拦不住 KeyboardInterrupt（好事），但裸 `except:` 连它都拦，Ctrl+C 都失灵；循环体内吞异常会让整批数据静默丢失。
- **关联**：`→ PY-12-01：except 的处置原则` / `→ PY-12-07：记录后正确上抛`

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| except vs else | except 接 try 抛的 | else 走 try 没抛的 | 异常发生没有 | 有险情找 except、平安走 else |
| finally vs else | 无论如何都走 | 没异常才走 | 是否保证执行 | finally 总闸 else 旁门 |
| raise vs raise from | 抛新异常 | 抛新并交代原因 | 有没有因果要留 | 有因果加 from |
| __cause__ vs __context__ | from 显式指定 | 自动挂前因 | 看有没有 from | 显式 from、隐式 context |
| assert vs raise | 开发者自查 | 对外错误处理 | 谁的错、-O 会移除吗 | assert 查自己 raise 报外界 |
| EAFP vs LBYL | 先做再处理 | 先查再做 | Python 惯用 EAFP | 先闯后补 vs 先检后进 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-12-01 | try/except | 烟雾报警器+处置 | 报警器 |
| PY-12-02 | 多分支/元组捕获 | 分警情处置台/一铃罩多情 | 分警情处置 |
| PY-12-03 | 异常层级 | 消防警情分类树 | 警情树 |
| PY-12-04 | 异常对象 args | 警报单 | 警报单 |
| PY-12-05 | else 子句 | 合格才开的旁门 | 平安旁门 |
| PY-12-06 | finally 子句 | 总电闸 | 总闸 |
| PY-12-07 | raise | 手动报警按钮 | 手动报警 |
| PY-12-08 | raise from | 警报单写起火原因 | 写明起因 |
| PY-12-09 | __context__ 隐式链 | 单背自动贴上一单 | 背面贴单 |
| PY-12-10 | from None | 警报单不写前因 | 不写前因 |
| PY-12-11 | 自定义异常 | 自家警情分类牌 | 警情牌 |
| PY-12-12 | EAFP/LBYL | 先闯后补 vs 先检后进 | 先闯后补 |
| PY-12-13 | assert | 灭火器压力表自查 | 压力表 |
| PY-12-14 | 内置异常速查 | 消控室警情速查表 | 速查表 |
| PY-12-15 | 资源清理 | 灭火后关电闸 | 关电闸 |
| PY-12-16 | 吞异常 | 把报警器捂住 | 捂报警器 |

## ✅ 自测清单（合上本篇，先写再看）
1. （写代码）`try: x=int("a") ... ` 想让 ValueError 被处理、其他异常继续传播，except 该怎么写？
   > 答案：`except ValueError as e: ...`（只列 ValueError），其余自动继续向上传播。
2. （说顺序）try 成功、try 失败两种情况下，else/except/finally 的执行顺序各是什么？
   > 答案：成功 → try→else→finally；失败 → try→匹配的 except→finally（PY-12-05/06）。
3. （说机制）`raise E2 from e1` 与在 except 里直接 `raise E2` 的 traceback 有何不同？
   > 答案：前者显示 "The above exception was the direct cause"（`__cause__=e1`）；后者显示 "During handling..."（`__context__` 隐式链）。
4. （改错）`assert user_age >= 18` 用来挡未成年用户，有什么坑？
   > 答案：`python -O` 下 assert 全部失效；对外校验应 `raise ValueError(...)`（PY-12-13）。
5. （说区别）`except:` 与 `except Exception:` 差在哪？
   > 答案：前者是裸 except，连 KeyboardInterrupt/SystemExit 一起拦；后者只拦 Exception 族（PY-12-03）。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-11 迭代与生成器](py-11-iterators-generators.md) ｜ ➡️ 下一篇：[py-13 模块与包](py-13-modules-packages.md)
