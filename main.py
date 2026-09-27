#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tool-taxonomy-arbiter: 软件架构形态确定性仲裁决策装具
=====================================================
Universal CLI Facade (UCFS v1.0) Standard Entrypoint.

5 Standard Verbs:
  setup     Verify Python runtime and engine dependencies
  run       Execute deterministic archetype arbitration (judge idea, audit repo, or audit catalog)
  test      Execute automated regression unit tests
  health    Diagnostic self-test
  clean     Clean bytecode artifacts and cached reports
"""
import sys
import os
import json
import argparse
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.models import ArchetypeEnum, DimensionVector, ArbiterVerdict, ARCHETYPE_METADATA
from core.decision_engine import DecisionEngine
from core.repo_analyzer import RepoAnalyzer
from core.catalog_auditor import CatalogAuditor


def run_setup(args) -> int:
    status = {
        "status": "ready",
        "tool": "tool-taxonomy-arbiter",
        "version": "1.0.0",
        "python_version": sys.version.split()[0],
        "base_dir": BASE_DIR,
        "archetypes_count": len(ArchetypeEnum)
    }
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print(f"[tool-taxonomy-arbiter] Setup OK: Runtime ready (Python {status['python_version']}, {status['archetypes_count']} Archetypes configured).")
    return 0


def run_test(args) -> int:
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.join(BASE_DIR, "tests"))
    runner = unittest.TextTestRunner(verbosity=2 if not args.json else 0)
    result = runner.run(suite)
    data = {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "passed": result.wasSuccessful()
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if result.wasSuccessful() else 1


def run_health(args) -> int:
    # Diagnostic test on known canonical concepts
    test_vec = DimensionVector(lifecycle=0.0, execution=1.0, protocol=0.0, agenticity=0.0)
    v_tool = DecisionEngine.evaluate_vector(test_vec, "test-cli-tool")
    is_tool_ok = (v_tool.archetype == ArchetypeEnum.TOOL)

    test_vec_svc = DimensionVector(lifecycle=1.0, execution=1.0, protocol=1.0, agenticity=0.0)
    v_svc = DecisionEngine.evaluate_vector(test_vec_svc, "test-gateway-daemon")
    is_svc_ok = (v_svc.archetype == ArchetypeEnum.SVC)

    healthy = is_tool_ok and is_svc_ok
    data = {
        "status": "HEALTHY" if healthy else "UNHEALTHY",
        "invariance_check": "PASS" if healthy else "FAIL",
        "sample_evaluations": {
            "test_cli_tool": v_tool.archetype.value,
            "test_gateway_daemon": v_svc.archetype.value
        }
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"[tool-taxonomy-arbiter] Health: {'HEALTHY' if healthy else 'UNHEALTHY'} (Determinism Check: {data['invariance_check']})")
    return 0 if healthy else 1


def run_clean(args) -> int:
    cleaned = 0
    for root, dirs, files in os.walk(BASE_DIR):
        for d in dirs:
            if d == "__pycache__":
                try:
                    import shutil
                    shutil.rmtree(os.path.join(root, d))
                    cleaned += 1
                except Exception:
                    pass
    data = {"status": "success", "cleaned_dirs": cleaned}
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"[tool-taxonomy-arbiter] Cleaned {cleaned} cache directories.")
    return 0


def run_arbiter(args) -> int:
    # 1. Direct path audit
    if args.path:
        target = os.path.abspath(args.path)
        if os.path.isfile(target) and target.endswith(".md"):
            # Catalog file audit
            catalog_res = CatalogAuditor.audit_catalog_file(target, base_repo_dir=os.path.dirname(target))
            if args.json:
                print(json.dumps(catalog_res, ensure_ascii=False, indent=2))
            else:
                print("=" * 80)
                print(f" 🎯 Fleet Taxonomy Catalog Audit: {os.path.basename(target)}")
                print(f" • Total Audited:    {catalog_res['total_repositories_audited']}")
                print(f" • Aligned/Agreed:   {catalog_res['aligned_count']}")
                print(f" • Alignment Rate:   {catalog_res['alignment_rate_pct']}%")
                print(f" • Invariant Stable: {'PASS (>=90%)' if catalog_res['is_invariant_stable'] else 'FAIL'}")
                print("=" * 80)
            return 0
        elif os.path.isdir(target):
            # Physical codebase audit
            verdict = RepoAnalyzer.analyze_path(target)
            if args.json:
                print(verdict.to_json())
            else:
                _print_verdict(verdict)
            return 0
        else:
            print(f"[ERROR] Path not recognized: {args.path}", file=sys.stderr)
            return 1

    # 2. Idea / Prompt text evaluation
    idea_text = args.idea or (args.extra_args[0] if args.extra_args else "")
    if not idea_text:
        idea_text = "开发一个自动从GitHub嗅探安装包并一键静默更新各平台客户端的工具"

    vec, notes = DecisionEngine.extract_vector_from_text(idea_text)
    verdict = DecisionEngine.evaluate_vector(vec, concept_title=idea_text, derivation_notes=notes)

    if args.json:
        print(verdict.to_json())
    else:
        _print_verdict(verdict)
    return 0


def _print_verdict(v: ArbiterVerdict):
    print("=" * 80)
    print(f" 🎯 架构形态确定性仲裁裁决书 (Taxonomy Arbiter Verdict)")
    print("=" * 80)
    print(f" • 输入概念/项目:   {v.input_summary}")
    print(f" • 确定性裁定形态:   【 {v.archetype.value.upper()} 】 (前缀: {v.recommended_prefix})")
    print(f" • 推荐标准命名:     {v.suggested_name}")
    print(f" • 决策置信度:       {v.confidence:.2%}")
    print(f" • 对应生态位:       {v.slot_description}")
    print("-" * 80)
    print(" 📊 七维正交特征空间投影坐标:")
    for dim, score in v.dimension_scores.items():
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        print(f"   [{dim:12s}] {bar} {score:.2f}")
    print("-" * 80)
    print(" 🔍 形式化数学推导逻辑链:")
    for i, step in enumerate(v.derivation_path, 1):
        print(f"   {i}. {step}")
    print("-" * 80)
    print(" 🛡️ 遵循核心刚性不变量 (Core Invariants):")
    for inv in v.invariants_required:
        print(f"   ✓ {inv}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="tool-taxonomy-arbiter: Deterministic Software Archetype & Architectural Decision Arbiter"
    )
    parser.add_argument("verb", nargs="?", default="run", choices=["setup", "run", "test", "health", "clean", "judge", "audit"])
    parser.add_argument("extra_args", nargs="*", help="Extra arguments or concept prompt")
    parser.add_argument("--idea", "-i", type=str, help="Idea or concept description to judge")
    parser.add_argument("--path", "-p", type=str, help="Local repo path or catalog markdown to audit")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON format")

    args = parser.parse_args()

    # Aliases
    if args.verb == "judge":
        args.verb = "run"
        if args.extra_args and not args.idea:
            args.idea = " ".join(args.extra_args)
    elif args.verb == "audit":
        args.verb = "run"
        if args.extra_args and not args.path:
            args.path = args.extra_args[0]

    dispatch = {
        "setup": run_setup,
        "run": run_arbiter,
        "test": run_test,
        "health": run_health,
        "clean": run_clean
    }

    fn = dispatch.get(args.verb, run_arbiter)
    sys.exit(fn(args))


if __name__ == "__main__":
    main()
