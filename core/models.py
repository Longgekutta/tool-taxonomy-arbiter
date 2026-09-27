#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/models.py: Data models and archetypes for tool-taxonomy-arbiter.
"""
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Any, Optional
import json


class ArchetypeEnum(str, Enum):
    SPEC = "spec"         # 规范标准与刚性神谕
    TOOL = "tool"         # 原子微装具 / 确定性 CLI
    SKILL = "skill"       # 智能体 SOP / 认知操作流
    RULE = "rule"         # 负向行为红线与约束守卫
    SVC = "svc"           # 网络长驻服务与微网关
    MCP = "mcp"           # Model Context Protocol 标准协议服务器
    CLUSTER = "cluster"   # 多智能体协同网格与自治集群
    APP = "app"           # 终端交互应用、GUI、移动端或端到端机器人
    INFRA = "infra"       # 边缘节点、网络穿透与服务器基建
    CFG = "cfg"           # 工作区、第三方平台配置与编排模板
    DOC = "doc"           # 知识库白皮书、战术手册与排障笔记


ARCHETYPE_METADATA = {
    ArchetypeEnum.SPEC: {
        "prefix": "spec-",
        "description": "刚性规范标准：定义全域第一性原理、代码动词、通信契约与验收神谕（纯文本/模式定义，无业务实现）。",
        "primary_slot": "Specification & Compliance Oracle",
        "invariants": ["Zero executable daemon", "Normative definitions only", "Semantic RFC versioning"]
    },
    ArchetypeEnum.TOOL: {
        "prefix": "tool-",
        "description": "原子微装具：无状态或单文件状态的极速命令行工具，输入输出确定，具备 UCFS 5 动词接口。",
        "primary_slot": "Deterministic CLI & Micro-Utility",
        "invariants": ["Stateless or local IO", "UCFS 5-verb compliance", "Zero daemon listening port"]
    },
    ArchetypeEnum.SKILL: {
        "prefix": "skill-",
        "description": "智能体 SOP：指导 AI Agent 在多步骤会话中调用各类工具完成端到端任务的认知操作规范与提示词工作流。",
        "primary_slot": "Agent Cognitive Workflow & SOP",
        "invariants": ["YAML frontmatter + Markdown", "Operated by AI Agent", "Composes atomic tools"]
    },
    ArchetypeEnum.RULE: {
        "prefix": "rule-",
        "description": "负向行为红线：定义绝对禁止行为、边界安全守卫与静态拦截规则（如禁止越权、禁止裸钥）。",
        "primary_slot": "Invariant Guardrail & Boundary Sentinel",
        "invariants": ["Negative constraint enforcement", "Passive / lint-time interception"]
    },
    ArchetypeEnum.SVC: {
        "prefix": "svc-",
        "description": "网络长驻服务：长驻后台守护进程，监听 HTTP/WebSocket/gRPC 端口，提供微网关与数据中继。",
        "primary_slot": "Network Gateway & Daemon Service",
        "invariants": ["Long-running event loop / daemon", "Network port binding", "Concurrent request handling"]
    },
    ArchetypeEnum.MCP: {
        "prefix": "mcp-",
        "description": "MCP 协议服务：标准化实现 Model Context Protocol (stdio/SSE)，专为 AI 宿主暴露工具与上下文资源。",
        "primary_slot": "Model Context Protocol Server",
        "invariants": ["MCP JSON-RPC 2.0 stdio/SSE", "Host-agnostic tool/resource schema"]
    },
    ArchetypeEnum.CLUSTER: {
        "prefix": "cluster-",
        "description": "集群自治中枢：调度多模型、多智能体协同网格、跨智能体级联与分布式任务执行大脑。",
        "primary_slot": "Multi-Agent Mesh & Swarm Orchestrator",
        "invariants": ["Multi-actor consensus/routing", "Swarm coordination topology"]
    },
    ArchetypeEnum.APP: {
        "prefix": "app-",
        "description": "业务应用机器人：端到端终端业务（知乎自动化、安卓 APK、Electron GUI、移动客户端）。",
        "primary_slot": "End-User Client & Interactive App",
        "invariants": ["User-facing interactive surface or specialized business pipeline"]
    },
    ArchetypeEnum.INFRA: {
        "prefix": "infra-",
        "description": "基础设施中继：边缘计算服务器、Tailscale DERP 中继、网络穿透与宿主机脚本。",
        "primary_slot": "Infrastructure Relay & Network Fabric",
        "invariants": ["Host / network virtualization", "Tunneling and proxy transport"]
    },
    ArchetypeEnum.CFG: {
        "prefix": "cfg-",
        "description": "环境配置工作区：第三方开源平台 (Dify, FastGPT, n8n, OpenClaw) 部署配置与模板。",
        "primary_slot": "Workspace Config & Third-Party Environment",
        "invariants": ["Docker-compose, YAML templates, workflow JSONs"]
    },
    ArchetypeEnum.DOC: {
        "prefix": "doc-",
        "description": "战术手册与知识库：技术白皮书、战术手册、排障笔记与研究文献。",
        "primary_slot": "Tactical Playbook & Knowledge Repository",
        "invariants": ["Zero code runtime", "Documentation and pedagogical knowledge"]
    }
}


@dataclass
class DimensionVector:
    """
    7-Dimensional Orthogonal Feature Vector (Normalized 0.0 - 1.0)
    """
    lifecycle: float = 0.0     # 0.0: One-shot CLI / Static  -> 1.0: Permanent Daemon / Port listener
    protocol: float = 0.0      # 0.0: CLI arguments/pipes    -> 0.5: MCP JSON-RPC -> 1.0: HTTP/WS/gRPC
    execution: float = 0.0     # 0.0: Pure text/spec/prompt  -> 1.0: Compilable/Executable machine code
    agenticity: float = 0.0    # 0.0: Strict mechanical code -> 1.0: LLM cognitive prompt / SOP guide
    boundary: float = 0.0      # 0.0: General implementation -> 0.5: Formal RFC spec -> 1.0: Invariant Guardrail
    swarm: float = 0.0         # 0.0: Single node/utility    -> 1.0: Multi-agent mesh / Cluster swarm
    interface: float = 0.0     # 0.0: Headless / Script CLI  -> 1.0: GUI / Mobile APK / Web Application

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class ArbiterVerdict:
    """
    Output decision verdict with complete mathematical derivation and traceability.
    """
    archetype: ArchetypeEnum
    recommended_prefix: str
    suggested_name: str
    confidence: float
    dimension_scores: Dict[str, float]
    candidate_ranking: List[Dict[str, Any]]
    derivation_path: List[str]
    slot_description: str
    invariants_required: List[str]
    input_summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "archetype": self.archetype.value,
            "recommended_prefix": self.recommended_prefix,
            "suggested_name": self.suggested_name,
            "confidence": round(self.confidence, 4),
            "dimension_scores": {k: round(v, 4) for k, v in self.dimension_scores.items()},
            "candidate_ranking": self.candidate_ranking,
            "derivation_path": self.derivation_path,
            "slot_description": self.slot_description,
            "invariants_required": self.invariants_required,
            "input_summary": self.input_summary
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
