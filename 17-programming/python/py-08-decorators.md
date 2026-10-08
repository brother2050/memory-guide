# py-08 装饰器 — 记忆编码
> **📍 本章导航**：前置 → [py-07 函数](py-07-functions.md) ｜ 相关 → [py-09 OOP](py-09-oop.md)·[py-14 标准库](py-14-stdlib.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐⭐ ｜ 阅读 ~11min（约 8k tokens）
>
> 本章逻辑链：py-07 留下问题"想给流水线加功能又不改车间"→ 本篇用"装修队"讲透装饰器（不改毛坯房，贴一层增强）→ 引出 py-09"更系统的复用：家族企业式的类与继承"。意象域：装修（毛坯房/墙纸/工头/合同）。
## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 装修原理：收毛坯还精装 | PY-08-01~04 | 不改原函数，包一层增强 |
| 门牌与身份 | PY-08-05~06 | wraps 把原房主门牌挂回去 |
| 装修合同：带参装饰器 | PY-08-07~08 | 合同带条款，三层套娃 |
| 工头亲自上：类装饰器 | PY-08-09~10 | 可调用对象也能当装修队 |
| 叠装与套餐 | PY-08-11~15 | 先包最里层，partial 预付定金 |

## 一、装修原理：收毛坯还精装（口号："房子不改结构，只加装修"）
### PY-08-01 装饰器与高阶函数 Decorator / Higher-Order Function
- **是什么**：装饰器（decorator）是"收进一个函数、还出一个函数"的高阶函数（higher-order function），不改原函数源码就加功能。
- **为什么**：日志/计时/鉴权想加给几十个函数、改源码会改出一片 → 把原函数当参数收进外层、内层 wrapper 里夹带增强 → 调用的其实是装修后的房子 → 边界：必须返回一个函数（一般 return wrapper）。
- **怎么写**：
```python
def deco(func):             # 装修队接下毛坯房
    def wrapper():
        print("贴墙纸+装灯") # 装修动作
        func()              # 原房照常住人
    return wrapper          # 还一套精装房
def house():
    print("毛坯房可用")
house = deco(house); house()   # 手动装修后入住
```
→ 运行输出：贴墙纸+装灯 ／ 毛坯房可用
- **何时用/不用**：横切功能（计时/日志/重试）≥2 处复用就上装饰器；单处一次性逻辑直接写进函数。
- **锚点**：装修队收一套毛坯房（原函数），施工后还一套精装房——结构没改，只是多了装修。
- **易错**：忘了 `return wrapper`，调用处报 'NoneType' object is not callable。
- **关联**：→ PY-08-02：@ 只是把"手动装修"这行写到函数头顶
### PY-08-02 @ 语法糖 Syntactic Sugar
- **是什么**：`@deco` 写在函数定义上方，等价于定义后立刻执行 `func = deco(func)`。
- **为什么**：手动写 `house = deco(house)` 容易忘 → 解释器在 def 后自动做一次重新绑定 → 原名指向新函数对象 → 边界：deco 必须先定义（写在被装饰函数之前）。
- **怎么写**：
```python
def deco(func):
    def wrapper():
        print("装修队进场")
        func()
    return wrapper
@deco                       # 等价于 house = deco(house)
def house(): print("毛坯房可用")
house()
```
→ 运行输出：装修队进场 ／ 毛坯房可用
- **何时用/不用**：一律用 @；需要"按配置决定装不装"的条件装饰才手动赋值。
- **锚点**：@ 像一卷展开贴上墙的墙纸（圈形是纸卷），写在房顶上方=装修队进场贴纸。
- **易错**：装饰器定义写在后面报 NameError；`@deco` 与 `@deco()`（带括号）语义不同，见 PY-08-07。
- **关联**：→ PY-08-03：@ 与 def 在同一瞬间完成
### PY-08-03 装饰时机 Decoration Time
- **是什么**：装饰发生在**函数定义时**（模块导入阶段），不是调用时。
- **为什么**：误以为"调用才装修"会判错打印顺序和开销 → def 语句一执行就调用装饰器并重绑名字 → 没调用被装饰函数，装饰器里的 print 照样出现 → 边界：装饰器工厂的参数求值也在定义时。
- **怎么写**：
```python
def deco(func):
    print(f"登记：收到 {func.__name__}")   # 导入/定义时就发生
    return func
@deco
def house():
    pass
print("模块跑完")
```
→ 运行输出：登记：收到 house ／ 模块跑完
- **何时用/不用**：给框架写装饰器必须清楚时机；"调用时才准备"的逻辑放 wrapper 里，别放装饰器外层。
- **锚点**：开工先在物业装修登记表登记——房子一交付（def 执行）就登记，不是住户入住（调用）才登记。
- **易错**：在装饰器外层做耗时/IO 操作，导入模块就全部执行一遍。
- **关联**：→ PY-08-02：@ 与 def 是同瞬间的两步动作
### PY-08-04 wrapper 透传 *args/**kwargs 与返回值
- **是什么**：通用 wrapper 用 `*args, **kwargs` 接住任意参数，把原函数返回值原样交还。
- **为什么**：wrapper 写死参数签名就只能装饰特定函数 → 收集参数转发 + return result → 一个装饰器适配任意签名 → 边界：忘了 return result，被装饰函数的返回值变 None。
- **怎么写**：
```python
def deco(func):
    def wrapper(*args, **kwargs):   # 万能接料口
        print(f"接料: {args} {kwargs}")
        return func(*args, **kwargs)   # 出料原样交还
    return wrapper
@deco
def paint(area, color="白"): return f"{area}刷{color}"
print(paint("墙面", color="灰"))
```
→ 运行输出：接料: ('墙面',) {'color': '灰'} ／ 墙面刷灰
- **何时用/不用**：写通用装饰器必用透传；确知签名且要强校验时可写明确参数。
- **锚点**：施工单是万能接料口——不管进什么料（位置/标签）都登记转发，出料原封不动交还业主。
- **易错**：打印调试后忘记 return，是最常见的"返回值消失"事故。
- **关联**：→ PY-07-07：**kwargs 的透传本领在此派上用场

## 二、门牌与身份（口号："装修完把门牌挂回去"）
### PY-08-05 functools.wraps
- **是什么**：`@functools.wraps(func)` 放在 wrapper 上，把原函数的 `__name__`/`__doc__` 等元数据抄回新函数。
- **为什么**：装修后门牌换成 wrapper，help()/日志/单测都找错人 → wraps 用 update_wrapper 复制元数据 → `house.__name__` 仍是 'house' → 边界：只复制元数据，不改调用逻辑。
- **怎么写**：
```python
import functools
def deco(func):
    @functools.wraps(func)  # 挂回原房主门牌
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper
@deco
def house(): "毛坯房文档"
print(house.__name__, house.__doc__)
```
→ 运行输出：house 毛坯房文档
- **何时用/不用**：写给别人用的装饰器**一律加** wraps；自己随手玩的临时装饰器可省。
- **锚点**：装修完把原房主门牌挂回去——房子新了，物业登记的还是原住户名字。
- **易错**：写成 `@functools.wraps`（漏了 `(func)`）不生效；wraps 要指向"被装饰的那个函数"。
- **关联**：→ PY-08-06：不加 wraps 的具体症状
### PY-08-06 丢身份的症状 Metadata Loss
- **是什么**：不加 wraps 时，被装饰函数的 `__name__` 变 'wrapper'、`__doc__` 变 None。
- **为什么**：症状隐蔽，只在文档/框架注册/序列化时爆雷 → 名字绑定到 wrapper 对象、元数据跟着丢 → print(house.__name__) 得 wrapper → 边界：功能仍正常，只有身份坏了。
- **怎么写**：
```python
def deco(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper            # 没挂门牌
@deco
def house(): "毛坯房文档"
print(house.__name__, house.__doc__)
```
→ 运行输出：wrapper None
- **何时用/不用**：遇"日志里全是 wrapper""路由名不对"先查 wraps；不是身份问题就不用管。
- **锚点**：新房换了门牌，物业查无此人——屋子能住（功能正常），名字对不上（元数据丢失）。
- **易错**：装饰后 `house is original` 必然 False，别拿 `is` 当"函数没被动过"的校验。
- **关联**：→ PY-08-05：wraps 是唯一解药

## 三、装修合同：带参装饰器（口号："先签合同再派工，三层一张不能少"）
### PY-08-07 带参装饰器三层结构 Decorator with Arguments
- **是什么**：`@contract("豪华")` 先调用合同层拿到真装饰器，再装饰函数——三层嵌套：参数层→装饰层→wrapper 层。
- **为什么**：装修套餐要参数（重试次数/日志级别）→ `@deco(arg)` 等价 `func = deco(arg)(func)` → 多套一层"返回 deco 的函数" → 边界：层多易晕，务必对齐每层 return。
- **怎么写**：
```python
def contract(level):              # 一层：合同条款
    def deco(func):               # 二层：装修队
        def wrapper():            # 三层：工人
            print(f"按{level}级标准施工"); func()
        return wrapper
    return deco
@contract("豪华")                # 先签合同，返回装修队
def house(): print("完工入住")
house()
```
→ 运行输出：按豪华级标准施工 ／ 完工入住
- **何时用/不用**：装饰器要配置参数就用三层；无参数保持两层（PY-08-01）更简单。
- **锚点**：装修合同三张纸——条款（参数）、派工单（deco）、施工单（wrapper），少一张工地就停工。
- **易错**：只写两层却用 `@deco("豪华")`，Python 把 "豪华" 当 func 传入，报 'str' object is not callable。
- **关联**：→ PY-08-08：三层结构的实战样例
### PY-08-08 实战样例：@retry(times=3)
- **是什么**：带参装饰器实例：失败自动重试 N 次的"返工条款"。
- **为什么**：网络/磁盘偶发失败，手写 for+try 到处复制 → wrapper 内循环调用原函数、捕获异常重试 → 第 i 次失败打印返工信息 → 边界：只捕获指定异常，重试耗尽静默返回 None（生产代码应显式处理）。
- **怎么写**：
```python
from functools import wraps
def retry(times):                  # 合同：最多返工 times 次
    def deco(func):
        @wraps(func)
        def wrapper(*a, **kw):
            for i in range(times):
                try: return func(*a, **kw)
                except ValueError as e: print(f"第{i+1}次返工: {e}")
        return wrapper
    return deco
fails = iter([True, True, False])  # 前两次必失败
@retry(3)
def install():
    if next(fails): raise ValueError("尺寸不合")
    return "安装完成"
print(install())
```
→ 运行输出：第1次返工: 尺寸不合 ／ 第2次返工: 尺寸不合 ／ 安装完成
- **何时用/不用**：临时性故障（超时/IO）用 retry；逻辑错误（参数错）重试无意义。
- **锚点**：合同写明"不合格返工 N 次"——验收不合格（ValueError）就重新施工，直到次数用完。
- **易错**：except 范围写成 `except Exception` 会把 bug 也重试三遍，掩盖真实错误。
- **关联**：→ PY-08-07：三层结构是它的骨架

## 四、工头亲自上：类装饰器（口号："装修队也能是个人"）
### PY-08-09 类装饰器 Class Decorator
- **是什么**：装饰器也可以是类：实例化时收下函数，`__call__` 里干活——装修队变成可调用对象（callable）。
- **为什么**：函数装饰器想存状态只能靠闭包 → `@Papering` 等价 `house = Papering(house)`，实例天然有属性槽 → 调用 house() 实际执行实例的 `__call__` → 边界：类必须实现 `__call__`。
- **怎么写**：
```python
class Papering:               # 装修队=可调用工头
    def __init__(self, func):
        self.func = func      # 收下毛坯房
    def __call__(self, *args, **kwargs):
        print("工头亲自贴墙纸"); return self.func(*args, **kwargs)
@Papering
def house(): return "毛坯房"
print(house())
```
→ 运行输出：工头亲自贴墙纸 ／ 毛坯房
- **何时用/不用**：需要状态或想复用方法时用类装饰器；轻量增强用函数装饰器更短。
- **锚点**：工头本人也上阵——装修队不再是"一张流程纸"（函数），而是有工具包、能干活的人（可调用对象）。
- **易错**：漏写 `__call__` 后 `house()` 报 TypeError: 'Papering' object is not callable。
- **关联**：→ 见 [py-10](py-10-magic-methods.md)：__call__ 属魔术方法协议
### PY-08-10 类装饰器带状态 Stateful Class Decorator
- **是什么**：实例属性保存状态（如接单数）；带参数的类装饰器把类当工厂：`@Papering("豪华")` 先实例化工头。
- **为什么**：闭包状态只能靠 nonlocal，类属性更顺手 → `__init__` 收函数存 self.func，`__call__` 更新 self.calls → 多次调用共享同一本台账 → 边界：状态在实例上，多线程要自己加锁。
- **怎么写**：
```python
class Counter:
    def __init__(self, func):
        self.func = func; self.calls = 0     # 台账
    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"第{self.calls}单"); return self.func(*args, **kwargs)
@Counter
def house(): return "完工"
print(house(), house())
```
→ 运行输出：第1单 ／ 第2单 ／ 完工 完工
- **何时用/不用**：计数/缓存/注册表用类装饰器；只要参数不要状态，用三层函数（PY-08-07）更轻。
- **锚点**：工头揣着台账进工地——每接一单记一笔，台账本（实例属性）跟着工头走。
- **易错**：`@Papering("豪华")` 返回的是工头实例再装饰函数，与 `@Papering`（直接收函数）是两种签名。
- **关联**：→ PY-08-09：__call__ 让实例冒充函数

## 五、叠装与套餐（口号："先包最里层，套餐预付定金"）
### PY-08-11 叠放多个装饰器 Stacked Decorators
- **是什么**：多个 @ 从上到下写在同一函数上，函数被层层包裹。
- **为什么**：既要计时又要日志又要鉴权 → 每个装饰器把上一层结果再包一层 → `@a @b def f` 等价 `f = a(b(f))` → 边界：顺序影响行为（PY-08-12）。
- **怎么写**：
```python
def deco_a(func):
    def wrapper(): print("A贴墙纸"); func()
    return wrapper
def deco_b(func):
    def wrapper(): print("B装灯"); func()
    return wrapper
@deco_a
@deco_b
def house(): print("毛坯房")
house()
```
→ 运行输出：A贴墙纸 ／ B装灯 ／ 毛坯房
- **何时用/不用**：功能正交才叠放；同职责叠两层是浪费。
- **锚点**：多层装修先水电后墙纸——离毛坯最近的（@b）先施工，墙纸（@a）最后铺在最外面。
- **易错**：某层返回 None/非函数，整条装饰链崩掉；排查时一层层拆开试。
- **关联**：→ PY-08-12：执行顺序实验
### PY-08-12 叠放顺序实验 Stacking Order
- **是什么**：装饰自下而上（先包内层），执行自外而内（最上面的先跑）。
- **为什么**：顺序写反，日志/计时的包裹范围就错 → `f = a(b(f))` 中 b 先拿原函数、a 再拿 b 的产物 → 调用从 a 的 wrapper 开始 → 边界：用"进/出"打印实验即可看清。
- **怎么写**：
```python
def tag(name):
    def deco(func):
        def wrapper(): print(f"进{name}"); func(); print(f"出{name}")
        return wrapper
    return deco
@tag("外层")                 # 最后包 → 最外层
@tag("内层")                 # 先包 → 最贴近原函数
def house(): print("干活")
house()
```
→ 运行输出：进外层 ／ 进内层 ／ 干活 ／ 出内层 ／ 出外层
- **何时用/不用**：叠放前想清"谁该在外面"（计时一般在最外层）；顺序敏感处写注释标注意图。
- **锚点**：进楼从大门（外层）一路走到毛坯房，出来原路返回；先贴的墙纸在最里层，最后才拆到。
- **易错**：把"书写顺序"当"执行顺序"；口诀：先包的最里层，最上面的最后包、最外层。
- **关联**：→ PY-08-11：叠放的语义源头
### PY-08-13 functools.partial 预绑定 Pre-Binding
- **是什么**：`partial(func, 固定参数)` 生成新函数，预先钉死部分参数，调用时只给剩下的。
- **为什么**：同一函数反复传相同参数（颜色/级别）→ partial 记住 func 与已给参数、调用时合并 → 新函数继续收剩余参数 → 边界：钉住的位置参数在最左，后续位置参数接在后面。
- **怎么写**：
```python
from functools import partial
def wire(length, color):
    return f"{color}电线{length}米"
red_wire = partial(wire, color="红")   # 颜色已定，只欠长度
print(red_wire(10), red_wire(5))
```
→ 运行输出：红电线10米 红电线5米
- **何时用/不用**：回调预置参数、固定配置造变体函数用 partial；就一两个短场景用 lambda/默认参数更直白。
- **锚点**：半包套餐预付定金——材料大头（color="红"）已定金钉死，剩下的（长度）到现场补。
- **易错**：钉住的是关键字参数时，调用处可覆盖：`red_wire(10, color="蓝")` 得"蓝电线10米"（实测）；`partial(int, base=2)` 与 `partial(int, 2)` 意义完全不同。
- **关联**：→ PY-08-14：partial 的典型岗位
### PY-08-14 partial 典型用途 Use Cases
- **是什么**：为固定配置派生变体函数：预置日志级别、按钮回调、固定 key 的排序函数。
- **为什么**：到处写 `lambda: send(msg, level="WARN")` 啰嗦难追踪 → partial 生成可复用 callable → `warn("墙皮开裂")` 一行调用 → 边界：partial 对象没有 `__name__`，调试栈显示 functools.partial。
- **怎么写**：
```python
from functools import partial
def send(msg, level="INFO"):
    print(f"[{level}] {msg}")
warn = partial(send, level="WARN")     # 预付定金：级别定死
warn("墙皮开裂")
send("正常施工")
```
→ 运行输出：[WARN] 墙皮开裂 ／ [INFO] 正常施工
- **何时用/不用**：GUI 回调、并发 map 的固定参数、测试桩用 partial；要文档和默认值直接给 def 加默认参数更好。
- **锚点**：预付定金的订单随用随取——订单（warn）攥在手里，需要时直接下单，不用每次重填配置。
- **易错**：`partial(f, x)` 钉死的是最左位置参数，后续位置实参从第二个开始填，容易错位。
- **关联**：→ PY-08-13：预绑定机制
### PY-08-15 装饰器应用全景 Where Decorators Live
- **是什么**：常见岗位：计时器、缓存（`functools.lru_cache`）、注册表（框架路由/插件）、鉴权、日志、重试。
- **为什么**：横切关注点散落各处难维护 → 增强逻辑集中在装饰器、业务函数保持干净 → `@app.route`、`@lru_cache` 都是同一套机制 → 边界：调试栈多一层，配 wraps 减痛。
- **怎么写**：
```python
from functools import lru_cache
@lru_cache
def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)
print(fact(5), fact(5))
print(fact.cache_info().hits)
```
→ 运行输出：120 120 ／ 1
- **何时用/不用**：增强逻辑与业务正交就用装饰器；业务逻辑本身别塞进装饰器（难读难测）。
- **锚点**：装修队的业务清单——贴墙纸（缓存）、装门禁（鉴权）、装监控（日志）、包验收（重试），全是"不改结构加功能"。
- **易错**：lru_cache 遇不可哈希参数直接 TypeError；长跑进程记得 `cache_clear()` 防缓存无限增长。
- **关联**：→ 见 [py-14](py-14-stdlib.md)：functools 全家桶（reduce/cached_property 等）
## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| `@deco` vs `@deco(arg)` | 装饰器收函数 | 装饰器工厂先收参数 | @ 后面有没有括号 | 带括号先签合同 |
| 函数装饰器 vs 类装饰器 | 闭包包一层 | 实例 __call__ | 要不要存状态 | 有状态用类，轻量用函数 |
| wraps vs 裸 wrapper | 元数据保真 | 门牌变 wrapper | 要不要 help/注册 | 对外装饰器必加 wraps |
| partial vs lambda | 钉死参数 | 一行匿名逻辑 | 固定的是参数还是逻辑 | 钉参数用 partial |
| 叠放书写序 vs 执行序 | 自上而下书写 | 最外层先执行 | 包裹嵌套关系 | 先包最里层，最后包最外层 |
| 装饰器 vs 改源码 | 不动原函数 | 直接改 | 横切复用还是一次性 | 复用加装饰器，单处改源码 |
## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-08-01 | 装饰器/高阶函数 | 收毛坯房还精装房 | 精装房 |
| PY-08-02 | @ 语法糖 | 一卷墙纸贴上房顶 | 墙纸卷 |
| PY-08-03 | 装饰时机 | 物业装修登记表 | 装修登记表 |
| PY-08-04 | wrapper 透传 | 万能接料口施工单 | 接料口 |
| PY-08-05 | functools.wraps | 挂回原房主门牌 | 原门牌 |
| PY-08-06 | 元数据丢失 | 新房换门牌查无此人 | 查无此人 |
| PY-08-07 | 带参装饰器 | 合同三张纸三层 | 三张纸 |
| PY-08-08 | @retry | 合同写明返工 N 次 | 返工条款 |
| PY-08-09 | 类装饰器 | 工头亲自上阵 | 工头上阵 |
| PY-08-10 | 带状态类装饰器 | 工头揣台账记单 | 台账本 |
| PY-08-11 | 叠放装饰器 | 先水电后墙纸多层装修 | 多层装修 |
| PY-08-12 | 叠放顺序 | 进楼从大门走到毛坯 | 原路返回 |
| PY-08-13 | functools.partial | 半包套餐预付定金 | 预付定金 |
| PY-08-14 | partial 用途 | 预付订单随用随取 | 随用随取 |
| PY-08-15 | 应用全景 | 装修队业务清单 | 业务清单 |
## ✅ 自测清单（合上本篇，先写再看）
1. `@deco` 和 `@deco("豪华")` 各自等价的赋值语句是什么？
   > 答案：`f = deco(f)`；`f = deco("豪华")(f)`（PY-08-02 / PY-08-07）。
2. 不加 wraps 的装饰器，`f.__name__` 和 `f.__doc__` 变成什么？怎么修？
   > 答案：'wrapper' 和 None；wrapper 上加 `@functools.wraps(func)`（PY-08-05~06）。
3. `red = partial(wire, color="红")` 后 `red(10)`、`red(10, color="蓝")` 各输出什么？
   > 答案：`红电线10米`、`蓝电线10米`（调用时可覆盖关键字，PY-08-13 易错）。
4. 类装饰器必须实现什么方法？`@Counter def f` 后 `f` 是函数还是对象？
   > 答案：`__call__`；f 是 Counter 实例（PY-08-09）。
## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-07 函数](py-07-functions.md) ｜ ➡️ 下一篇：[py-09 OOP](py-09-oop.md)
