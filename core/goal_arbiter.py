#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/goal_arbiter.py: First-Principles Goal-Driven Taxonomy Arbiter.
Strict forward deduction from Core Purpose & Intent -> Minimal Viable Archetype.
Does NOT reverse-engineer or "sketch after tracing" from existing code bloat.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Any, Optional
import json
import re


class ArchetypeEnum(str, Enum):
    SPEC = "spec"         # 刚性规范标准 (RFC契约 / 模式定义 / 验收神谕)
    RULE = "rule"         # 负向行为红线 (安全防线 / 拦截守卫 / 边界禁令)
    SKILL = "skill"       # 智能体认知 SOP (指导 AI 如何思考、拆解并调用现有工具)
    DOC = "doc"           # 战术手册与知识库 (人脑学习文献 / 排障手册 / 白皮书)
    TOOL = "tool"         # 原子微装具 (秒级退出、无状态/单文件状态、机器算力与算法)
    MCP = "mcp"           # MCP 协议服务 (专为大模型暴露专有工具与实时上下文的接头)
    SVC = "svc"           # 网络长驻服务 (监听网络端口、高并发处理请求的微服务/网关)
    CLUSTER = "cluster"   # 集群自治中枢 (单个程序搞不定，需多模型/多Agent分布式协同网格)
    APP = "app"           # 终端交互应用 (面向终端用户的 GUI/移动APK/或特定垂直业务闭环)
    INFRA = "infra"       # 基础设施中继 (网络穿透、VPS 中继节点、底层物理资源)
    CFG = "cfg"           # 工作区环境配置 (第三方平台编排模板、docker-compose)


