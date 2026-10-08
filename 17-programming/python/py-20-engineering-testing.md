# py-20 工程化与测试 — 记忆编码

> **📍 本章导航**：前置 → [py-13 模块包](py-13-modules-packages.md) ｜ 相关 → [py-12 异常](py-12-exceptions.md)·[py-17 类型](py-17-typing-modern.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐ ｜ 阅读 ~13min（约 9k tokens）
>
> 本章逻辑链：py-19 会优化单个程序了 → 本篇解决"项目怎么摆、质量怎么守、怎么交给别人维护" → 全库收尾，衔接 py-21 易混表与 py-22 复习系统。意象域：**4S 店质检流水线**（功能分区/质检单/广播站/出厂检测线），锚点不越域。
> 工具链输出全部实测（Python 3.12.3 ／ pytest 9.1.1 ／ ruff 0.16.10 ／ mypy 2.4.0 ／ poetry 2.5.1 ／ uv 0.12.23）。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 功能分区先摆对 | PY-20-01 | 项目结构决定好不好维护 |
| 质检单三件套 | PY-20-02~05 | 写检测、备工位、批量过检、测故障 |
| 广播站与开关牌 | PY-20-06~08 | 日志分级、喇叭配置、环境配置 |
| 出厂检测线 | PY-20-09~11 | 三件套检查、进货管家、极速物流 |
| 自动年检与排故 | PY-20-12,13 | CI 流水线、调试三板斧 |

## 一、功能分区先摆对（项目结构）
### PY-20-01 项目结构 src 布局
- **是什么**：约定式目录：`src/包名/` 放代码、`tests/` 放测试、`pyproject.toml` 放元数据，即"4S 店功能分区图"。
- **为什么**：痛点：脚本、测试、数据堆一个文件夹，三个月后自己都找不到入口 → 机制：src 布局让"源码"和"随手跑的脚本"物理隔离，测试只能按安装后的方式导入 → 行为：`pytest` 通过 `pythonpath=["src"]` 找到包 → 边界：小脚本不必全套，超过 3 个文件就该分区。
- **怎么写**：实测最小项目（`demo_proj/`）：
```
demo_proj/
├── pyproject.toml        # 元数据 + 工具配置
├── src/mymath/           # 源码包
│   ├── __init__.py
│   └── core.py
└── tests/test_core.py    # 测试
```
→ 运行验证：`PYTHONPATH=src python3 -c "from mymath.core import add; print('add(2, 3) =', add(2, 3))"` 输出 `add(2, 3) = 5`；`python3 -m pytest -q` 输出 `1 passed in 0.16s`
- **何时用/不用**：要做成包/多人协作必上；一次性分析脚本随意，但测试还是要写。
- **锚点**：**4S 店功能分区**——展厅（src）、车间（tests）、库房（data）、客户区（docs）各归各位，进店的人不用问路。
- **易错**：测试文件放 src 里会被当成源码发布；缺 `__init__.py`（或未配 pythonpath）导入直接 ModuleNotFoundError。
- **关联**：`→ PY-13-03：包与 __init__.py 机制`　`→ PY-20-02：tests/ 里放什么`

## 二、质检单三件套（pytest）
### PY-20-02 pytest 基础
- **是什么**：pytest 是"质检单"框架：`test_` 开头的函数 + `assert` 断言，跑 `python3 -m pytest -q` 出结果。
- **为什么**：痛点：改一行代码靠手工点点点验证，回归全靠运气 → 机制：pytest 自动发现并执行测试函数，断言失败即报"哪行、实际值、期望值" → 行为：`2 passed`；失败时给出 `assert 3 == 4` 级别的现场 → 边界：测试函数不能有返回值；测试之间应互相独立。
- **怎么写**：
```python
def add(a, b):
    return a + b
def test_add():
    assert add(1, 2) == 3
def test_add_negative():
    assert add(-1, 1) == 0
```
→ 运行输出（`python3 -m pytest -q test_calc.py`）：`2 passed in 0.15s`；故意写错期望值时输出（截取核心行）：
```
>       assert add(1, 2) == 4
E       assert 3 == 4
E        +  where 3 = add(1, 2)
1 failed in 0.10s
```
- **何时用/不用**：写函数就配测试，越早写越省；纯探索性分析可以后补。
- **锚点**：**质检单**——每辆车（函数）过检一项打一个勾（assert），不合格项直接圈出实测值和标准值。
- **易错**：文件名/函数名不符合 `test_*` 约定就静默"0 个测试"，以为没 bug 其实没跑。
- **关联**：`→ PY-20-03：测试数据用 fixture 备`　`→ PY-20-12：CI 里自动跑的就是它`

### PY-20-03 fixture 测试夹具
- **是什么**：`@pytest.fixture` 是"检测前的准备工位"：按需为每个测试现场造数据/环境，用完自动收。
- **为什么**：痛点：每个测试都写一遍"造数据"样板，改一处要改十处 → 机制：fixture 按名字注入，每调用一次重新执行一遍工厂逻辑 → 行为：两个用例各拿一份全新 `sample_list` → 边界：fixture 之间也能互相注入；重型 fixture 可设 `scope` 复用。
- **怎么写**：
```python
import pytest
@pytest.fixture
def sample_list():                 # 每个用例各拿一份全新数据
    print("  [准备] 造一份测试数据")
    return [3, 1, 2]
def test_sorted(sample_list):      # 参数名 = fixture 名，自动注入
    assert sorted(sample_list) == [1, 2, 3]
def test_len(sample_list):
    assert len(sample_list) == 3
```
→ 运行输出（`pytest -q -s test_fix.py`）：`  [准备] 造一份测试数据` / `.  [准备] 造一份测试数据` / `.` / `2 passed in 0.15s`（打印与进度点交错）
- **何时用/不用**：任何"测试前要先造的东西"都做成 fixture；一次性的简单值直接在用例里写更直白。
- **锚点**：**准备工位**——每辆车开上工位，技师先铺护套、摆工具（fixture），检测完工位复原给下一辆。
- **易错**：fixture 名写错（不匹配）会报"fixture not found"；在 fixture 里藏断言会让失败点难找。
- **关联**：`→ PY-20-02：pytest 基础`　`→ PY-20-04：参数化管批量，fixture 管准备`

### PY-20-04 参数化 parametrize
- **是什么**：`@pytest.mark.parametrize("n, expected", [...])` 一个用例函数批量喂多组数据，自动生成多个测试项。
- **为什么**：痛点：同类逻辑测 5 组数据复制 5 个函数 → 机制：装饰器为每组参数生成独立测试项，失败时点名是哪组 → 行为：4 组参数输出 `....` 四个点 → 边界：参数组之间不要有顺序依赖；大数据组考虑放到文件里读。
- **怎么写**：
```python
import pytest
@pytest.mark.parametrize("n, expected", [(2, True), (3, False), (0, True), (-4, True)])
def test_is_even(n, expected):
    assert (n % 2 == 0) == expected
```
→ 运行输出（`pytest -q test_param.py`）：`4 passed in 0.05s`
- **何时用/不用**：同一函数的边界值/典型值批量测；逻辑不同的用例别硬塞进一个参数化。
- **锚点**：**批量过检线**——同款检测项目（如灯光检）连过 4 边车，每辆车一张成绩单。
- **易错**：参数组全用同一个可变对象（如一个 list），某用例改了会影响后面的组（同 PY-17-07 的共享坑）。
- **关联**：`→ PY-20-03：fixture 造数据，参数化喂数据`　`→ PY-20-05：测异常也是参数化好搭档`

### PY-20-05 pytest.raises 测异常
- **是什么**：`with pytest.raises(ValueError):` 断言"这段代码必须抛出指定异常"，把异常路径也纳入质检。
- **为什么**：痛点：只测正常输入，错误处理永远没被走过，上线才炸 → 机制：上下文管理器捕获异常类型与文案（`match=` 正则），没抛或抛错类型则测试失败 → 行为：`3 passed`（正常/异常/报错文案三查）→ 边界：`pytest.raises` 内只放"必须抛"的最小代码。
- **怎么写**：
```python
import pytest
def parse_age(text):
    return int(text)
def test_parse_ok():
    assert parse_age("30") == 30
def test_parse_bad():
    with pytest.raises(ValueError):
        parse_age("十八")
def test_parse_bad_message():
    with pytest.raises(ValueError, match="invalid literal"):
        parse_age("abc")
```
→ 运行输出（`pytest -q test_age.py`）：`3 passed in 0.07s`
- **何时用/不用**：函数会抛异常就必须测异常分支（PY-12 的 try/except 同理）；不抛异常的纯计算不需要。
- **锚点**：**故意踩刹车测故障码**——质检员故意踩一脚刹车，看仪表盘是不是报出预期的故障码（异常类型+文案都对才算过）。
- **易错**：`pytest.raises` 包住的代码太多，别的行抛异常也被当成"测过"，掩盖真问题。
- **关联**：`→ PY-12-05：异常层级决定 except 精度`　`→ PY-20-02：断言家族`

## 三、广播站与开关牌（logging 与配置）
### PY-20-06 logging 分级
- **是什么**：`logging` 五级广播：DEBUG < INFO < WARNING < ERROR < CRITICAL，`basicConfig(level=...)` 设定播出门槛。
- **为什么**：痛点：满屏 print 调试信息，上线忘了删，真错误被淹 → 机制：低于设定级别的消息直接不发；级别随环境可调（开发看 DEBUG，生产只看 WARNING+）→ 行为：设 INFO 后 DEBUG 被拦、其余四档播出 → 边界：`basicConfig` 是 root 全局配置只生效一次。
- **怎么写**：
```python
import logging
logging.basicConfig(level=logging.INFO)   # 只放行 INFO 及以上
logging.debug("调试：工单 #42 的螺丝扭矩 12N·m")   # 被拦下
logging.info("信息：车辆进场登记")
logging.warning("警告：机油剩余 10%")
logging.error("错误：刹车片磨损超限")
logging.critical("致命：发动机无法启动")
```
→ 运行输出（DEBUG 一行被过滤）：`INFO:root:信息：车辆进场登记` / `WARNING:root:警告：机油剩余 10%` / `ERROR:root:错误：刹车片磨损超限` / `CRITICAL:root:致命：发动机无法启动`
- **何时用/不用**：程序里的观察信息一律 logging；给最终用户看的正式输出才用 print。
- **锚点**：车间**广播喇叭分级**——小事（调试）不广播，进场（信息）念一条，故障（警告/错误）全厂响。
- **易错**：用 print 排查问题，上线删漏一行；`basicConfig` 重复调用不生效（要先 `basicConfig(force=True)` 或用 handler）。
- **关联**：`→ PY-20-07：喇叭怎么接线`　`→ PY-20-13：调试第②法`

### PY-20-07 logging 配置：logger/handler/formatter
- **是什么**：三层组装：`logger`（发消息的部门）→ `handler`（喇叭/录音机：输出到哪）→ `formatter`（播音稿格式）。
- **为什么**：痛点：消息想同时进控制台和文件，格式还要带时间 → 机制：一个 logger 挂多个 handler，各 handler 有自己的 formatter → 行为：控制台+文件双输出，格式 `时间 级别 消息` → 边界：logger 有层级（`logging.getLogger("4s店")`），子 logger 会向上传播。
- **怎么写**：
```python
import logging
fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
console = logging.StreamHandler(); console.setFormatter(fmt)
fileh = logging.FileHandler("service.log", encoding="utf-8"); fileh.setFormatter(fmt)
logger = logging.getLogger("4s店"); logger.setLevel(logging.DEBUG)
logger.addHandler(console); logger.addHandler(fileh)
logger.info("车辆进场登记")
logger.error("检测到故障码 P0300")
```
→ 运行输出：`09:39:04 INFO     车辆进场登记` / `09:39:04 ERROR    检测到故障码 P0300`（时间戳为运行时刻）；文件内容同这两行
- **何时用/不用**：正式项目用 dictConfig/yaml 配置更整洁；小脚本 `basicConfig` 够用。
- **锚点**：**广播站三件套**——广播室里：发话的部门（logger）对着喇叭（console handler）和录音机（file handler）念统一格式的播音稿（formatter）。
- **易错**：重复 `addHandler` 导致日志打两遍；忘了 `setFormatter` 输出没有时间没法排障。
- **关联**：`→ PY-20-06：分级是门槛`　`→ PY-14-12：logging 标准库概览`

### PY-20-08 配置管理
- **是什么**：把"环境相关"的值（数据库地址、开关）交给环境变量/配置文件，代码只读配置对象。
- **为什么**：痛点：开发库地址写死在代码里，上线改代码有风险 → 机制：`os.environ.get(KEY, 默认值)` 读注入的环境变量 → 行为：同一份代码开发机走默认 sqlite，服务器被环境变量切成 mysql → 边界：秘密（密码）永远进环境变量/密钥管理，不进代码仓库。
- **怎么写**：
```python
import os
from dataclasses import dataclass
@dataclass(frozen=True)
class Settings:
    db_url: str
    debug: bool
def load_settings() -> Settings:
    return Settings(db_url=os.environ.get("APP_DB_URL", "sqlite:///default.db"),
                    debug=os.environ.get("APP_DEBUG", "0") == "1")
print("默认配置(开发机):", load_settings())
os.environ["APP_DB_URL"] = "mysql://prod-db/app"
os.environ["APP_DEBUG"] = "1"
print("环境变量覆盖(服务器):", load_settings())
```
→ 运行输出：`默认配置(开发机): Settings(db_url='sqlite:///default.db', debug=False)` ／ `环境变量覆盖(服务器): Settings(db_url='mysql://prod-db/app', debug=True)`
- **何时用/不用**：换环境就变的值都进配置；业务常量（如税率表）放代码或数据文件即可。
- **锚点**：**工位开关牌**——同一个工位，白天/夜班插不同的开关牌（环境变量），设备（代码）不用改装。
- **易错**：配置在 import 时读一次就缓存，运行中改环境变量不生效；调试开关写死 True 忘了关。
- **关联**：`→ PY-17-07：Settings 用 frozen dataclass 防误改`　`→ PY-15-05：配置文件读取`

## 四、出厂检测线（工具链）
### PY-20-09 ruff / black / mypy 三件套
- **是什么**：出厂前三道检测线：`ruff` 查错误与坏味道（lint）、`black` 统一格式（format）、`mypy` 验类型（→ PY-17-12）。
- **为什么**：痛点：代码风格争论浪费时间，低级错误流到线上 → 机制：机器按规则逐行检查，风格问题自动改、错误问题点名报 → 行为：同一份"有毛病"文件三件套各报各的 → 边界：ruff/black 管形式不管逻辑，mypy 管类型不管算法。
- **怎么写**：对故意写坏的 `test_49.py`（未用导入、格式乱、类型错）：
→ 实测输出：
```
$ ruff check test_49.py
I001 [*] Import block is un-sorted or un-formatted
F401 [*] `os` imported but unused
Found 2 errors.
[*] 2 fixable with the `--fix` option.
$ black --check test_49.py
would reformat test_49.py
1 file would be reformatted.
$ mypy test_49.py
test_49.py:7: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]
Found 1 error in 1 file (checked 1 source file)
```
改对后（`test_49b.py`）三线全绿：`All checks passed!` / `All done! ✨ 🍰 ✨`＋`1 file would be left unchanged.` / `Success: no issues found in 1 source file`
- **何时用/不用**：正式项目全上并接入 CI；临时脚本至少跑 ruff。
- **锚点**：**出厂三道检测线**——外观检（ruff 查毛病）、抛光线（black 拉平格式）、底盘测功机（mypy 验类型），三关都绿才准出厂。
- **易错**：把 black 的格式建议当语法错误去改逻辑；mypy 报错就随手 `# type: ignore` 掩盖。
- **关联**：`→ PY-17-12：mypy 专篇`　`→ PY-20-12：三件套进 CI`

### PY-20-10 poetry 依赖与打包
- **是什么**：poetry 是"进货管家"：`pyproject.toml` 写订货单（依赖+元数据），`poetry.lock` 锁死实际进货版本。
- **为什么**：痛点：requirements.txt 和打包配置两套账，依赖版本漂移 → 机制：一个 pyproject 统管依赖/构建/工具配置，lock 文件保证人人装同版本 → 行为：`poetry new demo_pkg` 秒建标准项目骨架 → 边界：poetry 自建虚拟环境管理，团队要统一用它。
- **怎么写**：实测命令卡：
```
① poetry --version        → Poetry (version 2.5.1)
② poetry new demo_pkg     → Created package demo_pkg in demo_pkg
③ 查看骨架                → demo_pkg/README.md / pyproject.toml / src/demo_pkg/__init__.py / tests/__init__.py
④ poetry install          → 按 lock 装依赖（首次会生成 poetry.lock）
```
- **何时用/不用**：要发布/多人协作的包用 poetry（或 uv）；单文件脚本不需要。
- **锚点**：**进货管家**——订货单（pyproject）交给管家，管家锁进一本进货账（lock），下次照账进货一件不差。
- **易错**：手改 `poetry.lock` 造成账实不符；`poetry install` 和 `pip install` 混用把环境搞成两套账。
- **关联**：`→ PY-20-01：pyproject 是项目结构的户口本`　`→ PY-20-11：uv 是同赛道的快管家`

### PY-20-11 uv 极速环境工具
- **是什么**：uv 是 Rust 写的"极速配件物流"：`uv venv` 秒建虚拟环境，`uv pip install` 秒装包，还能管项目依赖。
- **为什么**：痛点：pip/venv 慢、工具链碎片化（装环境半小时）→ 机制：单二进制 + 全局缓存 + 并行下载 → 行为：`uv venv` 即建环境，装 six 实测毫秒级（83ms） → 边界：生态较新，与 poetry 的 lock 格式不同，团队要选边站。
- **怎么写**：实测命令卡：
```
① uv --version            → uv 0.12.23 (x86_64-unknown-linux-gnu)
② uv venv demo_venv       → Creating virtual environment at: demo_venv
③ uv pip install --python demo_venv/bin/python six
                          → Installed 1 package in 83ms / + six==1.17.0（毫秒数随环境波动）
④ 验证 import              → six 1.17.0 装进了隔离环境
```
- **何时用/不用**：新项目/CI 提速强烈推荐；已深度绑定 poetry 的存量项目别中途换轨。
- **锚点**：**极速配件物流**——普通物流（pip）走陆运，uv 是同城闪送：下单到装车毫秒级。
- **易错**：uv 默认不激活环境，直接 `python` 仍用系统解释器，要用 `uv run` 或指定 `--python`。
- **关联**：`→ PY-13-08：venv/virtualenv 的原理`　`→ PY-20-10：poetry 对照`

## 五、自动年检与排故（CI 与调试）
### PY-20-12 CI 持续集成概念
- **是什么**：CI（持续集成）= 每次提交代码自动跑"检测流水线"：装依赖 → ruff/black/mypy → pytest，全绿才允许合并。
- **为什么**：痛点："在我机器上是好的"，合并后全组跑不动 → 机制：云端每次提交都从零装环境跑全套检查，结果直接挂在 PR 上 → 行为：三件套+测试任一红灯就挡合并 → 边界：CI 只保证"没破坏已测的部分"，覆盖率之外的逻辑照样漏。
- **怎么写**：`.github/workflows/ci.yml` 骨架（片段不可直接运行，本地等价命令见下）：
```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e . pytest ruff black mypy
      - run: ruff check . && black --check . && mypy . && pytest -q
```
→ 本地等价验证（实测）：`python3 -m pytest -q test_calc.py` 输出 `2 passed in 0.15s`；三件套输出见 PY-20-09
- **何时用/不用**：任何多人项目第一天就接 CI；纯本地一次性脚本不用。
- **锚点**：**自动年检流水线**——车（代码）每次进厂（提交）都自动上一遍检测线，红灯不放行出厂（合并）。
- **易错**：CI 里"先跳过测试"图快，流水线退化成摆设；只在本地跑测试不跑三件套。
- **关联**：`→ PY-20-09：CI 里跑的三件套`　`→ PY-20-02：CI 里跑的测试`

### PY-20-13 调试三法（print/assert、logging、pdb）
- **是什么**：排故三板斧：①print/断言现场看值 ②logging 分级留痕 ③pdb 逐行停看（`python3 -m pdb 脚本.py`）。
- **为什么**：痛点：bug 藏在中间变量里，肉眼看代码看不出来 → 机制：三法递进——print 看一眼、logging 留证据、pdb 冻住现场逐帧查 → 行为：pdb 在断点停住后 `p 变量` 看现场、`n` 单步 → 边界：print 一次性问题够用；线上问题用 logging；复杂状态机值得上 pdb/IDE 断点。
- **怎么写**：pdb 实测（`total_demo.py` 里 `total += p * rate` 处设断点；输出路径截短）：
```
命令流：b 5 → c → p p → n → p total → c → p p → p total → c → q
(Pdb) Breakpoint 1 at .../total_demo.py:5
(Pdb) > ...(5)total_price()   → total += p * rate
(Pdb) 100          # p p：第一个价格
(Pdb) 80.0         # p total：累计 100*0.8
(Pdb) > ...(5)total_price()   # c：断点第二次命中
(Pdb) 200
(Pdb) 80.0         # p total：第二轮前仍是 80.0
(Pdb) 合计: 240.0   # c：跑完
```
- **何时用/不用**：三五分钟的小 bug 用①；要留档/线上用②；断点级排查用③；三板斧都不行再上 cProfile（PY-19-08）。
- **锚点**：**排故三板斧**——听异响（print 一听）、装行车记录仪（logging 留档）、上举升机逐件拆检（pdb 单步）。
- **易错**：pdb 里 `n`（下一行）和 `s`（进函数）混用，追进底层库出不来（用 `u`/`q` 退出）；调试完忘删 print。
- **关联**：`→ PY-20-06：logging 分级`　`→ PY-12-07：traceback 是排故第一现场`

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| print vs logging | 一次性看值 | 分级留痕可关闭 | 看完要不要留/要不要分级 | 看一眼 print，长期 logging |
| fixture vs 参数化 | 造"测试要用的东西" | 喂"多组输入输出" | 要环境还是要数据 | fixture 备料，参数化上菜 |
| ruff vs black | 查错误坏味道 | 只管格式统一 | 要修 bug 还是要拉平 | ruff 抓坏人，black 理发 |
| poetry vs uv | 全能管家（打包发布强） | 极速物流（装环境快） | 项目要发布还是要快 | 发布找 poetry，提效用 uv |
| CI vs 本地测试 | 每次提交自动跑全套 | 开发者手动跑 | 有没有强制门禁 | 本地自测，CI 把门 |
| assert vs pytest.raises | 断言结果对不对 | 断言"必须报这个错" | 测正常路径还是异常路径 | 对结果用 assert，对异常用 raises |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-20-01 | 项目结构 | 4S 店功能分区图 | 功能分区 |
| PY-20-02 | pytest | 质检单打勾打叉 | 质检单 |
| PY-20-03 | fixture | 准备工位铺护套 | 准备工位 |
| PY-20-04 | parametrize | 批量过检线 | 批量过检 |
| PY-20-05 | pytest.raises | 踩刹车测故障码 | 测故障码 |
| PY-20-06 | logging 分级 | 广播喇叭分级 | 分级广播 |
| PY-20-07 | logging 配置 | 广播室三件套 | 广播室 |
| PY-20-08 | 配置管理 | 工位开关牌 | 开关牌 |
| PY-20-09 | ruff/black/mypy | 出厂三道检测线 | 三道检测线 |
| PY-20-10 | poetry | 进货管家+进货账 | 进货管家 |
| PY-20-11 | uv | 极速配件物流 | 闪送物流 |
| PY-20-12 | CI | 自动年检流水线 | 自动年检 |
| PY-20-13 | 调试三法 | 排故三板斧 | 三板斧 |

## ✅ 自测清单（合上本篇，先写再看）
1. 写出 src 布局的四个关键路径（项目根下的目录/文件）。
> 答案：`pyproject.toml`、`src/包名/__init__.py`、`src/包名/模块.py`、`tests/test_*.py`。
2. 写一个 fixture `db` 返回内存字典，并在测试中使用它。
> 答案：`@pytest.fixture` 装饰 `def db(): return {}`；测试签名 `def test_x(db):` 自动注入。
3. 用参数化测 `abs(x)` 的三组数据（含负数与零）。
> 答案：`@pytest.mark.parametrize("x, expected", [(3,3),(-3,3),(0,0)])` + `assert abs(x) == expected`。
4. 生产环境只看 WARNING 以上日志，一行怎么配？
> 答案：`logging.basicConfig(level=logging.WARNING)`（或 logger.setLevel）。
5. 调试时想在第 5 行停下来看变量 `total`，pdb 命令序列是什么？
> 答案：`b 5` → `c` → `p total`（跑完 `q` 退出）。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-19 内存与性能](py-19-memory-performance.md) ｜ ➡️ 下一篇：[py-21 易错与面试](py-21-pitfalls-interview.md)
