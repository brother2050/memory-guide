# 设计模式记忆 — GoF 23种设计模式编码

> 记忆策略：每个模式 → 问题场景 → 解决方案 → 生活类比 → 视觉画面
> 目标：看到模式名 → 脑中浮现类比画面 → 自动回忆结构和代码

---

## 一、创建型模式（Creational Patterns）— 5个
> 定位宫殿：**工厂车间**（想象一个巨大的制造工厂）

### 1. 单例模式 Singleton
- **问题**：全局只需要一个实例（配置管理器、连接池）
- **方案**：私有构造 + 静态方法获取唯一实例
- **类比**：**太阳** — 天上只能有一个太阳
- **画面**：工厂大门上挂一把大锁，门牌写着"唯一入口"，所有人排队从同一个门进
- **关键代码**：
  ```python
  class Singleton:
      _instance = None
      def __new__(cls):
          if cls._instance is None:
              cls._instance = super().__new__(cls)
          return cls._instance
  ```
- **编码**：`锁门+排队` → `__new__`控制实例化，`_instance`是唯一通行证
- **变体**：懒汉式（用时创建）、饿汉式（类加载时创建）、双重检查锁

### 2. 工厂方法模式 Factory Method
- **问题**：不确定要创建哪个具体类，让子类决定
- **方案**：定义创建对象的接口，子类决定实例化哪个类
- **类比**：**奶茶店** — 你说"要一杯奶茶"，店员根据口味决定做哪种
- **画面**：奶茶店柜台，顾客说"来一杯"，不同员工（子类）做出不同口味
- **关键代码**：
  ```python
  class Creator(ABC):
      @abstractmethod
      def create_product(self): pass
  class ConcreteCreator(Creator):
      def create_product(self):
          return ConcreteProduct()
  ```
- **编码**：`奶茶店点单` → 父类定义接口，子类决定产品

### 3. 抽象工厂模式 Abstract Factory
- **问题**：创建一系列相关对象，不指定具体类
- **方案**：提供创建一系列相关对象的接口
- **类比**：**家具商城** — 你要"北欧风格"，沙发、桌子、椅子全套配齐
- **画面**：家具展厅，选"北欧风"按钮，整套家具从传送带出来，风格统一
- **关键代码**：
  ```python
  class AbstractFactory(ABC):
      @abstractmethod
      def create_chair(self): pass
      @abstractmethod
      def create_table(self): pass
  ```
- **编码**：`家具展厅` → 一个工厂生产一整套产品族

### 4. 建造者模式 Builder
- **问题**：复杂对象的构建过程需要分步骤
- **方案**：将构建与表示分离，分步骤创建
- **类比**：**汉堡店** — 你说"加生菜、加芝士、加培根"，一步步组装
- **画面**：汉堡制作台，面包→生菜→肉饼→芝士→面包，每一步清晰可选
- **关键代码**：
  ```python
  class BurgerBuilder:
      def add_bun(self): self.bun = True; return self
      def add_cheese(self): self.cheese = True; return self
      def build(self): return Burger(self)
  ```
- **编码**：`汉堡台链式` → 每个方法return self，最后.build()

### 5. 原型模式 Prototype
- **问题**：创建对象成本高，想复制已有对象
- **方案**：通过克隆（拷贝）已有对象来创建新对象
- **类比**：**复印机** — 原件放进去，复印件出来
- **画面**：办公室复印机，原件按"复印"键，一份份相同的副本滑出
- **关键代码**：
  ```python
  import copy
  class Prototype:
      def clone(self):
          return copy.deepcopy(self)
  ```
- **编码**：`复印机deepcopy` → `copy.deepcopy()`深拷贝

---

## 二、结构型模式（Structural Patterns）— 7个
> 定位宫殿：**建筑工地**（想象一栋大楼的搭建过程）

### 6. 适配器模式 Adapter
- **问题**：接口不兼容，无法直接使用
- **方案**：创建适配器包装不兼容的接口
- **类比**：**电源转换插头** — 中国插头插不进美国插座，加个转换器
- **画面**：一个大插头和一个小插座之间，中间卡着一个转换器，灯亮了
- **关键代码**：
  ```python
  class Adapter:
      def __init__(self, adaptee):
          self.adaptee = adaptee
      def request(self):
          return self.adaptee.specific_request()
  ```
