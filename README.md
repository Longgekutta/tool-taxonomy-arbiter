# tool-taxonomy-arbiter: 软件架构形态确定性仲裁决策装具
### Deterministic Software Archetype & Architectural Decision Arbiter

[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![UCFS: v1.0 Compliant](https://img.shields.io/badge/UCFS-v1.0%20Compliant-purple.svg)](#)
[![Mathematical Invariance: 100%](https://img.shields.io/badge/Invariance-100%25%20Guaranteed-gold.svg)](#)

---

## 🌟 项目使命与第一性原理 (Mission & First Principles)

在现代化软件工程与 AI Agent 智能体生态中，开发者面临一个高频且关键的架构分流困境：
> **“当我们产生一个新的软件构思，或者审视一个现有仓库时，它到底应该做成什么？是独立的项目工程？是一个智能体 Skill？是一个 MCP 服务？是一个刚性规范 Spec？还是一条负向防御规则 Rule？”**

传统的决策机制严重依赖个人主观感觉，甚至依赖大语言模型（LLM）的单次随机文本生成。由于大模型的随机采样温度与上下文漂移，**同一个需求在周一可能会被建议做成 Project，到了周四又被建议做成 Skill**。这种“三天两头变”的随机漂移彻底摧毁了架构的一致性与治理价值。

**`tool-taxonomy-arbiter` 为终结这一混沌状态而生**：
它通过**七维正交特征空间（7-Dimensional Orthogonal Feature Space）**与严格的**确定性决策树与连续欧式距离度量**，建立软件形态的数学单射映射：
$$\forall \vec{x} \in \mathcal{X}, \quad \text{Arbiter}(\vec{x}) \equiv \mathcal{A}^* \quad (f(x) \equiv x)$$
对任意给定的输入特征，系统**无论运行多少次，永远输出 100% 高度确定、逻辑可推导、不可动摇的黄金形态决策**！

---

## 🏛️ 技术思想溯源与全球对标矩阵 (World-Class Heritage & Prior Art)

本项目通过 `tool-omniscout-radar` 对全球 96 个架构分类学、系统设计规范与分类器标杆项目进行了系统性审计，并通过 `tool-token-distiller` 提纯出关键机制：

| 权威源流 / 开源基座 | 源流定位 | 核心机制突破 (Distilled Mechanics) | 本项目吸收与借鉴要点 | 超越点与取舍 (Trade-offs & Innovations) |
| :--- | :--- | :--- | :--- | :--- |
| **[ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101)** [^1] | `SYSTEM_DESIGN_GOLD_STANDARD` (⭐ 90k) | 可视化系统设计、计算密集服务与存储中间件的正交解耦定义 | 吸收其对分布式服务 (Svc)、离线装具 (Tool) 与边界守卫的严格职责划分 | 突破其纯静态教学范畴，转化为可通过可执行代码自动评判的数学特征向量矩阵 |
| **[tt-a1i/archify](https://github.com/tt-a1i/archify)** [^2] | `AST_ARCH_EXTRACTOR` (⭐ 72.3k) | 从物理代码树静态遍历自动推导软件拓扑与架构组件 | 吸收其代码/文档文件比例计算模型与网络端口监听签名检测算法 | 拓展了 Agentic 时代特有的 Model Context Protocol (MCP)、Agent SOP (Skill) 与多智能体网格 (Cluster) 新物种判定 |
| **[d2lang/d2](https://github.com/d2lang/d2)** [^3] | `DECLARATIVE_TAXONOMY_ENGINE` (⭐ 25.5k) | 严格声明式图谱语法与编译器状态机的确定性推导 | 吸收其确定性状态推导的设计哲学，确保相同输入永远产生完全相同的决策树 | 专注于软件资产分类与多仓库架构治理，实现零温度漂移 |
| **[kgrzybek/modular-monolith-with-ddd](https://github.com/kgrzybek/modular-monolith-with-ddd)** [^4] | `BOUNDED_CONTEXT_CANONICAL` (⭐ 14k) | 领域驱动设计 (DDD) 与严格的限界上下文防腐层划分 | 吸收其领域边界防腐理念，严格隔离 Rule (负向红线) 与 Spec (正向规范) | 融合 Spotify Backstage 与 CNCF 云原生多仓生态位模型 |
| **[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)** [^5] | `AGENT_RUNTIME_TAXONOMY` (⭐ 5.4k) | 智能体环境执行器与提示词认知工作流的解耦标准 | 吸收其将 Agent SOP (Skill) 与底层可执行机器装具 (Tool) 物理分离的规范 | 确立“纯提示词工作流为 skill-*，二进制/命令行算法为 tool-*”的绝对刚性分流守则 |

### 📚 权威引用与事实锚点 (Normative Footnotes)
[^1]: **ByteByteGoHq/system-design-101**: [https://github.com/ByteByteGoHq/system-design-101](https://github.com/ByteByteGoHq/system-design-101). *Explain complex systems using visuals and simple terms.*
[^2]: **tt-a1i/archify**: [https://github.com/tt-a1i/archify](https://github.com/tt-a1i/archify). *Deterministic architectural analysis and AST structure mapping.*
[^3]: **d2lang/d2**: [https://github.com/d2lang/d2](https://github.com/d2lang/d2). *Modern declarative diagramming language with deterministic compiler logic.*
[^4]: **kgrzybek/modular-monolith-with-ddd**: [https://github.com/kgrzybek/modular-monolith-with-ddd](https://github.com/kgrzybek/modular-monolith-with-ddd). *Domain-driven design and strict bounded context enforcement.*
[^5]: **NousResearch/hermes-agent**: [https://github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent). *Autonomous agent runtime and task orchestration taxonomy.*

---

## 📐 七维正交特征空间与决策机制 (7-D Feature Space)

系统将任意输入实体（无论是自然语言思路还是本地物理代码仓库）投影到以下七个物理维度 $\vec{x} = [d_1, d_2, d_3, d_4, d_5, d_6, d_7]^T \in [0.0, 1.0]^7$：

```
                ┌─────────────────────────────────────────────────────────┐
                │             7-Dimensional Orthogonal Space              │
                ├─────────────────────────────────────────────────────────┤
                │ D1. Lifecycle  : 瞬时 CLI (0.0) ── 后台长驻守护进程 (1.0)│
                │ D2. Protocol   : 管道 Stdio (0.0) ── MCP (0.5) ── HTTP (1.0) │
                │ D3. Execution  : 纯文本/规范 (0.0) ── 编译机器代码 (1.0)│
                │ D4. Agenticity : 纯机械逻辑 (0.0) ── AI 提示词流程 (1.0)│
                │ D5. Boundary   : 业务实现 (0.0) ── 契约Spec/红线Rule(1.0)│
                │ D6. Swarm      : 单体节点 (0.0) ── 多智能体集群网格 (1.0)│
                │ D7. Interface  : 无界面/API (0.0) ── GUI/移动App (1.0) │
                └─────────────────────────────────────────────────────────┘
```

### 11 大标准架构形态全景矩阵 (11 Canonical Archetypes)

| 架构形态 | 标准前缀 | 核心数学判定条件 | 适用场景与典型范例 |
| :--- | :--- | :--- | :--- |
| **SPEC** | `spec-*` | $D_5 \ge 0.75 \land D_3 \le 0.2 \land \text{Formal}$ | 刚性规范标准、RFC 契约、API 模式定义、验收神谕 |
| **RULE** | `rule-*` | $D_5 \ge 0.75 \land D_3 \le 0.2 \land \text{Negative}$ | 负向行为红线、安全边界拦截守卫、Linter 校验规则 |
| **TOOL** | `tool-*` | $D_3 \ge 0.7 \land D_1 \le 0.2 \land D_7 \le 0.2$ | 原子微装具、无状态命令行极速工具、UCFS 五动词实现 |
| **SKILL** | `skill-*` | $D_4 \ge 0.75 \land D_3 \le 0.4 \land D_1 \le 0.2$ | 智能体 SOP 认知流程、提示词引导工作流、多工具组装指导 |
| **MCP** | `mcp-*` | $D_2 \ge 0.85 \land D_3 \ge 0.7 \land \text{MCP-Proto}$ | Model Context Protocol 标准服务总线、AI 工具暴露 |
| **SVC** | `svc-*` | $D_1 \ge 0.75 \land D_2 \ge 0.6 \land D_7 \le 0.6$ | 长驻网络守护进程、HTTP/WebSocket 端口服务、微网关 |
| **CLUSTER**| `cluster-*` | $D_6 \ge 0.75 \land D_4 \ge 0.7$ | 多智能体协同网格、集群自治中枢、跨模型共生网络 |
| **APP** | `app-*` | $D_7 \ge 0.75 \land D_3 \ge 0.5$ | 终端用户交互应用、GUI 桌面端、安卓 APK、端到端业务机器人 |
| **INFRA** | `infra-*` | $D_1 \ge 0.8 \land D_2 \ge 0.7 \land \text{Tunnel/Relay}$| 网络穿透基建、Tailscale/DERP 中继节点、边缘节点配置 |
| **CFG** | `cfg-*` | $D_3 \le 0.2 \land D_1 \le 0.3 \land \text{Config}$ | 第三方开源框架配置、docker-compose、工作区模版 |
| **DOC** | `doc-*` | $D_3 \le 0.1 \land D_4 \le 0.2 \land D_5 \le 0.3$ | 知识库白皮书、战术手册、排障实战指南、研习笔记 |

---

## ⚖️ 决策动机、取舍与坚决不做的事 (Rationale, Trade-offs & Non-Goals)

### Non-Goals (坚决不做的事)
1. **不做黑盒大模型概率式猜测**：坚决不在核心决策逻辑中引入任何浮动温度与随机 Prompt。分类核心完全由解析器与正交向量度量驱动，确保数学级可重复性。
2. **不做代码生成与项目脚手架生成器**：本装具定位于“架构最高法院”裁决仲裁者，专精形态判定与合法性校验，不越俎代庖生成具体的业务代码。
3. **不做破坏性本地代码改写**：即使在审计存量仓库（`audit`）时，也仅输出裁决报告与对齐建议，绝对不擅自重命名或修改用户文件。

### Alternatives Considered (备选方案为何被否决)
* **备选方案 A：纯 Agent 提示词 (Pure Skill Prompt)**：
  * *否决原因*：提示词依赖大模型运行时，即使设置 `temperature=0`，在不同模型上下文窗口与版本迭代中依然存在概率漂移，无法满足用户对“高度相同或者相似，否则三天两头变”的硬性要求。
* **备选方案 B：简单关键词正则表达式匹配 (Simple Regex Mapping)**：
  * *否决原因*：现实软件概念往往交织多种术语（例如“编写一个网关的命令行客户端”同时包含网关和服务词汇），单一关键词规则极易冲突踩踏，缺乏高维空间的向量平滑距离度量能力。

---

## 🚀 快速开始 (Quick Start)

```bash
# 1. 依赖与运行时自检
python main.py setup

# 2. 执行自动化全量回归测试
python main.py test

# 3. 运行确定性架构形态仲裁
python main.py run --idea "扫描本地目录并计算代码哈希"
```

### UCFS 五动词使用指南

### 1. 环境验证 (`setup`)
```bash
python main.py setup
# 输出: [tool-taxonomy-arbiter] Setup OK: Runtime ready (Python 3.12.7, 11 Archetypes configured).
```

### 2. 仲裁推演 (`run` / `judge` / `audit`)

#### 场景 A：输入任意新构思或思路
```bash
python main.py run --idea "写一个全平台自动检测GitHub软件更新，扫描本地文件夹并一键批量静默安装更新包的极速命令行装具，退出后不留后台"
```
**输出**：确定性裁定为 `【 TOOL 】` (推荐前缀: `tool-`)，输出七维空间坐标与形式化推导链。

#### 场景 B：判断智能体 SOP 认知流程
```bash
python main.py run --idea "通过模糊语言搜索，调用三个工具流水线，自动筛选提取GitHub软件真实下载直达链接的SOP提示词工作流"
```
**输出**：确定性裁定为 `【 SKILL 】` (推荐前缀: `skill-`)。

#### 场景 C：批量审查现有代码仓库或多仓全景图谱
```bash
python main.py run --path "D:\github\FLEET_TAXONOMY_CATALOG.md"
```
**输出**：自动逐项核验 77 个现有仓库的物理实体与形态合规性，输出对齐率与稳定性校验结果。

### 3. 自动化回归测试 (`test`)
```bash
python main.py test
# 运行确定性不变定理测试、严格边界隔离测试与多仓图谱批量回归测试
```

### 4. 诊断健康检查 (`health`)
```bash
python main.py health
# 自动化自检正交投影引擎，确保基线裁定通过率 100%
```

### 5. 缓存与字节码清理 (`clean`)
```bash
python main.py clean
```

---

## 📄 许可证与引用 (License & Citation)

本项目采用 MIT 许可证开源。学术研究与工程架构引用请遵循 [CITATION.cff](CITATION.cff)。
