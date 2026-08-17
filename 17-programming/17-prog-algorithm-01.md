# 算法记忆 — 20个经典算法编码

> 记忆策略：每个算法 → 原理画面 → 执行步骤 → 复杂度锚点 → 代码模板
> 目标：看到算法名 → 脑中浮现动态画面 → 自动回忆实现

---

## 一、排序算法（6个）
> 定位宫殿：**图书馆书架区**（想象整理书架上的书）

### 1. 冒泡排序 Bubble Sort
- **原理**：相邻元素两两比较，大的往后"冒泡"
- **画面**：一排水杯装着不同高度的水，相邻两杯比较，多的倒一点给少的，反复几轮就排好了
- **步骤**：
  1. 从头到尾，相邻比较，大的交换到后面
  2. 一轮后最大的到末尾
  3. 重复n-1轮
- **复杂度**：O(n²) — 想象n个人两两握手，握n轮
- **代码模板**：
  ```python
  def bubble_sort(arr):
      n = len(arr)
      for i in range(n):
          for j in range(n - i - 1):
              if arr[j] > arr[j + 1]:
                  arr[j], arr[j + 1] = arr[j + 1], arr[j]
      return arr
  ```
- **编码**：`两两冒泡` → 双层循环，内层比较相邻元素
- **锚点**：图书馆入口的**气泡灯箱** — 气泡一个个往上冒

### 2. 选择排序 Selection Sort
- **原理**：每轮选最小的放到前面
- **画面**：一堆苹果中每次挑最小的放到篮子最前面
- **步骤**：
  1. 从未排序部分找最小值
  2. 放到已排序部分末尾
  3. 重复直到全部排完
- **复杂度**：O(n²)
- **代码模板**：
  ```python
  def selection_sort(arr):
      for i in range(len(arr)):
          min_idx = i
          for j in range(i + 1, len(arr)):
              if arr[j] < arr[min_idx]:
                  min_idx = j
          arr[i], arr[min_idx] = arr[min_idx], arr[i]
      return arr
  ```
- **编码**：`选最小前置` → 外层定位置，内层找最小
- **锚点**：书架第一层的**选苹果篮**

### 3. 插入排序 Insertion Sort
- **原理**：像打扑克牌，每张牌插入已排序手牌的正确位置
- **画面**：左手拿已排好的牌，右手抽新牌，从右往左找位置插入
- **步骤**：
  1. 取下一个元素
  2. 与已排序部分从后往前比较
  3. 找到位置插入
- **复杂度**：O(n²)，但对近乎有序的数据接近O(n)
- **代码模板**：
  ```python
  def insertion_sort(arr):
      for i in range(1, len(arr)):
          key = arr[i]
          j = i - 1
          while j >= 0 and arr[j] > key:
              arr[j + 1] = arr[j]
              j -= 1
          arr[j + 1] = key
      return arr
  ```
- **编码**：`扑克插牌` → key暂存当前值，往前找位置插入
- **锚点**：书架旁的**扑克桌**

### 4. 快速排序 Quick Sort
- **原理**：选基准(pivot)，小的放左边，大的放右边，递归处理
- **画面**：学校排队，老师喊"比我矮的站左边，比我高的站右边"，然后左右两边各找新老师继续分
- **步骤**：
  1. 选基准元素（常用第一个/最后一个/随机）
  2. 分区(partition)：小于基准的放左边，大于的放右边
  3. 递归对左右两部分排序
- **复杂度**：平均O(n log n)，最坏O(n²)
- **代码模板**：
  ```python
  def quick_sort(arr):
      if len(arr) <= 1:
          return arr
      pivot = arr[0]
      left = [x for x in arr[1:] if x <= pivot]
      right = [x for x in arr[1:] if x > pivot]
      return quick_sort(left) + [pivot] + quick_sort(right)
  ```
- **编码**：`老师分队` → 选基准，分左右，递归
- **锚点**：书架中间的**指挥台** — 老师站在中间指挥

### 5. 归并排序 Merge Sort
- **原理**：分治法，先拆成小段，再两两合并
- **画面**：两摞已排好的扑克牌，每次比较两张牌顶，取小的放到新摞
- **步骤**：
  1. 从中间分成两半
  2. 递归排序左右两半
  3. 合并两个有序数组