- **编码**：`转换插头` → 包装旧接口，暴露新接口

### 7. 桥接模式 Bridge
- **问题**：抽象和实现耦合，扩展困难
- **方案**：将抽象与实现分离，独立变化
- **类比**：**遥控器和电视** — 遥控器（抽象）和电视（实现）可以独立更换
- **画面**：遥控器和电视之间有道桥（无线信号），换电视不用换遥控器
- **关键代码**：
  ```python
  class RemoteControl:
      def __init__(self, device):
          self.device = device  # 桥接到实现
      def press_power(self):
          self.device.toggle_power()
  ```
- **编码**：`遥控器桥` → 抽象持有实现的引用

### 8. 组合模式 Composite
- **问题**：树形结构中，叶子和容器需要统一处理
- **方案**：将对象组合成树形结构，统一处理单个对象和组合对象
- **类比**：**文件夹和文件** — 文件夹里可以放文件，也可以放子文件夹
- **画面**：电脑文件资源管理器，文件夹图标打开后有文件和子文件夹，递归嵌套
- **关键代码**：
  ```python
  class Component(ABC):
      def operation(self): pass
  class Leaf(Component):
      def operation(self): return "叶子"
  class Composite(Component):
      def __init__(self): self.children = []
      def add(self, child): self.children.append(child)
  ```
- **编码**：`文件夹递归` → 统一接口，容器包含子节点列表

### 9. 装饰器模式 Decorator
- **问题**：动态给对象添加职责，不想用继承
- **方案**：创建包装对象来动态添加功能
- **类比**：**穿衣服** — 人→穿T恤→穿外套→戴围巾，层层包裹
- **画面**：一个人站在中间，一层层衣服套上去，每层增加功能（保暖/防水/美观）
- **关键代码**：
  ```python
  class Decorator(Component):
      def __init__(self, component):
          self._component = component
      def operation(self):
          return self._component.operation() + " + 装饰"
  ```
- **编码**：`穿衣服层层包` → 装饰器持有组件引用，调用时叠加

### 10. 外观模式 Facade
- **问题**：子系统复杂，调用者需要简化接口
- **方案**：提供统一的高层接口，简化子系统使用
- **类比**：**酒店前台** — 你只需找前台，不用分别联系客房部、餐饮部、保洁部
- **画面**：酒店大堂，客人站在前台，前台背后有一堆部门（子系统），前台帮你搞定一切
- **关键代码**：
  ```python
  class Facade:
      def __init__(self):
          self._sub1 = SubSystem1()
          self._sub2 = SubSystem2()
      def operation(self):
          self._sub1.method1()
          self._sub2.method2()
  ```
- **编码**：`酒店前台` → 一个门面类封装多个子系统调用

### 11. 享元模式 Flyweight
- **问题**：大量相似对象消耗内存
- **方案**：共享细粒度对象，分离内部状态（共享）和外部状态（变化）
- **类比**：**共享自行车** — 1000人不需要买1000辆车，共享即可
- **画面**：自行车停放点，不同人骑同一辆车（不同时间），车（内部状态）不变，骑车人（外部状态）变
- **关键代码**：
  ```python
  class FlyweightFactory:
      _flyweights = {}
      def get_flyweight(self, key):
          if key not in self._flyweights:
              self._flyweights[key] = Flyweight(key)
          return self._flyweights[key]
  ```
- **编码**：`共享单车池` → 工厂缓存已创建对象，用key复用

### 12. 代理模式 Proxy
- **问题**：想控制对对象的访问
- **方案**：创建代理对象控制对原对象的访问
- **类比**：**经纪人** — 明星不直接见粉丝，通过经纪人安排
- **画面**：明星在房间里，粉丝在门外，经纪人站在中间传递信息/把关
- **关键代码**：
  ```python
  class Proxy:
      def __init__(self, real_subject):
          self._real = real_subject
      def request(self):
          if self.check_access():
              self._real.request()
  ```
- **编码**：`经纪人把关` → 代理持有真实对象，控制访问时机

---

## 三、行为型模式（Behavioral Patterns）— 11个
> 定位宫殿：**指挥中心**（想象一个作战指挥室）

