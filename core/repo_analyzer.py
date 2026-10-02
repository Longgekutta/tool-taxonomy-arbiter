#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/repo_analyzer.py: First-Principles Mission Extractor & Goal Deduction.
Extracts the repository's foundational purpose/intent from README and CORE_INVARIANTS,
then passes it to GoalDrivenArbiter for strictly forward architectural deduction.
"""
import os
import re
from typing import Dict, List, Tuple, Any, Optional
from core.goal_arbiter import GoalDrivenArbiter, GoalEvaluationVerdict, ArchetypeEnum


class RepoAnalyzer:
    """
    Introspects an existing local repository by extracting its original stated mission,
    then deducing what it SHOULD be from first principles (without tracing code bloat).
    """

    @classmethod
    def analyze_path(cls, target_input: str) -> GoalEvaluationVerdict:
        from core.repo_resolver import RepoResolver
        resolved_path, meta = RepoResolver.resolve(target_input)
        repo_name = os.path.basename(resolved_path)
        extracted_goal = cls.extract_mission_from_repo(resolved_path)

        # Forward deduction strictly based on the core goal
        verdict = GoalDrivenArbiter.deduce_from_goal(extracted_goal, entity_name=repo_name)
        return verdict

    @classmethod
    def extract_mission_from_repo(cls, repo_path: str) -> str:
        """
        Extract the core mission/intent statement from README.md or CORE_INVARIANTS.md.
        """
        readme_candidates = ["README.md", "readme.md", "README", "CORE_INVARIANTS.md", "SPEC.md", "SKILL.md"]
        raw_text = ""

        for candidate in readme_candidates:
            p = os.path.join(repo_path, candidate)
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        raw_text = f.read(4096) # read first 4KB
                        if raw_text.strip():
                            break
                except Exception:
                    pass

        repo_name = os.path.basename(os.path.abspath(repo_path))
        if not raw_text.strip():
            return f"项目 {repo_name} 的核心定位与初始意图"

        # Extract title and first meaningful paragraph
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        meaningful_lines = []

        for line in lines[:25]:
            # Skip badges, links, html comments, shields
            if line.startswith("[![") or line.startswith("<") or line.startswith("---") or line.startswith("```"):
                continue
            # Strip markdown headers and quotes
            cleaned = re.sub(r"^#+\s*", "", line)
            cleaned = re.sub(r"^>\s*", "", cleaned)
            if len(cleaned) > 10:
                meaningful_lines.append(cleaned)
            if len(meaningful_lines) >= 3:
                break

        summary = "；".join(meaningful_lines) if meaningful_lines else repo_name
        return f"{repo_name}：{summary}"
