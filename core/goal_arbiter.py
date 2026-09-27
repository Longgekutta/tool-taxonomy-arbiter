#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/goal_arbiter.py: First-Principles Goal-Driven Taxonomy Arbiter.
Strict forward deduction from Core Purpose & Intent -> Minimal Viable Archetype.
Does NOT reverse-engineer or "sketch after tracing" from existing code bloat.
Equipped with Intent De-noising Scalpel to expose and neutralize implementation bias.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Any, Optional
import json
import re
from core.intent_cleaner import IntentCleaner, IntentDenoiseReport


class ArchetypeEnum(str, Enum):
    SPEC = "spec"         # 刚性规范标准 (RFC契约 / 模式定义 / 验收神谕 - 零执行代码)
    RULE = "rule"         # 负向行为红线 (安全防线 / 拦截守卫 / 边界禁令 - 纯拦截谓词)
    SKILL = "skill"       # 智能体认知 SOP (指导 AI 如何思考、拆解并调用现有工具 - 纯提示词与策略)
    DOC = "doc"           # 战术手册与知识库 (人脑学习文献 / 排障手册 / 白皮书 - 零机器执行实体)
    TOOL = "tool"         # 原子微装具 (秒级退出、确定性转换、机器算法与CLI、无常驻端口)
    MCP = "mcp"           # MCP 协议服务 (专为大模型暴露专有工具与动态上下文的 JSON-RPC 接头)
    SVC = "svc"           # 网络长驻服务 (监听网络端口、承载不可预测外部网络并发的微服务/网关)
    CLUSTER = "cluster"   # 集群自治中枢 (单个程序搞不定，需多模型/多Agent分布式协同网格)
    APP = "app"           # 终端交互应用 (面向终端用户的 GUI/移动APK/或特定垂直业务闭环)
    INFRA = "infra"       # 基础设施中继 (物理网络穿透、VPS 中继节点、底层网络拓扑)
    CFG = "cfg"           # 工作区环境配置 (第三方平台编排模板、docker-compose)