### 13. 责任链模式 Chain of Responsibility
- **问题**：请求的处理者不确定，需要多个对象都有机会处理
- **方案**：将处理者连成链，沿链传递直到有人处理
- **类比**：**击鼓传花** — 鼓声停前，花在人与人之间传递
- **画面**：一排人坐成链条，包裹从左边传来，每人看一眼：不是我的→传给下一个
- **关键代码**：
  ```python
  class Handler:
      def __init__(self, successor=None):
          self.successor = successor
      def handle(self, request):
          if self.can_handle(request):
              return self.process(request)
          elif self.successor:
              return self.successor.handle(request)
  ```
- **编码**：`击鼓传花` → 每个handler持有next，处理不了就传

### 14. 命令模式 Command
- **问题**：想把请求封装成对象，支持撤销/排队
- **方案**：将请求封装为命令对象
- **类比**：**餐厅点菜单** — 你写菜单（命令），服务员传递给厨师执行
- **画面**：顾客写好菜单夹在夹子上，服务员取走交给厨师，厨师按单做菜
- **关键代码**：
  ```python
  class Command(ABC):
      @abstractmethod
      def execute(self): pass
      def undo(self): pass
  class ConcreteCommand(Command):
      def __init__(self, receiver): self.receiver = receiver
      def execute(self): self.receiver.action()
  ```
- **编码**：`菜单夹子` → 命令对象封装receiver和参数

### 15. 迭代器模式 Iterator
- **问题**：想遍历集合但不暴露内部结构
- **方案**：提供统一的遍历接口
- **类比**：**翻书** — 不管书多厚，一页一页翻就行
- **画面**：一本厚书，手指按页码顺序翻动，不需要知道书的装订方式
- **关键代码**：
  ```python
  class Iterator(ABC):
      def has_next(self): pass
      def next(self): pass
  ```
- **编码**：`翻书器` → has_next+next，Python内置`__iter__`/`__next__`

### 16. 中介者模式 Mediator
- **问题**：多个对象互相通信，关系复杂
- **方案**：通过中介者对象统一管理通信
- **类比**：**房产中介** — 买卖双方不直接谈，都通过中介沟通
- **画面**：买家和卖家各站一边，中间是中介，所有对话经过中介转发
- **关键代码**：
  ```python
  class Mediator(ABC):
      def notify(self, sender, event): pass
  class ConcreteMediator(Mediator):
      def __init__(self, comp1, comp2):
          self.comp1 = comp1
          self.comp2 = comp2
      def notify(self, sender, event):
          if event == "A": self.comp2.react()
  ```
- **编码**：`房产中介` → 中介持有所有同事引用，统一调度

### 17. 备忘录模式 Memento
- **问题**：想保存和恢复对象的内部状态
- **方案**：创建备忘录保存状态，需要时恢复
- **类比**：**游戏存档** — 打到Boss前存档，死了读档重来
- **画面**：游戏画面，按下"存档"按钮，当前状态压缩成一个小文件保存；读档时解压恢复
- **关键代码**：
  ```python
  class Memento:
      def __init__(self, state): self._state = state
  class Originator:
      def save(self): return Memento(self._state)
      def restore(self, memento): self._state = memento._state
  ```
- **编码**：`存读档` → save返回备忘录，restore接收备忘录

### 18. 观察者模式 Observer
- **问题**：对象状态变化时需要通知多个依赖对象
- **方案**：定义一对多依赖，状态变化时自动通知所有观察者
- **类比**：**公众号推送** — 作者发文章，所有粉丝自动收到通知
- **画面**：公众号后台，作者点"发布"，无数手机同时弹出通知
- **关键代码**：
  ```python
  class Subject:
      def __init__(self): self._observers = []
      def attach(self, obs): self._observers.append(obs)
      def notify(self):
          for obs in self._observers:
              obs.update(self)
  ```
- **编码**：`公众号推送` → subject维护观察者列表，状态变→遍历通知

### 19. 状态模式 State
- **问题**：对象行为随状态改变，大量if-else
- **方案**：将状态封装为独立对象，行为委托给当前状态
- **类比**：**红绿灯** — 红灯停、绿灯行、黄灯等，灯的状态决定行为
- **画面**：十字路口红绿灯，红灯亮时车辆停，绿灯亮时车辆行，切换时行为自动改变
- **关键代码**：
  ```python
  class State(ABC):
      def handle(self, context): pass
  class Context:
      def __init__(self, state): self._state = state
      def request(self): self._state.handle(self)
  ```
