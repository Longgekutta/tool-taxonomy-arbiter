#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/decision_engine.py: 100% Deterministic Orthogonal Decision Engine.
Guarantees f(x) == f(x) mathematical invariance without stochastic drift.
"""
import math
import re
from typing import Dict, List, Tuple, Any, Optional
from core.models import ArchetypeEnum, ARCHETYPE_METADATA, DimensionVector, ArbiterVerdict


# Centroids and dimensional importance weights for each archetype
ARCHETYPE_CENTROIDS: Dict[ArchetypeEnum, Dict[str, float]] = {
    ArchetypeEnum.SPEC: {
        "lifecycle": 0.0, "protocol": 0.0, "execution": 0.0,
        "agenticity": 0.1, "boundary": 0.95, "swarm": 0.0, "interface": 0.0
    },
    ArchetypeEnum.RULE: {
        "lifecycle": 0.0, "protocol": 0.0, "execution": 0.0,
        "agenticity": 0.2, "boundary": 1.0, "swarm": 0.0, "interface": 0.0
    },
    ArchetypeEnum.TOOL: {
        "lifecycle": 0.0, "protocol": 0.0, "execution": 1.0,
        "agenticity": 0.0, "boundary": 0.0, "swarm": 0.0, "interface": 0.0
    },
    ArchetypeEnum.SKILL: {
        "lifecycle": 0.0, "protocol": 0.0, "execution": 0.2,
        "agenticity": 1.0, "boundary": 0.1, "swarm": 0.1, "interface": 0.0
    },
    ArchetypeEnum.MCP: {
        "lifecycle": 0.6, "protocol": 0.95, "execution": 1.0,
        "agenticity": 0.5, "boundary": 0.0, "swarm": 0.0, "interface": 0.0
    },
    ArchetypeEnum.SVC: {
        "lifecycle": 1.0, "protocol": 0.9, "execution": 1.0,
        "agenticity": 0.2, "boundary": 0.0, "swarm": 0.2, "interface": 0.0
    },
    ArchetypeEnum.CLUSTER: {
        "lifecycle": 0.8, "protocol": 0.7, "execution": 1.0,
        "agenticity": 0.9, "boundary": 0.0, "swarm": 1.0, "interface": 0.2
    },
    ArchetypeEnum.APP: {
        "lifecycle": 0.5, "protocol": 0.3, "execution": 1.0,
        "agenticity": 0.2, "boundary": 0.0, "swarm": 0.0, "interface": 1.0
    },
    ArchetypeEnum.INFRA: {
        "lifecycle": 0.9, "protocol": 0.8, "execution": 0.4,
        "agenticity": 0.0, "boundary": 0.0, "swarm": 0.1, "interface": 0.0
    },
    ArchetypeEnum.CFG: {
        "lifecycle": 0.1, "protocol": 0.0, "execution": 0.0,
        "agenticity": 0.1, "boundary": 0.0, "swarm": 0.0, "interface": 0.0
    },
    ArchetypeEnum.DOC: {
        "lifecycle": 0.0, "protocol": 0.0, "execution": 0.0,
        "agenticity": 0.0, "boundary": 0.0, "swarm": 0.0, "interface": 0.0
    }
}

DIMENSION_WEIGHTS: Dict[str, float] = {
    "lifecycle": 1.3,
    "protocol": 1.2,
    "execution": 1.5,
    "agenticity": 1.4,
    "boundary": 1.6,
    "swarm": 1.4,
    "interface": 1.3
}


class DecisionEngine:
    """
    Deterministic Arbiter that maps a 7-dimensional technical vector or concept
    to its unique software archetype.
    """

    @classmethod
    def evaluate_vector(
        cls,
        vector: DimensionVector,
        concept_title: str = "custom-entity",
        derivation_notes: Optional[List[str]] = None,
        explicit_target: Optional[ArchetypeEnum] = None
    ) -> ArbiterVerdict:
        v_dict = vector.to_dict()
        derivation = list(derivation_notes or [])

        if explicit_target:
            derivation.append(f"触发物理实体显式命名契约 -> 直接锁定目标形态: {explicit_target.value}")
            return cls._create_verdict(explicit_target, vector, 0.99, concept_title, derivation)

        title_lower = concept_title.lower()

        # Step 1: Strict Cut-off Invariants
        # Invariant A: Rule vs Spec
        if v_dict["boundary"] >= 0.75 and v_dict["agenticity"] <= 0.5:
            if any(w in title_lower for w in ["禁止", "红线", "防线", "guard", "sentinel", "rule", "安全拦截"]):
                derivation.append("触发刚性不变量: 高边界性(>=0.75) + 负向约束/拦截定义 -> 锁定 ArchetypeEnum.RULE")
                return cls._create_verdict(ArchetypeEnum.RULE, vector, 0.98, concept_title, derivation)
            elif any(w in title_lower for w in ["规范", "spec", "契约", "protocol", "oracle", "标准"]):
                derivation.append("触发刚性不变量: 高边界性(>=0.75) + 正向规范/契约定义 -> 锁定 ArchetypeEnum.SPEC")
                return cls._create_verdict(ArchetypeEnum.SPEC, vector, 0.98, concept_title, derivation)

        # Invariant B: MCP Protocol Lock
        if v_dict["protocol"] >= 0.85 and ("mcp" in title_lower or "model context protocol" in title_lower):
            derivation.append("触发刚性不变量: 协议特征>=0.85 且显式声明 MCP 规范 -> 锁定 ArchetypeEnum.MCP")
            return cls._create_verdict(ArchetypeEnum.MCP, vector, 0.99, concept_title, derivation)

        # Invariant C: Swarm Multi-Agent Mesh Lock
        if v_dict["swarm"] >= 0.75:
            derivation.append("触发刚性不变量: 多智能体集群拓扑>=0.75 -> 锁定 ArchetypeEnum.CLUSTER")
            return cls._create_verdict(ArchetypeEnum.CLUSTER, vector, 0.96, concept_title, derivation)

        # Invariant D: Skill SOP Lock
        if v_dict["agenticity"] >= 0.75 and v_dict["execution"] <= 0.4 and v_dict["lifecycle"] <= 0.2:
            derivation.append("触发刚性不变量: 智能体SOP工作流>=0.75 + 低机器代码 + 瞬时加载 -> 锁定 ArchetypeEnum.SKILL")
            return cls._create_verdict(ArchetypeEnum.SKILL, vector, 0.95, concept_title, derivation)

        # Invariant E: Service Daemon Lock
        if v_dict["lifecycle"] >= 0.75 and v_dict["protocol"] >= 0.6 and v_dict["interface"] <= 0.6:
            derivation.append("触发刚性不变量: 常驻守护进程(>=0.75) + 网络协议(>=0.6) + 无独占GUI界面 -> 锁定 ArchetypeEnum.SVC")
            return cls._create_verdict(ArchetypeEnum.SVC, vector, 0.95, concept_title, derivation)

        # Invariant F: App GUI / End-User Bot Lock
        if v_dict["interface"] >= 0.75:
            derivation.append("触发刚性不变量: 终端用户UI/移动客户端/端到端机器人>=0.75 -> 锁定 ArchetypeEnum.APP")
            return cls._create_verdict(ArchetypeEnum.APP, vector, 0.95, concept_title, derivation)

        # Invariant G: Tool Atomic Utility Lock
        if v_dict["execution"] >= 0.7 and v_dict["lifecycle"] <= 0.2 and v_dict["interface"] <= 0.2 and v_dict["protocol"] <= 0.3:
            derivation.append("触发刚性不变量: 强机器执行(>=0.7) + 瞬时退出(<=0.2) + 无界面 + 命令行协议 -> 锁定 ArchetypeEnum.TOOL")
            return cls._create_verdict(ArchetypeEnum.TOOL, vector, 0.95, concept_title, derivation)

        # Step 2: Continuous Euclidean Distance & Softmax Weighting
        scores: Dict[ArchetypeEnum, float] = {}
        for archetype, centroid in ARCHETYPE_CENTROIDS.items():
            dist_sq = 0.0
            total_weight = 0.0
            for dim, weight in DIMENSION_WEIGHTS.items():
                diff = v_dict[dim] - centroid[dim]
                dist_sq += weight * (diff ** 2)
                total_weight += weight
            weighted_dist = math.sqrt(dist_sq / total_weight)
            sim = math.exp(-2.0 * weighted_dist)
            scores[archetype] = sim

        sorted_candidates = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        winner_arch, top_score = sorted_candidates[0]

        score_sum = sum(scores.values()) or 1.0
        confidence = top_score / score_sum * len(ARCHETYPE_CENTROIDS) / 2.0
        confidence = min(max(confidence, 0.50), 0.99)

        derivation.append(
            f"高维空间距离计算完成: 最佳投影形态为 {winner_arch.value} (相似度 {top_score:.4f}, 置信度 {confidence:.2%})"
        )

        ranking = [
            {"archetype": a.value, "score": round(s, 4), "prefix": ARCHETYPE_METADATA[a]["prefix"]}
            for a, s in sorted_candidates
        ]

        return cls._create_verdict(
            archetype=winner_arch,
            vector=vector,
            confidence=confidence,
            concept_title=concept_title,
            derivation_path=derivation,
            ranking=ranking
        )

    @classmethod
    def _create_verdict(
        cls,
        archetype: ArchetypeEnum,
        vector: DimensionVector,
        confidence: float,
        concept_title: str,
        derivation_path: List[str],
        ranking: Optional[List[Dict[str, Any]]] = None
    ) -> ArbiterVerdict:
        meta = ARCHETYPE_METADATA[archetype]
        prefix = meta["prefix"]

        clean_title = re.sub(r"[^a-zA-Z0-9_\-]+", "-", concept_title).strip("-").lower()
        for p in ["tool-", "skill-", "spec-", "rule-", "svc-", "mcp-", "cluster-", "app-", "infra-", "cfg-", "doc-", "archive-"]:
            if clean_title.startswith(p):
                clean_title = clean_title[len(p):]

        suggested_name = f"{prefix}{clean_title}" if clean_title else f"{prefix}module"

        if ranking is None:
            ranking = [{"archetype": archetype.value, "score": 1.0, "prefix": prefix}]

        return ArbiterVerdict(
            archetype=archetype,
            recommended_prefix=prefix,
            suggested_name=suggested_name,
            confidence=confidence,
            dimension_scores=vector.to_dict(),
            candidate_ranking=ranking,
            derivation_path=derivation_path,
            slot_description=meta["description"],
            invariants_required=meta["invariants"],
            input_summary=concept_title
        )

    @classmethod
    def extract_vector_from_text(cls, text: str) -> Tuple[DimensionVector, List[str]]:
        derivation = []
        text_lower = text.lower()

        is_agent_workflow = any(w in text_lower for w in ["sop", "提示词", "agent", "智能体", "prompt", "会话引导"])

        # D5: Boundary
        boundary = 0.0
        is_negative_rule = any(w in text_lower for w in ["禁止", "红线", "越界", "防线", "guard", "security rule", "防御", "拦截"])
        is_spec = (any(w in text_lower for w in ["rfc", "神谕", "oracle", "契约", "spec", "acceptance"]) or
                   ("规范" in text_lower and not is_agent_workflow and not any(w in text_lower for w in ["操作规范", "流程规范"])))

        if is_negative_rule:
            boundary = 1.0
            derivation.append("命中负向红线/防御拦截 -> Boundary 设定 1.0 (Rule)")
        elif is_spec:
            boundary = 0.9
            derivation.append("命中契约/RFC规范/验收神谕 -> Boundary 设定 0.90 (Spec)")

        # D1: Lifecycle
        lifecycle = 0.0
        daemon_signals = ["后台", "常驻", "daemon", "service", "长驻", "监听", "listen", "轮询", "cron", "interval", "定时器", "持续运行"]
        oneshot_signals = ["一次性", "脚本", "极速", "cli", "命令行", "单次", "秒级", "退出", "one-shot", "执行后退出"]
        if any(w in text_lower for w in daemon_signals):
            lifecycle += 0.85
            derivation.append("命中后台/常驻/定时信号 -> Lifecycle +0.85")
        if any(w in text_lower for w in oneshot_signals):
            lifecycle = max(0.0, lifecycle - 0.7)
            derivation.append("命中命令行/极速退出信号 -> Lifecycle 压降至 0.1")

        # D2: Protocol
        protocol = 0.0
        if "mcp" in text_lower or "model context protocol" in text_lower:
            protocol = 0.95
            derivation.append("命中 MCP/Model Context Protocol -> Protocol 设定 0.95")
        elif any(w in text_lower for w in ["http", "websocket", "grpc", "rest api", "端口", "网关", "gateway", "reverse proxy", "反向代理"]):
            protocol = 0.9
            derivation.append("命中 HTTP/WebSocket/API网关/反向代理信号 -> Protocol 设定 0.90")
        elif any(w in text_lower for w in ["cli", "stdio", "管道", "参数", "argparse"]):
            protocol = 0.05
            derivation.append("命中标准输入输出/参数解析 -> Protocol 设定 0.05")

        # D3: Execution
        if is_negative_rule or is_spec:
            execution = 0.05
            derivation.append("属于边界规范/规则，主体非运行期机器代码 -> Execution 压降至 0.05")
        else:
            execution = 0.5
            code_signals = ["可执行", "二进制", "算法", "实现", "计算", "装具", "解析器", "python", "rust", "go", "c++", "服务", "网关"]
            text_signals = ["提示词", "sop", "规范", "文档", "知识库", "指南", "手册", "纯文本", "markdown", "frontmatter"]
            if any(w in text_lower for w in code_signals):
                execution += 0.45
                derivation.append("命中算法/服务/可执行代码信号 -> Execution 升至 0.95")
            if any(w in text_lower for w in text_signals):
                execution = max(0.0, execution - 0.5)
                derivation.append("命中提示词/文档/规范信号 -> Execution 降至 0.15")

        # D4: Agenticity
        agenticity = 0.0
        if is_agent_workflow:
            agenticity = 0.95
            derivation.append("命中智能体/SOP/AI会话流程信号 -> Agenticity 设定 0.95")

        # D6: Swarm
        swarm = 0.0
        swarm_signals = ["集群", "多智能体", "swarm", "mesh", "多模型共生", "跨智能体", "自治中枢", "调度网格", "共识"]
        if any(w in text_lower for w in swarm_signals):
            swarm = 0.95
            derivation.append("命中多智能体集群/共生网格 -> Swarm 设定 0.95 (Cluster)")

        # D7: Interface
        interface = 0.0
        is_backend_server = any(w in text_lower for w in ["网关", "反向代理", "微服务", "服务中枢", "server", "常驻后台", "监听"])
        app_signals = ["app", "apk", "安卓应用", "桌面应用", "gui", "移动端", "网页前端", "web ui", "端到端业务", "知乎爬虫", "知乎发布", "爬虫机器人"]
        if any(w in text_lower for w in app_signals) and not is_backend_server:
            interface = 0.9
            derivation.append("命中客户端应用/GUI/移动App/端到端业务机器人 -> Interface 设定 0.90 (App)")

        vec = DimensionVector(
            lifecycle=min(max(lifecycle, 0.0), 1.0),
            protocol=min(max(protocol, 0.0), 1.0),
            execution=min(max(execution, 0.0), 1.0),
            agenticity=min(max(agenticity, 0.0), 1.0),
            boundary=min(max(boundary, 0.0), 1.0),
            swarm=min(max(swarm, 0.0), 1.0),
            interface=min(max(interface, 0.0), 1.0)
        )
        return vec, derivation
