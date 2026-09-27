#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/catalog_auditor.py: First-Principles Fleet Goal Auditor.
Audits multi-repository catalogs strictly from their stated core mission/responsibility.
"""
import os
import re
import json
from typing import Dict, List, Any, Optional
from core.goal_arbiter import GoalDrivenArbiter, GoalEvaluationVerdict, ArchetypeEnum
from core.repo_analyzer import RepoAnalyzer


class CatalogAuditor:
    """
    Audits an entire fleet catalog deterministically based on original stated goals.
    """

    @classmethod
    def audit_catalog_file(cls, catalog_path: str, base_repo_dir: Optional[str] = None) -> Dict[str, Any]:
        if not os.path.exists(catalog_path):
            raise FileNotFoundError(f"Catalog file not found: {catalog_path}")

        with open(catalog_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        row_pat = re.compile(r"\|\s*`([^`]+)`\s*\|\s*([^\|]+)\|\s*`?([^`\|]+)`?\s*\|\s*([^\|]+)\|\s*([^\|]+)\|")
        matches = row_pat.findall(content)

        results: List[Dict[str, Any]] = []
        agreements = 0
        total = 0

        for match in matches:
            orig_name = match[0].strip()
            status = match[1].strip()
            expected_name = match[2].strip()
            domain = match[3].strip()
            description = match[4].strip()

            if orig_name in ("原仓库名称", "---"):
                continue

            total += 1
            # Combine the original core mission statement
            core_goal = f"{orig_name}：{domain}。{description}"
            verdict = GoalDrivenArbiter.deduce_from_goal(core_goal, entity_name=orig_name)

            expected_prefix = expected_name.split("-")[0] if "-" in expected_name else expected_name

            # Alignment evaluation
            is_agreed = (verdict.archetype.value == expected_prefix) or (verdict.recommended_prefix.rstrip("-") == expected_prefix)

            # Special case 1: Archival transition mirrors
            if expected_name.startswith("archive-"):
                target_sub = expected_name[len("archive-"):]
                target_prefix = target_sub.split("-")[0]
                if verdict.archetype.value == target_prefix or verdict.recommended_prefix.rstrip("-") == target_prefix:
                    is_agreed = True

            # Special case 2: Airgap / permanently exempt repositories
            if "豁免" in description or "airgap" in description.lower() or expected_name == orig_name:
                is_agreed = True

            if is_agreed:
                agreements += 1

            results.append({
                "original_name": orig_name,
                "current_status": status,
                "catalog_expected_name": expected_name,
                "domain": domain,
                "stated_core_goal": description,
                "deduced_archetype": verdict.archetype.value,
                "recommended_prefix": verdict.recommended_prefix,
                "suggested_name": verdict.suggested_name,
                "confidence": round(verdict.confidence, 4),
                "is_aligned": is_agreed,
                "minimal_viable_rationale": verdict.minimal_viable_rationale,
                "deduction_chain": verdict.deduction_chain,
                "warning": verdict.anti_pattern_warning
            })

        alignment_rate = (agreements / total * 100) if total > 0 else 100.0

        return {
            "catalog_path": catalog_path,
            "total_repositories_audited": total,
            "aligned_count": agreements,
            "misaligned_count": total - agreements,
            "alignment_rate_pct": round(alignment_rate, 2),
            "is_invariant_stable": (alignment_rate >= 85.0),
            "details": results
        }
