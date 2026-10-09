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
| 锚点反查 | [py-24 锚点反查总表](py-24-anchor-registry.md) + 各篇"📌 锚点登记表" |

## 一、23 篇阅读顺序表

| # | 文件 | 主题 | 知识点 ID 范围 | 难度 | 阅读 | 预估 tokens |
|---|---|---|---|:---:|---|---|
| 1 | [py-00-roadmap.md](py-00-roadmap.md) | 全景图 / 阶段表 / 编号表 / 30 天路线 | —（总图，不设点号） | ⭐ | ~15min | ~10k |
| 2 | [py-01-setup-runtime.md](py-01-setup-runtime.md) | 环境搭建 / 解释器 / REPL / pip·venv | PY-01-01 ~ PY-01-16（16点） | ⭐ | ~12min | ~8k |
| 3 | [py-02-variables-types.md](py-02-variables-types.md) | 变量命名 / 动态类型 / 基本类型 / id·is·== | PY-02-01 ~ PY-02-16（16点） | ⭐ | ~12min | ~8k |
| 4 | [py-03-strings.md](py-03-strings.md) | 字符串方法 / 切片 / bytes·Unicode / 编解码 | PY-03-01 ~ PY-03-17（17点） | ⭐ | ~12min | ~8k |
| 5 | [py-04-containers.md](py-04-containers.md) | list·tuple·dict·set / 推导式 / 深浅拷贝 | PY-04-01 ~ PY-04-17（17点） | ⭐⭐ | ~13min | ~9k |
| 6 | [py-05-operators.md](py-05-operators.md) | 运算符 / 优先级 / 短路 / 海象 | PY-05-01 ~ PY-05-15（15点） | ⭐ | ~12min | ~8k |
| 7 | [py-06-control-flow.md](py-06-control-flow.md) | if·for·while / else 子句 / match-case | PY-06-01 ~ PY-06-16（16点） | ⭐ | ~12min | ~8k |
| 8 | [py-07-functions.md](py-07-functions.md) | 参数种类 / LEGB / 闭包 / 递归 / lambda | PY-07-01 ~ PY-07-18（18点） | ⭐⭐ | ~13min | ~9k |
| 9 | [py-08-decorators.md](py-08-decorators.md) | 装饰器原理 / wraps / 带参装饰器 / partial | PY-08-01 ~ PY-08-15（15点） | ⭐⭐ | ~12min | ~8k |
| 10 | [py-09-oop.md](py-09-oop.md) | class·self / 继承多态 / super·MRO / slots·property | PY-09-01 ~ PY-09-16（16点） | ⭐⭐ | ~14min | ~9k |
| 11 | [py-10-magic-methods.md](py-10-magic-methods.md) | 魔术方法与协议 / 运算符重载 | PY-10-01 ~ PY-10-19（19点） | ⭐⭐ | ~13min | ~9k |
| 12 | [py-11-iterators-generators.md](py-11-iterators-generators.md) | 迭代协议 / 生成器 / yield·send / itertools | PY-11-01 ~ PY-11-16（16点） | ⭐⭐ | ~13min | ~9k |
| 13 | [py-12-exceptions.md](py-12-exceptions.md) | 异常层级 / try 四件套 / 自定义异常 / 异常链 | PY-12-01 ~ PY-12-16（16点） | ⭐⭐ | ~12min | ~8k |
| 14 | [py-13-modules-packages.md](py-13-modules-packages.md) | import 机制 / 包结构 / __name__ / 发布·uv | PY-13-01 ~ PY-13-17（17点） | ⭐⭐ | ~12min | ~8k |
| 15 | [py-14-stdlib.md](py-14-stdlib.md) | 标准库精选（os·json·collections·itertools…） | PY-14-01 ~ PY-14-15（15点） | ⭐⭐ | ~12min | ~8k |
| 16 | [py-15-file-io.md](py-15-file-io.md) | open·with / 读写模式 / csv·json 文件 / 编码坑 | PY-15-01 ~ PY-15-13（13点） | ⭐⭐ | ~12min | ~8k |
| 17 | [py-16-regex.md](py-16-regex.md) | 正则元字符 / 分组 / 贪婪 / re API / 实战 5 例 | PY-16-01 ~ PY-16-18（18点） | ⭐⭐ | ~12min | ~8k |
| 18 | [py-17-typing-modern.md](py-17-typing-modern.md) | 类型注解 / dataclass·Enum·Protocol / mypy | PY-17-01 ~ PY-17-17（17点） | ⭐⭐⭐ | ~12min | ~8k |
| 19 | [py-18-concurrency.md](py-18-concurrency.md) | GIL / threading / multiprocessing / asyncio | PY-18-01 ~ PY-18-14（14点） | ⭐⭐⭐ | ~14min | ~9k |
| 20 | [py-19-memory-performance.md](py-19-memory-performance.md) | 引用计数·GC / slots / 生成器省内存 / profiling | PY-19-01 ~ PY-19-14（14点） | ⭐⭐⭐ | ~12min | ~8k |
| 21 | [py-20-engineering-testing.md](py-20-engineering-testing.md) | 项目结构 / pytest / logging / lint·CI / 调试法 | PY-20-01 ~ PY-20-13（13点） | ⭐⭐⭐ | ~12min | ~8k |
| 22 | [py-21-pitfalls-interview.md](py-21-pitfalls-interview.md) | 全局消混 13 组 + 面试高频 30 问 | —（只引用 PY-ID，不新建） | ⭐⭐⭐ | ~15min | ~10k |
| 23 | [py-22-review-drill.md](py-22-review-drill.md) | 自测四件套 / SRS 复习表 / 30·60·90 天计划 | —（只引用 PY-ID，不新建） | ⭐⭐ | ~12min | ~8k |
| 24 | [py-23-memory-system.md](py-23-memory-system.md) | 记忆体系总纲 / Python 城一条主线串全库 / 20 分钟走城复习 | —（不新建锚点，编排已有） | ⭐⭐ | ~12min | ~8k |
| 25 | [py-24-anchor-registry.md](py-24-anchor-registry.md) | 锚点反查总表（325 条全局坐标） | —（各篇登记表的合并视图） | ⭐ | ~3min | ~10k |