- **编码**：`红绿灯切换` → context持有当前state，state处理后可切换

### 20. 策略模式 Strategy
- **问题**：同一问题有多种算法，想动态切换
- **方案**：定义算法族，封装每个算法，可互相替换
- **类比**：**导航路线** — 同一目的地，可以选"最快""最短""不走高速"
- **画面**：手机地图App，三条路线用不同颜色显示，点一下就切换策略
- **关键代码**：
  ```python
  class Strategy(ABC):
      def algorithm(self): pass
  class Context:
      def __init__(self, strategy): self._strategy = strategy
      def execute(self): return self._strategy.algorithm()
  ```
- **编码**：`导航换路线` → context持有strategy，随时替换

### 21. 模板方法模式 Template Method
- **问题**：算法骨架相同，某些步骤不同
- **方案**：定义算法骨架，子类重写具体步骤
- **类比**：**考试答题卡** — 格式固定（模板），具体答案由学生填
- **画面**：标准答题卡，姓名栏/选择题/填空题格式固定，每个学生填不同内容
- **关键代码**：
  ```python
  class AbstractClass:
      def template_method(self):
          self.step1()
          self.step2()
      def step1(self): pass  # 抽象
      def step2(self): pass  # 抽象
  ```
- **编码**：`答题卡模板` → 父类定骨架，子类填步骤

### 22. 访问者模式 Visitor
- **问题**：对一组对象执行不同操作，不想修改类
- **方案**：将操作封装到访问者中，对象接受访问者
- **类比**：**体检医生** — 不同科室医生来检查同一病人，病人只需配合
- **画面**：体检中心，内科医生、外科医生、眼科医生依次走到病人面前检查
- **关键代码**：
  ```python
  class Visitor(ABC):
      def visit_element_a(self, a): pass
      def visit_element_b(self, b): pass
  class Element(ABC):
      def accept(self, visitor): pass
  ```
- **编码**：`体检医生巡诊` → element.accept(visitor)双分派

### 23. 解释器模式 Interpreter
- **问题**：有特定语法需要解析执行
- **方案**：为语法创建解释器，递归解析表达式
- **类比**：**翻译官** — 听到外语逐句翻译成母语
- **画面**：联合国会议，翻译官戴耳机，每句话实时翻译显示在屏幕上
- **关键代码**：
  ```python
  class Expression(ABC):
      def interpret(self, context): pass
  class TerminalExpression(Expression):
      def interpret(self, context):
          return context.contains(self.data)
  ```
- **编码**：`翻译官递归` → 文法规则→表达式类，interpret递归求值

---

## 四、模式分类宫殿（记忆定位）

### 🏭 创建型宫殿 — 工厂车间（5个模式）
| 位置 | 模式 | 画面锚点 |
|------|------|----------|
| 大门锁 | 单例 | 锁门排队 |
| 奶茶柜台 | 工厂方法 | 点单做奶茶 |
| 家具展厅 | 抽象工厂 | 按风格配全套 |
| 汉堡台 | 建造者 | 一步步组装 |
| 复印机旁 | 原型 | 复印原件 |

### 🏗️ 结构型宫殿 — 建筑工地（7个模式）
| 位置 | 模式 | 画面锚点 |
|------|------|----------|
| 插座墙 | 适配器 | 转换插头 |
| 桥梁 | 桥接 | 遥控器桥 |
| 文件柜 | 组合 | 文件夹递归 |
| 衣帽间 | 装饰器 | 穿衣服层层包 |
| 前台大厅 | 外观 | 酒店前台 |
| 停车场 | 享元 | 共享单车 |
| 门卫室 | 代理 | 经纪人把关 |