- **复杂度**：稳定O(n log n)
- **代码模板**：
  ```python
  def merge_sort(arr):
      if len(arr) <= 1:
          return arr
      mid = len(arr) // 2
      left = merge_sort(arr[:mid])
      right = merge_sort(arr[mid:])
      return merge(left, right)

  def merge(left, right):
      result = []
      i = j = 0
      while i < len(left) and j < len(right):
          if left[i] <= right[j]:
              result.append(left[i]); i += 1
          else:
              result.append(right[j]); j += 1
      return result + left[i:] + right[j:]
  ```
- **编码**：`拆牌合牌` → 分两半递归，双指针合并
- **锚点**：书架两端的**两摞牌**

### 6. 堆排序 Heap Sort
- **原理**：建大顶堆，每次取堆顶（最大值）放到末尾
- **画面**：一棵倒三角形的树，最大的在顶上，每次摘顶放到最后
- **步骤**：
  1. 建大顶堆（从最后一个非叶子节点开始调整）
  2. 堆顶与末尾交换，堆大小减1
  3. 重新调整堆，重复
- **复杂度**：稳定O(n log n)
- **代码模板**：
  ```python
  def heapify(arr, n, i):
      largest = i
      l, r = 2*i+1, 2*i+2
      if l < n and arr[l] > arr[largest]: largest = l
      if r < n and arr[r] > arr[largest]: largest = r
      if largest != i:
          arr[i], arr[largest] = arr[largest], arr[i]
          heapify(arr, n, largest)

  def heap_sort(arr):
      n = len(arr)
      for i in range(n//2-1, -1, -1):
          heapify(arr, n, i)
      for i in range(n-1, 0, -1):
          arr[0], arr[i] = arr[i], arr[0]
          heapify(arr, i, 0)
  ```
- **编码**：`堆顶摘果` → 建堆+反复摘堆顶
- **锚点**：书架顶端的**倒三角果树**

---

## 二、搜索算法（4个）
> 定位宫殿：**迷宫探险区**

### 7. 线性搜索 Linear Search
- **原理**：从头到尾逐个检查
- **画面**：在书架上一本本翻找目标书
- **复杂度**：O(n)
- **代码**：
  ```python
  def linear_search(arr, target):
      for i, val in enumerate(arr):
          if val == target:
              return i
      return -1
  ```
- **编码**：`逐本翻找` → for循环逐个比较
- **锚点**：迷宫入口的**一排书架**

### 8. 二分搜索 Binary Search
- **原理**：有序数组中，每次取中间值比较，缩小一半范围
- **画面**：猜数字游戏，"大了→往左猜""小了→往右猜"
- **复杂度**：O(log n) — 每次砍一半
- **代码模板**：
  ```python
  def binary_search(arr, target):
      lo, hi = 0, len(arr) - 1
      while lo <= hi:
          mid = (lo + hi) // 2
          if arr[mid] == target:
              return mid
          elif arr[mid] < target:
              lo = mid + 1
          else:
              hi = mid - 1
      return -1
  ```
- **编码**：`猜数字砍半` → lo/hi夹逼，mid比较
- **锚点**：迷宫中间的**天平** — 每次称一半

### 9. 深度优先搜索 DFS
- **原理**：一条路走到黑，走不通再回溯
- **画面**：走迷宫，右手扶墙一直走，遇到死路就退回来换条路
- **复杂度**：O(V+E)，V是顶点数，E是边数
- **代码模板（递归）**：
  ```python
  def dfs(graph, node, visited):
      visited.add(node)
      for neighbor in graph[node]:
          if neighbor not in visited:
              dfs(graph, neighbor, visited)
  ```
- **代码模板（栈）**：
  ```python
  def dfs_iterative(graph, start):
      visited = set()
      stack = [start]
      while stack:
          node = stack.pop()
          if node not in visited:
              visited.add(node)
              stack.extend(graph[node] - visited)
  ```
- **编码**：`右手扶墙走到底` → 递归/栈，先深入再回溯
- **锚点**：迷宫深处的**死胡同标志**

### 10. 广度优先搜索 BFS
- **原理**：一层一层扩展，先访问所有邻居再往下
- **画面**：往池塘扔石头，波纹一圈一圈向外扩散
- **复杂度**：O(V+E)
- **代码模板**：
  ```python
  from collections import deque
  def bfs(graph, start):
      visited = set([start])
      queue = deque([start])
      while queue:
          node = queue.popleft()
          for neighbor in graph[node]:
              if neighbor not in visited:
                  visited.add(neighbor)
                  queue.append(neighbor)
  ```
