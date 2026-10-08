# 🐍 Python 记忆编码 · 总线（INDEX）

> **📍 统一导航**：所属方法 → [M10 结构化/思维导图](../../方法地图.md#m10)·[M08 主动回忆/检索练习](../../方法地图.md#m08)·[M07-R 间隔重复](../../方法地图.md#m07-r) ｜ 难度 ⭐~⭐⭐⭐ ｜ 方法 ID 注册表 → [方法地图.md](../../方法地图.md)
>
> 本目录是 **Python 全知识点记忆编码**（py-00~py-23 共 24 篇、309 个知识点），按 [56-编程语言记忆方法](../../56-编程语言记忆方法.md) 八步流水线生成：P1 知识地图（py-00）→ P2~P6 逐篇编码 → P7 检索练习（py-22）→ P8 间隔复习（py-22）；**整库记忆体系**（一条主线串全部）见 [py-23 记忆体系总纲](py-23-memory-system.md)。
> **编号铁律**：知识点全局坐标 `PY-模块号-序号`（如 `PY-04-07`），发布后不改、只追加；本表是唯一总线——**未在本表登记的文档视为不存在**。

## 📋 快速查阅
| 你想做什么 | 去哪 |
|---|---|
| 第一次学 Python / 定路线 | [py-00 路线图](py-00-roadmap.md) |
| 顺序通读 | 下表 1 → 24 |
| 怎么把整库记成体系（一条主线串全库） | [py-23 记忆体系总纲](py-23-memory-system.md)（Python 城记忆宫殿） |
| 查一个易混点（is/==、深浅拷贝…） | [py-21 全局消混表](py-21-pitfalls-interview.md) |
| 面试冲刺 | [py-21 面试高频 30 问](py-21-pitfalls-interview.md) |
| 自测方法 / 复习排期 / 30-60-90 天计划 | [py-22 检索练习与复习系统](py-22-review-drill.md) |
| 锚点反查 | 本篇 §三 锚点反查总表 + 各篇"📌 锚点登记表" |

## 一、23 篇阅读顺序表

| # | 文件 | 主题 | 知识点 ID 范围 | 难度 | 阅读 | 预估 tokens |
|---|---|---|---|:---:|---|---|
| 1 | [py-00-roadmap.md](py-00-roadmap.md) | 全景图 / 阶段表 / 编号表 / 30 天路线 | —（总图，不设点号） | ⭐ | ~15min | ~10k |
| 2 | [py-01-setup-runtime.md](py-01-setup-runtime.md) | 环境搭建 / 解释器 / REPL / pip·venv | PY-01-01 ~ PY-01-16（16点）（16点） | ⭐ | ~12min | ~8k |
| 3 | [py-02-variables-types.md](py-02-variables-types.md) | 变量命名 / 动态类型 / 基本类型 / id·is·== | PY-02-01 ~ PY-02-16（16点）（16点） | ⭐ | ~12min | ~8k |
| 4 | [py-03-strings.md](py-03-strings.md) | 字符串方法 / 切片 / bytes·Unicode / 编解码 | PY-03-01 ~ PY-03-17（17点）（17点） | ⭐ | ~12min | ~8k |
| 5 | [py-04-containers.md](py-04-containers.md) | list·tuple·dict·set / 推导式 / 深浅拷贝 | PY-04-01 ~ PY-04-17（17点）（17点） | ⭐⭐ | ~13min | ~9k |
| 6 | [py-05-operators.md](py-05-operators.md) | 运算符 / 优先级 / 短路 / 海象 | PY-05-01 ~ PY-05-15（15点）（15点） | ⭐ | ~12min | ~8k |
| 7 | [py-06-control-flow.md](py-06-control-flow.md) | if·for·while / else 子句 / match-case | PY-06-01 ~ PY-06-16（16点）（16点） | ⭐ | ~12min | ~8k |
| 8 | [py-07-functions.md](py-07-functions.md) | 参数种类 / LEGB / 闭包 / 递归 / lambda | PY-07-01 ~ PY-07-18（18点）（18点） | ⭐⭐ | ~13min | ~9k |
| 9 | [py-08-decorators.md](py-08-decorators.md) | 装饰器原理 / wraps / 带参装饰器 / partial | PY-08-01 ~ PY-08-15（15点）（15点） | ⭐⭐ | ~12min | ~8k |
| 10 | [py-09-oop.md](py-09-oop.md) | class·self / 继承多态 / super·MRO / slots·property | PY-09-01 ~ PY-09-16（16点）（16点） | ⭐⭐ | ~14min | ~9k |
| 11 | [py-10-magic-methods.md](py-10-magic-methods.md) | 魔术方法与协议 / 运算符重载 | PY-10-01 ~ PY-10-15（15点）（15点） | ⭐⭐ | ~13min | ~9k |
| 12 | [py-11-iterators-generators.md](py-11-iterators-generators.md) | 迭代协议 / 生成器 / yield·send / itertools | PY-11-01 ~ PY-11-16（16点）（16点） | ⭐⭐ | ~13min | ~9k |
| 13 | [py-12-exceptions.md](py-12-exceptions.md) | 异常层级 / try 四件套 / 自定义异常 / 异常链 | PY-12-01 ~ PY-12-16（16点）（16点） | ⭐⭐ | ~12min | ~8k |
| 14 | [py-13-modules-packages.md](py-13-modules-packages.md) | import 机制 / 包结构 / __name__ / 发布·uv | PY-13-01 ~ PY-13-17（17点）（17点） | ⭐⭐ | ~12min | ~8k |
| 15 | [py-14-stdlib.md](py-14-stdlib.md) | 标准库精选（os·json·collections·itertools…） | PY-14-01 ~ PY-14-15（15点）（15点） | ⭐⭐ | ~12min | ~8k |
| 16 | [py-15-file-io.md](py-15-file-io.md) | open·with / 读写模式 / csv·json 文件 / 编码坑 | PY-15-01 ~ PY-15-13（13点）（13点） | ⭐⭐ | ~12min | ~8k |
| 17 | [py-16-regex.md](py-16-regex.md) | 正则元字符 / 分组 / 贪婪 / re API / 实战 5 例 | PY-16-01 ~ PY-16-18（18点）（18点） | ⭐⭐ | ~12min | ~8k |
| 18 | [py-17-typing-modern.md](py-17-typing-modern.md) | 类型注解 / dataclass·Enum·Protocol / mypy | PY-17-01 ~ PY-17-15（15点）（15点） | ⭐⭐⭐ | ~12min | ~8k |
| 19 | [py-18-concurrency.md](py-18-concurrency.md) | GIL / threading / multiprocessing / asyncio | PY-18-01 ~ PY-18-13（13点）（13点） | ⭐⭐⭐ | ~14min | ~9k |
| 20 | [py-19-memory-performance.md](py-19-memory-performance.md) | 引用计数·GC / slots / 生成器省内存 / profiling | PY-19-01 ~ PY-19-12（12点）（12点） | ⭐⭐⭐ | ~12min | ~8k |
| 21 | [py-20-engineering-testing.md](py-20-engineering-testing.md) | 项目结构 / pytest / logging / lint·CI / 调试法 | PY-20-01 ~ PY-20-13（13点）（13点） | ⭐⭐⭐ | ~12min | ~8k |
| 22 | [py-21-pitfalls-interview.md](py-21-pitfalls-interview.md) | 全局消混 13 组 + 面试高频 30 问 | —（只引用 PY-ID，不新建） | ⭐⭐⭐ | ~15min | ~10k |
| 23 | [py-22-review-drill.md](py-22-review-drill.md) | 自测四件套 / SRS 复习表 / 30·60·90 天计划 | —（只引用 PY-ID，不新建） | ⭐⭐ | ~12min | ~8k |
| 24 | [py-23-memory-system.md](py-23-memory-system.md) | 记忆体系总纲 / Python 城一条主线串全库 / 20 分钟走城复习 | —（不新建锚点，编排已有） | ⭐⭐ | ~12min | ~8k |

> 注：ID 范围与点数为合并期实测统计；锚点反查总表与各篇"📌 锚点登记表"一致，全库反查词唯一性已检查。合计 309 个知识点、309 条锚点登记（py-01~py-20），全库预算约 200k tokens。

## 二、阶段学习路径（阶段 0~6；日程主档见 [py-00](py-00-roadmap.md) 阶段表）

| 阶段 | 主题 | 篇目 | 出口检验 |
|---|---|---|---|
| 阶段 0 全景与开工 | 定路线、装环境 | py-00 ~ py-01 | 能默写模块划分；REPL 跑通 hello |
| 阶段 1 语法地基 | 变量 → 控制流 | py-02 ~ py-06 | T1 闭卷手写一次通过率 ≥70% |
| 阶段 2 抽象与封装 | 函数与装饰器 | py-07 ~ py-08 | 无资料手写闭包 + 装饰器 |
| 阶段 3 对象模型 | OOP 与协议 | py-09 ~ py-10 | 说清 MRO/super 与描述符 |
| 阶段 4 流程进阶 | 迭代 / 异常 / 模块 | py-11 ~ py-13 | 生成器改写循环；异常链规范 |
| 阶段 5 标准库实战 | 标准库 / 文件 / 正则 | py-14 ~ py-16 | 写出文件批处理小工具并跑通 |
| 阶段 6 现代工程与收官 | 类型 / 并发 / 性能 / 工程 | py-17 ~ py-22 | 面试 30 问一次答对率 ≥80% |

> 每天 1 小时的 30/60/90 天节奏、SRS 排期 → [py-22](py-22-review-drill.md)。

## 三、锚点反查总表（跨篇撞车检查）

| PY-ID | 术语 | 锚点意象 | 反查词 | 所在篇 |
|---|---|---|---|---|
| PY-01-01 | 解释器/CPython | 官方特级厨师念菜谱 | 特级厨师 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-02 | 版本确认 | 菜谱封面年份 | 封面年份 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-03 | print | 出餐口喊"出餐" | 出餐口 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-04 | REPL | 灶台前试味小勺 | 试味勺 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-05 | 脚本/shebang | 整本菜谱+封面厨师名 | 菜谱成册 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-06 | 冒号与代码块 | "步骤："后一串动作 | 步骤冒号 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-07 | 缩进 | 菜谱手稿步骤退一格写 | 退一格 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-08 | 注释/docstring | 菜谱旁铅笔小字 | 铅笔小字 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-09 | UTF-8 | 标签统一简体印刷 | 统一标签 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-10 | pip/PyPI | 食材采购市场 | 采购市场 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-11 | venv | 一间独立小厨房 | 独立厨房 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-12 | requirements.txt | 采购清单 | 采购清单 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-13 | __pycache__/.pyc | 冰箱里的备菜盒 | 备菜盒 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-14 | dir/help | 厨具说明书抽屉 | 说明书抽屉 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-15 | 常见报错 | 灶台报警蜂鸣器 | 报警蜂鸣 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-01-16 | import this/PEP 8 | 墙上的守则牌 | 守则牌 | [py-01-setup-runtime.md](py-01-setup-runtime.md) |
| PY-02-01 | 变量/赋值 | 标签拴在货箱上 | 栓标签 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-02 | 命名规则 | 标签书写规范 | 书写规范 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-03 | 动态类型 | 货位换货换标签 | 换货换签 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-04 | int | 整箱码放无上限 | 整箱货堆 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-05 | float | 散装称重有误差 | 散装秤 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-06 | bool | 货架指示灯 | 指示灯 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-07 | None | 空货位挂牌 | 空位牌 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-08 | type/isinstance | 看标签/验货核单 | 验货员 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-09 | 类型转换 | 换包装重新贴标 | 换包装 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-10 | input() | 手写订单纸条 | 手写订单 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-11 | id() | 货箱条码 | 条码 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-12 | is vs == | 比条码 vs 比货物 | 条码货物 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-13 | 可变/不可变 | 纸箱 vs 封死罐头 | 纸箱罐头 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-14 | 链式/交换赋值 | 多签同货/整位互换 | 整位互换 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-15 | 常量约定 | 封条区全大写 | 封条区 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-02-16 | f-string | 出库单卡槽打印 | 卡槽打印 | [py-02-variables-types.md](py-02-variables-types.md) |
| PY-03-01 | 字符串/引号 | 三种信封 | 信封 | [py-03-strings.md](py-03-strings.md) |
| PY-03-02 | 转义/raw | 特殊邮戳/免检信封 | 邮戳 | [py-03-strings.md](py-03-strings.md) |
| PY-03-03 | len/索引 | 字数与第几个字 | 数字数 | [py-03-strings.md](py-03-strings.md) |
| PY-03-04 | 切片 | 裁信刀 | 裁信刀 | [py-03-strings.md](py-03-strings.md) |
| PY-03-05 | 不可变 | 封口后重写一封 | 封口重写 | [py-03-strings.md](py-03-strings.md) |
| PY-03-06 | strip | 撕信封毛边 | 撕毛边 | [py-03-strings.md](py-03-strings.md) |
| PY-03-07 | split/join | 拆信与糊信封 | 拆信糊封 | [py-03-strings.md](py-03-strings.md) |
| PY-03-08 | replace | 改寄批条 | 批条 | [py-03-strings.md](py-03-strings.md) |
| PY-03-09 | find/in/startswith | 查邮编查邮戳 | 查邮编 | [py-03-strings.md](py-03-strings.md) |
| PY-03-10 | f-string 格式 | 盖章模板 | 盖章模板 | [py-03-strings.md](py-03-strings.md) |
| PY-03-11 | str.format | 空白信封填空 | 填空 | [py-03-strings.md](py-03-strings.md) |
| PY-03-12 | %-格式化 | 铅字排版印章 | 铅字印章 | [py-03-strings.md](py-03-strings.md) |
| PY-03-13 | ord/chr | 电报码本 | 码本 | [py-03-strings.md](py-03-strings.md) |
| PY-03-14 | encode/decode | 标准邮袋装拆 | 邮袋 | [py-03-strings.md](py-03-strings.md) |
| PY-03-15 | UTF-8/GBK | 方言邮袋装错 | 错袋 | [py-03-strings.md](py-03-strings.md) |
| PY-03-16 | 遍历/in | 邮差逐字投递 | 邮差 | [py-03-strings.md](py-03-strings.md) |
| PY-03-17 | 实战组合 | 分拣流水线 | 流水线 | [py-03-strings.md](py-03-strings.md) |
| PY-04-01 | 索引/切片 | 货架货位号标签，门口回头数是负数 | 货位号 | [py-04-containers.md](py-04-containers.md) |
| PY-04-02 | append/extend/insert | 上架三招：尾放、整排推、加急插队 | 上架三招 | [py-04-containers.md](py-04-containers.md) |
| PY-04-03 | pop/remove/del/clear | 按货位取件 vs 持面单找件 | 靠位/靠面单 | [py-04-containers.md](py-04-containers.md) |
| PY-04-04 | 改与查 | 换货位标签 + 扫码枪点数 | 换标签点数 | [py-04-containers.md](py-04-containers.md) |
| PY-04-05 | tuple | 塑封面单 + 尾逗号骑缝章 | 塑封面单 | [py-04-containers.md](py-04-containers.md) |
| PY-04-06 | dict 取值 | 取件码柜：报码开柜/报警/无此码 | 取件码 | [py-04-containers.md](py-04-containers.md) |
| PY-04-07 | dict 增删改 | 柜台三牌：开柜/登记/销柜 | 开柜销柜 | [py-04-containers.md](py-04-containers.md) |
| PY-04-08 | 遍历/顺序/嵌套 | 柜旁三张清单 + 分区图 | 三张清单 | [py-04-containers.md](py-04-containers.md) |
| PY-04-09 | set | 安检口去重传送带 | 安检去重 | [py-04-containers.md](py-04-containers.md) |
| PY-04-10 | 集合运算 | 两筐倒出来对账 | 安检对账 | [py-04-containers.md](py-04-containers.md) |
| PY-04-11 | frozenset | 封膜安检筐 | 封膜筐 | [py-04-containers.md](py-04-containers.md) |
| PY-04-12 | 列表推导式 | 分拣打包带逐件筛选拍照 | 打包带「推」 | [py-04-containers.md](py-04-containers.md) |
| PY-04-13 | 字典推导式 | 快递柜批量开柜贴码 | 批量开柜 | [py-04-containers.md](py-04-containers.md) |
| PY-04-14 | 集合/嵌套推导式 | 安检机去重带 + 回收箱 | 回收箱 | [py-04-containers.md](py-04-containers.md) |
| PY-04-15 | 解包/星号解包 | 拆包裹分货、星号大袋子收余件 | 拆包分货 | [py-04-containers.md](py-04-containers.md) |
| PY-04-16 | sorted/sort | 闭店重排货位号，key 是依据纸条 | 排号牌 | [py-04-containers.md](py-04-containers.md) |
| PY-04-17 | 浅拷贝/深拷贝 | 复印面单 vs 连货复制 | 复印面单 | [py-04-containers.md](py-04-containers.md) |
| PY-05-01 | 算术运算符 | 收银台计算器四颗大键 | 计算器 | [py-05-operators.md](py-05-operators.md) |
| PY-05-02 | // 与 % | 找零：整张钞票+硬币 | 找零 | [py-05-operators.md](py-05-operators.md) |
| PY-05-03 | ** 幂 | 翻堆键，右边先堆 | 翻堆 | [py-05-operators.md](py-05-operators.md) |
| PY-05-04 | 增强赋值 | 小票滚加键 | 滚加 | [py-05-operators.md](py-05-operators.md) |
| PY-05-05 | 比较/链式比较 | 验货天平 + 一串价签 | 天平 | [py-05-operators.md](py-05-operators.md) |
| PY-05-06 | is / is not | 验钞机认钞票冠字号 | 冠字号 | [py-05-operators.md](py-05-operators.md) |
| PY-05-07 | and/or/not | 两道审核闸 + 反向闸 | 两道闸 | [py-05-operators.md](py-05-operators.md) |
| PY-05-08 | 短路求值 | 第一道没过，第二道不通电 | 免扫放行 | [py-05-operators.md](py-05-operators.md) |
| PY-05-09 | 真值/any/all | 空购物车不响铃 | 空购物车 | [py-05-operators.md](py-05-operators.md) |
| PY-05-10 | in / not in | 扫码枪查会员名单 | 扫码查名单 | [py-05-operators.md](py-05-operators.md) |
| PY-05-11 | 位运算符 | 硬币面值 1/2/4/8 拆零 | 拆硬币 | [py-05-operators.md](py-05-operators.md) |
| PY-05-12 | 标志位/掩码 | 收银员权限牌别针 | 权限牌 | [py-05-operators.md](py-05-operators.md) |
| PY-05-13 | 海象 := | 扫码结果贴手背 | 贴手背 | [py-05-operators.md](py-05-operators.md) |
| PY-05-14 | 优先级 | 收银顺序：算账→比价→放行 | 收银顺序 | [py-05-operators.md](py-05-operators.md) |
| PY-05-15 | 魔术方法 | 按键下的操作手册 | 按键手册 | [py-05-operators.md](py-05-operators.md) |
| PY-06-01 | if/elif/else | 三岔路口换乘指示牌 | 换乘牌 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-02 | 条件表达式 | 一行迷你指示牌 | 迷你牌 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-03 | 条件组合 | 安检口 + 票检口联合判定 | 两道口 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-04 | for/range | 环线按时刻表跑圈 | 时刻表 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-05 | enumerate/zip | 站点编号牌 / 双线对照表 | 编号牌 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-06 | for-else | 终点站"全程未换乘"广播 | 终点广播 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-07 | while | 站台等车看显示屏 | 站台等车 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-08 | while-else | 末班车收车广播 | 收车广播 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-09 | break | 换乘出闸 | 出闸 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-10 | continue | 跳站不停 | 跳站 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-11 | pass | 施工中的空站台 | 空站台 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-12 | match-case | 智能闸机按票种开通道 | 智能闸机 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-13 | 模式进阶 | 闸机识别票面图案 | 票面图案 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-14 | 循环中改容器 | 行驶中换铁轨跳枕木 | 换轨 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-15 | 哨兵退出 | 环线的终点牌 | 终点牌 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-06-16 | 嵌套跳出 | 枢纽大厅逐线找人 | 枢纽找人 | [py-06-control-flow.md](py-06-control-flow.md) |
| PY-07-01 | def 与调用 | 铺流水线 + 绿色启动钮 | 启动钮 | [py-07-functions.md](py-07-functions.md) |
| PY-07-02 | 位置参数 | 传送带工位对号入座 | 对号入座 | [py-07-functions.md](py-07-functions.md) |
| PY-07-03 | 默认参数 | 进料口预装夹具 | 预装夹具 | [py-07-functions.md](py-07-functions.md) |
| PY-07-04 | 可变默认参数 | 夹具粘着上批余料 | 粘余料 | [py-07-functions.md](py-07-functions.md) |
| PY-07-05 | 关键字实参 | 料箱贴标签点名 | 标签点名 | [py-07-functions.md](py-07-functions.md) |
| PY-07-06 | *args | 敞口麻袋收散料 | 敞口麻袋 | [py-07-functions.md](py-07-functions.md) |
| PY-07-07 | **kwargs | 双层标签料箱 | 标签料箱 | [py-07-functions.md](py-07-functions.md) |
| PY-07-08 | keyword-only | 门口点名窗口 | 点名窗口 | [py-07-functions.md](py-07-functions.md) |
| PY-07-09 | positional-only | 传送带直通闸门 | 直通闸门 | [py-07-functions.md](py-07-functions.md) |
| PY-07-10 | 参数顺序 | 进料总布局图单向流动 | 布局图 | [py-07-functions.md](py-07-functions.md) |
| PY-07-11 | LEGB | 四级上报找工具 | 四级上报 | [py-07-functions.md](py-07-functions.md) |
| PY-07-12 | global/nonlocal | 改账填调拨单 | 调拨单 | [py-07-functions.md](py-07-functions.md) |
| PY-07-13 | 闭包 | 出厂带走私人工具箱 | 私人工具箱 | [py-07-functions.md](py-07-functions.md) |
| PY-07-14 | 递归 | 车间套车间贴收工单 | 收工单 | [py-07-functions.md](py-07-functions.md) |
| PY-07-15 | 递归深度 | 厂房限高牌 1000 层 | 限高牌 | [py-07-functions.md](py-07-functions.md) |
| PY-07-16 | lambda | 临时工（含码料员岗位） | 临时工 | [py-07-functions.md](py-07-functions.md) |
| PY-07-17 | return/多返回值 | 出料口放件、封箱一箱 | 封箱一箱 | [py-07-functions.md](py-07-functions.md) |
| PY-07-18 | 一等公民 | 机器贴牌转让 | 贴牌转让 | [py-07-functions.md](py-07-functions.md) |
| PY-08-01 | 装饰器/高阶函数 | 收毛坯房还精装房 | 精装房 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-02 | @ 语法糖 | 一卷墙纸贴上房顶 | 墙纸卷 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-03 | 装饰时机 | 物业装修登记表 | 装修登记表 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-04 | wrapper 透传 | 万能接料口施工单 | 接料口 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-05 | functools.wraps | 挂回原房主门牌 | 原门牌 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-06 | 元数据丢失 | 新房换门牌查无此人 | 查无此人 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-07 | 带参装饰器 | 合同三张纸三层 | 三张纸 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-08 | @retry | 合同写明返工 N 次 | 返工条款 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-09 | 类装饰器 | 工头亲自上阵 | 工头上阵 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-10 | 带状态类装饰器 | 工头揣台账记单 | 台账本 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-11 | 叠放装饰器 | 先水电后墙纸多层装修 | 多层装修 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-12 | 叠放顺序 | 进楼从大门走到毛坯 | 原路返回 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-13 | functools.partial | 半包套餐预付定金 | 预付定金 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-14 | partial 用途 | 预付订单随用随取 | 随用随取 | [py-08-decorators.md](py-08-decorators.md) |
| PY-08-15 | 应用全景 | 装修队业务清单 | 业务清单 | [py-08-decorators.md](py-08-decorators.md) |
| PY-09-01 | 类与实例 | 注册执照开出分公司 | 执照 | [py-09-oop.md](py-09-oop.md) |
| PY-09-02 | self | 随身工牌"本人" | 工牌 | [py-09-oop.md](py-09-oop.md) |
| PY-09-03 | __init__ | 入职登记表 | 入职登记表 | [py-09-oop.md](py-09-oop.md) |
| PY-09-04 | 实例变量 | 私房钱各人一份 | 私房钱 | [py-09-oop.md](py-09-oop.md) |
| PY-09-05 | 类变量/遮蔽 | 祠堂家训匾与门口挂牌 | 家训匾 | [py-09-oop.md](py-09-oop.md) |
| PY-09-06 | 继承 | 分号挂总号招牌 | 总号招牌 | [py-09-oop.md](py-09-oop.md) |
| PY-09-07 | 方法重写 | 接班人改章程 | 改章程 | [py-09-oop.md](py-09-oop.md) |
| PY-09-08 | 多态 | 同家训各房各异 | 各房各异 | [py-09-oop.md](py-09-oop.md) |
| PY-09-09 | isinstance 等 | 查户口验族谱 | 验族谱 | [py-09-oop.md](py-09-oop.md) |
| PY-09-10 | _x / __x | 内务标签 vs 暗格保险柜 | 保险柜 | [py-09-oop.md](py-09-oop.md) |
| PY-09-11 | property/setter | 信托柜台与守门人 | 信托柜台 | [py-09-oop.md](py-09-oop.md) |
| PY-09-12 | super() | 家祠请示族长 | 请示族长 | [py-09-oop.md](py-09-oop.md) |
| PY-09-13 | MRO | 族谱长幼排序 | 长幼排序 | [py-09-oop.md](py-09-oop.md) |
| PY-09-14 | __slots__ | 家族编制名额 | 编制名额 | [py-09-oop.md](py-09-oop.md) |
| PY-09-15 | class/staticmethod | 家族大会/外聘顾问 | 大会与顾问 | [py-09-oop.md](py-09-oop.md) |
| PY-09-16 | 组合 vs 继承 | 联姻合资 vs 子承父业 | 联姻合资 | [py-09-oop.md](py-09-oop.md) |
| PY-10-01 | 魔术方法/协议 | 万能遥控器按键排布（行业约定） | 按键排布 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-02 | __repr__ | 后台节目单（照着能重排） | 后台节目单 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-03 | __str__ | 台前预告牌（观众看大字） | 台前预告牌 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-04 | __len__ | 数遥控器频道数 | 数频道 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-05 | __bool__ | 舞台开演灯 | 开演灯 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-06 | __eq__ | 同一频道号=同台 | 同台判定 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-07 | __lt__ | 按频道号排队 | 号小排前 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-08 | __hash__ | 按键位编号定格子 | 按键位 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-09 | __getitem__ | 按频道号换台 | 换台下标 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-10 | __setitem__/__delitem__ | 按键位存台/删台 | 存台删台 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-11 | __call__ | 遥控器大按钮一按换台 | 大按钮 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-12 | __enter__/__exit__ | 幕布拉开/拉上 | 开闭幕 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-13 | __add__/__mul__ | 两张频道表叠加 | 叠频道表 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-14 | __radd__ | 客串顶替（问右边） | 客串顶替 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-10-15 | __iadd__ | 原节目单续写 | 续写旧单 | [py-10-magic-methods.md](py-10-magic-methods.md) |
| PY-11-01 | 可迭代对象/迭代器 | 售货机整机 vs 取货口 | 整机与取货口 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-02 | iter() | 开取货口/供货员送"STOP" | 开取货口 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-03 | next()/StopIteration | 按钮取货/售罄灯 | 售罄灯 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-04 | for 真面目 | 自动手指连按按钮 | 自动手指 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-05 | 自定义迭代器类 | 货道出货指针 | 出货指针 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-06 | 可迭代≠迭代器 | 传送带 vs 喝完的可乐 | 传送带可复用 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-07 | 生成器函数 yield | 售货机按钮吐货 | 售货机按钮 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-08 | 挂起与状态 | 断电记忆货道位置 | 断电记忆 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-09 | 生成器表达式 | 出货小票（小括号） | 出货小票 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-10 | 惰性求值 | 不囤货现做 vs 堆满店 | 不囤货 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-11 | yield from | 传送带接传送带 | 接传送带 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-12 | send() | 投币口投币 | 投币口 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-13 | close()/GeneratorExit | 拉闸关门 | 拉闸 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-14 | count/chain/accumulate | 流水线接头（转盘/对接/累加秤） | 流水线接头 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-15 | takewhile/groupby/cycle | 质检闸/分拣员/循环转盘 | 质检闸分拣员 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-11-16 | 惰性管道 | 传送带加工线 | 加工线 | [py-11-iterators-generators.md](py-11-iterators-generators.md) |
| PY-12-01 | try/except | 烟雾报警器+处置 | 报警器 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-02 | 多分支/元组捕获 | 分警情处置台/一铃罩多情 | 分警情处置 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-03 | 异常层级 | 消防警情分类树 | 警情树 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-04 | 异常对象 args | 警报单 | 警报单 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-05 | else 子句 | 合格才开的旁门 | 平安旁门 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-06 | finally 子句 | 总电闸 | 总闸 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-07 | raise | 手动报警按钮 | 手动报警 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-08 | raise from | 警报单写起火原因 | 写明起因 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-09 | __context__ 隐式链 | 单背自动贴上一单 | 背面贴单 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-10 | from None | 警报单不写前因 | 不写前因 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-11 | 自定义异常 | 自家警情分类牌 | 警情牌 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-12 | EAFP/LBYL | 先闯后补 vs 先检后进 | 先闯后补 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-13 | assert | 灭火器压力表自查 | 压力表 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-14 | 内置异常速查 | 消控室警情速查表 | 速查表 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-15 | 资源清理 | 灭火后关电闸 | 关电闸 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-12-16 | 吞异常 | 把报警器捂住 | 捂报警器 | [py-12-exceptions.md](py-12-exceptions.md) |
| PY-13-01 | import 三种写法 | 柜台三种借书法：整本/单章/登别名 | 借书三手续 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-02 | import 机制 | 找书三步：登记簿→路线图→翻印 | 找书三步曲 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-03 | sys.modules 缓存 | 已翻印登记簿，重印才再执行 | 翻印登记簿 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-04 | `__name__` | 扉页藏书章：本人所有/某某馆藏 | 藏书章 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-05 | 主程序守卫 | 演示角告示牌，铃只给本人响 | 演示角铃 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-06 | 包 package | 书架+架头书架牌=分区 | 书架牌 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-07 | `__init__.py` | 架头牌三用：挂牌/展示书/外借清单 | 架头三用牌 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-08 | 相对导入 | "本架第 3 格" vs 全馆索书号 | 本架第几格 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-09 | 命名空间包 | 没挂牌的共享自习区 | 无牌自习区 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-10 | sys.path | 门口的找书路线图 | 路线图 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-11 | PYTHONPATH/append | 路线图末尾贴便签 | 贴便签 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-12 | `python -m` | 大门进知分区 vs 后门进没户口 | 大门后门 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-13 | `__all__` | 书架牌上的可外借清单 | 外借清单 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-14 | `_` 前缀 | 书脊"馆内阅览"小标签 | 馆内阅览签 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-15 | pyproject.toml | 开分馆的办馆申请书 | 办馆申请书 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-16 | venv | 每项目一间独立馆藏 | 独立馆藏 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-13-17 | uv | 馆际物流高铁：建馆+进书直达 | 馆际高铁 | [py-13-modules-packages.md](py-13-modules-packages.md) |
| PY-14-01 | os | 工作台卷尺：量台/搭台/看公告栏 | 老卷尺 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-02 | sys | 工具箱盖内侧参数铭牌 | 参数铭牌 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-03 | pathlib | 一支探针的万用表 | 万用表 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-04 | json | 零件标签打印机 | 标签打印机 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-05 | datetime | 车间打卡钟 | 打卡钟 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-06 | collections | 多格零件收纳柜 | 收纳柜 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-07 | itertools | 多头组合工具钳 | 组合钳 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-08 | functools | 工具改装店 | 改装店 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-09 | math | 水平仪与直角尺 | 水平仪 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-10 | random | 抓阄竹罐 | 抓阄罐 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-11 | logging | 检修登记本（五色笔） | 登记本 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-12 | argparse | 门口工单登记板 | 工单板 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-13 | dataclasses | 标准件规格铭牌 | 规格铭牌 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-14 | copy | 配钥匙摊：钥匙坯/整套锁芯 | 配钥匙 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-14-15 | re 概览 | 样板挑零件：样板=模式，合规格全挑出 | 样板挑件 | [py-14-stdlib.md](py-14-stdlib.md) |
| PY-15-01 | open() | 柜台开窗口，凭证夹=文件对象 | 开窗口 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-02 | with | VIP 自动关窗落锁 | 自动关窗 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-03 | read 三兄弟 | 点钞三式：整捆/一张张/装订沓 | 点钞三式 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-04 | 模式 r/w/a/x | 窗口业务牌：取款/销户/续存/开户 | 业务牌 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-05 | w vs a | 重开存折 vs 流水往下记 | 存折与流水 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-06 | 文本 vs 二进制 | 手抄汉字 vs 点钞机过钞 | 过钞 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-07 | 编码坑 | 凭证字迹章：盖错章对不上账 | 字迹章 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-08 | 换行符 newline | 小票回车+换行两步走 | 小票换行 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-09 | csv 读 | 批量点验票据（逐格/带票头） | 点验票据 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-10 | csv 写 | 开票打单 | 开票打单 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-11 | json 文件 | 保险柜存取件凭条 | 存取凭条 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-12 | os.walk | 金库逐层盘点单 | 金库盘点 | [py-15-file-io.md](py-15-file-io.md) |
| PY-15-13 | pathlib 实操 | VIP 电子流水单 | 电子流水单 | [py-15-file-io.md](py-15-file-io.md) |
| PY-16-01 | 正则/re | 安检扫描仪捞可疑物 | 扫描仪 | [py-16-regex.md](py-16-regex.md) |
| PY-16-02 | 元字符 | 可疑特征卡（形状卡） | 特征卡 | [py-16-regex.md](py-16-regex.md) |
| PY-16-03 | 字符类 | 自选渔网网眼规格 | 自选网眼 | [py-16-regex.md](py-16-regex.md) |
| PY-16-04 | 转义与 r"" | 通缉令贴保护膜 | 保护膜 | [py-16-regex.md](py-16-regex.md) |
| PY-16-05 | 量词 | 渔网松紧绳 | 松紧绳 | [py-16-regex.md](py-16-regex.md) |
| PY-16-06 | 贪婪/懒惰 | 两种撒网手法 | 撒网手法 | [py-16-regex.md](py-16-regex.md) |
| PY-16-07 | 分组捕获 | 渔网分格兜过秤 | 分格兜 | [py-16-regex.md](py-16-regex.md) |
| PY-16-08 | 命名分组 | 给网兜贴名字标签 | 贴标签兜 | [py-16-regex.md](py-16-regex.md) |
| PY-16-09 | 选择 \ |  | 三条并排安检通道 | [py-16-regex.md](py-16-regex.md) |
| PY-16-10 | match/search | 定点检查 vs 全场巡逻 | 定点巡逻 | [py-16-regex.md](py-16-regex.md) |
| PY-16-11 | findall/finditer | 战利品清单 vs 位置小票 | 位置小票 | [py-16-regex.md](py-16-regex.md) |
| PY-16-12 | sub | 没收替换贴标签 | 没收贴签 | [py-16-regex.md](py-16-regex.md) |
| PY-16-13 | compile/标志 | 扫描仪预设程序与指示灯 | 预设程序 | [py-16-regex.md](py-16-regex.md) |
| PY-16-14 | 邮箱模式 | 扫行李托运条三段 | 托运条 | [py-16-regex.md](py-16-regex.md) |
| PY-16-15 | 手机号模式 | 查 11 位号码牌 | 号码牌 | [py-16-regex.md](py-16-regex.md) |
| PY-16-16 | 日期模式 | 捞三种撕法的日历页 | 日历页 | [py-16-regex.md](py-16-regex.md) |
| PY-16-17 | 日志解析 | 拆安检登记卡各栏 | 登记卡拆栏 | [py-16-regex.md](py-16-regex.md) |
| PY-16-18 | 前瞻断言 | 三通道探头安检 | 探头安检 | [py-16-regex.md](py-16-regex.md) |
| PY-17-01 | 类型注解 | 图纸尺寸标注（只标不查） | 尺寸标注 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-02 | typing 图例 | 图纸标准图例表 | 图例表 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-03 | 竖线联合 | 门洞隔断二选一 | 隔断门洞 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-04 | Optional | 可选车位可空着 | 可选车位 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-05 | 类型别名 | 图纸简称"标准间" | 图纸简称 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-06 | dataclass | 预制板模具 | 预制模具 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-07 | field/frozen | 承重墙+入户电表 | 承重墙 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-08 | Enum | 材料等级牌 | 等级牌 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-09 | Protocol | 对样板验收 | 对样板 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-10 | TypedDict | 材料清单表 | 清单表 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-11 | TypeVar | 万能尺寸代号 W | 代号W | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-12 | mypy | 质检章（静态盖章） | 质检章 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-13 | match-case | 分拣台按形状滑槽 | 分拣台 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-14 | match 进阶 | 卡尺+合格章 | 卡尺合格章 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-17-15 | 海象 := | 量完顺手贴标签 | 贴标签 | [py-17-typing-modern.md](py-17-typing-modern.md) |
| PY-18-01 | GIL | 路口唯一红绿灯 | 唯一红绿灯 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-02 | threading | 多条车道 | 多车道 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-03 | Lock | 岗亭闸机一次一辆 | 岗亭闸机 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-04 | multiprocessing | 平行高架独立路口 | 平行高架 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-05 | Pool | 调度站派单墙 | 派单墙 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-06 | ThreadPoolExecutor | 网约车派单平台 | 网约车派单 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-07 | ProcessPoolExecutor | 货运整车专线 | 整车专线 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-08 | queue.Queue | 待转区排队 | 待转区 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-09 | async/await | 潮汐车道让道 | 潮汐车道 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-10 | 事件循环 | 中央调度亭 | 调度亭 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-11 | gather/create_task | 车队同时发车 | 车队发车 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-12 | wait_for | 绿灯倒计时拦车 | 绿灯倒计时 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-18-13 | 实战选型 | 方案对照板 | 对照板 | [py-18-concurrency.md](py-18-concurrency.md) |
| PY-19-01 | 引用计数 | 行李牌 | 行李牌 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-02 | gc 回收 | 互相绑着的行李牌→保洁剪牌 | 剪牌保洁 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-03 | 深浅拷贝 | 搬家装箱两种装法 | 装箱搬家 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-04 | __slots__ | 定格收纳柜 | 定格柜 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-05 | 生成器 | 断舍离传送口 | 传送口 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-06 | join 拼接 | 一次装箱 vs 来一件搬一次 | 一次装箱 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-07 | timeit | 厨房计时器 | 掐表 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-08 | cProfile | 上秤盘点找最重 | 上秤盘点 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-09 | tracemalloc | 收纳前后拍照对比 | 前后拍照 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-10 | lru_cache | 门口鞋架 | 门口鞋架 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-11 | set/dict 查找 | 贴标签收纳箱直取 | 标签直取 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-19-12 | 优化三步法 | 盘点→改造→复称 | 复称 | [py-19-memory-performance.md](py-19-memory-performance.md) |
| PY-20-01 | 项目结构 | 4S 店功能分区图 | 功能分区 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-02 | pytest | 质检单打勾打叉 | 质检单 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-03 | fixture | 准备工位铺护套 | 准备工位 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-04 | parametrize | 批量过检线 | 批量过检 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-05 | pytest.raises | 踩刹车测故障码 | 测故障码 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-06 | logging 分级 | 广播喇叭分级 | 分级广播 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-07 | logging 配置 | 广播室三件套 | 广播室 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-08 | 配置管理 | 工位开关牌 | 开关牌 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-09 | ruff/black/mypy | 出厂三道检测线 | 三道检测线 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-10 | poetry | 进货管家+进货账 | 进货管家 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-11 | uv | 极速配件物流 | 闪送物流 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-12 | CI | 自动年检流水线 | 自动年检 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |
| PY-20-13 | 调试三法 | 排故三板斧 | 三板斧 | [py-20-engineering-testing.md](py-20-engineering-testing.md) |

> 源头是各篇"📌 锚点登记表"；合并期由维护者汇总到本表，并按 [MEMORY-ENCODING-RULES 铁律 2](../../MEMORY-ENCODING-RULES.md) 做全库意象撞车检查。py-21/py-22 不新建锚点，只引用 PY-ID。

## 🔗 相关章节
- → [../INDEX.md](../INDEX.md)（17-programming/INDEX.md）：编程记忆编码总入口（语法/设计模式/算法/面试）
- → [../../56-编程语言记忆方法.md](../../56-编程语言记忆方法.md)：八步流水线方法论（本目录的生成规则）
- → [../../方法地图.md](../../方法地图.md)：方法 ID（M01~M42+M07-R）注册表与术语约定
- → [../../templates/记忆训练进度追踪表.md](../../templates/记忆训练进度追踪表.md)：训练记录表（配合 [py-22 §五](py-22-review-drill.md) 使用）

## 📍 导航
> [返回 17-programming/INDEX](../INDEX.md) ｜ [返回主页](../../README.md)
