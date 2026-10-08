# py-18 并发编程 — 记忆编码

> **📍 本章导航**：前置 → [py-11 迭代生成](py-11-iterators-generators.md) ｜ 相关 → [py-19 内存与性能](py-19-memory-performance.md) ｜ 方法 → [M13](../../方法地图.md#m13)·[M15](../../方法地图.md#m15) ｜ 难度 ⭐⭐⭐ ｜ 阅读 ~13min（约 9k tokens）
>
> 本章逻辑链：py-11 的程序一次只跑一条道 → 本篇解决"多件事同时干怎么调度、怎么不打架" → 引出 py-19"并发之后内存和性能怎么收拾"。意象域：**十字路口调度**，锚点不越域；代码全部实测（Python 3.12.3），示例规模控制在秒级。

## 🗺️ 本篇知识地图
| 组块（口号） | 成员 | 一句话 |
|---|---|---|
| 一个红绿灯的地基 | PY-18-01 | GIL 决定线程能不能真并行 |
| 多线程车道三件套 | PY-18-02,03,08 | 开车道、设闸机、建待转区 |
| 多进程立交 | PY-18-04,05 | 修高架绕开红绿灯，批量派单 |
| 调度中心 | PY-18-06,07 | 线程池/进程池统一派单接口 |
| 潮汐车道与对照板 | PY-18-09~13 | 协程让道、调度亭、选型对照 |
| 车队编组 | PY-18-14 | TaskGroup 同进同出，一车抛锚全组回场 |

## 一、路口只有一个红绿灯（并发地基）
### PY-18-01 GIL 全局解释器锁
- **是什么**：CPython 的全局解释器锁（Global Interpreter Lock）：同一时刻只允许一个线程执行 Python 字节码。
- **为什么**：痛点：多线程跑 CPU 密集计算反而不见快 → 机制：解释器内存管理靠引用计数，多线程同改计数会互相踩，索性一把大锁 → 行为：IO 等待时线程让出 GIL 所以 IO 密集仍提速，CPU 密集则排队执行 → 边界：多进程/NumPy 原生扩展可绕开（每进程一锁）。
- **怎么写**：
```python
import threading, time
def busy(n):
    total = 0
    for i in range(n):
        total += i * i
N = 3_000_000
t0 = time.perf_counter(); busy(N); busy(N)
print(f"顺序跑 2 个计算任务: {time.perf_counter()-t0:.2f}s")
ts = [threading.Thread(target=busy, args=(N,)) for _ in range(2)]
t0 = time.perf_counter()
for t in ts: t.start()
for t in ts: t.join()
print(f"2 线程跑 2 个计算任务: {time.perf_counter()-t0:.2f}s")
```
→ 运行输出：`顺序跑 2 个计算任务: 0.26s` ／ `2 线程跑 2 个计算任务: 0.28s`（两行几乎一样；耗时随机器浮动）
- **何时用/不用**：写多线程前先问"任务是等 IO 还是烧 CPU"；烧 CPU 别用线程求快（用 PY-18-04 进程）。
- **锚点**：路口**唯一的红绿灯**——四条车道（线程）都得看同一盏灯，一次只放行一个方向，车再多也快不起来。
- **易错**：把"多线程=快"当公理；GIL 下 CPU 密集任务开线程可能更慢（多了切换开销）。
- **关联**：`→ PY-18-04：绕开 GIL 用多进程`　`→ PY-18-13：IO 密集 vs CPU 密集选型`

## 二、多线程车道三件套（threading/锁/队列）
### PY-18-02 threading 线程基础
- **是什么**：`threading.Thread` 开一条并行车道：`start()` 发车，`join()` 等它到站。
- **为什么**：痛点：下载 3 个文件串行要 1.5s，其实大部分时间在干等网络 → 机制：每个线程独立执行函数，IO 等待时让出 GIL 给别的线程 → 行为：3 个 0.5s 的下载任务并行约 0.5s 完成 → 边界：`join()` 不写主线程会提前收工；共享数据要加锁（PY-18-03）。
- **怎么写**：
```python
import threading, time
def download(name, sec):
    print(f"{name} 开始下载")
    time.sleep(sec)                # 模拟网络 IO 等待（让出 GIL）
    print(f"{name} 下载完成")
t0 = time.perf_counter()
ts = [threading.Thread(target=download, args=(f"文件{i}", 0.5)) for i in range(3)]
for t in ts: t.start()
for t in ts: t.join()
print(f"3 线程下载总耗时 {time.perf_counter()-t0:.2f}s（≈0.5s，不是 1.5s）")
```
→ 运行输出（三条下载交错）：`文件0 开始下载` …（交错）… `文件2 下载完成` ／ `3 线程下载总耗时 0.50s（≈0.5s，不是 1.5s）`
- **何时用/不用**：IO 密集（网络/磁盘/睡眠）用线程；纯计算别指望线程提速。
- **锚点**：路口的**多条车道**——车（任务）同时上路，等红灯的那条让别人先走。
- **易错**：忘写 `join()`，主线程先退出，任务"看起来没跑"；顺序打印语句会交错，别当 bug。
- **关联**：`→ PY-18-01：为什么 IO 才提速`　`→ PY-18-06：线程池是它的批量版`

### PY-18-03 线程锁 Lock
- **是什么**：`threading.Lock()` 互斥锁：同一时刻只有一个线程能进临界区（`with lock:`）。
- **为什么**：痛点：`counter = bump(counter)` 是"读→改→写"三步，中间被切走就丢更新 → 机制：锁把三步圈成不可插队的整段 → 行为：加锁后 8 线程各加 10 万次恒等于 80 万 → 边界：锁粒度过大会让线程排队变慢，还可能死锁（互相等对方放锁）。
- **怎么写**：
```python
import sys, threading
sys.setswitchinterval(0.000001)    # 演示用：切换更频繁，放大竞争
def bump(x): return x + 1
counter = 0
lock = threading.Lock()
def add_safe(n):
    global counter
    for _ in range(n):
        with lock:                 # 同一时刻只有一个线程能进
            counter = bump(counter)
def add_racy(n):                   # 同款但去掉 with lock
    global counter
    for _ in range(n):
        counter = bump(counter)    # 读→调用→写三步被切走就丢更新
for fn in (add_racy, add_safe):    # 驱动：8 线程 × 10 万次
    counter = 0
    ts = [threading.Thread(target=fn, args=(100_000,)) for _ in range(8)]
    for t in ts: t.start()
    for t in ts: t.join()
    print(f"{fn.__name__:10s} counter={counter}（应为 800000）")
```
→ 运行输出（8 线程 × 10 万次）：`add_racy   counter=202228（应为 800000）` ／ `add_safe   counter=800000（应为 800000）`（racy 每次不同）
- **何时用/不用**：多线程改共享数据必加锁；线程间只传数据用队列（PY-18-08）更省心。
- **锚点**：收费站**岗亭闸机**——取卡、抬杆、记录三步不许别的车插进来。
- **易错**：以为 `counter += 1` 是原子的；紧凑循环里看似没丢，一旦中间夹函数调用就大规模丢数据（实测丢七成）。
- **关联**：`→ PY-18-08：不共享就不用锁`　`→ PY-18-01：丢更新的根源是交错执行`

### PY-18-08 queue.Queue 线程安全队列
- **是什么**：`queue.Queue` 线程安全的"待转区"：生产者 `put()`，消费者 `get()`，满/空自动等待。
- **为什么**：痛点：线程间传数据要么共享变量（要锁）要么各干各的（要同步）→ 机制：队列内置锁+条件变量，写入读取自动互斥 → 行为：`maxsize=3` 满了生产者阻塞，空了消费者阻塞 → 边界：队列只传数据不传控制，结束要约定信号（如放入 None）。
- **怎么写**（节选：再起 1 个生产者线程 + 1 个消费者线程并 join 即可跑）：
```python
import threading, queue, time
q = queue.Queue(maxsize=3)
def producer():
    for i in range(5):
        q.put(f"商品{i}")
        print(f"生产 商品{i}（库存 {q.qsize()}）")
        time.sleep(0.05)           # 生产比消费快，队列会涨满让生产者等
    q.put(None)                    # 结束信号
def consumer(name):
    while True:
        item = q.get()
        if item is None: break
        time.sleep(0.1)
        print(f"{name} 消费 {item}")
```
→ 运行输出（交错顺序）：`生产 商品0（库存 1）` … `超市 消费 商品0` … `超市 消费 商品4` ／ `队列收尾为空: True`
- **何时用/不用**：生产者-消费者、任务分发用队列；一次性结果收集用 `concurrent.futures` 的 future 更简。
- **锚点**：路口的**待转区**——左转车排队候放行：路口空了放一辆进去，满了新车在停止线等。
- **易错**：`get()` 在空队列上永远等（死等），没结束信号的消费者线程会让 `join()` 挂住。
- **关联**：`→ PY-18-03：队列内置了锁`　`→ PY-18-06：线程池内部也用队列派活`

## 三、多进程立交（绕开红绿灯）
### PY-18-04 multiprocessing 基础
- **是什么**：`multiprocessing` 起独立进程：每个进程有自己的解释器与 GIL，CPU 密集可以真并行。
- **为什么**：痛点：GIL 卡死线程提速天花板 → 机制：进程有独立内存与锁，多核同时开工 → 行为：2 个计算任务 2 进程约省一半时间（实测 1.40s→0.71s）→ 边界：进程启动/通信有固定开销，任务太小反而亏；跨进程不能直接共享对象。
- **怎么写**：
```python
import multiprocessing as mp, time
def busy(n):
    total = 0
    for i in range(n):
        total += i * i
if __name__ == "__main__":         # spawn 模式下防递归创建进程
    N = 16_000_000
    t0 = time.perf_counter(); busy(N); busy(N)
    print(f"顺序 2 个计算任务: {time.perf_counter()-t0:.2f}s")
    t0 = time.perf_counter()
    with mp.Pool(2) as pool:
        pool.map(busy, [N, N])
    print(f"2 进程 2 个计算任务: {time.perf_counter()-t0:.2f}s")
```
→ 运行输出：`顺序 2 个计算任务: 1.40s` ／ `2 进程 2 个计算任务: 0.71s`（耗时随机器浮动）
- **何时用/不用**：CPU 密集（压缩/计算/解析大文件）用进程；IO 密集用线程或协程。
- **锚点**：另修一条**平行高架**——地面路口只有一盏灯（GIL），高架上的车有自己独立的路口，两头车流真并行。
- **易错**：Windows/macOS(spawn) 下忘写 `if __name__ == "__main__":` 会疯狂创建子进程直至崩溃。
- **关联**：`→ PY-18-01：进程为什么能绕开 GIL`　`→ PY-18-05：批量派活用进程池`

### PY-18-05 进程池 Pool
- **是什么**：`mp.Pool(n)` 预雇 n 个工人进程，`map/starmap` 把一批参数派下去收结果。
- **为什么**：痛点：每个任务起一个新进程，进程创建成本吃掉收益 → 机制：池内进程常驻复用，任务通过队列分发 → 行为：`pool.map(square, range(8))` 一次拿回全部结果 → 边界：任务函数必须可被 pickle（模块顶层 def）；返回值要能序列化。
- **怎么写**：
```python
import multiprocessing as mp
def square(n): return n * n
if __name__ == "__main__":
    with mp.Pool(processes=3) as pool:
        print("map 结果:", pool.map(square, range(8)))
        print("starmap 解包参数:", pool.starmap(pow, [(2, 10), (3, 3), (10, 2)]))
```
→ 运行输出：`map 结果: [0, 1, 4, 9, 16, 25, 36, 49]` ／ `starmap 解包参数: [1024, 27, 100]`
- **何时用/不用**：批量同构任务用池；单个大任务用 `ProcessPoolExecutor`（PY-18-07）。
- **锚点**：调度站**派单墙**——固定几名司机（工人进程）轮流接单，单子贴上墙就不用管谁接。
- **易错**：在交互式环境直接跑 `Pool` 会因缺 `__main__` 守卫报错；lambda 不能 pickle，别派给进程池。
- **关联**：`→ PY-18-04：进程基础`　`→ PY-18-07：futures 接口更统一`

## 四、调度中心（concurrent.futures 派单）
### PY-18-06 ThreadPoolExecutor 线程池
- **是什么**：`ThreadPoolExecutor(max_workers=4)` 统一派单接口：`submit()` 派活，`as_completed()` 谁先完收谁。
- **为什么**：痛点：手工管 Thread 的启动/join/结果传递太碎 → 机制：池内预开工人线程，任务队列自动分发，future 对象装结果 → 行为：6 个 0.3s 的 IO 任务 4 个工人约 0.6s 两批跑完 → 边界：线程仍受 GIL 限制，只对 IO 密集划算。
- **怎么写**：
```python
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
def fetch(i):
    time.sleep(0.3)                # 模拟网络请求
    return f"页面{i}"
t0 = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(fetch, i) for i in range(6)]
    for f in as_completed(futures):
        print("收到:", f.result())
print(f"6 任务 4 线程耗时 {time.perf_counter()-t0:.2f}s（≈0.6s，两批）")
```
→ 运行输出：`收到: 页面0` … `收到: 页面5`（完成顺序交错）／ `6 任务 4 线程耗时 0.60s（≈0.6s，两批）`
- **何时用/不用**：批量 IO（爬页、调接口）首选；CPU 密集换 PY-18-07。
- **锚点**：**网约车派单平台**——4 名司机在线，6 张订单进池子自动派，谁送完一单立刻接下一单。
- **易错**：`ex.map` 结果是惰性的，异常在迭代或 `future.result()` 时才抛出来。
- **关联**：`→ PY-18-07：同一接口换进程引擎`　`→ PY-18-02：线程池是 Thread 的批量管理版`

### PY-18-07 ProcessPoolExecutor 进程池
- **是什么**：和线程池同款接口、进程引擎：CPU 密集批量任务走"整车专线"。
- **为什么**：痛点：CPU 任务排在线程池里照旧被 GIL 卡 → 机制：`ProcessPoolExecutor` 用多进程并行，`map` 接口不变 → 行为：8 个计算任务 4 进程约省一半（1.08s→0.57s）→ 边界：任务函数需可 pickle；小任务会被进程开销吞掉收益。
- **怎么写**：
```python
from concurrent.futures import ProcessPoolExecutor
import time
def sum_squares(n): return sum(i * i for i in range(n))
if __name__ == "__main__":
    data = [3_000_000] * 8
    t0 = time.perf_counter()
    seq = [sum_squares(x) for x in data]
    print(f"顺序 8 任务: {time.perf_counter()-t0:.2f}s")
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(sum_squares, data))   # 接口和线程池一致
    print(f"4 进程 8 任务: {time.perf_counter()-t0:.2f}s")
    print("结果一致:", seq == results)
```
→ 运行输出：`顺序 8 任务: 1.08s` ／ `4 进程 8 任务: 0.57s` ／ `结果一致: True`（耗时随机器浮动）
- **何时用/不用**：批量 CPU 任务用它；单个超大任务+需要共享状态改多线程加锁或分块。
- **锚点**：货运站的**整车专线**——大件货（CPU 重活）不走小电驴（线程），整批装大货车走专线。
- **易错**：脚本顶层写多进程代码（无 `__main__` 守卫），spawn 系统上直接递归炸掉。
- **关联**：`→ PY-18-05：底层同为进程池`　`→ PY-18-06：接口一致只是换了引擎`

## 五、协程潮汐车道（asyncio）与选型
### PY-18-09 asyncio 协程 async/await
- **是什么**：协程（coroutine）是"会主动让道"的函数：`async def` 定义，`await` 暂停点，等待时让别的协程用线程。
- **为什么**：痛点：上万并发连接用线程，内存和切换扛不住 → 机制：协程是用户态调度，`await asyncio.sleep` 只是登记唤醒，不占 OS 线程 → 行为：3 个 0.3s 的泡茶协程总耗时约 0.3s → 边界：`await` 只能用于可等待对象；CPU 密集代码会卡住整个事件循环。
- **怎么写**：
```python
import asyncio, time
async def brew(name, sec):
    print(f"{name} 开始泡")
    await asyncio.sleep(sec)       # 等待时把控制权交回事件循环
    print(f"{name} 泡好了")
async def main():
    t0 = time.perf_counter()
    await asyncio.gather(brew("绿茶", 0.3), brew("红茶", 0.3), brew("乌龙茶", 0.3))
    print(f"三杯茶总耗时 {time.perf_counter()-t0:.2f}s")
asyncio.run(main())
```
→ 运行输出：`绿茶 开始泡` / `红茶 开始泡` / `乌龙茶 开始泡` / 三声"泡好了" / `三杯茶总耗时 0.30s`（≈0.3s 而非 0.9s）
- **何时用/不用**：海量 IO 并发（爬虫、聊天服务）用协程；少量 IO 任务线程池足够，CPU 用进程。
- **锚点**：**潮汐车道**——谁在等红灯（await 等 IO）就把车道借给对向车流，一条路跑出双向效率。
- **易错**：写 `async def` 却不 `await`，协程永不执行只报 RuntimeWarning；协程里跑重计算会堵死全部协程。
- **关联**：`→ PY-18-10：谁来驱动协程`　`→ PY-18-13：协程适合 IO 密集`

### PY-18-10 事件循环与 asyncio.run
- **是什么**：事件循环（event loop）是"路口中央调度亭"：`asyncio.run(main())` 创建循环、驱动协程、收尾清理。
- **为什么**：痛点：协程定义了却不跑，新手常问"我的 async 函数怎么没输出" → 机制：协程对象只是"待办单"，必须被循环调度才执行 → 行为：调用 `hello("A")` 不产生任何输出，`await` 才开始跑 → 边界：一个线程同时只有一个事件循环；循环内别用阻塞调用。
- **怎么写**：
```python
import asyncio
async def hello(tag):
    print(f"[{tag}] 协程开始执行")
    await asyncio.sleep(0.01)
coro = hello("A")
print("① 创建协程对象后，函数体还没跑")
async def main():
    await coro                     # 被 await 才开始跑
    print("③ main 里 await 后协程跑完了")
print("② 调用 asyncio.run 驱动事件循环")
asyncio.run(main())
```
→ 运行输出：`① 创建协程对象后，函数体还没跑` ／ `② 调用 asyncio.run 驱动事件循环` ／ `[A] 协程开始执行` ／ `③ main 里 await 后协程跑完了`
- **何时用/不用**：程序入口一个 `asyncio.run()` 足够；库作者用 `asyncio.run` 之外的入口会被诟病。
- **锚点**：路口**中央调度亭**——车（协程）排好队不动，调度亭一声令下才依次放行；没有调度亭路口瘫痪。
- **易错**：`asyncio.run()` 在已有循环里调用会报 RuntimeError；同步阻塞函数放进协程等于堵死调度亭。
- **关联**：`→ PY-18-09：协程定义`　`→ PY-18-11：循环里并发调度靠 create_task/gather`

### PY-18-11 create_task 与 gather
- **是什么**：`asyncio.create_task()` 把协程登记为并发任务；`asyncio.gather()` 并发跑一批并汇合结果。
- **为什么**：痛点：`await` 一个再 `await` 另一个，串行等满全程 → 机制：create_task 立即排进循环并发执行，gather 等全部完成 → 行为：3 个 0.2s 任务并发 0.2s 拿到全部结果 → 边界：gather 默认"全部成功才返回"，任一异常会冒泡（要 `return_exceptions=True`）。
- **怎么写**：
```python
import asyncio, time
async def worker(name, sec):
    await asyncio.sleep(sec)
    return f"{name}干完了"
async def main():
    t0 = time.perf_counter()
    tasks = [asyncio.create_task(worker(f"工位{i}", 0.2)) for i in range(3)]
    results = await asyncio.gather(*tasks)
    print(results)
    print(f"3 协程并发耗时 {time.perf_counter()-t0:.2f}s（≈0.2s）")
asyncio.run(main())
```
→ 运行输出：`['工位0干完了', '工位1干完了', '工位2干完了']` ／ `3 协程并发耗时 0.20s（≈0.2s）`
- **何时用/不用**：多个 IO 一起发就 gather；"谁先完成用谁"用 `asyncio.wait/as_completed`。
- **锚点**：**车队同时发车**——gather 是车队集合令：三辆车同时出发各跑各的路，回场统一报到。
- **易错**：`gather` 忘了 `*` 解包协程列表，或忘 `await` gather 本身，任务就"发车没人等"。
- **关联**：`→ PY-18-10：调度亭在管这些任务`　`→ PY-18-06：线程池的 as_completed 思路相同`

### PY-18-12 wait_for 超时控制
- **是什么**：`asyncio.wait_for(coro, timeout=0.3)` 给协程上闹钟：超时抛 `TimeoutError` 并取消任务。
- **为什么**：痛点：外部接口慢成狗，一条慢协程拖垮整条链路 → 机制：循环在超时点向任务发取消，`await` 收到异常 → 行为：1s 的慢任务 0.3s 被取消，循环继续跑别的 → 边界：取消是协作式的，纯 CPU 代码要跑到下一个 await 才响应。
- **怎么写**：
```python
import asyncio
async def slow():
    await asyncio.sleep(1.0)
    return "慢任务结果"
async def main():
    try:
        await asyncio.wait_for(slow(), timeout=0.3)   # 只等 0.3 秒
    except TimeoutError:
        print("超时！慢任务被取消（asyncio.TimeoutError）")
    print("事件循环还活着")
asyncio.run(main())
```
→ 运行输出：`超时！慢任务被取消（asyncio.TimeoutError）` ／ `事件循环还活着`
- **何时用/不用**：调外部接口、读外部资源必设超时；本地纯计算不需要。
- **锚点**：绿灯**倒计时牌**——倒计时归零还没过路口的车被拦下（取消）。
- **易错**：`TimeoutError` 在 3.11+ 即 `asyncio.TimeoutError`；捕获写成 `except Exception` 会吞掉别的错。
- **关联**：`→ PY-18-11：gather 也接受 timeout 参数`　`→ PY-12-02：超时是异常要处理`

### PY-18-13 实战选型：IO 密集 vs CPU 密集
- **是什么**：并发工具选择表：按"任务在等 IO 还是烧 CPU"选线程/协程/进程。
- **为什么**：痛点：三套 API 都能"同时跑"，选错工具零加速还更慢 → 机制：IO 等待让出 GIL（线程/协程够用），CPU 占用不放 GIL（必须进程）→ 行为：5 个 IO 任务协程 0.2s 完成，CPU 任务进进程池 → 边界：混合负载可以协程+进程池搭配（`run_in_executor`）。
- **怎么写**（节选：完整版含 `import`、`cpu_heavy` 定义与耗时统计）：
```python
async def main():
    async def fetch(i):
        await asyncio.sleep(0.2)    # 模拟 IO
        return i
    await asyncio.gather(*(fetch(i) for i in range(5)))   # IO → 协程
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(2) as ex:
        await loop.run_in_executor(ex, cpu_heavy, 8_000_000)  # CPU → 进程
```
→ 运行输出：`IO 密集 5 任务(协程): 0.20s（≈0.2s）` ／ `CPU 密集单任务(进程池): 0.36s`（耗时随机器浮动）
- **何时用/不用**：照对照板选；拿不准先写单线程，用 py-19 的 profiling 找到瓶颈再换。
- **锚点**：调度岗的**方案对照板**——板上写明"小车走潮汐车道、重卡走高架专线"，司机进路口先看板。
- **易错**：CPU 任务塞进 asyncio 直接跑（不 `run_in_executor`），整个事件循环被堵死。
- **关联**：`→ PY-18-01：GIL 是选型的根因`　`→ PY-19-08：先测量再决定优化哪里`

## 六、车队编组 TaskGroup（3.11+，口号：一车抛锚全组回场）

### PY-18-14 asyncio.TaskGroup 任务组
- **是什么**：`TaskGroup` 是 3.11+ 的结构化并发容器：`async with` 里批量建任务，出组时全部完成或全部收尾，错误打包成 `ExceptionGroup` 抛出。
- **为什么**：痛点是 `create_task` 裸飞任务后"谁失败了、别的任务收尾了没"一团糨糊 → 机制是 TaskGroup 把一组任务绑成车队：一组任务里任何一车抛锚，全组收到取消并统一回场，错误以 `ExceptionGroup`（`except*` 捕获）汇总 → 行为是并发任务成组管理、不丢错误不漏取消 → 边界是 3.11+ 才有；`gather` 也能并行但取消语义松散，新代码优先 TaskGroup。
- **怎么写**：
  ```python
  import asyncio
  async def job(n, fail=False):
      await asyncio.sleep(0.01)
      if fail: raise RuntimeError(f"车{n}抛锚")
      return n * 10
  async def main():
      try:
          async with asyncio.TaskGroup() as tg:
              tg.create_task(job(1))
              tg.create_task(job(2, fail=True))
      except* RuntimeError as eg:
          print("全组回场:", [str(e) for e in eg.exceptions])
  asyncio.run(main())
  ```
  → 运行输出：`全组回场: ['车2抛锚']`
- **何时用/不用**：一组协程要"同生共死"（批量请求、并行 IO 编组）就用；只是简单并行几个无关联任务且不关心取消，`gather` 写起来更短。
- **锚点**：调度中心的**车队编组发车**——编了组的车同进同出，一车抛锚全组回场点名（ExceptionGroup 就是回场点名簿）。
- **易错**：捕获要用 `except*`（星号）拿 `ExceptionGroup`，普通 `except RuntimeError` 接不到；组内任务抛错会取消其余任务，别指望"坏车不影响好车"（要隔离就各自开组）。
- **关联**：→ PY-18-11：gather/create_task 是散车发车，TaskGroup 是编组发车 ｜ → PY-12-09：ExceptionGroup 的展开读法同异常链思路。

## ⚔️ 对比消混表
| 易混点 | A | B | 判据 | 一句口诀 |
|---|---|---|---|---|
| threading vs multiprocessing | 共享内存、受 GIL | 独立内存、真并行 | 等 IO 还是烧 CPU | 等 IO 用线程，烧 CPU 用进程 |
| 线程 vs 协程 | OS 线程、切换贵 | 用户态调度、切换廉 | 并发量级（百级 vs 万级） | 少量线程够，海量靠协程 |
| Lock vs Queue | 保护共享数据 | 传递数据 | 要"护"还是要"传" | 共享加锁，传货用队列 |
| Pool.map vs submit | 一次派整批 | 逐个派活收集 | 批量同构 vs 灵活收集 | 批量 map，零碎 submit |
| gather vs wait_for | 汇合一组协程 | 给单个协程设时限 | 要"一起"还是要"限时" | 汇合是集合令，wait_for 是闹钟 |
| create_task vs await | 立即并发排程 | 当前位置暂停等待 | 要不要并发 | 先上车再等，还是站着等 |

## 📌 锚点登记表
| ID | 术语 | 锚点意象 | 反查词 |
|---|---|---|---|
| PY-18-01 | GIL | 路口唯一红绿灯 | 唯一红绿灯 |
| PY-18-02 | threading | 多条车道 | 多车道 |
| PY-18-03 | Lock | 岗亭闸机一次一辆 | 岗亭闸机 |
| PY-18-08 | queue.Queue | 待转区排队 | 待转区 |
| PY-18-04 | multiprocessing | 平行高架独立路口 | 平行高架 |
| PY-18-05 | Pool | 调度站派单墙 | 派单墙 |
| PY-18-06 | ThreadPoolExecutor | 网约车派单平台 | 网约车派单 |
| PY-18-07 | ProcessPoolExecutor | 货运整车专线 | 整车专线 |
| PY-18-09 | async/await | 潮汐车道让道 | 潮汐车道 |
| PY-18-10 | 事件循环 | 中央调度亭 | 调度亭 |
| PY-18-11 | gather/create_task | 车队同时发车 | 车队发车 |
| PY-18-12 | wait_for | 绿灯倒计时拦车 | 绿灯倒计时 |
| PY-18-13 | 实战选型 | 方案对照板 | 对照板 |
| PY-18-14 | TaskGroup | 车队编组同进同出 | 车队编组 |

## ✅ 自测清单（合上本篇，先写再看）
1. 用一句话解释：为什么多线程跑 CPU 密集任务不提速？
> 答案：GIL 使同一时刻只有一个线程执行字节码，CPU 任务不释放锁，只能排队。
2. 写出 4 个线程各执行 `work()` 并等待全部结束的三行骨架。
> 答案：`ts=[threading.Thread(target=work) for _ in range(4)]` → `for t in ts: t.start()` → `for t in ts: t.join()`。
3. 为什么 `counter = bump(counter)` 多线程会丢数？怎么修？
> 答案：读-改-写三步非原子，中间被切走就覆盖别人的写入；用 `with lock:` 包住。
4. spawn 系统下跑 multiprocessing 必须加什么？写出来。
> 答案：`if __name__ == "__main__":` 守卫包住创建进程的代码。

6. （说机制）TaskGroup 里一个任务抛错，其余任务会怎样？
   > 答案：全组被取消收尾（同进同出），错误打包成 `ExceptionGroup` 用 `except*` 捕获（PY-18-14）；要互不影响就各自开组。

## 📍 导航
> [返回 python/INDEX](INDEX.md) ｜ ⬅️ 上一篇：[py-17 现代语法](py-17-typing-modern.md) ｜ ➡️ 下一篇：[py-19 内存与性能](py-19-memory-performance.md)