- **编码**：`水波纹扩散` → 队列，先进先出，一层层扩展
- **锚点**：迷宫中央的**水池涟漪**

---

## 三、动态规划（4个）
> 定位宫殿：**阶梯教室**（想象一排排递增的台阶）

### 11. 斐波那契数列 Fibonacci
- **原理**：f(n) = f(n-1) + f(n-2)，自底向上填表
- **画面**：台阶上，每一步踩在前两步的肩膀上
- **复杂度**：O(n)
- **代码**：
  ```python
  def fib(n):
      if n <= 1: return n
      dp = [0] * (n + 1)
      dp[1] = 1
      for i in range(2, n + 1):
          dp[i] = dp[i-1] + dp[i-2]
      return dp[n]
  ```
- **编码**：`踩肩膀上台阶` → dp[i] = dp[i-1] + dp[i-2]
- **锚点**：阶梯教室第一排的**兔子雕塑**

### 12. 爬楼梯 Climbing Stairs
- **原理**：每次爬1或2阶，到第n阶有多少种走法
- **画面**：一个人站在楼梯前，每次迈1步或2步，数有多少种到达顶端的方式
- **复杂度**：O(n)
- **代码**：
  ```python
  def climb_stairs(n):
      if n <= 2: return n
      dp = [0] * (n + 1)
      dp[1], dp[2] = 1, 2
      for i in range(3, n + 1):
          dp[i] = dp[i-1] + dp[i-2]
      return dp[n]
  ```
- **编码**：`迈一步或两步` → dp[i] = dp[i-1] + dp[i-2]
- **锚点**：阶梯教室的**楼梯模型**

### 13. 最长公共子序列 LCS
- **原理**：两个序列的最长公共子序列（不连续）
- **画面**：两条DNA链并排放，相同碱基用线连起来，数最长连线
- **复杂度**：O(m*n)
- **代码**：
  ```python
  def lcs(text1, text2):
      m, n = len(text1), len(text2)
      dp = [[0]*(n+1) for _ in range(m+1)]
      for i in range(1, m+1):
          for j in range(1, n+1):
              if text1[i-1] == text2[j-1]:
                  dp[i][j] = dp[i-1][j-1] + 1
              else:
                  dp[i][j] = max(dp[i-1][j], dp[i][j-1])
      return dp[m][n]
  ```
- **编码**：`DNA配对` → 相同则左上+1，不同取max(上,左)
- **锚点**：阶梯教室讲台上的**双链DNA模型**

### 14. 背包问题 Knapsack
- **原理**：有限容量的背包，选物品使总价值最大
- **画面**：登山背包，只能装10kg，每件装备有重量和价值，选最有价值的组合
- **复杂度**：O(n*W)
- **代码（0-1背包）**：
  ```python
  def knapsack(weights, values, W):
      n = len(weights)
      dp = [[0]*(W+1) for _ in range(n+1)]
      for i in range(1, n+1):
          for w in range(W+1):
              if weights[i-1] <= w:
                  dp[i][w] = max(dp[i-1][w],
                                 dp[i-1][w-weights[i-1]] + values[i-1])
              else:
                  dp[i][w] = dp[i-1][w]
      return dp[n][W]
  ```
- **编码**：`登山选装备` → 不装dp[i-1][w] vs 装dp[i-1][w-wi]+vi
- **锚点**：阶梯教室后排的**登山背包**

---

## 四、图算法（3个）
> 定位宫殿：**地图导航区**

### 15. Dijkstra最短路径
- **原理**：贪心，每次选距离最近的未访问节点
- **画面**：导航App，从当前位置出发，每次选最近的路口扩展
- **复杂度**：O((V+E) log V) — 用优先队列
- **代码**：
  ```python
  import heapq
  def dijkstra(graph, start):
      dist = {node: float('inf') for node in graph}
      dist[start] = 0
      pq = [(0, start)]
      while pq:
          d, u = heapq.heappop(pq)
          if d > dist[u]: continue
          for v, w in graph[u]:
              if dist[u] + w < dist[v]:
                  dist[v] = dist[u] + w
                  heapq.heappush(pq, (dist[v], v))
      return dist
  ```
- **编码**：`最近路口扩展` → 小根堆贪心，松弛更新
- **锚点**：地图区的**导航仪**

