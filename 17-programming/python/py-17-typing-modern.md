# py-17 现代语法与类型标注 — 记忆编码

> **📍 本章导航**：前置 → [py-09 OOP](py-09-oop.md) ｜ 相关 → [py-20 工程化](py-20-engineering-testing.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~12min（约 8k tokens）
>
> 本章逻辑链：py-09 以前的代码"能跑就行" → 本篇给代码画**图纸**（类型标注）并盖**质检章**（mypy），再装上现代语法工具箱 → 引出 py-20"怎么把图纸管起来"。意象域：**建筑图纸与质检章**，本篇锚点只取"图纸/施工/质检"画面，不越域。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 图纸标注四件套 | PY-17-01~05 | 注解、图例、竖线二选一、可选项、图纸简称 |
| 施工模具四件套 | PY-17-06~10 | 预制件、冻结墙、等级牌、对样板、清单表 |
| 质检章与新工具 | PY-17-11~15 | 万能代号、质检章、分拣台、卡尺、量完贴标签 |

## 一、图纸标注四件套（先学会画图纸）
### PY-17-01 类型注解 Type Annotation
- **是什么**：在参数/返回值后写 `: 类型` 的"图纸尺寸标注"（annotation），给变量和函数标注期望的类型。
- **为什么**：痛点：代码一多人就忘了"参数该传什么"，跑起来才炸 → 机制：解释器把标注存成元数据 `__annotations__`，**运行期不检查** → 行为：标错也能跑，标对也不强制 → 边界：真检查要靠 mypy（PY-17-12）。
- **怎么写**：
```python
def greet(name: str, times: int = 1) -> str:
    return f"你好{name}！" * times
print(greet.__annotations__)
print("类型标错也能跑：", greet(123, 1))
```
→ 运行输出：`{'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}` ／ `类型标错也能跑： 你好123！`
- **何时用/不用**：给别人和 mypy 看就标；一次性脚本可不标，函数边界建议保留。
- **锚点**：图纸上的**尺寸标注**——只标注不检查，就像图纸标了层高 3 米，工人盖 2.8 米也没人当场拦。
- **易错**：以为加了注解运行期就会拦类型错（并不会）；`greet(123, 1)` 照跑不误。
- **关联**：`→ PY-17-12：mypy 才是真正盖章检查的人`　`→ PY-07-01：def 语法的参数位置`

### PY-17-02 typing 常用类型集
- **是什么**：`typing` 模块是"图纸标准图例表"：`List/Dict/Tuple`、`Optional`、`Callable`、`Any`、`Iterable` 等泛型类型词汇。
- **为什么**：痛点：内置 `list` 说不清"里面装什么" → 机制：`list[int]`/`List[int]` 这种下标泛型给容器标内芯 → 行为：`Any` 表示"随便什么类型"（关检查）→ 边界：3.9+ 直接写 `list[int]` 即可，`typing.List` 是兼容老写法。
- **怎么写**：
```python
from typing import Callable, Optional
def maybe(n: int) -> Optional[int]:
    return n if n > 0 else None
def apply(fn: Callable[[int], int], x: int) -> int:
    return fn(x)
print(maybe(5), maybe(-1), apply(lambda x: x * x, 7))
```
→ 运行输出：`5 None 49`
- **何时用/不用**：容器内芯不明就用泛型标注；`Any` 只在真不知道类型时用，用多等于没标。
- **锚点**：**图纸图例表**——每种符号（管道/电路/门窗）一个标准画法，看图的人不猜。
- **易错**：`Callable[[int], int]` 的方括号里是"参数列表的列表"，漏一层括号就不合法。
- **关联**：`→ PY-17-04：Optional 是图例里"可空"符号`

### PY-17-03 竖线联合 X | Y（3.10+）
- **是什么**：PEP 604 的联合类型写法：`int | str` 表示"int 或 str 都收"，替代旧的 `Union[int, str]`。
- **为什么**：痛点：`Union` 写法啰嗦且像函数调用 → 机制：3.10 起 `|` 直接构造联合类型，还能用于 `isinstance` → 行为：`int | None` 一眼读出"整数或空" → 边界：3.9 及以下只能写 `Union`，竖线会报错。
- **怎么写**：
```python
def parse(raw: str) -> int | str:
    return int(raw) if raw.isdigit() else raw
print(parse("42"), parse("abc"))
print(isinstance(1, int | str), isinstance("x", int | str), isinstance(1.5, int | str))
```
→ 运行输出：`42 abc` ／ `True True False`
- **何时用/不用**：3.10+ 一律用竖线；要兼容 3.9 就用 `Union`/`Optional`。
- **锚点**：门洞中间立一道**隔断**——竖线 `|` 就是隔断，左边门进、右边门进都算合法通道。
- **易错**：`isinstance(x, int | str)` 是 3.10+ 才支持的用法；老版本必须传元组 `isinstance(x, (int, str))`。
- **关联**：`→ PY-17-04：int | None 就是 Optional[int]`　`→ PY-17-13：match-case 常按联合类型分拣`

### PY-17-04 Optional 与可空字段
- **是什么**：`Optional[int]` 表示"`int` 或 `None`"，等价于 `int | None`，专门标注"可能没有值"的字段。
- **为什么**：痛点：`None` 是"查无结果"的通用信号，但不标注就会误当成正常值用 → 机制：类型系统逼你处理 `None` 分支 → 行为：`Optional[int] == int | None` 为 True → 边界：标注不等于判空，代码里仍要 `if x is None`。
- **怎么写**：
```python
from typing import Optional, get_args, get_origin
def find(xs: list[int], target: int) -> Optional[int]:
    return xs.index(target) if target in xs else None
print(find([10, 20, 30], 20), find([10, 20, 30], 99))
print(get_origin(Optional[int]), get_args(Optional[int]))
print("和 int | None 等价：", Optional[int] == (int | None))
```
→ 运行输出：`1 None` ／ `typing.Union (<class 'int'>, <class 'NoneType'>)` ／ `和 int | None 等价： True`
- **何时用/不用**：函数可能无返回值、字段允许为空时用；永远非空的值别标 Optional，徒增判空负担。
- **锚点**：图纸上的**"可选车位"标注**——车位可以空着（None），但验收时要按"可能空"来检查。
- **易错**：把 `Optional[int]` 误读成"可选参数"——它是"可空值"，参数默认值是另一回事（PY-07）。
- **关联**：`→ PY-17-03：Optional 就是 X | None`　`→ PY-12-01：返回 None 前先想清楚要不要抛异常`

### PY-17-05 类型别名 TypeAlias
- **是什么**：给复杂类型起短名：旧式 `Vec: TypeAlias = list[float]`；3.12+ 新式 `type Coord = tuple[float, float]`（type 语句）。
- **为什么**：痛点：`dict[str, list[tuple[float, float]]]` 写三遍就眼花 → 机制：别名只换名字不造新类型，mypy 视为同一个类型 → 行为：`type` 语句定义的别名惰性求值、可自引用 → 边界：赋值式别名在运行期就是原类型，`type` 语句是 3.12+ 专属。
- **怎么写**：
```python
type Coord = tuple[float, float]    # 3.12+ 新式别名
def dist(a: Coord, b: Coord) -> float:
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5
print(dist((0.0, 0.0), (3.0, 4.0)))
```
→ 运行输出：`5.0`
- **何时用/不用**：同一复杂类型出现 ≥2 次就起别名；只用一次别起，多一层跳转反而难读。
- **锚点**：给常用图起**图纸简称**——"标准间"三个字顶一张完整平面图，看图人秒懂。
- **易错**：`type Coord = ...` 是 3.12+ 语法，3.11 及以下报 SyntaxError，要兼容就用赋值式。
- **关联**：`→ PY-17-02：别名的原料是 typing 图例`　`→ PY-17-11：泛型别名还能带类型参数`

## 二、施工模具四件套（用类型造数据）
### PY-17-06 dataclass 基础
- **是什么**：`@dataclass` 装饰器按类的类型标注自动生成 `__init__`/`__repr__`/`__eq__`，是"数据类预制板"。
- **为什么**：痛点：纯存数据的类要手写样板方法，写三行忘一行 → 机制：装饰器读类标注，注入样板方法 → 行为：字段声明即构造参数，比较按字段逐一比 → 边界：默认值字段必须放无默认值字段之后。
- **怎么写**：
```python
from dataclasses import dataclass
@dataclass
class Point:
    x: float
    y: float
    label: str = "无名"
print(Point(1.5, 2.5))
print(Point(1.5, 2.5) == Point(1.5, 2.5))
```
→ 运行输出：`Point(x=1.5, y=2.5, label='无名')` ／ `True`
- **何时用/不用**：纯数据容器用 dataclass；行为复杂的大类写普通 class（PY-09）。
- **锚点**：**预制板模具**——标注好尺寸浇一次，`init/repr/eq` 三件成型，不用手工绑钢筋。
- **易错**：给可变默认值写 `tags: list = []` 直接报 ValueError，必须用 `field(default_factory=list)`（见 PY-17-07）。
- **关联**：`→ PY-17-07：field 处理可变默认值与冻结`　`→ PY-09-02：dataclass 本质仍是 class`

### PY-17-07 dataclass 进阶 field 与 frozen
- **是什么**：`field(default_factory=...)` 为每个实例现场造默认值；`@dataclass(frozen=True)` 冻结实例字段（不可重新赋值）。
- **为什么**：痛点：`tags: list = []` 让所有实例共享同一个列表（PY-04 深坑）→ 机制：`default_factory` 每次构造时调用工厂函数造新对象 → 行为：`frozen` 把字段设为只读，赋值抛 `FrozenInstanceError` → 边界：冻结只挡"重新赋值"，列表内容仍可变。
- **怎么写**：
```python
from dataclasses import dataclass, field
@dataclass(frozen=True)
class Config:
    host: str = "localhost"
    tags: list = field(default_factory=list)
c = Config()
c.tags.append("web")   # 冻的是字段绑定，列表内容仍可变
print(c)
try:
    c.host = "example.com"
except Exception as e:
    print("改字段被拒:", type(e).__name__, e)
```
→ 运行输出：`Config(host='localhost', tags=['web'])` ／ `改字段被拒: FrozenInstanceError cannot assign to field 'host'`
- **何时用/不用**：配置对象、常量数据用 frozen 防误改；需要频繁改字段的业务对象别冻结。
- **锚点**：**承重墙与入户电表**——frozen 是承重墙砸不得（重新赋值被拒）；`default_factory` 是每户新装一块电表，绝不整栋楼共用。
- **易错**：`frozen=True` 后 `c.tags.append(...)` 依然成功（冻的是字段绑定，不是对象内部），别误以为深度不可变。
- **关联**：`→ PY-17-06：dataclass 基础`　`→ PY-19-03：共享可变默认值的深浅拷贝陷阱`

### PY-17-08 Enum 枚举
- **是什么**：`Enum` 把一组固定常量关进"等级牌"：成员是单例对象，有 `.name`/`.value`。
- **为什么**：痛点：状态用魔法数字 1/2/3，传 4 也能跑但语义崩了 → 机制：枚举成员是唯一实例，越界值取不到成员 → 行为：`Status(3)` 按值取成员，`Status(99)` 抛 ValueError → 边界：枚举成员比较用 `is`，别当成普通整数做算术。
- **怎么写**：
```python
from enum import Enum
class Status(Enum):
    PENDING = 1
    RUNNING = 2
    DONE = 3
print(Status.RUNNING, "| name:", Status.RUNNING.name, "| value:", Status.RUNNING.value)
print(Status(3), Status.DONE is Status(3))
try:
    Status(99)
except ValueError as e:
    print("越界值被拒:", e)
```
→ 运行输出：`Status.RUNNING | name: RUNNING | value: 2` ／ `Status.DONE True` ／ `越界值被拒: 99 is not a valid Status`
- **何时用/不用**：状态机/类别等封闭集合用 Enum；真要"任意整数"的场景别硬套。
- **锚点**：工地的**材料等级牌**——只有甲/乙/丙三块牌，想拿"丁等"没有这块牌。
- **易错**：`Status.RUNNING == 2` 在普通 Enum 里是 False（成员不等于它的值），只有 `IntEnum` 才和整数互通。
- **关联**：`→ PY-17-13：match-case 常按枚举成员分拣`　`→ PY-10-02：枚举靠 __eq__/__hash__ 单例机制`

### PY-17-09 Protocol 协议（结构化类型）
- **是什么**：`Protocol` 定义"长得像就行"的接口：类不用继承，只要方法签名匹配就算合格（结构化子类型，structural subtyping）。
- **为什么**：痛点：Python 鸭子类型好用但 mypy 说不清"到底要什么形状" → 机制：Protocol 声明最小方法集合，mypy 检查结构是否兼容 → 行为：`io.StringIO` 没继承 `Writer` 却能通过检查 → 边界：运行期 Protocol 不做任何检查，纯静态工具。
- **怎么写**：
```python
from typing import Protocol
class Writer(Protocol):
    def write(self, s: str) -> int: ...
def shout(w: Writer, msg: str) -> None:
    w.write(msg.upper())
import io
buf = io.StringIO()
shout(buf, "hello")
print("StringIO 冒充 Writer 成功:", repr(buf.getvalue()))
```
→ 运行输出：`StringIO 冒充 Writer 成功: 'HELLO'`
- **何时用/不用**：给"只要求有某方法"的参数定接口用 Protocol；要求真正继承关系时用 ABC（PY-09）。
- **锚点**：**对样板验收**——包工头不查施工队户口（不看继承），只拿样板对活儿：尺寸对得上就收。
- **易错**：Protocol 里方法体写 `...` 是声明不是实现，别在协议类里写业务代码。
- **关联**：`→ PY-09-06：ABC 抽象类是"必须继承"路线`　`→ PY-10-03：魔术方法本质也是协议`

### PY-17-10 TypedDict
- **是什么**：给字典画"材料清单表"：标注每条键的类型，静态检查字典结构，运行期它就是普通 dict。
- **为什么**：痛点：函数返回 `{"name": ..., "year": ...}` 的字典，键写错只能靠运行时 KeyError → 机制：TypedDict 声明必需键与类型，mypy 检查字面量 → 行为：`isinstance(m, dict)` 为 True → 边界：运行期不拦多键/少键，只是"图纸上的清单"。
- **怎么写**：
```python
from typing import TypedDict, get_type_hints
class Movie(TypedDict):
    name: str
    year: int
m: Movie = {"name": "流浪地球", "year": 2019}
print(m["name"], m["year"], "| 本质还是 dict:", isinstance(m, dict))
print("字段图纸:", get_type_hints(Movie))
```
→ 运行输出：`流浪地球 2019 | 本质还是 dict: True` ／ `字段图纸: {'name': <class 'str'>, 'year': <class 'int'>}`
- **何时用/不用**：JSON 风格的结构化数据用 TypedDict；需要默认值/行为就升级 dataclass（PY-17-06）。
- **锚点**：**材料清单表**——每行必须写"名称+数量"两栏，缺栏的单子质检不收（mypy 报缺键）。
- **易错**：`m: Movie = {...}` 传了清单外的键，运行期照样存进去，别指望它当校验器。
- **关联**：`→ PY-17-06：要行为和默认值改用 dataclass`　`→ PY-15-04：JSON 文件读进来常配 TypedDict`

## 三、质检章与新工具（把图纸管起来）
### PY-17-11 TypeVar 泛型入门
- **是什么**：`TypeVar` 是"万能尺寸代号"：`def first(items: Sequence[T]) -> T` 表示"进去什么类型，出来同类型"。
- **为什么**：痛点：想写"适用于任何列表"的函数，标注写死 `int` 就把 `str` 拒之门外 → 机制：mypy 对 T 做类型推断，每个调用点具体化 → 行为：`first([10,20])` 推断返回 `int` → 边界：T 是静态概念，运行期只是 `~T` 对象。
- **怎么写**：
```python
from typing import TypeVar, Sequence
T = TypeVar("T")
def first(items: Sequence[T]) -> T:
    return items[0]
print(first([10, 20]), first(["a", "b"]))
```
→ 运行输出：`10 a`
- **何时用/不用**：容器/工具函数写通用签名时用；具体业务函数不需要硬套泛型。
- **锚点**：图纸上的**万能尺寸代号 W**——图上写 W，实测多宽就多宽，图纸不用改。
- **易错**：`TypeVar("T")` 的字符串名字要和变量名一致，写 `T = TypeVar("X")` 只会自找混乱。
- **关联**：`→ PY-17-05：泛型别名是 TypeVar 的组合用法`

### PY-17-12 mypy 静态检查
- **是什么**：mypy 是"质检章"：不运行代码，按注解逐行验收类型是否合规（static type checking）。
- **为什么**：痛点：注解画了图纸没人验收就是废纸 → 机制：mypy 读注解建类型模型，跑数据流推断，报"施工违规" → 行为：运行不报错的错误也能被揪出来 → 边界：mypy 只管类型，逻辑错误（算法错）它不管。
- **怎么写**：违规示例 `mypy_bad.py`（`area("3", 4)` 传 str 给 float 参数）：
```python
def area(width: float, height: float) -> float:
    return width * height
result: float = area("3", 4)
print(result)
```
→ 实测：`python3 mypy_bad.py` 输出 `3333`（运行居然没报错！）；`mypy mypy_bad.py` 输出：
```
mypy_bad.py:3: error: Argument 1 to "area" has incompatible type "str"; expected "float"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```
- **何时用/不用**：提交前/CI 里跑 `mypy .`（见 PY-20-09）；一次性脚本可免，但库代码强烈建议。
- **锚点**：**质检章**——章是静态的：不搬砖不施工，只对照图纸盖"合格/不合格"，违规行直接点名。
- **易错**：mypy 绿灯≠程序正确，它只验收类型这一个维度；`Any` 太多会让质检形同虚设。
- **关联**：`→ PY-17-01：注解是图纸，mypy 是验收`　`→ PY-20-09：三件套之一`

### PY-17-13 match-case 基础（3.10+）
- **是什么**：结构模式匹配（structural pattern matching）：`match` 按数据"形状"分拣，`case` 是每条分拣通道。
- **为什么**：痛点：按命令/JSON 形状分流要写层层 if-elif，读起来像钻迷宫 → 机制：match 逐个尝试 case 的模式，匹配即绑定变量并执行 → 行为：`case _` 兜底；无兜底分支则一个 case 都不执行 → 边界：3.10+ 语法，旧版本不识别。
- **怎么写**：
```python
def handle(cmd: str) -> str:
    match cmd.split():
        case ["quit"]:
            return "退出"
        case ["go", direction]:
            return f"向{direction}走"
        case ["go", direction, steps]:
            return f"向{direction}走{steps}步"
        case _:
            return "听不懂"
print(handle("quit"), "|", handle("go north"), "|", handle("what"))
```
→ 运行输出：`退出 | 向north走 | 听不懂`
- **何时用/不用**：按结构分流（命令解析、JSON 分发）用 match；简单两三分支 if 更直白。
- **锚点**：工地**分拣台**——砖块按形状滑进对应料槽：整块的进 A 槽、带把手的进 B 槽，认不出的走兜底槽。
- **易错**：`case ["go", direction]` 里的 `direction` 是**绑定变量**（小写名字都绑），拼错变量名不会报错而是永远匹配成功。
- **关联**：`→ PY-17-08：常按枚举成员分拣`　`→ PY-06-08：match 出现前的 if-elif 写法`

### PY-17-14 match 进阶：序列/类/守卫模式
- **是什么**：case 模式家族：序列模式 `[x, y]`、类模式 `Point(x=0)`、OR 模式 `A | B`、守卫 `if 条件`。
- **为什么**：痛点：真实分拣不止看长度，还要看"字段值是不是 0""两数是否相等" → 机制：模式先解构再逐项比较，守卫在模式通过后再加条件过滤 → 行为：模式+守卫组合表达力接近规则引擎 → 边界：类模式按类名匹配，字段名写错等于永不匹配。
- **怎么写**：
```python
from dataclasses import dataclass
@dataclass
class Point:
    x: float
    y: float
def describe(p) -> str:
    match p:
        case Point(x=0, y=0): return "原点"
        case Point(x=x, y=0): return f"x轴上的点({x}, 0)"
        case [0, 0] | (0, 0): return "原点序列"
        case [x, y] if x == y: return f"对角线上的点({x}, {y})"
        case _: return "普通点"
print(describe(Point(5, 0)), "|", describe([3, 3]), "|", describe([2, 9]))
```
→ 运行输出：`x轴上的点(5, 0) | 对角线上的点(3, 3) | 普通点`
- **何时用/不用**：AST/JSON/命令等树状数据分发最划算；扁平数据用 if 更省脑。
- **锚点**：分拣台上的**卡尺与合格章**——卡尺量"两数是否相等"（守卫 if），合格章按"构件类型"盖戳（类模式）。
- **易错**：case 顺序敏感：`case [x, y]` 会先吞掉两元素序列，宽模式放后面。
- **关联**：`→ PY-17-13：基础分拣语法`　`→ PY-17-06：类模式常搭配 dataclass`

### PY-17-15 海象运算符 :=（3.8+）
- **是什么**：赋值表达式（assignment expression）：在表达式内部"顺便"把值赋给变量，写作 `:=`。
- **为什么**：痛点：`m = re.search(...)` 后再 `if m:`，同一个式子写两遍 → 机制：`if m := re.search(...)` 在求值同时完成赋值 → 行为：while 循环取值+判断可合并 → 边界：优先级低于普通赋值，表达式里加括号更清晰。
- **怎么写**：
```python
import re
data = "订单金额: 42 元"
if m := re.search(r"\d+", data):
    print("找到数字:", m.group())
lines = ["读第一行", "读第二行", ""]
while (line := lines.pop(0)) != "":
    print("处理:", line)
```
→ 运行输出：`找到数字: 42` ／ `处理: 读第一行` ／ `处理: 读第二行`
- **何时用/不用**：同一值"先算再判/再用"时用；简单赋值别追新潮写 `:=`，可读性优先。
- **锚点**：**量完顺手贴标签**——工人量完门洞宽度顺手把标签贴上（赋值），不用回办公室登记一遍再来用。
- **易错**：`while (line := f.readline())` 少写外层括号会 SyntaxError；`:=` 里赋的变量会泄漏到外层作用域。
- **关联**：`→ PY-16-04：正则匹配结果常用海象接收`　`→ PY-05-06：海象是表达式不是语句`

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| Optional vs 可选参数 | `Optional[int]`：值可为 None | `x: int = 0`：参数可不传 | 看"能不能不传"还是"能不能是空" | 可空是值的事，可省是参数的事 |
| Union 竖线 vs Union 函数 | `int \| str`（3.10+） | `Union[int, str]` | 看解释器版本 | 新写竖线旧写 Union |
| Protocol vs ABC | 结构像即可 | 必须继承 | 要不要强制血缘 | 对样板看活儿，ABC 验户口 |
| dataclass vs TypedDict | 有行为/默认值/校验 | 纯键值字典结构 | 要不要方法和默认值 | 有血有肉 dataclass，只有清单 TypedDict |
| 注解 vs mypy | 只是图纸标注 | 真静态验收 | 有没有人盖章 | 标注不检查，检查靠 mypy |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-17-01 | 类型注解 | 图纸尺寸标注（只标不查） | 尺寸标注 |
| PY-17-02 | typing 图例 | 图纸标准图例表 | 图例表 |
| PY-17-03 | 竖线联合 | 门洞隔断二选一 | 隔断门洞 |
| PY-17-04 | Optional | 可选车位可空着 | 可选车位 |
| PY-17-05 | 类型别名 | 图纸简称"标准间" | 图纸简称 |
| PY-17-06 | dataclass | 预制板模具 | 预制模具 |
| PY-17-07 | field/frozen | 承重墙+入户电表 | 承重墙 |
| PY-17-08 | Enum | 材料等级牌 | 等级牌 |
| PY-17-09 | Protocol | 对样板验收 | 对样板 |
| PY-17-10 | TypedDict | 材料清单表 | 清单表 |
| PY-17-11 | TypeVar | 万能尺寸代号 W | 代号W |
| PY-17-12 | mypy | 质检章（静态盖章） | 质检章 |
| PY-17-13 | match-case | 分拣台按形状滑槽 | 分拣台 |
| PY-17-14 | match 进阶 | 卡尺+合格章 | 卡尺合格章 |
| PY-17-15 | 海象 := | 量完顺手贴标签 | 贴标签 |

## ✅ 自测清单（合上本篇，先写再看）
1. 写一个函数 `first_word(s: str) -> str`，带完整注解，并说明注解何时才拦截错误。
> 答案：`def first_word(s: str) -> str: return s.split()[0]`；注解本身永不拦截，要靠 mypy 静态检查。
2. 用 dataclass 定义 `Config`，含可变默认值 `tags: list`，并冻结它。
> 答案：`@dataclass(frozen=True)` + `tags: list = field(default_factory=list)`。
3. `match [1, 2, 3]` 时，写一条"首元素是 0 的三元序列"的 case。
> 答案：`case [0, a, b]:`（序列模式+绑定变量）。
4. 用海象一行完成"取正则结果并判断"。
> 答案：`if m := re.search(r"\d+", s): print(m.group())`。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-16 正则](py-16-regex.md) ｜ ➡️ 下一篇：[py-18 并发](py-18-concurrency.md)
