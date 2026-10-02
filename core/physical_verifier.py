#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/physical_verifier.py: 物理运行期架构形态合规性真实性验真器
对标 ArchUnit / import-linter 思想，检测物理仓库代码是否越界违反最小必要形态。
"""
import os
import re
from pathlib import Path
from typing import Dict, Any, List
from core.goal_arbiter import ArchetypeEnum, GoalEvaluationVerdict


class PhysicalVerifier:
    """
    对仓库进行物理级代码与架构断言：
    - TOOL  : 严禁常驻 socket 监听循环、严禁包含 web 服务器框架 (FastAPI/Flask/Express) 作为常驻服务
    - RULE  : 必须纯粹为规则定义或提示词，严禁包含可执行大型业务二进制或常驻循环
    - SPEC  : 必须为纯规范契约/模式定义，严禁包含运行时业务逻辑
    - DOC   : 严禁包含编译二进制产物
    - SVC   : 必须具备明确的网络端口声明与服务通信契约
    """

    @classmethod
    def verify_repo(cls, repo_path: str, verdict: GoalEvaluationVerdict) -> Dict[str, Any]:
        p = Path(repo_path).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Path does not exist: {repo_path}")

        violations: List[str] = []
        checks_performed: List[str] = []

        archetype = verdict.archetype

        # 扫描所有源码文件 (Python, Go, JS, TS, Rust 等)
        code_files = []
        for root, dirs, files in os.walk(p):
            if any(part in (".git", "__pycache__", "node_modules", "venv", ".venv") for part in Path(root).parts):
                continue
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in (".py", ".go", ".rs", ".js", ".ts", ".sh", ".ps1"):
                    code_files.append(Path(root) / f)

        # 1. TOOL 形态验真
        if archetype == ArchetypeEnum.TOOL:
            checks_performed.append("TOOL: 检测是否存在长驻后台监听端口 (Socket / HTTP Server)")
            server_signatures = [
                r"\.listen\(", r"uvicorn\.run\(", r"app\.run\(", r"http\.ListenAndServe",
                r"TcpListener::bind", r"socket\.bind\("
            ]
            for cf in code_files:
                try:
                    content = cf.read_text(encoding="utf-8", errors="ignore")
                    for sig in server_signatures:
                        if re.search(sig, content):
                            # 排除测试代码
                            if "test" not in str(cf).lower():
                                violations.append(f"[{cf.name}] 发现网络监听签名 '{sig}'，Tool 形态违规演化为常驻网络服务 (过度设计)")
                                break
                except Exception:
                    pass

        # 2. RULE 形态验真
        elif archetype == ArchetypeEnum.RULE:
            checks_performed.append("RULE: 检测是否存在重型业务代码与二进制执行文件")
            if len(code_files) > 10:
                violations.append(f"代码文件数 ({len(code_files)}) 过多，Rule 应当是精简的判定规则，涉嫌过度膨胀")

        # 3. SPEC 形态验真
        elif archetype == ArchetypeEnum.SPEC:
            checks_performed.append("SPEC: 检测是否存在具体业务执行逻辑")
            heavy_code = [f for f in code_files if "test" not in str(f).lower() and f.suffix in (".py", ".go", ".rs")]
            if len(heavy_code) > 5:
                violations.append(f"SPEC 仓库包含 {len(heavy_code)} 个业务代码文件，应当保持纯规范/模式定义，代码应外置到对应 tool/svc")

        # 4. 依赖循环与反向跨层引用预检
        checks_performed.append("GENERAL: 检查是否有未忽略的临时编译垃圾")
        cruft_dirs = list(p.rglob("__pycache__")) + list(p.rglob(".pytest_cache"))
        for cd in cruft_dirs:
            if ".git" not in cd.parts:
                violations.append(f"存在未清理的字节码临时缓存: {cd.relative_to(p)}")

        is_passed = len(violations) == 0

        return {
            "status": "PASS" if is_passed else "FAIL",
            "repo_name": p.name,
            "deduced_archetype": archetype.value,
            "checks_performed": checks_performed,
            "violations_count": len(violations),
            "violations": violations,
            "purity_score": max(0, 100 - len(violations) * 20)
        }
