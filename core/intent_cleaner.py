#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/intent_cleaner.py: Intent Cleansing & Implementation De-noising Scalpel.
Separates Problem Domain (Core Intent/Goal) from Solution Domain (Architecture/Tech Stack).
Inspired by Michael Jackson's Problem Frames and KAOS Goal-Oriented Requirements Engineering.
"""
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional


@dataclass
class IntentDenoiseReport:
    raw_input: str
    pure_problem_goal: str
    injected_tech_stack: List[str]
    injected_architecture_claims: List[str]
    has_solution_bias: bool
    is_pure_boilerplate: bool
    bias_explanation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_input": self.raw_input,
            "pure_problem_goal": self.pure_problem_goal,
            "injected_tech_stack": self.injected_tech_stack,
            "injected_architecture_claims": self.injected_architecture_claims,
            "has_solution_bias": self.has_solution_bias,
            "is_pure_boilerplate": self.is_pure_boilerplate,
            "bias_explanation": self.bias_explanation
        }


class IntentCleaner:
    """
    De-couples 'What Problem to Solve' (Problem Domain) from 'What Stack was Used' (Solution Domain).
    Exposes and neutralizes implementation bias ('夹带私货 / 技术绑架').
    """

    # Solution domain tech stack keywords
    TECH_STACK_KEYWORDS = [
        "fastapi", "flask", "django", "tornado", "gin", "actix", "spring", "express", "koa", "nest.js",
        "next.js", "react", "vue", "electron", "pyqt", "tkinter", "flutter", "swiftui",
        "redis", "kafka", "rabbitmq", "mysql", "postgresql", "sqlite", "mongodb", "elasticsearch",
        "docker", "docker-compose", "k8s", "kubernetes", "nginx", "caddy", "traefik",
        "python", "golang", "rust", "typescript", "c++", "bash", "powershell"
    ]

    # Architecture / Over-engineering claims
    ARCHITECTURE_PATTERNS = [
        (r"(基于|采用|使用)\s*[\w\.\-]+\s*(微服务|框架|架构|中间件)", "声明技术架构/框架"),
        (r"(常驻|长驻)\s*(后台|守护进程|进程|运行)", "声明常驻后台"),
        (r"(监听|绑定)\s*(\d+|http|ws|tcp|udp|端口)", "声明网络端口监听"),
        (r"(提供|暴露)\s*(http|rest|grpc|rpc|websocket|api)\s*(接口|服务)", "声明服务暴露接口"),
        (r"(构建|开发|作为)\s*(一个|一款)?\s*(微服务|后端服务|网关服务|后台服务)", "声明微服务形态"),
        (r"(高并发|高可用|分布式|高吞吐)", "声明非功能性架构修饰词"),
        (r"(用|写了|编写了|开发了|运行一个)\s*(python|go|rust|bash)?\s*(脚本|程序|代码)", "声明编程实现手段")
    ]

    # Pure template boilerplate sentences that contain ZERO problem domain semantics
    BOILERPLATE_PATTERNS = [
        r"包含长驻留后台进程[、，\s]*http/websocket\s*端口监听与服务接口",
        r"属于\s*ai\s*集群核心调度大脑或多模型共生网格",
        r"端到端业务工具（如知乎自动化、邮件监控、移动压测等）",
        r"管理边缘节点[、，\s]*tailscale/derp\s*穿透或代理分流",
        r"纯技术白皮书[、，\s]*战术手册或排障实战笔记",
        r"已符合\s*[\w\*\-]+\s*命名规范"
    ]

    @classmethod
    def clean(cls, raw_text: str) -> IntentDenoiseReport:
        text = raw_text.strip()
        lower_text = text.lower()

        found_tech: List[str] = []
        found_arch: List[str] = []

        # 1. Detect explicit tech stack
        for tech in cls.TECH_STACK_KEYWORDS:
            pattern = rf"(?i)\b{re.escape(tech)}\b"
            if re.search(pattern, text):
                found_tech.append(tech)

        # 2. Detect architecture / solution claims
        for pat, desc in cls.ARCHITECTURE_PATTERNS:
            matches = re.findall(pat, text, re.IGNORECASE)
            if matches:
                found_arch.append(desc)

        # 3. Check if input is 100% meaningless boilerplate
        is_pure_boilerplate = False
        for bp in cls.BOILERPLATE_PATTERNS:
            if re.search(bp, text, re.IGNORECASE) and len(text) < 60:
                is_pure_boilerplate = True
                break

        # 4. Extract pure goal (Problem Domain)
        cleaned = text

        # Strategy A: Target indicators ("用于", "用来", "旨在", "负责", "致力于", "实现", "核心功能", "核心目标")
        target_marker = re.search(r"(?:用于|用来|旨在|负责|致力于|核心目的在于|核心功能为|主要目标是|实现)\s*[:：]?\s*(.+)$", cleaned, re.IGNORECASE)
        if target_marker:
            candidate = target_marker.group(1).strip()
            if len(candidate) >= 3:
                cleaned = candidate

        # Strategy B: Remove implementation clauses (clauses with ports, frameworks, daemons)
        clauses = re.split(r"[，,。；;]", cleaned)
        valid_clauses = []
        for c in clauses:
            c_str = c.strip()
            if not c_str:
                continue
            c_lower = c_str.lower()
            # If the clause only talks about technology/daemon/ports, discard it
            is_tech_only = any(re.search(pat, c_str, re.IGNORECASE) for pat, _ in cls.ARCHITECTURE_PATTERNS)
            is_bp = any(re.search(bp, c_str, re.IGNORECASE) for bp in cls.BOILERPLATE_PATTERNS)
            if is_tech_only or is_bp:
                continue
            # Remove leading introductory noise
            c_str = re.sub(r"^(基于|采用|使用)\s*[\w\.\+\-\s、]+\s*(框架|技术栈)?", "", c_str)
            c_str = re.sub(r"^(本项目|本仓库|本工具|本程序|本服务|本系统|该项目|该工具|该系统)?\s*(是一个|是)?\s*", "", c_str)
            c_str = c_str.strip()
            if c_str:
                valid_clauses.append(c_str)

        if valid_clauses:
            cleaned = "，".join(valid_clauses)

        # Final cleanup of noise punctuation
        cleaned = re.sub(r"^[\s，,。；;:：\-—]+", "", cleaned)
        cleaned = re.sub(r"[\s，,。；;:：\-—]+$", "", cleaned)

        if not cleaned:
            cleaned = text

        has_bias = bool(found_tech or found_arch)
        if is_pure_boilerplate:
            explanation = "【纯技术模板私货警报】输入未包含任何具体业务问题域陈述，全系从分类目录照抄的技术模板套话！"
        elif has_bias:
            explanation = f"检测到输入中掺杂了 {len(found_tech)} 个技术栈选型与 {len(found_arch)} 项实现层架构声明（解域私货）。"
        else:
            explanation = "输入为纯粹的问题域/目标描述，未掺杂实现层技术栈偏见。"

        return IntentDenoiseReport(
            raw_input=text,
            pure_problem_goal=cleaned,
            injected_tech_stack=list(set(found_tech)),
            injected_architecture_claims=list(set(found_arch)),
            has_solution_bias=has_bias,
            is_pure_boilerplate=is_pure_boilerplate,
            bias_explanation=explanation
        )
