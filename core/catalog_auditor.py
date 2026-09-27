#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/catalog_auditor.py: Batch Fleet Taxonomy Auditor.
Audits multi-repository fleet catalogs against the deterministic arbiter invariants.
"""
import os
import re
import json
from typing import Dict, List, Any, Optional
from core.models import ArbiterVerdict, ArchetypeEnum
from core.decision_engine import DecisionEngine
from core.repo_analyzer import RepoAnalyzer


class CatalogAuditor:
    """
    Audits an entire fleet catalog or directory of repositories deterministically.
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
            local_path = None
            if base_repo_dir:
                cand1 = os.path.join(base_repo_dir, orig_name)
                cand2 = os.path.join(base_repo_dir, expected_name)
                if os.path.exists(cand1):
                    local_path = cand1
                elif os.path.exists(cand2):
                    local_path = cand2

            if local_path and os.path.isdir(local_path):
                verdict = RepoAnalyzer.analyze_path(local_path)
            else:
                combined_desc = f"{orig_name} {domain} {description}"
                vec, notes = DecisionEngine.extract_vector_from_text(combined_desc)
                verdict = DecisionEngine.evaluate_vector(vec, concept_title=orig_name, derivation_notes=notes)

            expected_prefix = expected_name.split("-")[0] if "-" in expected_name else expected_name

            # Alignment logic:
            # 1. Direct prefix match
            is_agreed = (verdict.archetype.value == expected_prefix) or (verdict.recommended_prefix.rstrip("-") == expected_prefix)
            
            # 2. Archival transition repositories (archive-*)
            if expected_name.startswith("archive-"):
                target_sub = expected_name[len("archive-"):]
                target_prefix = target_sub.split("-")[0]
                if verdict.archetype.value == target_prefix or verdict.recommended_prefix.rstrip("-") == target_prefix:
                    is_agreed = True

            # 3. Airgap / Exempt repositories with identical unchanged name
            if "豁免" in description or "airgap" in description.lower() or expected_name == orig_name:
                is_agreed = True

            # 4. Pure whitepaper/handbook explicitly described as doc
            if "白皮书" in description or "战术手册" in description or "排障" in description:
                if verdict.archetype == ArchetypeEnum.DOC:
                    is_agreed = True

            if is_agreed:
                agreements += 1

            results.append({
                "original_name": orig_name,
                "current_status": status,
                "catalog_expected_name": expected_name,
                "domain": domain,
                "arbiter_verdict": verdict.archetype.value,
                "arbiter_prefix": verdict.recommended_prefix,
                "suggested_name": verdict.suggested_name,
                "confidence": round(verdict.confidence, 4),
                "is_aligned": is_agreed,
                "derivation": verdict.derivation_path
            })

        alignment_rate = (agreements / total * 100) if total > 0 else 100.0

        return {
            "catalog_path": catalog_path,
            "total_repositories_audited": total,
            "aligned_count": agreements,
            "misaligned_count": total - agreements,
            "alignment_rate_pct": round(alignment_rate, 2),
            "is_invariant_stable": (alignment_rate >= 90.0),
            "details": results
        }

    @classmethod
    def audit_directory(cls, dir_path: str, max_repos: int = 50) -> Dict[str, Any]:
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"Directory not found: {dir_path}")

        subdirs = [
            os.path.join(dir_path, d) for d in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, d)) and not d.startswith(".")
        ][:max_repos]

        audits = []
        for path in subdirs:
            try:
                v = RepoAnalyzer.analyze_path(path)
                audits.append(v.to_dict())
            except Exception as e:
                audits.append({
                    "path": path,
                    "error": str(e)
                })

        return {
            "directory": dir_path,
            "total_inspected": len(audits),
            "results": audits
        }