### 16. Kruskal最小生成树
- **原理**：按边权排序，依次选最小的不形成环的边
- **画面**：修公路连接所有城市，每次选最短的路，但不能形成环路
- **复杂度**：O(E log E)
- **代码**：
  ```python
  def kruskal(n, edges):
      edges.sort(key=lambda x: x[2])  # 按权重排序
      parent = list(range(n))
      def find(x):
          if parent[x] != x:
              parent[x] = find(parent[x])
          return parent[x]
      mst = []
      for u, v, w in edges:
          if find(u) != find(v):
              parent[find(u)] = find(v)
              mst.append((u, v, w))
      return mst
  ```
- **编码**：`最短路不环` → 排序+并查集判环
- **锚点**：地图区的**公路规划图**

### 17. 拓扑排序 Topological Sort
- **原理**：有向无环图(DAG)的线性排序，保证依赖关系
- **画面**：大学选课，必须先修完前置课程才能选后续课程
- **复杂度**：O(V+E)
- **代码**：
  ```python
  from collections import deque
  def topo_sort(graph, in_degree):
      queue = deque([n for n in in_degree if in_degree[n] == 0])
      order = []
      while queue:
          node = queue.popleft()
          order.append(node)
          for neighbor in graph[node]:
              in_degree[neighbor] -= 1
              if in_degree[neighbor] == 0:
                  queue.append(neighbor)
      return order
  ```
- **编码**：`选课依赖` → BFS，入度为0的先修
- **锚点**：地图区的**课程表**

---

## 五、其他经典算法（3个）
> 定位宫殿：**工具箱**

### 18. KMP字符串匹配
- **原理**：利用已匹配信息跳过不必要的比较
- **画面**：在文章中找一个词，发现不匹配时不是从头开始，而是利用已匹配部分跳着找
- **复杂度**：O(n+m)
- **代码**：
  ```python
  def kmp_search(text, pattern):
      n, m = len(text), len(pattern)
      # 构建next数组（部分匹配表）
      nxt = [0] * m
      j = 0
      for i in range(1, m):
          while j > 0 and pattern[i] != pattern[j]:
              j = nxt[j - 1]
          if pattern[i] == pattern[j]:
              j += 1
          nxt[i] = j
      # 匹配
      j = 0
      for i in range(n):
          while j > 0 and text[i] != pattern[j]:
              j = nxt[j - 1]
          if text[i] == pattern[j]:
              j += 1
          if j == m:
              return i - m + 1
      return -1
  ```
- **编码**：`跳着找词` → next数组记录最长前后缀，失配时跳转
- **锚点**：工具箱里的**放大镜**

### 19. 并查集 Union-Find
- **原理**：管理不相交集合，支持合并和查询
- **画面**：社交网络，查两个人是不是同一个圈子，是的话合并圈子
- **复杂度**：近O(1)（路径压缩+按秩合并）
- **代码**：
  ```python
  class UnionFind:
      def __init__(self, n):
          self.parent = list(range(n))
          self.rank = [0] * n
      def find(self, x):
          if self.parent[x] != x:
              self.parent[x] = self.find(self.parent[x])
          return self.parent[x]
      def union(self, x, y):
          px, py = self.find(x), self.find(y)
          if px == py: return
          if self.rank[px] < self.rank[py]:
              px, py = py, px
          self.parent[py] = px
          if self.rank[px] == self.rank[py]:
              self.rank[px] += 1
  ```
- **编码**：`社交圈子` → find找老大，union合圈子
- **锚点**：工具箱里的**社交网络图**

### 20. 回溯法 Backtracking
- **原理**：试探+剪枝，走不通就退回上一步
- **画面**：走迷宫，每到岔路口标记"来过"，死路就擦掉标记退回
- **复杂度**：取决于问题，通常指数级
- **代码模板（N皇后）**：
  ```python
  def solve_n_queens(n):
      def backtrack(row, cols, diag1, diag2, board):
          if row == n:
              result.append(["".join(r) for r in board])
              return
          for col in range(n):
              if col in cols or row-col in diag1 or row+col in diag2:
                  continue  # 剪枝
              board[row][col] = 'Q'
              backtrack(row+1, cols|{col}, diag1|{row-col},
                       diag2|{row+col}, board)
              board[row][col] = '.'  # 回溯
      result = []
      backtrack(0, set(), set(), set(),
                [['.']*n for _ in range(n)])
      return result
  ```
- **编码**：`迷宫探路` → 选择→递归→撤销选择
- **锚点**：工具箱里的**迷宫棋盘**

---

## 六、算法分类宫殿

