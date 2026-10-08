# py-09 面向对象 — 记忆编码
> **📍 本章导航**：前置 → [py-07 函数](py-07-functions.md) ｜ 相关 → [py-08 装饰器](py-08-decorators.md)·[py-10 魔术方法](py-10-magic-methods.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐⭐ ｜ 阅读 ~12min（约 9k tokens）
>
> 本章逻辑链：py-07~08 会把"动作"打包复用了 → 本篇解决"数据+动作怎么绑成一个组织"（家族企业：族谱/家规/接班）→ 引出 py-10"给对象装万能遥控器（魔术方法）"。意象域：家族企业（执照/工牌/家训/族谱/编制）。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 开张立户：class/self/init | PY-09-01~05 | 执照、工牌、入职登记、私房钱与家训 |
| 子承父业：继承与多态 | PY-09-06~09 | 分号挂招牌，同家规各房各异 |
| 家规内务：封装与属性 | PY-09-10~11 | 内务贴标签、保险柜上锁、信托过柜台 |
| 族谱排序：super 与 MRO | PY-09-12~13 | 请示族长，族谱长幼排序 |
| 编制与岗位 | PY-09-14~16 | 编制有名额，大会归家族，顾问不进谱 |
## 一、开张立户：class/self/init（口号："注册执照、本人工牌、入职登记"）
### PY-09-01 类与实例化 Class & Instance
- **是什么**：类（class）是"家族企业的注册执照"，规定成员有哪些能力；实例（instance）是按执照开出来的分公司。
- **为什么**：数据和函数散落、传参传到晕 → 把数据和操作绑进一个类 → `类名()` 造实例、实例调方法 → 边界：类只是模板，干活的永远是实例。
- **怎么写**：
```python
class Workshop:               # 注册执照
    def run(self):
        return "开工"
w = Workshop()                # 开一家分公司
print(type(w).__name__, w.run())
```
→ 运行输出：Workshop 开工
- **何时用/不用**：数据+行为强绑定、要造多个同类对象时用类；一次性脚本用 py-07 的函数更轻。
- **锚点**：注册一张家族企业执照（class），照执照开出一家家分公司（实例）；执照本身不开门营业。
- **易错**：类体里的方法不调用永不执行；`Workshop.run()` 少给 self 报 TypeError。
- **关联**：→ PY-09-02：方法第一个参数永远是"本人"
### PY-09-02 self
- **是什么**：实例方法的第一个参数 `self`，指"调用它的那个实例本人"。
- **为什么**：同一段方法要服务无数实例、得知道在替谁干活 → `m.who()` 调用时解释器自动把 m 塞进首参 → 方法内 `self.name` 即"本人的名字" → 边界：名字可改但惯例必须叫 self。
- **怎么写**：
```python
class Member:
    def __init__(self, name): self.name = name   # 本人工牌
    def who(self): return f"我是{self.name}"
m = Member("小王")
print(m.who(), Member.who(m))  # 等价的两种叫法
```
→ 运行输出：我是小王 我是小王
- **何时用/不用**：实例方法必写 self；类方法用 cls（PY-09-15），静态方法谁都不用。
- **锚点**：随身工牌"本人"——干活先亮工牌（self），公司才知道这单算谁的。
- **易错**：定义漏写 self，`m.who("小王")` 报 TypeError: who() takes 1 positional argument but 2 were given。
- **关联**：→ PY-09-03：__init__ 里的 self.x 就是发工牌
### PY-09-03 __init__ 初始化 Constructor Init
- **是什么**：`__init__` 是实例出生时的入职登记：收构造参数、给实例装初始属性；它不"返回对象"。
- **为什么**：新成员出生要登记姓名/初始资产 → `类名(...)` 先造空实例再自动调 __init__ → 登记完即用 → 边界：`__init__` 必须返回 None。
- **怎么写**：
```python
class Member:
    def __init__(self, name): # 入职登记：只做初始化
        self.name = name
        print(f"登记{name}")
m = Member("小王")
print(m.name)
```
→ 运行输出：登记小王 ／ 小王
- **何时用/不用**：实例需要初始状态就写 __init__；无状态类可省略（默认继承 object 的）。
- **锚点**：入职登记表——新生儿（实例）一落地就填表（__init__），填完就能上岗。
- **易错**：__init__ 里 `return 5` 报 TypeError: __init__() should return None, not 'int'（实测）。
- **关联**：→ PY-09-04：登记表上填的就是实例变量
### PY-09-04 实例变量 Instance Variable
- **是什么**：`self.x = ...` 创建的属性，每个实例各存一份，互不相干。
- **为什么**：同族成员各有档案/私房钱 → 属性存在实例的 `__dict__` 里 → 改一个不影响其他 → 边界：别在类外凭空挂太多属性。
- **怎么写**：
```python
class Member:
    def __init__(self, name, savings=0):
        self.name, self.savings = name, savings   # 私房钱各一份
a, b = Member("甲", 100), Member("乙")
a.savings += 50
print(a.savings, b.savings)
```
→ 运行输出：150 0
- **何时用/不用**：对象独有的数据用实例变量；全族共享数据用类变量（PY-09-05）。
- **锚点**：私房钱——各人揣各人的兜，甲加了 50，乙的兜纹丝不动。
- **易错**：方法里写 `name = x`（漏 self.）只是本地变量，出方法就消失。
- **关联**：→ PY-09-05：与类变量一比就懂
### PY-09-05 类变量：全族共享与遮蔽 Class Variable & Shadowing
- **是什么**：类体里的变量全族共享一份；但通过实例**赋值**会新建实例变量就地遮蔽（shadowing）；可变类变量则是全员共改一份。
- **为什么**：家训/默认配置不该一人一份，可又常被误改 → 类变量存类对象上、实例赋值在实例上建属性 → 读走共享、写变独有 → 边界：改类变量须写 `Family.motto = x`。
- **怎么写**：
```python
class Family:
    motto = "勤俭持家"; assets = []   # 家训与祖产账本：共享
f1, f2 = Family(), Family()
f1.assets.append("祖宅"); f2.motto = "耕读传家"   # 共享 vs 遮蔽
print(f2.assets, f1.motto, f2.motto)
```
→ 运行输出：['祖宅'] 勤俭持家 耕读传家
- **何时用/不用**：常量/共享配置用类变量；每对象数据用实例变量，永远别拿可变类变量当 per-instance 数据。
- **锚点**：家训匾挂祠堂全族看一块匾；祖产账本谁记一笔全族可见；子孙在自家门口挂新门牌（遮蔽）只盖自己家。
- **易错**：类里 `assets = []` 当默认值用＝共享账本（与 PY-07-04 可变默认同坑）；以为 `f.motto=x` 改了家训。
- **关联**：→ PY-09-04：实例变量是遮蔽的载体

## 二、子承父业：继承与多态（口号："分号挂招牌，同家规各房各异"）
### PY-09-06 继承 Inheritance
- **是什么**：`class Branch(Family)` 让子类自动拥有父类的属性和方法，再添自己的新本事。
- **为什么**：分号不想把总号功能抄一遍 → 创建子类时沿族谱向上找缺失的属性/方法 → `b.brand()` 直接用父类方法 → 边界：继承是"沿谱查找"，不是复制代码。
- **怎么写**：
```python
class Family:                 # 总号
    def brand(self): return "王氏字号"
class Branch(Family):         # 分号挂总号招牌
    def sell(self): return "卖货"
b = Branch()
print(b.brand(), b.sell())
```
→ 运行输出：王氏字号 卖货
- **何时用/不用**：真有 is-a 关系（分号是家族企业）才继承；只是 has-a 用组合（PY-09-16）。
- **锚点**：分号开张挂总号招牌——没写的本事（brand）沿族谱向上找，总号的照用。
- **易错**：父类方法改签名子类全崩；继承层级超过 2~3 层就该怀疑设计。
- **关联**：→ PY-09-07：接班人可以改章程
### PY-09-07 方法重写 Method Override
- **是什么**：子类定义与父类同名方法，就地替换父类版本。
- **为什么**：老章程不合分号水土 → 属性查找在子类命中即停、不再向上 → 子类用自己的实现 → 边界：想调回父类版本用 super()（PY-09-12）。
- **怎么写**：
```python
class Family:
    def rule(self): return "祖训：勤俭"
class Branch(Family):
    def rule(self):           # 接班人改章程
        return "新规：勤俭+创新"
print(Family().rule(), Branch().rule())
```
→ 运行输出：祖训：勤俭 新规：勤俭+创新
- **何时用/不用**：行为确实要变才重写；只加不改就别动父类方法名。
- **锚点**：接班人修订家规——新版盖过旧版，老宅（父类实例）还按祖训办。
- **易错**：重写时拼错方法名（`ruel`）不报错，等于悄悄新增了一个没人调的方法。
- **关联**：→ PY-09-08：多态靠重写才能成立
### PY-09-08 多态 Polymorphism
- **是什么**：同一句调用（`shop.rule()`），不同子类执行不同实现；Python 只看对象有没有该方法（鸭子类型 duck typing），不看类型。
- **为什么**：总号不想为每家分号写 if/else → 调用方统一发号令、对象各自响应 → 加新分号不改调用方 → 边界：对象缺方法就运行期 AttributeError。
- **怎么写**：
```python
class Branch:
    def rule(self): return "勤俭"
class Online(Branch):
    def rule(self): return "快送"
shops = [Branch(), Online()]     # 同一条家规，各房各执行
print(" ".join(s.rule() for s in shops))
```
→ 运行输出：勤俭 快送
- **何时用/不用**：一族对象"统一接口、各自实现"时用；分支极少时直接写 if 更直白。
- **锚点**：同一条"勤俭"家训，各房执行各的——族长喊"按家规办"，每家做法不同但接口一致。
- **易错**：以为多态必须继承才成立；任何有 `rule()` 的对象都能进这个循环。
- **关联**：→ PY-09-09：查身份靠 isinstance
### PY-09-09 isinstance / issubclass / type
- **是什么**：身份查询三件套：`isinstance(对象, 类)`、`issubclass(子类, 父类)`、`type(对象)` 精确取类。
- **为什么**：有时必须确认来人是不是本族 → isinstance 沿族谱认亲（子类实例也算父类实例）→ issubclass 查族谱渊源 → 边界：`type(x) is A` 只认精确类型。
- **怎么写**：
```python
class Family: pass
class Branch(Family): pass
b = Branch()
print(isinstance(b, Branch), isinstance(b, Family),
      issubclass(Branch, Family), type(b) is Branch)
```
→ 运行输出：True True True True
- **何时用/不用**：类型分流/断言用 isinstance；想写"多分支 isinstance 链"先反省是否该用多态（PY-09-08）。
- **锚点**：查户口验族谱——isinstance 认"族谱上有名的都算"，type 只认身份证号一字不差。
- **易错**：`isinstance(True, int)` 为 True（bool 是 int 子类），判整数会被布尔混入。
- **关联**：→ PY-09-06：继承关系是 isinstance 宽容的根源

## 三、家规内务：封装与属性（口号："内务贴标签，保险柜上锁，信托过柜台"）
### PY-09-10 封装：_x 与 __x Private Convention
- **是什么**：`_x` 是约定私有（贴"内务"标签）；`__x` 触发名称改写（name mangling），存成 `_类名__x`，外部直接访问报错。
- **为什么**：账本被外部随手改坏 → 双下划线让外部"够不着"、内部仍用 self.__x → 属性名被悄悄改写 → 边界：这不是安全机制，改个名照样能访问。
- **怎么写**：
```python
class Account:
    def __init__(self):
        self._note = "内务"   # 贴标签
        self.__safe = "账本"  # 上锁：改名 _Account__safe
a = Account()
print(a._note, a._Account__safe)
```
→ 运行输出：内务 账本（`a.__safe` 报 AttributeError: 'Account' object has no attribute '__safe'，实测）
- **何时用/不用**：外部不该碰的状态用 __x；同包协作/子类要用的用 _x；想真控读写用 property（PY-09-11）。
- **锚点**：_ 是贴"内务"标签的柜子（挡君子），__ 是带暗格的保险柜（钥匙孔叫 _Account__safe）。
- **易错**：子类访问 `self.__x` 会因改名找不到父类私有属性；`__x` 在类体内外含义不同。
- **关联**：→ PY-09-11：想给外部留窗口就用 property
### PY-09-11 property 与 setter 属性柜台
- **是什么**：`@property` 把方法伪装成属性（`t.money` 不加括号、读时现算）；`@money.setter` 给赋值加校验守门。
- **为什么**：裸字段没法计算/校验/懒加载 → 访问属性时偷调 getter/setter → 读写都受控 → 边界：装饰链须先 @property 再 @x.setter。
- **怎么写**：
```python
class Trust:
    @property
    def money(self): return self._money
    @money.setter
    def money(self, v):       # 柜台守门人：验成色再入库
        if v < 0: raise ValueError("金额不能为负")
        self._money = v
t = Trust(); t.money = 100; print(t.money)
```
→ 运行输出：100（`t.money = -1` 报 ValueError: 金额不能为负，实测）
- **何时用/不用**：读时计算/校验/缓存用 property；纯数据存取用普通属性，别过度包装。
- **锚点**：家族信托柜台——客户以为在查"属性"，实际每次都在柜台（getter）现算现给；存钱先过守门人（setter）验成色。
- **易错**：只写 getter 时 `t.money = 3` 报 AttributeError: can't set attribute；setter 里赋 `self.money` 会无限递归，须赋 `self._money`。
- **关联**：→ PY-09-10：比名称改写更体面的封装

## 四、族谱排序：super 与 MRO（口号："请示族长，族谱排辈"）
### PY-09-12 super()
- **是什么**：`super().method()` 从"族谱中的下一环"开始找方法，常用于子类扩展父类同名方法。
- **为什么**：想在父类版本上加码而不是整个替换 → super 按 MRO 找父类实现接着办 → 子类增量扩展 → 边界：super 依赖 MRO，多继承时尤其关键（PY-09-13）。
- **怎么写**：
```python
class Family:
    def rule(self): return "祖训"
class Branch(Family):
    def rule(self):
        return "接班+" + super().rule()   # 请示族长接着办
print(Branch().rule())
```
→ 运行输出：接班+祖训
- **何时用/不用**：重写+扩展父类行为必用 super；单继承里 `Family.rule(self)` 虽等价但多继承下会失效。
- **锚点**：到家祠请示族长——接班人先办自己的新规矩，再按族谱往上问祖训（super）。
- **易错**：漏写 super 会"断了祖训"（父类逻辑丢失）；`super()` 括号不能漏（3.x 必须写 super()）。
- **关联**：→ PY-09-13：super 的查找顺序由 MRO 决定
### PY-09-13 方法解析顺序 MRO
- **是什么**：MRO（method resolution order）是类的线性化族谱（C3 算法），决定多继承先找谁；`类.__mro__` 可查。
- **为什么**：多继承"钻石结构"先找谁有争议 → C3 保证子类优先、父类保持相对顺序 → super 沿 MRO 上行 → 边界：顺序=基类列表顺序，写反就换优先级。
- **怎么写**：
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
print([cls.__name__ for cls in D.__mro__])
```
→ 运行输出：['D', 'B', 'C', 'A', 'object']
- **何时用/不用**：多继承/混入（mixin）排查"调了谁的实现"必查 __mro__；单继承不用管。
- **锚点**：族谱长幼排序——族长（D）先问大房（B）再问二房（C）最后到共同祖先（A），排序固定不乱。
- **易错**：`class D(C, B)` 悄悄换了查找优先级；MRO 无法线性化时创建类直接抛 TypeError。
- **关联**：→ PY-09-12：super() 走的就是这条链

## 五、编制与岗位（口号："编制有名额，大会归家族，顾问不进谱"）
### PY-09-14 __slots__ 编制限制 Slots
- **是什么**：`__slots__ = ("name",)` 给类定死属性名单，实例不再有 `__dict__`，省内存、防乱挂属性。
- **为什么**：百万级小对象各带 __dict__ 太费内存 → 实例按槽位存属性、跳过字典 → 属性名单固定 → 边界：未列入 slots 的属性赋值直接 AttributeError。
- **怎么写**：
```python
class Staff:
    __slots__ = ("name",)     # 家族编制：只有一个坑位
s = Staff(); s.name = "小王"
try: s.age = 30
except AttributeError as e: print("报错:", e)
print(s.name)
```
→ 运行输出：报错: 'Staff' object has no attribute 'age' ／ 小王
- **何时用/不用**：海量小对象/想锁属性集合用 slots；普通业务类不必（损失灵活性）。
- **锚点**：家族编制名额——进人（属性）必须有坑位，没编制的（age）连门都进不来。
- **易错**：带 slots 的子类再定义 `__dict__` 会前功尽弃；slots 与类变量同名互相踩。
- **关联**：→ 见 [py-19](py-19-memory-performance.md)：slots 省内存实测
### PY-09-15 类方法与静态方法 classmethod / staticmethod
- **是什么**：`@classmethod` 首参是 cls（整个家族），常做"另类入口"工厂；`@staticmethod` 无 self 无 cls，是挂在类名下的普通函数。
- **为什么**：`Date("2026-10-06")` 这类另类构造塞不进 __init__ → classmethod 收到 cls 能造子类实例 → staticmethod 只做工具计算 → 边界：classmethod 继承时指向子类，staticmethod 完全不关心类。
- **怎么写**：
```python
class Date:
    def __init__(self, y, m, d): self.y, self.m, self.d = y, m, d
    @classmethod
    def from_text(cls, s):    # 家族会议：cls=整个家族
        y, m, d = map(int, s.split("-")); return cls(y, m, d)
    @staticmethod                                     # 外聘顾问：不进族谱
    def valid(s): return len(s.split("-")) == 3
d = Date.from_text("2026-10-06"); print(d.y, Date.valid("2026-10-06"))
```
→ 运行输出：2026 True
- **何时用/不用**：多入口构造用 classmethod；纯工具函数用 staticmethod 或干脆放模块里。
- **锚点**：classmethod=家族大会（cls 是全族代表，开完会发新成员）；staticmethod=外聘顾问（挂着公司名，其实不进族谱）。
- **易错**：classmethod 里写 `return Date(...)` 丢子类，须写 `return cls(...)`；staticmethod 没有任何隐式参数。
- **关联**：→ PY-09-03：classmethod 是绕开默认签名的第二入口
### PY-09-16 组合 vs 继承 Composition vs Inheritance
- **是什么**：继承是"子承父业"（is-a）；组合是"外购装机"（has-a）：把别的对象当属性装进来。
- **为什么**：为复用一个功能就继承整族、族谱越挂乱 → 组合把职责拆给协作对象、不绑死血缘 → 换供应商不改本类 → 边界：需要多态族谱时继承仍是正解。
- **怎么写**：
```python
class Engine:                 # 外姓供应商
    def power(self): return "电机"
class Car:
    def __init__(self):
        self.engine = Engine()   # 组合：装一台别人的电机
    def run(self): return "车动了+" + self.engine.power()
print(Car().run())
```
→ 运行输出：车动了+电机
- **何时用/不用**：默认优先组合；确有稳定 is-a 关系且要多态才继承（"组合优于继承"）。
- **锚点**：联姻办合资公司（组合，装外姓电机）vs 子承父业（继承，挂祖传招牌）——能合作不收养。
- **易错**：为复用一个方法继承大类，父类一改全族遭殃；组合件没在 __init__ 装配就 AttributeError。
- **关联**：→ PY-09-06：继承的边界条件

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| 实例变量 vs 类变量 | self.x 各人一份 | 类体变量全族共享 | 数据归人还是归族 | 私房钱归人，家训归族 |
| _x vs __x | 贴内务标签 | 改名上锁 | 要不要挡住外部 | 一道杠挡君子，两道杠上锁 |
| 实例/类/静态方法 | self 本人 | cls 全族 | 需不需要 cls | 顾问谁都不带 |
| 继承 vs 组合 | 子承父业 is-a | 外购装机 has-a | 是不是同类 | 能合作不收养 |
| super() vs 类名.方法(self) | 沿 MRO 找下一环 | 写死找某父类 | 多继承走哪条路 | super 跟族谱走 |
| type vs isinstance | 精确身份证 | 族谱认亲 | 子类算不算 | type 只认本尊 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-09-01 | 类与实例 | 注册执照开出分公司 | 执照 |
| PY-09-02 | self | 随身工牌"本人" | 工牌 |
| PY-09-03 | __init__ | 入职登记表 | 入职登记表 |
| PY-09-04 | 实例变量 | 私房钱各人一份 | 私房钱 |
| PY-09-05 | 类变量/遮蔽 | 祠堂家训匾与门口挂牌 | 家训匾 |
| PY-09-06 | 继承 | 分号挂总号招牌 | 总号招牌 |
| PY-09-07 | 方法重写 | 接班人改章程 | 改章程 |
| PY-09-08 | 多态 | 同家训各房各异 | 各房各异 |
| PY-09-09 | isinstance 等 | 查户口验族谱 | 验族谱 |
| PY-09-10 | _x / __x | 内务标签 vs 暗格保险柜 | 保险柜 |
| PY-09-11 | property/setter | 信托柜台与守门人 | 信托柜台 |
| PY-09-12 | super() | 家祠请示族长 | 请示族长 |
| PY-09-13 | MRO | 族谱长幼排序 | 长幼排序 |
| PY-09-14 | __slots__ | 家族编制名额 | 编制名额 |
| PY-09-15 | class/staticmethod | 家族大会/外聘顾问 | 大会与顾问 |
| PY-09-16 | 组合 vs 继承 | 联姻合资 vs 子承父业 | 联姻合资 |

## ✅ 自测清单（合上本篇，先写再看）
1. `f.motto = "耕读传家"` 后 `Family.motto` 变了吗？`f.assets.append(x)` 为什么全族可见？
   > 答案：没变（只是给 f 建实例变量遮蔽）；assets 是可变类变量、共享一份（PY-09-05）。
2. `class D(B, C)` 的 `D.__mro__` 顺序？`super().rule()` 从谁开始找？
   > 答案：D→B→C→A→object；从 MRO 中当前类的下一环（B）开始（PY-09-12~13）。
3. `__init__` 里写 `return 5` 会发生什么？
   > 答案：TypeError: __init__() should return None, not 'int'（PY-09-03）。
4. `t.money = 3` 时若 money 只有 @property 会怎样？怎么修？
   > 答案：AttributeError: can't set attribute；加 `@money.setter`（PY-09-11）。
5. classmethod 造实例为什么写 `cls(...)` 而不是 `Date(...)`？
   > 答案：cls 指向实际调用的类（含子类），写死 Date 会丢子类（PY-09-15）。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-08 装饰器](py-08-decorators.md) ｜ ➡️ 下一篇：[py-10 魔术方法](py-10-magic-methods.md)