@dataclass
class GoalEvaluationVerdict:
    target_goal: str
    archetype: ArchetypeEnum
    recommended_prefix: str
    suggested_name: str
    confidence: float
    minimal_viable_rationale: str
    deduction_chain: List[str]
    anti_pattern_warning: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_goal": self.target_goal,
            "archetype": self.archetype.value,
            "recommended_prefix": self.recommended_prefix,
            "suggested_name": self.suggested_name,
            "confidence": round(self.confidence, 4),
            "minimal_viable_rationale": self.minimal_viable_rationale,
            "deduction_chain": self.deduction_chain,
            "anti_pattern_warning": self.anti_pattern_warning
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class GoalDrivenArbiter:
    """
    First-Principles Goal-to-Archetype Deduction Engine.
    Deduces the ONLY rational architectural archetype strictly from:
    1. What problem does this solve?
    2. Who/What executes the core logic?
    3. What is the minimal viable physical footprint?
    """

    @classmethod
    def deduce_from_goal(cls, goal_description: str, entity_name: str = "") -> GoalEvaluationVerdict:
        desc = goal_description.strip()
        desc_lower = desc.lower()
        chain: List[str] = [f"原始核心目标陈述: '{desc}'"]

        # Step 1: Does achieving this goal inherently require writing and compiling new machine execution code?

        # A: Negative prohibition / guardrail (Rule)
        is_negative_constraint = any(w in desc_lower for w in ["禁止", "红线", "越界", "防线", "拦截", "安全边界", "禁止提交", "违规过滤", "guard", "security rule"])
        if is_negative_constraint and not any(w in desc_lower for w in ["服务器", "端口", "app", "apk"]):
            chain.append("第一性原理推演 [分流点 1: 负向防御红线]: 该目标的本质是设立绝对边界禁止行为，而非业务运算逻辑")
            chain.append("-> 最小必要形态: rule-* (负向守卫/Linter规则)")
            return cls._make_verdict(ArchetypeEnum.RULE, desc, entity_name, 0.98,
                                     "负向安全防线与行为拦截规则，无需独立工程或常驻服务，应以规则约束形式生效。", chain)

        # B: Rigid specification, contract, acceptance oracle (Spec)
        is_formal_spec = any(w in desc_lower for w in ["标准规范", "rfc", "神谕", "契约", "格式定义", "协议标准", "统一规范", "spec", "acceptance"])
        if is_formal_spec and not any(w in desc_lower for w in ["常驻", "服务器", "客户端", "apk", "sop"]):
            chain.append("第一性原理推演 [分流点 1: 刚性规范标准]: 该目标的本质是确立跨系统的数据契约与验收神谕，无独立机器执行生命周期")
            chain.append("-> 最小必要形态: spec-* (刚性规范标准)")
            return cls._make_verdict(ArchetypeEnum.SPEC, desc, entity_name, 0.98,
                                     "正向数据契约、通信规范或验收神谕，应以纯文本/RFC Schema 存在，避免过度设计为可执行程序。", chain)

        # C: Agent Cognitive Workflow / SOP (Skill)
        is_agent_guidance = (
            any(w in desc_lower for w in ["sop", "提示词", "指导ai", "教agent", "操作指南", "智能体工作流", "口语搜索", "会话引导", "操作步骤"]) or
            ("调用" in desc_lower and "工具" in desc_lower and any(w in desc_lower for w in ["ai", "大模型", "智能体", "流程"]))
        )
        if is_agent_guidance and not any(w in desc_lower for w in ["常驻后台", "监听端口", "桌面端", "apk"]):
            chain.append("第一性原理推演 [分流点 1: 智能体认知 SOP]: 该目标的核心缺口是'大模型不知道该按什么步骤思考与组合工具'，底层执行力已由既有工具/API具备")
            chain.append("-> 最小必要形态: skill-* (Agent 认知特种技能)")
            warning = "【警惕过度设计】切忌为此编写庞大项目！它只需一份严密的 Markdown SOP 与轻量辅助脚本即可在 AI 宿主中无缝运行。"
            return cls._make_verdict(ArchetypeEnum.SKILL, desc, entity_name, 0.96,
                                     "智能体多轮会话认知指导与工具装配流程，属于纯智力策略层。", chain, warning)

        # D: Documentation & Knowledge base (Doc)
        is_doc = any(w in desc_lower for w in ["白皮书", "知识库", "战术手册", "排障实战", "经验总结", "研习笔记", "学习手册", "guide", "notes", "playbook"])
        if is_doc and not any(w in desc_lower for w in ["代码", "编译", "算法实现", "自动运行", "自动化", "微服务"]):
            chain.append("第一性原理推演 [分流点 1: 知识沉淀与文献]: 该目标是为了人类心智的认知同步与经验传承，无机器运行实体")
            chain.append("-> 最小必要形态: doc-* (战术白皮书与知识库)")
            return cls._make_verdict(ArchetypeEnum.DOC, desc, entity_name, 0.98,
                                     "人类开发者阅读的经验沉淀与战术参考，严禁包装成代码工程。", chain)

        # E: Third-party Workspace Config (Cfg)
        is_config = any(w in desc_lower for w in ["配置", "工作区环境", "docker-compose", "编排模板", "n8n", "dify", "fastgpt", "ragflow"])
        if is_config and not any(w in desc_lower for w in ["开发代码", "编译", "独立算法", "网关服务"]):
            chain.append("第一性原理推演 [分流点 1: 第三方环境配置]: 该目标是为了编排开源框架的运行期 YAML 与配置文件模版")
            chain.append("-> 最小必要形态: cfg-* (工作区环境配置)")
            return cls._make_verdict(ArchetypeEnum.CFG, desc, entity_name, 0.95,
                                     "第三方框架声明式配置模版，无需自定义机器代码。", chain)

        # Step 2: Now the goal INHERENTLY REQUIRES executable machine logic/code.

        # F: Network Tunnel / VPS Relay (Infrastructure)
        is_infra = any(w in desc_lower for w in ["网络穿透", "derp", "tailscale", "边缘节点", "内网穿透", "vps中继", "服务器基建", "代理分流"])
        if is_infra:
            chain.append("第一性原理推演 [分流点 2: 基础设施中继]: 该目标是解决物理网络拓扑互联、中继转发与边缘宿主环境")
            chain.append("-> 最小必要形态: infra-* (基础设施与中继网络)")
            return cls._make_verdict(ArchetypeEnum.INFRA, desc, entity_name, 0.95,
                                     "物理网络中继与基础设施配置，支撑跨网络通信底座。", chain)

        # G: Model Context Protocol (MCP) Server
        is_mcp_bridge = any(w in desc_lower for w in ["mcp", "model context protocol", "为大模型提供专有工具接头", "供ai宿主调用的标准接头"])
        if is_mcp_bridge:
            chain.append("第一性原理推演 [分流点 2: AI 上下文协议接头]: 该目标是为大模型宿主（Cursor/Claude/Antigravity）提供标准化的外部数据与动作总线")
            chain.append("-> 最小必要形态: mcp-* (Model Context Protocol 服务)")
            return cls._make_verdict(ArchetypeEnum.MCP, desc, entity_name, 0.99,
                                     "标准化 MCP JSON-RPC 协议接头，专为 LLM 暴露受控能力与动态上下文。", chain)

        # H: Multi-Agent Swarm / Cluster Orchestrator
        is_swarm_cluster = any(w in desc_lower for w in ["集群", "多智能体协同", "多模型共生", "跨智能体调度", "网格中枢", "分布式共识", "agent mesh", "dual-engine"])
        if is_swarm_cluster:
            chain.append("第一性原理推演 [分流点 2: 集群自治中枢]: 单个程序或单智能体无法承载，该目标必须依赖多个模型或智能体分布式协同治理")
            chain.append("-> 最小必要形态: cluster-* (智能体集群中枢)")
            return cls._make_verdict(ArchetypeEnum.CLUSTER, desc, entity_name, 0.95,
                                     "多模型、多智能体协同调度与自治演化架构。", chain)

        # Check explicit one-shot / CLI negative modifier
        # e.g., "不留后台", "无需后台", "非后台", "极速命令行装具", "退出后不留"
        is_explicit_oneshot = any(w in desc_lower for w in [
            "不留后台", "无需后台", "非后台", "不常驻", "无需常驻", "非常驻",
            "一次性", "单次退出", "执行后退出", "算完就走", "秒级退出", "极速命令行", "退出后不留"
        ])

        # I: Network Service / Daemon / Gateway
        # Clean text by removing negated daemon phrases before checking
        cleaned_for_daemon = re.sub(r"(不留后台|无需后台|非后台|不常驻|无需常驻|非常驻|退出后不留)", "", desc_lower)
        is_network_daemon = (
            not is_explicit_oneshot and
            any(w in cleaned_for_daemon for w in ["常驻", "后台", "监听", "端口", "网关", "反向代理", "微服务", "http服务", "websocket服务", "持续监听", "守护进程", "daemon", "server"])
        )
        is_pure_client_ui = any(w in desc_lower for w in ["apk", "安卓应用", "桌面应用", "gui界面", "移动端app"])
        if is_network_daemon and not is_pure_client_ui:
            chain.append("第一性原理推演 [分流点 2: 长驻网络守护服务]: 该目标必须持续在线、绑定 TCP/HTTP/WS 端口等待外部并发请求，无法在算完后退出")
            chain.append("-> 最小必要形态: svc-* (后台服务 / API网关)")
            return cls._make_verdict(ArchetypeEnum.SVC, desc, entity_name, 0.96,
                                     "长驻后台网络进程与请求中继微网关，承载并发吞吐。", chain)

        # J: End-User Application (App / GUI / Mobile APK / Specialized Business Robot)
        is_end_user_app = any(w in desc_lower for w in [
            "apk", "安卓", "桌面端", "桌面应用", "gui", "界面", "客户端", "网页端",
            "知乎自动化", "邮件监控", "移动压测", "端到端业务", "爬虫机器人", "业务应用", "app"
        ])
        if is_end_user_app and not is_explicit_oneshot:
            chain.append("第一性原理推演 [分流点 2: 终端交互应用]: 该目标直接面对最终人类用户（需交互式界面、移动设备安装）或特定闭环业务机器人")
            chain.append("-> 最小必要形态: app-* (终端业务应用 / 客户端)")
            return cls._make_verdict(ArchetypeEnum.APP, desc, entity_name, 0.95,
                                     "终端人机交互界面、移动应用或端到端特定业务产出机器人。", chain)

        # K: Default Invariant: Deterministic Atomic Tool (Tool)
        chain.append("第一性原理推演 [分流点 2: 原子微装具判定]: 该目标需要确定的机器计算/本地IO操作，但无常驻监听端口必要，执行完毕即可极速退出")
        chain.append("-> 最小必要形态: tool-* (原子微装具 / 确定性 CLI)")
        warning = "【极简不变量】坚决不要做成长驻常开的后台 Daemon！严格以无状态命令行（UCFS 五动词）交付，达到最高性能与零维护成本。"
        return cls._make_verdict(ArchetypeEnum.TOOL, desc, entity_name, 0.95,
                                 "原子微装具：本地确定性执行、输入变输出、秒级退出、符合 UCFS 五动词契约。", chain, warning)

    @classmethod
    def _make_verdict(
        cls,
        arch: ArchetypeEnum,
        desc: str,
        entity_name: str,
        confidence: float,
        rationale: str,
        chain: List[str],
        warning: Optional[str] = None
    ) -> GoalEvaluationVerdict:
        prefix = f"{arch.value}-"
        clean = re.sub(r"[^a-zA-Z0-9_\-]+", "-", entity_name).strip("-").lower() if entity_name else ""
        for p in ["tool-", "skill-", "spec-", "rule-", "svc-", "mcp-", "cluster-", "app-", "infra-", "cfg-", "doc-", "archive-"]:
            if clean.startswith(p):
                clean = clean[len(p):]

        suggested = f"{prefix}{clean}" if clean else f"{prefix}module"

        return GoalEvaluationVerdict(
            target_goal=desc,
            archetype=arch,
            recommended_prefix=prefix,
            suggested_name=suggested,
            confidence=confidence,
            minimal_viable_rationale=rationale,
            deduction_chain=chain,
            anti_pattern_warning=warning
        )
