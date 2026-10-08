# py-13 模块与包 — 记忆编码

> **📍 本章导航**：前置 → [py-07 函数](py-07-functions.md) ｜ 相关 → [py-14 标准库](py-14-stdlib.md)·[py-20 工程测试](py-20-engineering-testing.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~12min（约 8k tokens）
>
> 本章逻辑链：py-07 把逻辑封装成函数 → 本篇解决"函数怎么装进文件、跨文件借来用" → 引出 py-14"标准图书馆里有哪些现成的书"。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 借书三手续 | PY-13-01~03 | import 怎么写、怎么找、怎么缓存 |
| 开馆铃与门牌 | PY-13-04~05 | `__name__` 区分"自己翻看还是被翻印" |
| 书架分区法 | PY-13-06~09 | 包 = 带书架牌的目录，`__init__` 是书架牌 |
| 找书路线图 | PY-13-10~12 | `sys.path` 决定去哪排架子找书 |
| 外借清单 | PY-13-13~14 | `__all__` 与下划线管"借哪些" |
| 开分馆手续 | PY-13-15~17 | 打包发布 + venv/uv 独立馆藏 |

## 一、借书三手续（import 的写、找、存）

### PY-13-01 import 的三种写法 Import Statements
- **是什么**：把模块（module，一个 `.py` 文件）加载进来用它的名字；三种写法：`import x`／`from x import y`／`import x as z`。
- **为什么**：复用不能靠复制粘贴（改一处漏九处）→ import 实现"一份定义、多处引用"→ 三种写法对应"整本借／只借一章／借书卡登记别名"三种粒度 → 边界：拿错粒度要么名字啰嗦要么丢命名空间。
- **怎么写**：
```python
import math            # ① 整本借
from math import sqrt  # ② 只借一章
import math as m       # ③ 借书记别名
print(math.sqrt(16), sqrt(16), m.pi)
print("三个名字指向同一模块对象:", math is m)
```
→ 运行输出：`4.0 4.0 3.141592653589793` ｜ `三个名字指向同一模块对象: True`
- **何时用/不用**：一两个成员用 `from`，用得多或怕重名用 `import x`，名字长/同名用 `as`（`import numpy as np`）；别用 `from x import *`（→ PY-13-13）。
- **锚点**：柜台三种借书法——整本、只借一章、借书卡上登记小名；柜员递书时问"整本、单章，还是登个别名？"
- **易错**：`from math import sqrt` 后写 `math.sqrt(16)` 报 `NameError`——只借了"一章"没借"整本"。
- **关联**：`→ PY-13-13：import * 拿什么由 __all__ 决定`；`→ PY-14-01：import os 后第一批常用成员`。

### PY-13-02 import 的查找与执行机制 Import Machinery
- **是什么**：一次 `import` 的固定流程：查缓存 `sys.modules` → 内置/冻结模块 → 按 `sys.path` 找文件 → 执行文件顶层代码 → 把模块对象绑定到名字。
- **为什么**：报错形态全由机制决定——找不到是路线图（PY-13-10）问题、跑两遍是缓存（PY-13-03）问题；不懂机制只能靠猜。关键行为：import 不是声明，是**当场执行**。
- **怎么写**（`book.py` 顶层有打印，模拟"翻开书"）：
```python
import sys, book       # book.py 顶层代码会执行
print("book.pages =", book.pages)
print("book.read() =", book.read())
print("已缓存在 sys.modules:", "book" in sys.modules)
```
→ 运行输出：`《book》被翻开：顶层代码开始执行` ｜ `book.pages = 300` ｜ `book.read() = 读了 300 页` ｜ `已缓存在 sys.modules: True`
- **何时用/不用**：机制不用手写，但排 `ModuleNotFoundError`、循环导入必须靠它；模块顶层别放假动作（会被 import 触发）。
- **锚点**：管理员找书三步曲——先查借阅登记簿（`sys.modules`）→ 按索书号路线图逐排找（`sys.path`）→ 找到才翻印（执行顶层代码）。
- **易错**：把 import 当"声明"→ 顶层 `print`/读文件在 import 瞬间就跑，测试里冒出意外输出。
- **关联**：`→ PY-13-03：命中缓存则不再执行`；`→ PY-13-10：sys.path 是找书路线图`。

### PY-13-03 sys.modules 缓存只执行一次 Module Cache
- **是什么**：`sys.modules` 是"已加载模块登记簿"：同一模块 import 几次都只执行一次顶层代码，返回同一个模块对象。
- **为什么**：没有缓存，10 个文件 import book 就跑 10 遍顶层副作用，且各处对象不同导致 `is` 判断混乱；缓存保证"一份定义全馆共享一个翻印本"。
- **怎么写**：
```python
import sys
import book
import book            # 第二次：命中缓存，不再执行
print("两次 import 是同一对象:", book is sys.modules["book"])
import importlib
importlib.reload(book)  # 显式重印才再次执行
```
→ 运行输出（《book》只在首 import 和 reload 时翻开）：`《book》被翻开：顶层代码开始执行` ｜ `两次 import 是同一对象: True` ｜ `《book》被翻开：顶层代码开始执行`
- **何时用/不用**：日常不碰 `sys.modules`；调试想立即生效用 `importlib.reload`，生产代码别依赖它。
- **锚点**："已翻印登记簿"：一本书只翻印一次存档，再借直接给翻印本；想换新版要主动要求"重印"（reload）。
- **易错**：改了 .py 后旧会话仍跑旧代码（缓存没清）——重启解释器最省事；循环导入（A↔B）本质是缓存里拿到"半初始化模块"。
- **关联**：`→ PY-13-02：机制流程第三步`。

## 二、开馆铃与门牌（`__name__` 家族）

### PY-13-04 `__name__` 变量：`__main__` 还是模块名 The `__name__` Attribute
- **是什么**：每个模块自带的属性：被直接运行时 `__name__ == "__main__"`，被 import 时等于模块名（如 `"story"`）。
- **为什么**：同一份 .py 有"自己当主程序跑"和"被别人当库借"两种身份 → 需要开关区分行为 → `__name__` 就是那块身份门牌 → 边界：只在运行期有意义，静态文本里看不到。
- **怎么写**（`story.py` 只有一行 `print("story.py 的 __name__ =", __name__)`）：
```python
import story
print("test_13_04.py 自己的 __name__ =", __name__)
```
→ 运行输出：`story.py 的 __name__ = story` ｜ `test_13_04.py 自己的 __name__ = __main__`；直接运行 `python3 story.py`：`story.py 的 __name__ = __main__`
- **何时用/不用**："既当脚本又当库"的文件必用；纯库文件不需要。
- **锚点**：扉页藏书章——自己翻看盖"本人所有"（`__main__`），被别馆借走盖"某某馆藏"（模块名）。
- **易错**：是双下划线开头结尾（dunder 名），写成 `name_`、`__name` 都拿不到预期值。
- **关联**：`→ PY-13-05：用它做守卫`；`→ PY-13-12：python -m 时 __name__ 同样是 __main__`。

### PY-13-05 `if __name__ == "__main__":` 守卫 Main Guard
- **是什么**：把"只在直接运行时执行"的代码（测试、演示、入口）放进这个 if 块；被 import 时不触发。
- **为什么**：demo 代码裸写在顶层，任何 `import demo` 都立刻跑演示（副作用外泄）→ 守卫让"可导入、可运行"互不打扰 → 行为：`__name__` 不是 `__main__` 就跳过。
- **怎么写**（`demo.py`：`main()` 打印一行，下面挂守卫）：
```python
import demo
print("导入者视角：没有触发演示，只拿到函数", demo.main.__name__)
```
→ 运行输出：`导入者视角：没有触发演示，只拿到函数 main`；直接运行 `python3 demo.py`：`演示彩排开始（只有直接运行才会走到这里）`
- **何时用/不用**：交付库文件一律加；一次性临时脚本可省，但加上不亏。
- **锚点**：演示角的告示牌：铃（守卫）只在"本人来翻看"时响，借书客（import）路过不响。
- **易错**：写成 `if __name__ = "__main__"`（单等号）→ `SyntaxError`；守卫内函数没缩进对齐也会报错。
- **关联**：`→ PY-13-04：判断依据是 __name__`。

## 三、书架分区法（包与 `__init__.py`）

### PY-13-06 包 = 目录 + `__init__.py` Package
- **是什么**：包（package）是带 `__init__.py` 的目录，包里每个 `.py` 是子模块；包有 `__path__` 属性（普通模块没有）。
- **为什么**：十几个模块平铺会撞名难找 → 包把模块收成"一排书架一个分区"，名字自带层级（`mylib.tools`）→ 边界：目录名合法（标识符规则）才能当包名。
- **怎么写**（`mylib/`：`__init__.py` + `tools.py`，后者 `hello()` 返回一句问候）：
```python
import mylib, mylib.tools as t
print("mylib 是包（有 __path__）:", hasattr(mylib, "__path__"))
print("tools.py 是模块（有 __file__）:", hasattr(t, "__file__"))
print(t.hello())
```
→ 运行输出：`mylib 是包（有 __path__）: True` ｜ `tools.py 是模块（有 __file__）: True` ｜ `tools 模块问好`
- **何时用/不用**：≤3 个模块平铺即可；开始分层（core/、utils/）就建包；无 `__init__` 的写法见 PY-13-09。
- **锚点**：一排书架（目录）+ 架头书架牌（`__init__.py`）才算分区；没挂牌的角落只是堆放处。
- **易错**：漏建或写成 `init.py` →（3.3 前）`import mylib` 直接 `ModuleNotFoundError`。
- **关联**：`→ PY-13-07：书架牌上写什么`；`→ PY-13-08：包内互借怎么写`。

### PY-13-07 `__init__.py` 的三重身份 Package Initializer
- **是什么**：包的初始化文件：①标识"这是包"；②包被 import 时**最先执行**（放初始化代码）；③决定 `from 包 import *` 的默认名单。
- **为什么**：用户想 `import shelflib` 就直接用 `shelflib.hello`，不想关心它在哪个子模块 → `__init__.py` 里 `from .tools import hello` 把深层成员摆上架头 → 边界：里面放重逻辑会拖慢所有 import。
- **怎么写**（`shelflib/__init__.py`：`__version__` + `from .tools import hello` + `__all__`）：
```python
import shelflib
print(shelflib.hello())
print("版本号来自 __init__:", shelflib.__version__)
from shelflib import *
print("星号导入拿到:", hello.__name__, __version__)
```
→ 运行输出：`tools 模块问好` ｜ `版本号来自 __init__: 1.0` ｜ `星号导入拿到: hello 1.0`
- **何时用/不用**：小包留空只当牌子；要"开箱即用"或统一版本号就做导出；重逻辑别放。
- **锚点**：书架牌三用——挂架牌（标识分区）、开馆摆展示书（初始化代码）、写明外借清单（`__all__`）。
- **易错**：`from tools import hello`（漏点号）报 `ModuleNotFoundError`；包内互借必须 `from .tools import ...`。
- **关联**：`→ PY-13-13：__all__ 管星号导入`；`→ PY-13-08：这里的点号是相对导入`。

### PY-13-08 绝对导入 vs 相对导入 Absolute vs Relative Import
- **是什么**：绝对导入从包顶全名写起（`from mylib.tools import hello`）；相对导入以当前模块为起点（`.`=本包，`..`=上一层）。
- **为什么**：包内互借写全名又长又怕改包名 → 相对导入写"本架第几格"，改包名不动内部引用 → 边界："本架"只在包内有户口，顶层脚本里必报错。
- **怎么写**（`mylib/greet.py` 用 `from .tools import hello`）：
```python
from mylib.greet import greet
print(greet())
```
→ 运行输出：`问候：tools 模块问好`；反例（顶层脚本写 `from .tools import hello`）真实报错：`ImportError: attempted relative import with no known parent package`
- **何时用/不用**：包内互借优先相对；对外示例/跨顶层包用绝对；顶层脚本绝不用相对。
- **锚点**：架内互借写"本架第 3 格"（`.`），跨架写全馆索书号（绝对）；出了图书馆说"本架"没人听得懂 → 报错。
- **易错**：`from . import tools`（借整个模块）与 `from .tools import hello`（借成员）混用；点号后带空格是语法错误。
- **关联**：`→ PY-13-12：python -m 才给相对导入"包名户口"`。

### PY-13-09 命名空间包 Namespace Package（了解）
- **是什么**：Python 3.3+（PEP 420）允许没有 `__init__.py` 的目录当包用，其 `__file__` 为 `None`。
- **为什么**：多个目录（甚至多个安装来源）要拼成同一个逻辑包名时，不该强迫每处放空 `__init__.py` → 命名空间包把"分区"从挂牌改为登记在册 → 边界：与普通包同名混放时解析微妙。
- **怎么写**（`nsarea/` 无 `__init__.py`，内含 `placer.py`）：
```python
import nsarea, nsarea.placer as p
print(p.NAME)
print("nsarea.__file__ =", nsarea.__file__)
```
→ 运行输出：`共享自习区的书` ｜ `nsarea.__file__ = None`
- **何时用/不用**：新手项目老老实实放 `__init__.py` 最稳；只有多目录插件体系才用它。
- **锚点**："共享自习区"：没有书架牌的开放区，书照样找得到；问它"牌子在哪"（`__file__`）答"没牌子"（None）。
- **易错**：代码假定"包必有 `__file__`"会在它这里崩；两个目录抢同一包名时合并结果依赖路径顺序。
- **关联**：`→ PY-13-06：普通包有 __init__.py`。

## 四、找书路线图（`sys.path` 与运行方式）

### PY-13-10 `sys.path`：找书路线图 Module Search Path
- **是什么**：一个 list，保存 import 时按顺序查找的目录；第 0 条默认是"脚本所在目录/当前目录"。
- **为什么**：`ModuleNotFoundError` 十有八九不是拼写错而是文件不在路线图上 → 按顺序逐条找 → 行为：排在前面的同名文件截胡 → 边界：动态改路径只影响改后发生的 import。
- **怎么写**：
```python
import os, sys
print("sys.path 类型:", type(sys.path).__name__, "条目数:", len(sys.path))
print("第 0 条是本脚本所在目录:", sys.path[0] == os.path.dirname(os.path.abspath(__file__)))
print("查找优先级: sys.modules → 内置模块 → 依 sys.path 顺序找文件")
```
→ 运行输出：`sys.path 类型: list 条目数: 7` ｜ `第 0 条是本脚本所在目录: True` ｜ `查找优先级: sys.modules → 内置模块 → 依 sys.path 顺序找文件`（条目数随环境增减，其余两行稳定）
- **何时用/不用**：排错时打印它；改查找路径优先环境变量（PY-13-11），少在代码硬塞绝对路径。
- **锚点**：贴在图书馆门口的"找书路线图"：先查登记簿、再按图上顺序一排排找；排在前面的"分馆"截胡同名书。
- **易错**：自己写的 `json.py`、`random.py` 等同名文件会遮蔽标准库 → 报各种诡异 `ImportError`，先查脚本目录（第 0 条）。
- **关联**：`→ PY-13-02：机制中"按 sys.path 找文件"一步`；`→ PY-14-02：sys 的其他成员`。

### PY-13-11 增加找书路线：PYTHONPATH 与 append
- **是什么**：给 `sys.path` 加条目的两条路：环境变量 `PYTHONPATH=目录`（启动前）或 `sys.path.append("目录")`（运行时打补丁）。
- **为什么**：开发时包不在脚本目录（项目根、src/），不加路线就 `ModuleNotFoundError` → PYTHONPATH 适合临时实验、append 适合一次性脚本 → 边界：两者都是临时措施，不是工程方案。
- **怎么写**（`extra/shelf.py` 里 `ITEM = "馆外书库的《借调书》"`）：
```python
import sys
sys.path.append("extra")   # 路线图末尾加一行
import shelf
print(shelf.ITEM)
print("extra 已加入路线图:", "extra" in sys.path)
```
→ 运行输出：`馆外书库的《借调书》` ｜ `extra 已加入路线图: True`；命令行等价：`PYTHONPATH=extra python3 -c "import shelf; print(shelf.ITEM)"` → `馆外书库的《借调书》`
- **何时用/不用**：正式项目用打包安装（PY-13-15）解决，别把 append 散落各处。
- **锚点**：给路线图末尾贴便签"馆外书库也可查"（append 一行）；便签贴在末尾，优先级最低。
- **易错**：append 相对路径时换个工作目录就失效——"在 A 处能跑、B 处报错"常源于此。
- **关联**：`→ PY-13-10：路线图本体`；`→ PY-13-15：正式做法是打包`。

### PY-13-12 `python -m` vs `python 文件.py` Run Modes
- **是什么**：`python3 -m pkg.mod` 把模块当包成员运行（`__package__` 有值）；`python3 pkg/mod.py` 当普通脚本运行（`__package__` 为 `None`，`sys.path[0]` 是文件所在目录）。
- **为什么**：相对导入需要"包名户口"（`__package__`）→ 直接跑文件没有户口，相对导入全报错 → 行为：两者 `__name__` 都是 `__main__`，但 `sys.path[0]` 不同 → 这正是"换个方式就 ModuleNotFoundError"的根源。
- **怎么写**（`pkgdemo/whoami.py` 打印三个信号）：
→ `python3 -m pkgdemo.whoami`：`__name__    = __main__` ｜ `__package__ = pkgdemo` ｜ `找书路线第 0 条指向包外目录: True`
→ `python3 pkgdemo/whoami.py`：`__name__    = __main__` ｜ `__package__ = None` ｜ `找书路线第 0 条指向包外目录: False`
- **何时用/不用**：含相对导入的包内模块一律在项目根 `python -m` 跑；独立单文件脚本直接 `python 文件.py`。
- **锚点**：大门进（`-m`：馆里知道你在哪个分区）vs 后门进（直接跑文件：没有分区户口）→ "本架"类引用全断。
- **易错**：`__name__` 两种方式都一样，别用它判断"怎么启动的"——看 `__package__`。
- **关联**：`→ PY-13-08：相对导入依赖 __package__`；`→ PY-13-05：守卫在两种方式下都触发`。

## 五、外借清单（导出控制）

### PY-13-13 `__all__` 与 `from x import *` Public List
- **是什么**：`__all__` 是模块/包里的字符串列表，声明"`import *` 允许拿走的名单"；没写时星号拿走所有不带下划线的名字。
- **为什么**：`import *` 像"把整架书搬走"，内部工具名全倒进命名空间互相覆盖 → `__all__` 把外借范围白纸黑字列出 → 边界：只约束星号，不挡显式 import。
- **怎么写**（`menu.py`：`__all__ = ["招牌书"]`，另有未登记的 `冷门书`）：
```python
from menu import *
print(招牌书)
try:
    print(冷门书)
except NameError as e:
    print("冷门书借不到 →", e)
```
→ 运行输出：`《算法导论》` ｜ `冷门书借不到 → name '冷门书' is not defined`
- **何时用/不用**：写对外库时精确导出；日常优先显式 `from x import y`，能不用星号就不用。
- **锚点**：书架牌上的"可外借清单"：代借员（`import *`）按清单取书，没登记的一律不给。
- **易错**：`__all__` 只管星号——`import menu` 后 `menu.冷门书` 照样可用，它不是访问控制。
- **关联**：`→ PY-13-07：__init__.py 里的 __all__ 同理`；`→ PY-13-14：下划线是另一层约定`。

### PY-13-14 私有约定：下划线前缀 Private Convention
- **是什么**：名字以 `_` 开头（`_internal`）表示"内部使用、请勿依赖"，`import *` 默认跳过；是约定不是强制。
- **为什么**：库的实现细节随时会改，用户依赖它升级就崩 → 下划线是"馆内阅览"标签，划出稳定边界 → 行为：星号跳过、显式 import 仍能拿。
- **怎么写**（`menu2.py`：`畅销书` 与 `_内部台账`）：
```python
from menu2 import *
print(畅销书)
print("_内部台账 被 import * 跳过:", "_内部台账" not in dir())
import menu2
print("显式点名仍能借到（只是约定）:", menu2._内部台账)
```
→ 运行输出：`《畅销榜》` ｜ `_内部台账 被 import * 跳过: True` ｜ `显式点名仍能借到（只是约定）: 馆员专用库存本`
- **何时用/不用**：辅助函数加 `_`，对外 API 不加；要真"锁"看封装（→ PY-09-12）。
- **锚点**：书脊贴"馆内阅览"小标签（下划线）：代借员见标签不拿，真点名硬借馆员也不拦。
- **易错**：把"下划线=私有"当安全边界（一 import 就拿到）；单独一个 `_` 常作占位变量，场景不同别混。
- **关联**：`→ PY-13-13：__all__ 管星号，下划线管默认名单`。

## 六、开分馆手续（打包与独立环境）

### PY-13-15 打包发布基础 pyproject.toml
- **是什么**：现代 Python 包的"办馆申请书"：`pyproject.toml` 写包名/版本/构建后端（PEP 621）；`python -m build` 产出 `.tar.gz` 与 `.whl`。
- **为什么**：要 `pip install` 给别人用就需要标准元数据 → 早年 `setup.py` 各写各的，`pyproject.toml` 统一申报格式 → 边界：只到"能构建分发"，发布 PyPI 属 py-20。
- **怎么写**（`tinyproj/`：`pyproject.toml` + `tinybook/__init__.py`）：
```python
import tomllib
with open("tinyproj/pyproject.toml", "rb") as f:
    meta = tomllib.load(f)["project"]
print("包名:", meta["name"], "| 版本:", meta["version"])
```
→ 运行输出：`包名: tinybook | 版本: 0.1.0`；在 `tinyproj/` 跑 `python3 -m build --no-isolation` 真实输出：`Successfully built tinybook-0.1.0.tar.gz and tinybook-0.1.0-py3-none-any.whl`
- **何时用/不用**：要分发才打包；内部脚本不需要；装完先自测（→ PY-20-18）。
- **锚点**：开分馆的办馆申请书：写清馆名（name）、开馆日期（version）、申报哪些文件；审核过了盖章出包（build 产物）。
- **易错**：`[project]` 漏 `version` → 构建 `KeyError`；目录名与包名撞车（同名嵌套）→ 导入混乱。
- **关联**：`→ PY-13-16：产物装进哪个环境由 venv 决定`。

### PY-13-16 venv 虚拟环境 Virtual Environment
- **是什么**：`python3 -m venv 目录` 造一个独立 `prefix` 的迷你环境，装包只落在里面，不污染系统 Python。
- **为什么**：A 项目要 `requests==2.0`、B 项目要 2.31，全局只能装一个 → 必须隔离 → 行为：`sys.prefix != sys.base_prefix` → 边界：venv 只隔离包，不隔离系统库版本。
- **怎么写**（缺 ensurepip 时用 `--without-pip`，见易错）：
```python
# 用 .venv2/bin/python 运行本段
import sys
print("venv 内 prefix :", sys.prefix.rsplit("/", 1)[-1])
print("系统 base     :", sys.base_prefix)
print("隔离生效      :", sys.prefix != sys.base_prefix)
```
→ 运行输出：`venv 内 prefix : .venv2` ｜ `系统 base     : /usr` ｜ `隔离生效      : True`
- **何时用/不用**：每项目开工先建（或用 uv，PY-13-17）；只跑标准库小脚本可省。
- **锚点**：每项目一间独立馆藏：A 馆装修（升级依赖）不影响 B 馆；馆内书架（`prefix`）≠ 总馆（`base_prefix`）。
- **易错**：Debian/Ubuntu 缺 `python3-venv` 时报真实错误 `The virtual environment was not created successfully because ensurepip is not available` → `apt install python3.12-venv` 后重建；忘激活会装到全局。
- **关联**：`→ PY-13-17：uv 一条命令建环境+装包`；`→ PY-20-17：工程依赖管理`。

### PY-13-17 uv：新一代工具链 uv Toolchain
- **是什么**：Rust 写的 Python 包管理器：`uv venv` 建环境、`uv pip install` 装包，比 pip+venv 快一个数量级，还能自动管理 Python 版本。
- **为什么**：pip 解析慢、venv+pip 两步易错位 → uv 把"建馆+进书"并成一条直达线 → 边界：`uv pip install` 只装进"当前选中的环境"，不指对解释器就装错地方。
- **怎么写**（实测 `uv 0.12.23`）：
```bash
uv venv .venvuv
uv pip install --python .venvuv/bin/python six
```
→ 运行输出：`Using CPython 3.12.3 interpreter at: /usr/bin/python3` ｜ `Creating virtual environment at: .venvuv` ｜ `Installed 1 package in 147ms`（`+ six==1.17.0`；毫秒数随环境波动）；用该解释器验证：`uv venv prefix: .venvuv` ｜ `隔离生效      : True`
- **何时用/不用**：新项目推荐 uv（或 poetry，→ PY-20-17）；只需复现老 requirements.txt 时 pip 够用。
- **锚点**：馆际物流高铁：过去"建馆（venv）+进书（pip）"两班车换乘，现在一条直达；车票上印着用哪个版本的馆长（interpreter）。
- **易错**：命令前忘激活/没指向 venv 解释器 → 装进系统环境；网络受限报下载超时，配置 `UV_INDEX_URL` 换镜像。
- **关联**：`→ PY-13-16：uv venv 产物的隔离机制相同`；`→ PY-13-15：装的就是 build 出的 wheel`。

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| 直接运行 vs 被导入 | `__name__=="__main__"` | `__name__` 是模块名 | 打印 `__name__` | 自己翻看盖"本人"，被借走盖馆名 |
| `import x` vs `from x import y` | 带前缀 `x.` | 只拿成员裸名 | 用时写不写 `x.` | 整本借带书名，单章借只拿篇 |
| 绝对 vs 相对导入 | `from mylib.tools import h` | `from .tools import h` | 有没有点号 | 跨架写索书号，架内写本架第几格 |
| 模块 vs 包 | 一个 `.py`，有 `__file__` | 目录+`__init__.py`，有 `__path__` | `hasattr(obj,"__path__")` | 单本书 vs 一排书架 |
| `python -m` vs `python 文件.py` | `__package__` 有值 | `__package__` 是 None | 相对导入能否用 | 大门进知分区，后门进没户口 |
| `__all__` vs `_` 前缀 | 管星号导入名单 | 管默认不外借 | 哪条路拿不到 | 清单管代借员，标签管所有客 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-13-01 | import 三种写法 | 柜台三种借书法：整本/单章/登别名 | 借书三手续 |
| PY-13-02 | import 机制 | 找书三步：登记簿→路线图→翻印 | 找书三步曲 |
| PY-13-03 | sys.modules 缓存 | 已翻印登记簿，重印才再执行 | 翻印登记簿 |
| PY-13-04 | `__name__` | 扉页藏书章：本人所有/某某馆藏 | 藏书章 |
| PY-13-05 | 主程序守卫 | 演示角告示牌，铃只给本人响 | 演示角铃 |
| PY-13-06 | 包 package | 书架+架头书架牌=分区 | 书架牌 |
| PY-13-07 | `__init__.py` | 架头牌三用：挂牌/展示书/外借清单 | 架头三用牌 |
| PY-13-08 | 相对导入 | "本架第 3 格" vs 全馆索书号 | 本架第几格 |
| PY-13-09 | 命名空间包 | 没挂牌的共享自习区 | 无牌自习区 |
| PY-13-10 | sys.path | 门口的找书路线图 | 路线图 |
| PY-13-11 | PYTHONPATH/append | 路线图末尾贴便签 | 贴便签 |
| PY-13-12 | `python -m` | 大门进知分区 vs 后门进没户口 | 大门后门 |
| PY-13-13 | `__all__` | 书架牌上的可外借清单 | 外借清单 |
| PY-13-14 | `_` 前缀 | 书脊"馆内阅览"小标签 | 馆内阅览签 |
| PY-13-15 | pyproject.toml | 开分馆的办馆申请书 | 办馆申请书 |
| PY-13-16 | venv | 每项目一间独立馆藏 | 独立馆藏 |
| PY-13-17 | uv | 馆际物流高铁：建馆+进书直达 | 馆际高铁 |

## ✅ 自测清单（合上本篇，先写再看）
1. 写 `lib.py`（含 `def f(): return 1` 与 `_hidden = 2`），用三种 import 写法各调用一次 `f()`。
> 答案：`import lib; lib.f()`／`from lib import f; f()`／`import lib as L; L.f()`；`from lib import *` 拿不到 `_hidden`。
2. `import story` 时 story.py 里 `print(__name__)` 输出什么？直接 `python3 story.py` 呢？
> 答案：`story`／`__main__`。
3. 为什么 `from .tools import hello` 写在顶层脚本必报错？怎么改？
> 答案：脚本无包上下文（`__package__` 为 None）→ `attempted relative import with no known parent package`；改 `from mylib.tools import hello` 并 `python -m` 运行。
4. `__all__ = ["a"]` 的模块里有 `b`，星号导入后怎么拿到 `b`？
> 答案：`import m; m.b` 或 `from m import b`——`__all__` 只管 `import *`。
5. `ModuleNotFoundError: No module named 'mylib'`，列两个最可能原因和验证命令。
> 答案：①mylib 不在 `sys.path`（打印 `sys.path` 对照）；②运行位置不对（改在项目根 `python -m`）。
6. 建隔离环境并一行证明隔离生效。
> 答案：`python3 -m venv .venv`（缺 ensurepip 加 `--without-pip`）后 `import sys; print(sys.prefix != sys.base_prefix)` → `True`。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-12 异常](py-12-exceptions.md) ｜ ➡️ 下一篇：[py-14 标准库](py-14-stdlib.md)
