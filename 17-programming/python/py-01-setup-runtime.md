# py-01 环境搭建与运行 — 记忆编码

> **📍 本章导航**：前置 → 无（阶段 0 起点）｜ 相关 → [py-13 模块与包](py-13-modules-packages.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐ ｜ 阅读 ~12min（约 9k tokens）
>
> 本章逻辑链：py-00 画好了登山地图 → 本篇解决"开工第一步：灶台怎么点火、菜谱怎么写、食材怎么进厨房" → 引出 py-02"数据这盘菜怎么摆"。

## 🗺️ 本篇知识地图

| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 灶台点火三件套 | PY-01-01~03 | 认识解释器、确认版本、跑通第一行代码 |
| 试味与整桌宴席 | PY-01-04~05 | REPL 现场试味，脚本照菜谱做整桌 |
| 菜谱书写规矩 | PY-01-06~09 | 冒号起块、缩进定层级、注释与编码 |
| 食材供应线 | PY-01-10~12 | pip 采购、venv 独立厨房、清单复现 |
| 灶台保养与自查 | PY-01-13~16 | 备菜盒、说明书、报警读法、厨房守则 |

## 一、灶台点火三件套

### PY-01-01 解释器与 CPython Interpreter
- **是什么**：解释器（interpreter）是把 Python 源码逐句翻译成机器可执行指令的程序；官方实现叫 CPython。
- **为什么**：痛点：CPU 只认机器码 → 机制：解释器先把源码编译成字节码（bytecode）再在虚拟机上执行 → 行为：写完即跑、无需手动编译 → 边界：换实现（PyPy/Jython）速度与兼容性会变。
- **怎么写**：
```python
# test_01.py
import sys
print(sys.version.split()[0])
print(sys.implementation.name)
```
→ 运行输出：`3.12.3` 换行 `cpython`
- **何时用/不用**：定位"这段代码在谁肚子里跑"时用；日常写代码不用管，报错说"某某实现不支持"时才回来查。
- **锚点**：厨房里那位"官方特级厨师"——菜谱（源码）没人看得懂就下锅，全靠他逐句念成动作；菜谱写得他念不下去就是报错。
- **易错**：把 Python 版本（语言）和 CPython（实现）混为一谈；装了 Python 不等于命令是 `python`（见 PY-01-02）。
- **关联**：`→ PY-01-13：字节码的成品半成品就藏在 __pycache__`；`→ PY-18-01：GIL 是 CPython 实现的锁，不是语言的`。

### PY-01-02 版本确认与命令名 python3
- **是什么**：用命令行查看当前解释器版本；Linux/macOS 上标准命令名是 `python3`（version check）。
- **为什么**：痛点：机器上常共存 Python 2 与 3、或多版本 3.x → 机制：`python`/`python3` 各自指向一个可执行文件 → 行为：敲命令前先验版本，可避免"代码没错但版本不对" → 边界：虚拟环境激活后命令指向会变（PY-01-11）。
- **怎么写**：
```bash
$ python3 --version
```
→ 运行输出（实测）：`Python 3.12.3`
- **何时用/不用**：每换一台机器、每个新终端开工前先敲一次；已在同一环境连续工作时不必反复敲。
- **锚点**：菜谱封面印着"2026 年版"——开火前先看封面年份，别拿 20 年前的菜谱做今天的宴席。
- **易错**：在只装了 Python 2 的老机器上 `python --version` 显示 `Python 2.7.x`，照抄 3.x 代码会满屏 `SyntaxError`。
- **关联**：`→ PY-01-05：脚本首行的 shebang 也依赖 python3 这个命令名`。

### PY-01-03 第一个程序与 print()
- **是什么**：`print()` 是把内容输出到屏幕的内置函数（built-in function）。
- **为什么**：痛点：程序在黑盒里算，看不见结果 → 机制：`print` 把对象转成文本写到标准输出（stdout）→ 行为：括号里放什么就显示什么 → 边界：print 只管显示，不等于"返回值"（PY-07 返回值另说）。
- **怎么写**：
```python
# test_03.py
print("你好，Python！")
print(1 + 1)
```
→ 运行输出：`你好，Python！` 换行 `2`
- **何时用/不用**：调试看值、脚本出结果用；写库/模块给别人 import 时少 print，多用 return 与 logging（PY-14）。
- **锚点**：厨房的**出餐口**——菜做好了要从窗口喊出来递给客人，`print` 就是那声"出餐！"。
- **易错**：`print "hi"`（Python 2 写法）在 3.x 报 `SyntaxError`；print 多个值默认空格分隔，要精确拼接用 f-string（PY-02-15）。
- **关联**：`→ PY-02-15：f-string 让 print 输出带上变量值`。

## 二、试味与整桌宴席

### PY-01-04 交互式环境 REPL
- **是什么**：REPL（Read-Eval-Print Loop，读取-求值-打印循环）即敲 `python3` 进入的 `>>>` 交互界面。
- **为什么**：痛点：改一行代码要新建文件、存盘、执行，试错太慢 → 机制：REPL 每读一行就立刻求值并打印 → 行为：随手验证表达式、查看对象 → 边界：关掉窗口代码就没了，正式代码必须落盘成脚本。
- **怎么写**：
```
$ python3
Python 3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 2 ** 10
1024
>>> 'py' * 3
'pypypy'
>>> exit()
```
→ 运行输出（真实终端实录）：见上。
- **何时用/不用**：验证一个小语法、试一个方法时用 REPL 或 `python3 -c "代码"`；超过 5 行的逻辑写脚本文件。
- **锚点**：灶台前的**试味小勺**——汤咸淡舀一勺尝一口就知，不必盛出整锅摆盘。
- **易错**：REPL 里定义的变量/函数退出即失；粘贴多行代码时缩进错乱会得 `IndentationError`（PY-01-07）。
- **关联**：`→ PY-01-14：REPL 里最常用的两个帮手是 dir() 和 help()`。

### PY-01-05 脚本运行与 shebang
- **是什么**：脚本（script）是存成 `.py` 的完整程序；shebang 是首行 `#!/usr/bin/env python3`，告诉系统用哪个解释器执行。
- **为什么**：痛点：REPL 里的好代码关窗即失 → 机制：`python3 文件名` 逐行执行文件；加 shebang 与执行权限后可 `./文件` 直接跑 → 行为：代码可保存复用 → 边界：shebang 只在类 Unix 生效，Windows 用 `python 文件名`。
- **怎么写**：
```python
#!/usr/bin/env python3
print('Hello from a script!')
```
```bash
$ chmod +x hello_demo.py && ./hello_demo.py
```
→ 运行输出（实测）：`Hello from a script!` 且 `returncode = 0`
- **何时用/不用**：一切要保存、复用、交付的代码写成脚本；只验证一个表达式用 REPL（PY-01-04）。
- **锚点**：从"随手试味"升级到"**照整本菜谱做一桌菜**"——菜谱存成册子（.py 文件），封面上写明用哪位厨师（shebang）。
- **易错**：忘了 `chmod +x` 就 `./hello.py` 会得 `Permission denied`；在 Windows 记事本里存成 `hello.py.txt` 会报找不到文件。
- **关联**：`→ PY-01-06：脚本主体就是一串按规矩书写的语句块`。

## 三、菜谱书写规矩

### PY-01-06 语句、冒号与代码块
- **是什么**：冒号（`:`）标志一个代码块（block）的开始，块内是缩进的多条语句（statement）。
- **为什么**：痛点：多条语句要分组归属（if 成立做什么、for 每轮做什么）→ 机制：Python 用冒号+缩进划定块边界，而非 `{}` → 行为：`if/for/while/def/class` 后必跟冒号 → 边界：冒号后同一行写单条语句可以，但块内多条必须缩进（PY-01-07）。
- **怎么写**：
```python
# test_06.py
for i in range(3):
    if i % 2 == 0:
        print(f"{i} 是偶数")
    else:
        print(f"{i} 是奇数")
```
→ 运行输出：`0 是偶数` / `1 是奇数` / `2 是偶数`
- **何时用/不用**：所有分支/循环/函数/类定义都按此规矩；一行式如 `if x: y = 1` 仅用于极简场景。
- **锚点**：菜谱里"**步骤：**"后面永远跟一串动作——看到冒号就知道下面是一套连招。
- **易错**：写 `if x > 0` 忘了冒号，报 `SyntaxError: expected ':'`；冒号是中文全角`：`也报错。
- **关联**：`→ PY-06-01：if/for/while 的完整语法在控制流篇`。

### PY-01-07 缩进 Indentation
- **是什么**：缩进（indentation）是行首的空白，Python 用它区分代码层级；惯例是 4 个空格。
- **为什么**：痛点：靠 `{}` 的语言里格式乱了还能跑，Python 要求"格式即语法" → 机制：解释器按缩进深度建立块结构 → 行为：同一块内缩进必须一致 → 边界：Tab 与空格混用会得 `TabError`。
- **怎么写**：
```python
# test_07.py
src_bad = "def greet():\nprint('hi')\n"
try:
    compile(src_bad, "bad.py", "exec")
except (IndentationError, SyntaxError) as e:
    print(f"{type(e).__name__}: {e}")
```
→ 运行输出：`IndentationError: expected an indented block after function definition on line 1 (bad.py, line 2)`
- **何时用/不用**：永远 4 空格（PEP 8 约定）；接手工项目时保持该项目原有缩进风格。
- **锚点**：菜谱手稿**每个步骤整齐退一格写**——少退一格，主料配料的从属关系就乱了，主厨（解释器）当场打回。
- **易错**：IDE 里 Tab 被替换成 8 空格导致层级错位；复制网页代码带不可见空白，报 `IndentationError` 却肉眼看不出。
- **关联**：`→ PY-01-08：注释的缩进要跟它描述的代码同层`。

### PY-01-08 注释与文档字符串 Docstring
- **是什么**：`#` 开头是行注释；函数/模块首行的三引号字符串是文档字符串（docstring），可被 `help()` 读取。
- **为什么**：痛点：代码只有作者自己看得懂 → 机制：`#` 后内容解释器直接丢弃；docstring 存进对象的 `__doc__` 属性 → 行为：写给未来的自己和队友 → 边界：注释不解释"这行在干什么"（代码本身应自解释），而解释"为什么这么做"。
- **怎么写**：
```python
# test_08.py
def add(a, b):
    """两数相加，返回和。"""
    return a + b  # 行内注释

print(add(2, 3))
print(add.__doc__)
```
→ 运行输出：`5` 换行 `两数相加，返回和。`
- **何时用/不用**：对外函数必写 docstring；临时调试别堆几十行注释，删干净再交付。
- **锚点**：菜谱旁的**铅笔小字**："这道菜少放盐，因为客人血压高"——写的是原因，不是"把盐放进锅"。
- **易错**：三引号忘闭合会一路吃到文件尾得 `SyntaxError`；把 docstring 写在函数体第二行就不算 docstring（`__doc__` 为 None）。
- **关联**：`→ PY-01-14：help() 读的就是 docstring`。

### PY-01-09 源文件编码 UTF-8
- **是什么**：Python 3 源文件默认按 UTF-8（一种 Unicode 编码）读取，中文注释与字符串可直接写。
- **为什么**：痛点：早年源码含中文需在首行声明编码，否则报错 → 机制：PEP 3120 规定默认 UTF-8 → 行为：中文变量名、注释、字符串都合法 → 边界：读写文件时的编码是另一回事，仍需显式指定（PY-15）。
- **怎么写**：
```python
# test_09.py
s = "中文字符串没问题"
print(s)
print(len(s))
```
→ 运行输出：`中文字符串没问题` 换行 `8`
- **何时用/不用**：3.x 项目不必写 `# -*- coding: utf-8 -*-`（写了也无害）；维护 Python 2 遗留文件时才需要它。
- **锚点**：全厨房的食材标签**统一用简体中文印刷**——不用每张标签单独注明"本标签为中文"。
- **易错**：终端/编辑器不是 UTF-8 时显示乱码，被误判为代码错误；Windows 记事本另存为 ANSI 后中文报 `SyntaxError`。
- **关联**：`→ PY-03-15：str 与 bytes 的编码差异在字符串篇展开`。

## 四、食材供应线

### PY-01-10 pip 与 PyPI
- **是什么**：pip 是 Python 包管理器（package manager），从 PyPI（公共包仓库）下载安装第三方库。
- **为什么**：痛点：正则、日期、Web 请求不该每次重写 → 机制：`pip install 包名` 把包下载并放进解释器能找到的 site-packages 目录 → 行为：装完 `import` 即用 → 边界：默认装进当前解释器的环境，多项目混装会互相污染（PY-01-11 解决）。
- **怎么写**：
```bash
$ python3 -m pip --version
$ python3 -m pip install six
```
→ 运行输出（实测）：`pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)`；`[退出码 0] Requirement already satisfied: six in /usr/local/lib/python3.12/dist-packages (1.17.0)`
- **何时用/不用**：需要第三方库时用；标准库（PY-14）已覆盖的功能不必装包。
- **锚点**：厨房旁的**食材采购市场**——缺什么食材（第三方库）就去市场买一份回来放进库房（site-packages）。
- **易错**：`pip` 与 `python3` 不是同一个解释器的配套工具时，"装了却 import 不到"；国内环境建议配镜像源再装。
- **关联**：`→ PY-01-12：安装结果冻结成清单才能复现`；`→ PY-13-12：包从发布到安装的完整链路`。

### PY-01-11 venv 虚拟环境 Virtual Environment
- **是什么**：venv（virtual environment）为单个项目创建独立的解释器与包目录。
- **为什么**：痛点：项目 A 要 Django 2、项目 B 要 Django 4，全局只能装一个 → 机制：venv 目录里放一份解释器链接与独立 site-packages → 行为：激活后 `python`/`pip` 都指向该目录 → 边界：venv 不装新 Python 本体，只复制/链接已有的解释器。
- **怎么写**：
```bash
$ python3 -m venv .venv          # 建环境
$ source .venv/bin/activate       # 激活（Windows：.venv\Scripts\activate）
$ python --version                # 验证
```
→ 运行输出（实测）：`Python 3.12.3`；`sys.prefix` 从系统 `/usr` 变为 `.venv` 的绝对路径（本机实测 `…/pycheck/A/venv_demo`）
- **何时用/不用**：每个正式项目必建；临时跑三行验证代码可不动用。
- **锚点**：**每场宴席一间独立小厨房**——川菜的花椒味不会串到粤菜的汤里；宴席结束（项目删掉）厨房整个撤走。
- **易错**：Debian/Ubuntu 缺 `python3-venv` 时报 `The virtual environment was not created successfully because ensurepip is not available.`（实测原文），按报错提示 `apt install python3.12-venv` 即可；忘了 activate 就 pip install，包又装回了系统环境。
- **关联**：`→ PY-01-10：激活后 pip 才装进这间厨房`；`→ PY-13-13：uv 是新一代更快的环境与包管理工具`。

### PY-01-12 requirements.txt 依赖清单
- **是什么**：requirements.txt 是纯文本的依赖清单，一行一个包（可钉死版本号）。
- **为什么**：痛点：在我机器上能跑，拷给你就缺包 → 机制：`pip install -r requirements.txt` 按清单批量安装 → 行为：环境可复现 → 边界：清单只锁直接依赖的版本，不锁传递依赖（工程级用锁文件，PY-20）。
- **怎么写**：
```bash
$ pip freeze > requirements.txt   # 导出当前环境
$ pip install -r requirements.txt # 按清单复现
```
→ 运行输出（实测，清单含 `six==1.17.0`）：`[退出码 0] Requirement already satisfied: six==1.17.0 in /usr/local/lib/python3.12/dist-packages (from -r requirements.txt (line 1)) (1.17.0)`
- **何时用/不用**：项目交付、上服务器、团队协作必写；一次性小脚本不必。
- **锚点**：**采购清单**——新厨师（新同事）拿着清单跑一趟市场，就能把厨房备得跟你一模一样。
- **易错**：把 `pip freeze` 全量清单当手写清单，会装出一堆没用的包甚至冲突；`>=` 可能装到不兼容的新版。
- **关联**：`→ PY-20-05：工程级依赖管理（poetry/uv）在工程篇`。

## 五、灶台保养与自查

### PY-01-13 __pycache__ 与 .pyc
- **是什么**：导入模块时，解释器把源码编译成字节码缓存在 `__pycache__/` 目录下的 `.pyc` 文件。
- **为什么**：痛点：每次 import 都重新编译太慢 → 机制：只有源码变过才重编译，否则直接用缓存 → 行为：二次启动明显变快 → 边界：删掉缓存不影响正确性，只是下次稍慢；改了源码却看到旧结果，多半是缓存或改错文件。
- **怎么写**：
```python
# test_13.py：建个模块导入一次，再看目录
import os, subprocess, sys
os.makedirs("pkgdemo", exist_ok=True)
open("pkgdemo/food.py", "w").write("X = 1\n")
subprocess.run([sys.executable, "-c", "import pkgdemo.food"], check=True)
print(sorted(os.listdir("pkgdemo")))
```
→ 运行输出：`['__pycache__', 'food.py']`（实测进 `__pycache__` 一查是 `['food.cpython-312.pyc']`，未打印）
- **何时用/不用**：交付代码、排查"改了没生效"时想到它；平时无需理会。
- **锚点**：**备菜盒**——切好的配菜（字节码）装盒贴标签放冰箱，下回直接取用；菜谱（源码）一改，这盒就倒掉重切。
- **易错**：把 `__pycache__` 提交进 git（应加进 `.gitignore`）；`python3 -B` 可禁用缓存，别在生产环境乱开。
- **关联**：`→ PY-01-01：字节码就是解释器的中间产物`。

### PY-01-14 dir() 与 help()
- **是什么**：`dir(对象)` 列出对象的属性与方法名；`help(对象/方法)` 显示官方说明文档。
- **为什么**：痛点：记不住方法名、参数记混 → 机制：dir 遍历对象的 `__dict__` 等结构给出名字清单；help 读取 docstring（PY-01-08）渲染 → 行为：不查网页也能自查 → 边界：dir 只给名字不给用法，用法看 help 或官网文档。
- **怎么写**：
```python
# test_14.py
print("upper" in dir(str))
print(str.upper.__doc__)
```
→ 运行输出：`True` 换行 `Return a copy of the string converted to uppercase.`
- **何时用/不用**：忘方法名时 dir，懂了名字但不知参数时 help；熟练后直接查文档更快。
- **锚点**：灶台旁的**厨具说明书抽屉**——不知道这把刀（对象）能干什么，拉开抽屉（dir）看清单，再翻对应说明书（help）。
- **易错**：`help()` 在脚本里输出长文刷屏，应放 REPL 里用；dir 输出按字母序，不代表调用顺序。
- **关联**：`→ PY-01-04：REPL 是用这对帮手的最佳场所`。

### PY-01-15 启动期常见报错读法
- **是什么**：写代码头几天最常撞的四类错误：SyntaxError（语法）、IndentationError（缩进）、NameError（名字未定义）、FileNotFoundError（文件不存在）。
- **为什么**：痛点：满屏 Traceback 不知从哪看 → 机制：错误类型、消息、文件与行号都写在最后几行 → 行为：先读最后一行"类型：消息"，再按行号回源码 → 边界：消息是英文但结构固定，记类型名即可。
- **怎么写**：
```python
# test_15.py：把四种错误各触发一次
demos = [
    lambda: compile("if True print('x')", "demo.py", "exec"),  # 语法错
    lambda: 1 / 0,                # 除零
    lambda: nope,                 # 名字未定义
    lambda: open("不存在的文件.txt"),  # 文件不存在
]
for demo in demos:
    try:
        demo()
    except BaseException as e:
        print(f"{type(e).__name__}: {e}")
```
→ 运行输出（实测四条）：`SyntaxError: invalid syntax (demo.py, line 1)`；`ZeroDivisionError: division by zero`；`NameError: name 'nope' is not defined`；`FileNotFoundError: [Errno 2] No such file or directory: '不存在的文件.txt'`
- **何时用/不用**：每次报错先自己按"类型→消息→行号"三步读；连读三遍仍不懂再搜/问人。
- **锚点**：灶台的**报警蜂鸣器**——不同的响法对应不同险情：短促尖叫（SyntaxError=语法当场错）、长鸣（NameError=找不到食材）。
- **易错**：只盯着报错第一行的文件路径发愁，真正的答案在最后一行；改错时一次改多处，新错掩盖旧错。
- **关联**：`→ PY-12-01：可预期的运行期错误应当用 try/except 接住`；`→ PY-12-06：Traceback 的完整读法在异常篇`。

### PY-01-16 import this 与 PEP 8
- **是什么**：`import this` 打印 Python 之禅（The Zen of Python）；PEP 8 是官方风格指南（4 空格缩进、命名小写下划线等）。
- **为什么**：痛点：能跑的代码人人写法不同，读起来费劲 → 机制：之禅给价值观、PEP 8 给可执行细则 → 行为：社区风格趋同，一眼可读 → 边界：风格非语法，违反不报错（ruff 会警告）。
- **怎么写**：
```python
# test_16.py
import this
```
→ 运行输出（实测节选）：`The Zen of Python, by Tim Peters / Beautiful is better than ugly. / Explicit is better than implicit.`（全文 20 行）
- **何时用/不用**：入门期读一遍建立审美；争论写法时用它裁决。
- **锚点**：厨房墙上挂的**灶王爷前的守则牌**——"明火不离人、刀具归位"，新人第一天先拜读。
- **易错**：把之禅当教条钻牛角尖；它说的是权衡（"Simple is better than complex" 的下一句是"Complex is better than complicated"）。
- **关联**：`→ PY-20-06：ruff/black 自动执行风格检查`。

## ⚔️ 对比消混表

| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| REPL vs 脚本 | 关窗即失的临时会话 | 落盘的 `.py` 文件 | 要不要保存复用 | 试味用勺，宴席用菜谱 |
| `python` vs `python3` | 可能指 Python 2 | 明确指 3.x | 敲 `--version` 验明正身 | 先问版本再动手 |
| pip 装在哪 | 系统/全局环境 | venv 激活后的项目环境 | 看 `which python` | 先进厨房再买菜 |
| `# 注释` vs docstring | 给人看的旁注，解释器丢弃 | 存进 `__doc__`，help 可读 | 要不要被 help() 读到 | 旁注用井号，说明书用三引号 |
| `.py` vs `.pyc` | 源码，人写人读 | 字节码缓存，机器用 | 改代码后要不要重新生成 | 源码是菜谱，pyc 是备菜 |

## 📌 锚点登记表

| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-01-01 | 解释器/CPython | 官方特级厨师念菜谱 | 特级厨师 |
| PY-01-02 | 版本确认 | 菜谱封面年份 | 封面年份 |
| PY-01-03 | print | 出餐口喊"出餐" | 出餐口 |
| PY-01-04 | REPL | 灶台前试味小勺 | 试味勺 |
| PY-01-05 | 脚本/shebang | 整本菜谱+封面厨师名 | 菜谱成册 |
| PY-01-06 | 冒号与代码块 | "步骤："后一串动作 | 步骤冒号 |
| PY-01-07 | 缩进 | 菜谱手稿步骤退一格写 | 退一格 |
| PY-01-08 | 注释/docstring | 菜谱旁铅笔小字 | 铅笔小字 |
| PY-01-09 | UTF-8 | 标签统一简体印刷 | 统一标签 |
| PY-01-10 | pip/PyPI | 食材采购市场 | 采购市场 |
| PY-01-11 | venv | 一间独立小厨房 | 独立厨房 |
| PY-01-12 | requirements.txt | 采购清单 | 采购清单 |
| PY-01-13 | __pycache__/.pyc | 冰箱里的备菜盒 | 备菜盒 |
| PY-01-14 | dir/help | 厨具说明书抽屉 | 说明书抽屉 |
| PY-01-15 | 常见报错 | 灶台报警蜂鸣器 | 报警蜂鸣 |
| PY-01-16 | import this/PEP 8 | 墙上的守则牌 | 守则牌 |

## ✅ 自测清单（合上本篇，先写再看）

1. 写出确认当前 Python 版本的命令，并写出输出格式。
> 答案：`python3 --version` → `Python 3.12.3`（版本号随环境而变，格式固定）。
2. 不查资料，写出 REPL 里验证 `2 ** 10` 的会话三行（提示符、输入、输出）。
> 答案：`>>> 2 ** 10` 回车后显示 `1024`。
3. `def greet():` 下一行顶格写 `print('hi')`，报什么错？末尾括号里是什么？
> 答案：`IndentationError: expected an indented block after function definition on line 1`，括号里是文件名与行号 `(bad.py, line 2)`。
4. 写出创建并激活虚拟环境的两条命令（Linux/macOS），并说出解决什么痛点。
> 答案：`python3 -m venv .venv`；`source .venv/bin/activate`；解决多项目依赖互相污染。
5. `import` 一个模块后，磁盘上多了什么？删掉会怎样？
> 答案：`__pycache__/` 目录，内含 `模块名.cpython-312.pyc`；删掉不影响正确性，只是下次导入重新编译。

## 📍 导航

> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-00 学习路线图](py-00-roadmap.md) ｜ ➡️ 下一篇：[py-02 变量与类型](py-02-variables-types.md)
