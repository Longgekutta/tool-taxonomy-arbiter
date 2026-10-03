#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/fleet_auditor.py: Comprehensive Bidirectional Fleet Taxonomy Auditor.
Audits all GitHub repositories across the entire organization/account.
Performs bidirectional verification:
  1. Goal -> Archetype (Forward first-principles deduction from Problem Domain)
  2. Repo Prefix -> Goal (Reverse audit: does the current prefix match physical reality?)
"""
import os
import re
import json
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from core.goal_arbiter import GoalDrivenArbiter, ArchetypeEnum, GoalEvaluationVerdict
from core.intent_cleaner import IntentCleaner


class FleetAuditor:
    """
    Audits 100+ GitHub repositories with bidirectional checks and anti-pattern detection.
    """

    KNOWN_PREFIXES = [
        "tool-", "skill-", "spec-", "rule-", "svc-", "mcp-",
        "cluster-", "app-", "infra-", "cfg-", "doc-", "archive-"
    ]

    @classmethod
    def get_repo_prefix(cls, repo_name: str) -> str:
        for p in cls.KNOWN_PREFIXES:
            if repo_name.startswith(p):
                return p.rstrip("-")
        return "unprefixed"

    @classmethod
    def get_default_base_dir(cls) -> str:
        env_dir = os.environ.get("AGENT_WORKSPACE_ROOT") or os.environ.get("GITHUB_TOOLS_ROOT")
        if env_dir and os.path.exists(env_dir):
            return env_dir
        from pathlib import Path
        sibling_dir = str(Path(__file__).resolve().parent.parent.parent)
        if os.path.exists(sibling_dir):
            return sibling_dir
        return "D:/github"

    @classmethod
    def extract_goal_for_repo(
        cls,
        repo_name: str,
        gh_desc: Optional[str] = None,
        base_dir: Optional[str] = None,
        catalog_map: Optional[Dict[str, Dict[str, str]]] = None
    ) -> Tuple[str, str]:
        base_dir = base_dir or cls.get_default_base_dir()
        """
        Extracts the most authentic problem-domain goal possible.
        Priority:
          1. Official GitHub description (if non-empty)
          2. Local SKILL.md YAML description (for skills)
          3. Local README.md single-responsibility positioning
          4. FLEET_TAXONOMY_CATALOG entry
          5. Repository name itself
        """
        # 1. GitHub description (Author's explicit external positioning)
        if gh_desc and gh_desc.strip():
            return gh_desc.strip(), "github_description"

        # 2. Local SKILL.md (for skill-* repos)
        local_skill = os.path.join(base_dir, repo_name, "SKILL.md")
        if os.path.exists(local_skill):
            try:
                with open(local_skill, "r", encoding="utf-8", errors="ignore") as f:
                    s_content = f.read()
                m_desc = re.search(r'description:\s*>-?\s*\n((?:\s+[^\n]+\n)+)', s_content)
                if m_desc:
                    cleaned_s = " ".join([l.strip() for l in m_desc.group(1).splitlines() if l.strip()])
                    if cleaned_s:
                        return cleaned_s, "local_skill_frontmatter"
                m_single = re.search(r'description:\s*([^\n\r]+)', s_content)
                if m_single:
                    return m_single.group(1).strip(), "local_skill_frontmatter"
            except Exception:
                pass

        # 3. Local README
        local_readme = os.path.join(base_dir, repo_name, "README.md")
        if os.path.exists(local_readme):
            try:
                with open(local_readme, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                # Try single-responsibility blockquote
                m = re.search(r'>\s*\*\*单一职责定位\*\*[：:]\s*([^\n\r]+)', content)
                if m:
                    return m.group(1).strip(), "local_readme_positioning"
                # Try problem domain heading
                m = re.search(r'##\s*🎯[^\n\r]+\n+([^#\n\r]+)', content)
                if m:
                    return m.group(1).strip(), "local_readme_target"
                # Try title subtitle
                m_title = re.search(r'^#\s*[\w\.\-]+\s*[:：]\s*([^\n\r]+)', content, re.MULTILINE)
                if m_title:
                    return m_title.group(1).strip(), "local_readme_title"
                # Try first blockquote
                m = re.search(r'>\s*([^\n\r]{10,})', content)
                if m:
                    return m.group(1).strip(), "local_readme_blockquote"
            except Exception:
                pass

        # 4. Catalog map
        if catalog_map and repo_name in catalog_map:
            cat = catalog_map[repo_name]
            goal_text = f"{cat.get('domain', '')} {cat.get('description', '')}".strip()
            if goal_text:
                return goal_text, "catalog_entry"

        # 5. Fallback to repo name
        return repo_name.replace("-", " "), "repo_name_fallback"

    @classmethod
    def load_catalog_map(cls, catalog_path: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        catalog_path = catalog_path or os.path.join(cls.get_default_base_dir(), "FLEET_TAXONOMY_CATALOG.md")
        catalog_map = {}
        if not os.path.exists(catalog_path):
            return catalog_map
        try:
            with open(catalog_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            row_pat = re.compile(r"\|\s*`([^`]+)`\s*\|\s*([^\|]+)\|\s*`?([^`\|]+)`?\s*\|\s*([^\|]+)\|\s*([^\|]+)\|")
            matches = row_pat.findall(content)
            for m in matches:
                orig_name = m[0].strip()
                if orig_name in ("原仓库名称", "---"):
                    continue
                catalog_map[orig_name] = {
                    "status": m[1].strip(),
                    "expected_name": m[2].strip(),
                    "domain": m[3].strip(),
                    "description": m[4].strip()
                }
        except Exception:
            pass
        return catalog_map

    @classmethod
    def audit_all_github_repos(
        cls,
        json_file: Optional[str] = None,
        base_dir: Optional[str] = None,
        catalog_path: Optional[str] = None
    ) -> Dict[str, Any]:
        base_dir = base_dir or cls.get_default_base_dir()
        json_file = json_file or os.path.join(base_dir, "all_github_repos.json")
        catalog_path = catalog_path or os.path.join(base_dir, "FLEET_TAXONOMY_CATALOG.md")
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"GitHub repos json not found: {json_file}")

        with open(json_file, "r", encoding="utf-8") as f:
            repos_data = json.load(f)

        catalog_map = cls.load_catalog_map(catalog_path)

        total = len(repos_data)
        aligned_count = 0
        misaligned_count = 0
        unprefixed_count = 0
        over_engineering_alerts = 0
        boilerplate_alerts = 0

        details = []

        for r in repos_data:
            name = r["name"]
            gh_desc = r.get("description")
            is_archived = r.get("isArchived", False)

            current_prefix = cls.get_repo_prefix(name)
            goal_text, goal_source = cls.extract_goal_for_repo(name, gh_desc, base_dir, catalog_map)

            verdict = GoalDrivenArbiter.deduce_from_goal(goal_text, entity_name=name)
            deduced_archetype = verdict.archetype.value

            # Alignment logic
            is_aligned = False
            alignment_status = "UNKNOWN"

            if current_prefix == "unprefixed":
                unprefixed_count += 1
                alignment_status = "UNPREFIXED_LEGACY"
                # If catalog had an expected prefix, compare against that
                if name in catalog_map:
                    exp = catalog_map[name]["expected_name"]
                    exp_p = exp.split("-")[0] if "-" in exp else exp
                    if deduced_archetype == exp_p:
                        alignment_status = "UNPREFIXED_ALIGN_CATALOG"
            else:
                if current_prefix == "archive":
                    # Check archived sub-prefix if any, or if it's archived
                    alignment_status = "ARCHIVED_MIRROR"
                    is_aligned = True
                    aligned_count += 1
                elif current_prefix == deduced_archetype:
                    is_aligned = True
                    aligned_count += 1
                    alignment_status = "ALIGNED"
                else:
                    misaligned_count += 1
                    alignment_status = "MISALIGNED"

            if verdict.anti_pattern_warning and "过度设计" in verdict.anti_pattern_warning:
                over_engineering_alerts += 1
            if verdict.anti_pattern_warning and "纯模板套话" in verdict.anti_pattern_warning:
                boilerplate_alerts += 1

            details.append({
                "repo_name": name,
                "current_prefix": current_prefix,
                "deduced_archetype": deduced_archetype,
                "recommended_name": verdict.suggested_name,
                "confidence": round(verdict.confidence, 4),
                "is_aligned": is_aligned,
                "alignment_status": alignment_status,
                "goal_source": goal_source,
                "raw_goal": goal_text,
                "pure_problem_goal": verdict.pure_problem_goal,
                "has_solution_bias": verdict.has_solution_bias,
                "injected_tech_stack": verdict.injected_tech_stack,
                "minimal_viable_rationale": verdict.minimal_viable_rationale,
                "warning": verdict.anti_pattern_warning
            })

        # Calculate prefixed alignment rate
        prefixed_total = total - unprefixed_count
        prefixed_alignment_rate = (aligned_count / prefixed_total * 100) if prefixed_total > 0 else 0.0

        return {
            "total_github_repositories": total,
            "prefixed_repositories_count": prefixed_total,
            "unprefixed_legacy_count": unprefixed_count,
            "prefixed_aligned_count": aligned_count,
            "prefixed_misaligned_count": misaligned_count,
            "prefixed_alignment_rate_pct": round(prefixed_alignment_rate, 2),
            "over_engineering_alerts_count": over_engineering_alerts,
            "boilerplate_warnings_count": boilerplate_alerts,
            "details": details
        }