@dataclass
class GoalEvaluationVerdict:
    target_goal: str
    pure_problem_goal: str
    archetype: ArchetypeEnum
    recommended_prefix: str
    suggested_name: str
    confidence: float
    minimal_viable_rationale: str
    deduction_chain: List[str]
    has_solution_bias: bool = False
    injected_tech_stack: List[str] = field(default_factory=list)
    injected_architecture_claims: List[str] = field(default_factory=list)
    anti_pattern_warning: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_goal": self.target_goal,
            "pure_problem_goal": self.pure_problem_goal,
            "archetype": self.archetype.value,
            "recommended_prefix": self.recommended_prefix,
            "suggested_name": self.suggested_name,
            "confidence": round(self.confidence, 4),
            "minimal_viable_rationale": self.minimal_viable_rationale,
            "deduction_chain": self.deduction_chain,
            "has_solution_bias": self.has_solution_bias,
            "injected_tech_stack": self.injected_tech_stack,
            "injected_architecture_claims": self.injected_architecture_claims,
            "anti_pattern_warning": self.anti_pattern_warning
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class GoalDrivenArbiter:
    """
    First-Principles Goal-to-Archetype Deduction Engine.
    Deduces the ONLY rational architectural archetype strictly from:
    1. Problem Domain: What problem does this solve in the outside world?
    2. Execution Actor: Who executes the logic (Human, LLM Host, Local Process, Remote Network Client, Swarm)?
    3. Minimal Viable Footprint: What is the irreducible runtime lifecycle?
    """

    @classmethod
    def deduce_from_goal(cls, goal_description: str, entity_name: str = "") -> GoalEvaluationVerdict:
        raw_desc = goal_description.strip()
        chain: List[str] = [f"原始输入陈述: '{raw_desc}'"]

        # Step 0: De-noise implementation bias via IntentCleaner
        denoise_report = IntentCleaner.clean(raw_desc)
        pure_goal = denoise_report.pure_problem_goal
        pure_lower = pure_goal.lower()

        if denoise_report.has_solution_bias:
            chain.append(f"解域私货剥离与意图清洗: 识别出注入技术栈 {denoise_report.injected_tech_stack}，提取纯粹问题域目标: '{pure_goal}'")
        else:
            chain.append(f"意图验真: 确认为纯粹问题域陈述: '{pure_goal}'")

        if denoise_report.is_pure_boilerplate:
            chain.append("🚨 发现100%模板废话: 输入未包含任何真实业务目标，属于分类目录的循环自证套话！")

        # Step 1: Does achieving this goal inherently require writing and compiling new machine execution code?

        # A: Negative prohibition / guardrail (Rule)
        is_negative_constraint = any(w in pure_lower for w in ["禁止", "红线", "越界", "防线", "拦截", "安全边界", "禁止提交", "违规过滤", "guard", "security rule"])
        if is_negative_constraint and not any(w in pure_lower for w in ["服务器", "端口", "app", "apk"]):
            chain.append("第一性原理推演 [分流点 1: 负向防御红线]: 该目标的本质是设立绝对边界禁止违规行为，而非独立业务运算")
            chain.append("-> 最小必要形态: rule-* (负向守卫/Linter规则)")
            return cls._make_verdict(ArchetypeEnum.RULE, raw_desc, pure_goal, entity_name, 0.98,
                                     "负向安全防线与行为拦截规则，无需独立工程或常驻服务，应以规则约束形式生效。", chain, denoise_report)

        # B: Rigid specification, contract, acceptance oracle (Spec)
        is_formal_spec = any(w in pure_lower for w in ["标准规范", "rfc", "神谕", "契约", "格式定义", "协议标准", "统一规范", "spec", "acceptance", "命名规范"])
        if is_formal_spec and not any(w in pure_lower for w in ["常驻", "服务器", "客户端", "apk", "sop"]):
            chain.append("第一性原理推演 [分流点 1: 刚性规范标准]: 该目标的本质是确立跨系统的数据契约与验收神谕，零独立机器执行代码")
            chain.append("-> 最小必要形态: spec-* (刚性规范标准)")
            return cls._make_verdict(ArchetypeEnum.SPEC, raw_desc, pure_goal, entity_name, 0.98,
                                     "正向数据契约、通信规范或验收神谕，应以纯文本/RFC Schema 存在，严禁过度设计为可执行程序。", chain, denoise_report)

        # C: Agent Cognitive Workflow / SOP (Skill)
        is_agent_guidance = (
            any(w in pure_lower for w in ["sop", "提示词", "指导ai", "教agent", "操作指南", "智能体工作流", "口语搜索", "会话引导", "操作步骤"]) or
            ("调用" in pure_lower and "工具" in pure_lower and any(w in pure_lower for w in ["ai", "大模型", "智能体", "流程"]))
        )
        if is_agent_guidance and not any(w in pure_lower for w in ["常驻后台", "监听端口", "桌面端", "apk"]):
            chain.append("第一性原理推演 [分流点 1: 智能体认知 SOP]: 该目标的核心缺口是'大模型不知道该按什么步骤思考与编排工具'，底层执行力已由既有工具/API具备")
            chain.append("-> 最小必要形态: skill-* (Agent 认知特种技能)")
            warning = "【警惕过度设计】切忌为此编写庞大项目！它只需一份严密的 Markdown SOP 与轻量辅助脚本即可在 AI 宿主中无缝运行。"
            return cls._make_verdict(ArchetypeEnum.SKILL, raw_desc, pure_goal, entity_name, 0.96,
                                     "智能体多轮会话认知指导与工具装配流程，属于纯智力策略层。", chain, denoise_report, warning)

        # D: Documentation & Knowledge base (Doc)
        is_doc = any(w in pure_lower for w in [
            "白皮书", "知识库", "战术手册", "排障实战", "经验总结", "研习笔记", "学习手册",
            "guide", "notes", "playbook", "feasibility study", "可行性研究", "调研报告", "安装指南"
        ])
        if is_doc and not any(w in pure_lower for w in ["自动编译", "算法实现", "自动运行", "自动化执行", "网关服务"]):
            chain.append("第一性原理推演 [分流点 1: 知识沉淀与文献]: 该目标是为了人类心智的认知同步、调研论证与经验传承，无机器运行实体")
            chain.append("-> 最小必要形态: doc-* (战术白皮书与知识库)")
            return cls._make_verdict(ArchetypeEnum.DOC, raw_desc, pure_goal, entity_name, 0.98,
                                     "人类开发者阅读的经验沉淀、技术调研或排障笔记，严禁包装成代码工程。", chain, denoise_report)

        # E: Third-party Workspace Config (Cfg)
        is_config = any(w in pure_lower for w in ["配置", "工作区环境", "docker-compose", "编排模板", "n8n", "dify", "fastgpt", "ragflow"])
        if is_config and not any(w in pure_lower for w in ["开发代码", "独立算法", "网关服务"]):
            chain.append("第一性原理推演 [分流点 1: 第三方环境配置]: 该目标是为了编排开源框架的运行期 YAML 与配置文件模版")
            chain.append("-> 最小必要形态: cfg-* (工作区环境配置)")
            return cls._make_verdict(ArchetypeEnum.CFG, raw_desc, pure_goal, entity_name, 0.95,
                                     "第三方框架声明式配置模版，无需自定义业务机器代码。", chain, denoise_report)

        # Step 2: Now the goal INHERENTLY REQUIRES executable machine logic/code.

        # F: Network Tunnel / VPS Relay (Infrastructure)
        is_infra = any(w in pure_lower for w in ["网络穿透", "derp", "tailscale", "边缘节点", "内网穿透", "vps中继", "服务器基建", "代理分流"])
        if is_infra and not is_doc:
            chain.append("第一性原理推演 [分流点 2: 基础设施中继]: 该目标是解决物理网络拓扑互联、中继转发与边缘宿主环境")
            chain.append("-> 最小必要形态: infra-* (基础设施与中继网络)")
            return cls._make_verdict(ArchetypeEnum.INFRA, raw_desc, pure_goal, entity_name, 0.95,
                                     "物理网络中继与基础设施配置，支撑跨网络通信底座。", chain, denoise_report)

        # G: Model Context Protocol (MCP) Server
        is_mcp_bridge = any(w in pure_lower for w in ["mcp", "model context protocol", "为大模型提供专有工具接头", "供ai宿主调用的标准接头"])
        if is_mcp_bridge:
            chain.append("第一性原理推演 [分流点 2: AI 上下文协议接头]: 该目标是为大模型宿主（Cursor/Claude/Antigravity）提供标准化的外部数据与动作总线")
            chain.append("-> 最小必要形态: mcp-* (Model Context Protocol 服务)")
            return cls._make_verdict(ArchetypeEnum.MCP, raw_desc, pure_goal, entity_name, 0.99,
                                     "标准化 MCP JSON-RPC 协议接头，专为 LLM 暴露受控能力与动态上下文。", chain, denoise_report)

        # H: Multi-Agent Swarm / Cluster Orchestrator
        is_swarm_cluster = any(w in pure_lower for w in ["集群", "多智能体协同", "多模型共生", "跨智能体调度", "网格中枢", "分布式共识", "agent mesh", "dual-engine"])
        if is_swarm_cluster:
            chain.append("第一性原理推演 [分流点 2: 集群自治中枢]: 单个程序或单智能体无法承载，该目标必须依赖多个模型或智能体分布式协同治理")
            chain.append("-> 最小必要形态: cluster-* (智能体集群中枢)")
            return cls._make_verdict(ArchetypeEnum.CLUSTER, raw_desc, pure_goal, entity_name, 0.95,
                                     "多模型、多智能体协同调度与自治演化架构。", chain, denoise_report)

        # I: Network Service / Daemon / Gateway (SVC)
        # Rigid First-Principles Invariant: A service MUST have an inherent problem-domain need to bind ports
        # and serve asynchronous, unpredictable remote concurrent clients (e.g. API Gateway, Web Bridge, Chat Server).
        # Local calculation, hashing, cost matrix, git operations DO NOT qualify for SVC, even if written in FastAPI!
        is_inherent_remote_service = (
            any(w in pure_lower for w in [
                "网关", "反向代理", "web bridge", "即时通信服务端", "万人长连接", "外部系统调用中继",
                "跨网络转发代理", "消息推送服务", "实时转录服务"
            ])
        )
        if is_inherent_remote_service:
            chain.append("第一性原理推演 [分流点 2: 长驻网络守护服务]: 该目标的业务本质必须持续在线、绑定网络端口等待不可预测的远程异步请求，无法算完即走")
            chain.append("-> 最小必要形态: svc-* (后台服务 / API网关)")
            return cls._make_verdict(ArchetypeEnum.SVC, raw_desc, pure_goal, entity_name, 0.96,
                                     "长驻后台网络进程与请求中继微网关，承载并发吞吐。", chain, denoise_report)

        # J: End-User Application (App / GUI / Mobile APK / Specialized Business Robot)
        is_end_user_app = any(w in pure_lower for w in [
            "apk", "安卓", "桌面端", "桌面应用", "gui", "界面", "客户端", "网页端",
            "知乎自动化", "邮件监控", "移动压测", "爬虫机器人", "app"
        ])
        if is_end_user_app:
            chain.append("第一性原理推演 [分流点 2: 终端交互应用]: 该目标直接面对最终人类用户（需交互式界面、移动设备安装）或特定闭环业务机器人")
            chain.append("-> 最小必要形态: app-* (终端业务应用 / 客户端)")
            return cls._make_verdict(ArchetypeEnum.APP, raw_desc, pure_goal, entity_name, 0.95,
                                     "终端人机交互界面、移动应用或端到端特定业务产出机器人。", chain, denoise_report)

        # K: Default Invariant: Deterministic Atomic Tool (Tool)
        # Any offline transformation, file I/O, hash calculation, token cost calculation, matrix generation,
        # linter, patcher, syntax checker is fundamentally an ATOMIC TOOL!
        chain.append("第一性原理推演 [分流点 2: 原子微装具判定]: 该目标需要确定的机器计算/本地IO/算法转换，但无常驻监听端口必要，执行完毕即可极速退出")
        chain.append("-> 最小必要形态: tool-* (原子微装具 / 确定性 CLI)")

        # Over-engineering check: Did the author declare svc/daemon/microservice for an atomic problem?
        warning = None
        has_claimed_svc = any(w in raw_desc.lower() for w in ["微服务", "fastapi", "flask", "常驻后台", "监听端口", "8080", "守护进程", "daemon"])
        if has_claimed_svc:
            warning = (
                "⚠️ 【过度设计警报 (Over-engineering Anti-Pattern)】本目标在物理本质上仅需 'tool-*'（秒级退出的确定性原子装具/CLI）即可完美闭环！"
                "原输入中掺杂了微服务/常驻后台/端口监听等解域私货，属于典型的高射炮打蚊子、引入非必要常驻内存开销与安全暴露面。"
            )
        else:
            warning = "【极简不变量】坚决不要做成长驻常开的后台 Daemon！严格以无状态命令行（UCFS 五动词）交付，达到最高性能与零维护成本。"

        return cls._make_verdict(ArchetypeEnum.TOOL, raw_desc, pure_goal, entity_name, 0.95,
                                 "原子微装具：本地确定性执行、输入变输出、秒级退出、符合 UCFS 五动词契约。", chain, denoise_report, warning)

    @classmethod
    def _make_verdict(
        cls,
        arch: ArchetypeEnum,
        raw_desc: str,
        pure_goal: str,
        entity_name: str,
        confidence: float,
        rationale: str,
        chain: List[str],
        denoise_report: IntentDenoiseReport,
        warning: Optional[str] = None
    ) -> GoalEvaluationVerdict:
        prefix = f"{arch.value}-"
        clean = re.sub(r"[^a-zA-Z0-9_\-]+", "-", entity_name).strip("-").lower() if entity_name else ""
        for p in ["tool-", "skill-", "spec-", "rule-", "svc-", "mcp-", "cluster-", "app-", "infra-", "cfg-", "doc-", "archive-"]:
            if clean.startswith(p):
                clean = clean[len(p):]

        suggested = f"{prefix}{clean}" if clean else f"{prefix}module"

        # Additional anti-pattern warning if author claimed something vastly different from MVA
        final_warning = warning
        if denoise_report.is_pure_boilerplate:
            final_warning = "🚨 【纯模板套话警报】输入内容为通用模板填充，缺乏真实问题域定义，判定置信度受限！"

        return GoalEvaluationVerdict(
            target_goal=raw_desc,
            pure_problem_goal=pure_goal,
            archetype=arch,
            recommended_prefix=prefix,
            suggested_name=suggested,
            confidence=confidence,
            minimal_viable_rationale=rationale,
            deduction_chain=chain,
            has_solution_bias=denoise_report.has_solution_bias,
            injected_tech_stack=denoise_report.injected_tech_stack,
            injected_architecture_claims=denoise_report.injected_architecture_claims,
            anti_pattern_warning=final_warning
        )