> 注：ID 范围与点数为合并期实测统计；锚点反查总表与各篇"📌 锚点登记表"一致，全库反查词唯一性已检查。合计 318 个知识点、325 条锚点登记（py-00~py-20），全库预算约 200k tokens。

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
| 全量 325 条 → 见 [py-24 锚点反查总表](py-24-anchor-registry.md) | — | — | — | — |

> 源头是各篇"📌 锚点登记表"；全量 325 行已拆分至 **[py-24 锚点反查总表](py-24-anchor-registry.md)**（独立文件，全库反查词唯一性已按 [MEMORY-ENCODING-RULES 铁律 2](../../MEMORY-ENCODING-RULES.md) 检查）。py-21~py-24 不新建锚点，只引用 PY-ID。

## 🔗 相关章节
- → [../INDEX.md](../INDEX.md)（17-programming/INDEX.md）：编程记忆编码总入口（语法/设计模式/算法/面试）
- → [../../56-编程语言记忆方法.md](../../56-编程语言记忆方法.md)：八步流水线方法论（本目录的生成规则）
- → [../../方法地图.md](../../方法地图.md)：方法 ID（M01~M42+M07-R）注册表与术语约定
- → [../../templates/记忆训练进度追踪表.md](../../templates/记忆训练进度追踪表.md)：训练记录表（配合 [py-22 §五](py-22-review-drill.md) 使用）

## 📍 导航
> [返回 17-programming/INDEX](../INDEX.md) ｜ [返回主页](../../README.md)
