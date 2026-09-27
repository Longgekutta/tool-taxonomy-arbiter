#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/repo_analyzer.py: Physical Codebase AST & Feature Introspector.
Deterministically maps a local codebase directory to the 7-dimensional vector.
"""
import os
import re
from typing import Dict, List, Tuple, Any, Optional
from core.models import DimensionVector, ArbiterVerdict, ArchetypeEnum
from core.decision_engine import DecisionEngine


CODE_EXTS = {".py", ".rs", ".go", ".ts", ".js", ".c", ".cpp", ".h", ".hpp", ".java", ".kt", ".swift", ".cs", ".rb", ".php"}
DOC_EXTS = {".md", ".markdown", ".rst", ".txt", ".pdf"}
CFG_EXTS = {".yaml", ".yml", ".json", ".toml", ".ini", ".conf", ".xml"}


class RepoAnalyzer:
    """
    Introspects an existing local repository and extracts its deterministic physical signature.
    """

    @classmethod
    def analyze_path(cls, repo_path: str) -> ArbiterVerdict:
        if not os.path.exists(repo_path):
            raise FileNotFoundError(f"Path does not exist: {repo_path}")

        repo_name = os.path.basename(os.path.abspath(repo_path)).lower()
        derivation = [f"正在分析物理代码仓库: {repo_name} (路径: {repo_path})"]

        # Fast-track 1: If repo is already standard canonical prefix
        for arch in ArchetypeEnum:
            if repo_name.startswith(f"{arch.value}-"):
                derivation.append(f"物理仓库显式冠以标准前缀 '{arch.value}-' -> 符合生态位命名规范")
                vec = cls._create_default_vector_for_archetype(arch)
                return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=arch)

        # 1. Traverse repository files
        code_files = 0
        doc_files = 0
        cfg_files = 0
        total_files = 0

        has_skill_md = False
        has_docker_compose = False
        has_gradle_or_apk = False
        has_electron_or_frontend = False
        has_mcp_signature = False
        has_port_listener = False
        has_agent_cluster = False

        port_patterns = [
            re.compile(r"(\.listen\s*\(|socket\.bind|uvicorn\.run|FastAPI\(|createServer|app\.run\()"),
            re.compile(r"(PORT\s*=\s*\d+|port:\s*\d+|addr\s*:=\s*\":\d+\")")
        ]
        mcp_patterns = [
            re.compile(r"(from\s+mcp|import\s+fastmcp|FastMCP\(|mcp\.server|ModelContextProtocol|JSON-RPC\s*2\.0)"),
            re.compile(r"(\"jsonrpc\":\s*\"2\.0\"|StdioServerTransport)")
        ]
        cluster_patterns = [
            re.compile(r"(autogen|langgraph|crewai|swarm|multi-agent|agent_mesh|agent_matrix|interagent)")
        ]

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}]
            for f in files:
                total_files += 1
                rel_path = os.path.relpath(os.path.join(root, f), repo_path).replace("\\", "/")
                ext = os.path.splitext(f)[1].lower()

                if ext in CODE_EXTS:
                    code_files += 1
                elif ext in DOC_EXTS:
                    doc_files += 1
                elif ext in CFG_EXTS:
                    cfg_files += 1

                if f.lower() == "skill.md" or "skills/" in rel_path.lower():
                    has_skill_md = True

                if f.lower() in ("docker-compose.yml", "docker-compose.yaml"):
                    has_docker_compose = True

                if f.lower() in ("androidmanifest.xml", "build.gradle", "build.gradle.kts") or ext == ".apk":
                    has_gradle_or_apk = True

                if f.lower() in ("package.json", "index.html", "app.tsx", "app.vue"):
                    has_electron_or_frontend = True

                if ext in CODE_EXTS and code_files <= 50:
                    try:
                        with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fh:
                            content = fh.read(16384)
                            for pat in port_patterns:
                                if pat.search(content):
                                    has_port_listener = True
                            for pat in mcp_patterns:
                                if pat.search(content):
                                    has_mcp_signature = True
                            for pat in cluster_patterns:
                                if pat.search(content):
                                    has_agent_cluster = True
                    except Exception:
                        pass

        derivation.append(f"文件扫描统计: 代码 {code_files} 个, 文档 {doc_files} 个, 配置 {cfg_files} 个 (总计 {total_files})")

        # Semantic keywords in legacy repository names
        is_infra_keyword = any(k in repo_name for k in ["derp", "relay", "tailscale", "tunnel", "mirror", "edge-server", "server-network"])
        is_cfg_keyword = any(k in repo_name for k in ["config", "workflows", "workspace", "dify", "fastgpt", "ragflow"])
        is_doc_keyword = any(k in repo_name for k in ["guide", "playbook", "notes", "tutorial", "roadmap", "handbook", "knowledge", "record", "standards", "study"])
        is_cluster_keyword = any(k in repo_name for k in ["cluster", "mesh", "matrix", "dual-engine"])
        is_svc_keyword = any(k in repo_name for k in ["gateway", "bridge", "router", "cache-engine", "web-to-api"])
        is_app_keyword = any(k in repo_name for k in ["auto", "hub", "publisher", "pipeline", "120fps", "study", "baidu", "client"])

        # Prioritize archetypes based on physical reality
        if is_infra_keyword:
            derivation.append("命中网络中继/边缘节点/穿透特征 -> 判定为 INFRA")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.INFRA)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.INFRA)

        if is_cfg_keyword and code_files <= 3:
            derivation.append("命中平台配置/工作流模板特征 -> 判定为 CFG")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.CFG)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.CFG)

        if is_doc_keyword and code_files == 0:
            derivation.append("纯战术手册/知识库/排障指南且无代码 -> 判定为 DOC")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.DOC)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.DOC)

        if has_skill_md or repo_name.startswith("skill-"):
            derivation.append("检测到 SKILL.md / Agent SOP 工作流规范 -> 判定为 SKILL")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.SKILL)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.SKILL)

        if has_mcp_signature or "mcp" in repo_name:
            derivation.append("检测到 MCP 协议服务器代码特征 -> 判定为 MCP")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.MCP)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.MCP)

        if is_cluster_keyword or has_agent_cluster:
            derivation.append("检测到多智能体网格协同 / 集群调度拓扑 -> 判定为 CLUSTER")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.CLUSTER)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.CLUSTER)

        if is_svc_keyword or has_port_listener:
            derivation.append("检测到网络端口监听 / 后台网关特征 -> 判定为 SVC")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.SVC)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.SVC)

        if is_app_keyword or has_gradle_or_apk or (has_electron_or_frontend and code_files > 5):
            derivation.append("检测到终端应用 / 业务机器人 / APK 前端特征 -> 判定为 APP")
            vec = cls._create_default_vector_for_archetype(ArchetypeEnum.APP)
            return DecisionEngine.evaluate_vector(vec, concept_title=repo_name, derivation_notes=derivation, explicit_target=ArchetypeEnum.APP)

        # Default fallback to vector evaluation
        lifecycle = 0.95 if has_port_listener else 0.05
        protocol = 0.9 if has_port_listener else 0.05
        execution = min(1.0, 0.4 + (code_files / max(total_files, 1)) * 0.6) if code_files > 0 else 0.05
        agenticity = 0.9 if has_skill_md else 0.0
        boundary = 0.9 if ("spec" in repo_name or "schema" in repo_name) else 0.0
        swarm = 0.95 if has_agent_cluster else 0.0
        interface = 0.9 if (has_gradle_or_apk or has_electron_or_frontend) else 0.0

        vector = DimensionVector(
            lifecycle=lifecycle,
            protocol=protocol,
            execution=execution,
            agenticity=agenticity,
            boundary=boundary,
            swarm=swarm,
            interface=interface
        )
        return DecisionEngine.evaluate_vector(vector, concept_title=repo_name, derivation_notes=derivation)

    @classmethod
    def _create_default_vector_for_archetype(cls, arch: ArchetypeEnum) -> DimensionVector:
        from core.decision_engine import ARCHETYPE_CENTROIDS
        c = ARCHETYPE_CENTROIDS.get(arch, {})
        return DimensionVector(
            lifecycle=c.get("lifecycle", 0.0),
            protocol=c.get("protocol", 0.0),
            execution=c.get("execution", 0.0),
            agenticity=c.get("agenticity", 0.0),
            boundary=c.get("boundary", 0.0),
            swarm=c.get("swarm", 0.0),
            interface=c.get("interface", 0.0)
        )