### 🎖️ 行为型宫殿 — 指挥中心（11个模式）
| 位置 | 模式 | 画面锚点 |
|------|------|----------|
| 传令线 | 责任链 | 击鼓传花 |
| 命令台 | 命令 | 菜单夹子 |
| 阅览室 | 迭代器 | 翻书器 |
| 通讯室 | 中介者 | 房产中介 |
| 档案室 | 备忘录 | 游戏存档 |
| 广播站 | 观察者 | 公众号推送 |
| 信号灯 | 状态 | 红绿灯 |
| 导航台 | 策略 | 导航换路线 |
| 考场 | 模板方法 | 答题卡模板 |
| 体检中心 | 访问者 | 医生巡诊 |
| 翻译室 | 解释器 | 翻译官递归 |

---

## 五、模式间关系网络

### 核心关联图
```
                    ┌───────────┐
                    │  单例     │
                    └─────┬─────┘
                          │ 常配合
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
     ┌────────┐     ┌──────────┐    ┌────────┐
     │ 工厂   │────▶│ 抽象工厂 │    │ 原型   │
     └───┬────┘     └────┬─────┘    └────┬───┘
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ 建造者  │    │ 组合     │    │ 装饰器   │
    └─────────┘    └──────────┘    └──────────┘
```

### 常见搭配
- **单例 + 工厂**：工厂本身常为单例
- **组合 + 迭代器**：遍历树形结构
- **装饰器 + 适配器**：包装+转换接口
- **观察者 + 中介者**：一对多通信 vs 多对多通信
- **策略 + 状态**：都封装行为，策略由外部选择，状态由内部切换
- **命令 + 备忘录**：命令支持撤销，备忘录保存状态
- **模板方法 + 工厂方法**：模板方法中的步骤常由工厂方法实现
- **代理 + 装饰器**：结构相似，代理控制访问，装饰器增加功能

### 易混模式对比
| 对比 | 区别 |
|------|------|
| 工厂方法 vs 抽象工厂 | 工厂方法创建一个产品，抽象工厂创建一族产品 |
| 策略 vs 状态 | 策略由客户端选择，状态由对象内部自动切换 |
| 代理 vs 装饰器 | 代理控制访问（权限/缓存），装饰器增加功能 |
| 观察者 vs 中介者 | 观察者一对多广播，中介者多对多协调 |
| 组合 vs 装饰器 | 组合是树形结构管理，装饰器是链式功能增强 |
| 适配器 vs 桥接 | 适配器让不兼容的接口合作，桥接分离抽象与实现 |
| 命令 vs 策略 | 命令封装"做什么"，策略封装"怎么做" |

---

## 六、速记口诀

### 创建型口诀
> **单工抽建原**（单例、工厂方法、抽象工厂、建造者、原型）
> 谐音：**单公抽剑远** — 单独的公公抽出剑走远了

### 结构型口诀
> **适桥组装外享代**（适配器、桥接、组合、装饰器、外观、享元、代理）
> 谐音：**七桥组装饰外乡带** — 七座桥上装饰着外乡的彩带

### 行为型口诀
> **责命迭中备观状策模访解**
> （责任链、命令、迭代器、中介者、备忘录、观察者、状态、策略、模板方法、访问者、解释器）
> 谐音：**责命叠中被关状策莫方解** — 负责命运叠加中被关押，状况策略莫名其妙方得解

---

## 七、实战速查表

| 场景 | 推荐模式 |
|------|----------|
| 全局唯一实例 | 单例 |
| 根据参数创建不同对象 | 工厂方法 |
| 创建一套风格统一的对象 | 抽象工厂 |
| 构建步骤复杂的对象 | 建造者 |
| 快速复制已有对象 | 原型 |
| 接口不兼容 | 适配器 |
| 多维度独立变化 | 桥接 |
| 树形结构统一处理 | 组合 |
| 动态添加功能 | 装饰器 |
| 简化复杂子系统 | 外观 |
| 大量相似对象省内存 | 享元 |
| 控制对象访问 | 代理 |
| 多级审批/处理 | 责任链 |
| 撤销/重做/队列 | 命令 |
| 遍历集合 | 迭代器 |
| 多对象复杂通信 | 中介者 |
| 保存/恢复状态 | 备忘录 |
| 一对多通知 | 观察者 |
| 对象行为随状态变 | 状态 |
| 算法可替换 | 策略 |
| 固定流程可变步骤 | 模板方法 |
| 对固定结构做多种操作 | 访问者 |
| 自定义语法解析 | 解释器 |
