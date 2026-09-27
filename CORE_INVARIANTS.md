# Core Invariants & Axiomatic Foundation (CORE_INVARIANTS.md)

## 1. Mathematical Classification Invariance (确定性决策不变量)

`tool-taxonomy-arbiter` 贯彻数学函数严格确定性：
对于任意给定的输入特征向量 $\vec{x}$（无论是软件思路或代码仓库的静态特征）：
$$\forall \vec{x} \in \mathcal{X}, \quad \text{Arbiter}(\vec{x}) \equiv \mathcal{A}^* \quad \text{其中 } \mathcal{A}^* \in \{\text{spec}, \text{tool}, \text{skill}, \text{rule}, \text{svc}, \text{mcp}, \text{cluster}, \text{app}, \text{infra}, \text{cfg}, \text{doc}\}$$

无论在任何操作系统、任何时间、调用多少次，计算结果永远一致（零温度漂移，零随机种子扰动，严格单射/满射闭包）。

---

## 2. 7-Dimensional Orthogonal Feature Space (七维正交特征空间)

分类引擎基于以下正交特征基底 $\mathcal{B} = \{d_1, d_2, d_3, d_4, d_5, d_6, d_7\}$：

| 维度标号 | 物理量名称 | 取值域 | 判定物理依据 |
| :--- | :--- | :--- | :--- |
| **D1: Lifecycle** | 进程生命周期与常驻状态 | $[0.0, 1.0]$ | 0 = 瞬时退出 CLI (One-shot)；1 = 长驻后台守护进程 (Daemon / Event Loop) |
| **D2: Protocol** | 外部协议边界表面 | $[0.0, 1.0]$ | 0 = 命令行 Stdio / 管道；1 = 网络套接字 (HTTP/gRPC/WebSocket) 或 MCP JSON-RPC |
| **D3: Execution** | 主体执行载体与解释介质 | $[0.0, 1.0]$ | 0 = 纯文本规范/约束/SOP；1 = 机器指令 / 原生可执行代码 (Python/Rust/Go/C/JS) |
| **D4: Agenticity** | 智能体操作流依赖度 | $[0.0, 1.0]$ | 0 = 机械确定性算法；1 = 依赖 LLM 认知推理的提示词 SOP 工作流 |
| **D5: Boundary** | 规范权威度与边界性质 | $[0.0, 1.0]$ | 0 = 业务功能实现；1 = 刚性验收神谕 (Spec) 或 负向行为红线 (Rule) |
| **D6: Swarm** | 多智能体集群拓扑 | $[0.0, 1.0]$ | 0 = 单智能体/单节点；1 = 分布式共识、多智能体协同网格 (Swarm Mesh) |
| **D7: Interface** | 用户交互终端表象 | $[0.0, 1.0]$ | 0 = 无界面/Headless/API；1 = GUI/Web 前端/移动 App/端到端机器人 |

---

## 3. Strict Boundary Invariants (严格形态隔离法则)

1. **Rule vs Spec**:
   - `rule-*`：绝对禁止/被动边界拦截（例如：禁止提交私钥、禁止越界写内存）。
   - `spec-*`：正向验收神谕与数据契约（例如：CLI 五动词规范、JSON-RPC 契约）。
2. **Tool vs Skill**:
   - `tool-*`：无状态机器代码，输入输出数学确定，执行耗时通常 $< 5s$，符合 UCFS 五动词。
   - `skill-*`：引导 AI 智能体的 SOP 流程，纯 Markdown + YAML 元数据，运行在智能体推理循环中。
3. **Tool vs Svc vs Mcp**:
   - `tool-*`：单次触发即退出，无常驻端口。
   - `svc-*`：绑定 TCP/HTTP/WS 端口，常驻监听网络请求。
   - `mcp-*`：专门实现 Model Context Protocol (stdio/SSE)，专为 AI 宿主暴露工具与资源。
4. **Tool vs Cluster**:
   - `cluster-*`：调度多模型、多智能体协作闭环，具备自治拓扑。

---

## 4. Universal CLI Facade (UCFS v1.0) 五动词严格契约

所有装具命令必须 100% 具备并支持五大标准动词：
- `setup`: 验证环境完整性
- `run`: 执行确定性仲裁推演 (`judge` / `audit`)
- `test`: 运行自动化回归与数学不变量单元测试
- `health`: 诊断装具健康度与自检
- `clean`: 清理运行时字节码与中间产物

---

## 5. Provenance & Citation Standards

本组件严格符合 IEEE/ACM 软件工程学术溯源体系与 `.provenance.json` 规范，所有参考设计均具备可验证的 GitHub 拓扑哈希与星标坐标。