### 📚 图书馆书架区 — 排序算法
| 位置 | 算法 | 画面锚点 |
|------|------|----------|
| 入口气泡灯 | 冒泡排序 | 两两冒泡 |
| 第一层苹果篮 | 选择排序 | 选最小前置 |
| 旁边扑克桌 | 插入排序 | 扑克插牌 |
| 中间指挥台 | 快速排序 | 老师分队 |
| 两端牌摞 | 归并排序 | 拆牌合牌 |
| 顶端果树 | 堆排序 | 堆顶摘果 |

### 🏰 迷宫探险区 — 搜索算法
| 位置 | 算法 | 画面锚点 |
|------|------|----------|
| 入口书架 | 线性搜索 | 逐本翻找 |
| 中央天平 | 二分搜索 | 猜数字砍半 |
| 深处死胡同 | DFS | 右手扶墙 |
| 中央水池 | BFS | 水波纹扩散 |

### 🪜 阶梯教室 — 动态规划
| 位置 | 算法 | 画面锚点 |
|------|------|----------|
| 第一排兔子 | 斐波那契 | 踩肩膀上台阶 |
| 楼梯模型 | 爬楼梯 | 迈一步或两步 |
| 讲台DNA | LCS | DNA配对 |
| 后排背包 | 背包问题 | 登山选装备 |

### 🗺️ 地图导航区 — 图算法
| 位置 | 算法 | 画面锚点 |
|------|------|----------|
| 导航仪 | Dijkstra | 最近路口扩展 |
| 公路图 | Kruskal | 最短路不环 |
| 课程表 | 拓扑排序 | 选课依赖 |

### 🧰 工具箱 — 其他算法
| 位置 | 算法 | 画面锚点 |
|------|------|----------|
| 放大镜 | KMP | 跳着找词 |
| 社交图 | 并查集 | 社交圈子 |
| 迷宫棋盘 | 回溯法 | 迷宫探路 |

---

## 七、易混算法对比

### 排序算法速查
| 算法 | 平均 | 最坏 | 最好 | 空间 | 稳定 |
|------|------|------|------|------|------|
| 冒泡 | O(n²) | O(n²) | O(n) | O(1) | ✅ |
| 选择 | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| 插入 | O(n²) | O(n²) | O(n) | O(1) | ✅ |
| 快排 | O(nlogn) | O(n²) | O(nlogn) | O(logn) | ❌ |
| 归并 | O(nlogn) | O(nlogn) | O(nlogn) | O(n) | ✅ |
| 堆排 | O(nlogn) | O(nlogn) | O(nlogn) | O(1) | ❌ |

**记忆口诀**：
> **快选堆不稳**（快排、选择、堆排序不稳定）
> **冒插归稳定**（冒泡、插入、归并排序稳定）

### DFS vs BFS
| 特性 | DFS | BFS |
|------|-----|-----|
| 数据结构 | 栈（递归） | 队列 |
| 搜索方式 | 深度优先 | 广度优先 |
| 适合场景 | 路径存在性、连通性 | 最短路径（无权图） |
| 空间 | O(h) 树高 | O(w) 最大宽度 |
| 画面 | 右手扶墙走到底 | 水波纹一圈圈扩散 |

### 贪心 vs 动态规划
| 特性 | 贪心 | 动态规划 |
|------|------|----------|
| 策略 | 每步选局部最优 | 考虑所有子问题 |
| 正确性 | 需证明贪心选择性质 | 一定最优 |
| 复杂度 | 通常更低 | 通常更高 |
| 画面 | 眼前最好的就拿 | 列表比较所有可能 |

---

## 八、复杂度记忆锚点

### 常见复杂度阶梯
```
O(1)       → 开灯         （一步到位）
O(log n)   → 翻字典       （每次翻一半）
O(n)       → 点名         （逐个喊）
O(n log n) → 排队分组     （分组+合并）
O(n²)      → 握手大会     （每人跟每人握手）
O(2ⁿ)      → 子集爆炸     （每元素选或不选）
O(n!)      → 全排列       （所有排列方式）
```

### 速记
- **O(1)**：哈希表查找 — 钥匙开门
- **O(log n)**：二分搜索 — 猜数字
- **O(n)**：遍历数组 — 点名
- **O(n log n)**：快排/归并 — 分治
- **O(n²)**：冒泡/选择 — 双重循环
- **O(2^n)**：递归子集 — 指数爆炸
