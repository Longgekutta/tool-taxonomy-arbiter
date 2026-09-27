#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tool-taxonomy-arbiter: 基于第一性原理核心目标的架构形态确定性仲裁装具
===================================================================
Universal CLI Facade (UCFS v1.0) Standard Entrypoint.

5 Standard Verbs:
  setup     Verify Python runtime and engine dependencies
  run       Deduce optimal archetype strictly from Core Mission & Intent
  test      Execute automated regression unit tests
  health    Diagnostic self-test
  clean     Clean bytecode artifacts
"""
import sys
import os
import json
import argparse
import unittest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.goal_arbiter import GoalDrivenArbiter, GoalEvaluationVerdict, ArchetypeEnum
from core.repo_analyzer import RepoAnalyzer
from core.catalog_auditor import CatalogAuditor


def run_setup(args) -> int:
    status = {
        "status": "ready",
        "tool": "tool-taxonomy-arbiter",
        "version": "2.0.0-goal-driven",
        "python_version": sys.version.split()[0],
        "base_dir": BASE_DIR,
        "engine": "First-Principles Forward Goal-Driven Deduction Engine"
    }
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print(f"[tool-taxonomy-arbiter] Setup OK: {status['engine']} ready.")
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
    v_tool = GoalDrivenArbiter.deduce_from_goal("极速无状态命令行脚本，计算数据后秒级退出")
    v_skill = GoalDrivenArbiter.deduce_from_goal("指导AI智能体如何一步步调用现有工具提取链接的SOP提示词流程")
    v_svc = GoalDrivenArbiter.deduce_from_goal("常驻后台监听8080端口，接收并发HTTP请求的反向代理网关")

    healthy = (v_tool.archetype == ArchetypeEnum.TOOL and
               v_skill.archetype == ArchetypeEnum.SKILL and
               v_svc.archetype == ArchetypeEnum.SVC)

    data = {
        "status": "HEALTHY" if healthy else "UNHEALTHY",
        "forward_deduction_check": "PASS" if healthy else "FAIL",
        "sample_verdicts": {
            "cli_script": v_tool.archetype.value,
            "agent_sop": v_skill.archetype.value,
            "gateway_daemon": v_svc.archetype.value
        }
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"[tool-taxonomy-arbiter] Health: {'HEALTHY' if healthy else 'UNHEALTHY'} (Deduction Engine: {data['forward_deduction_check']})")
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
            catalog_res = CatalogAuditor.audit_catalog_file(target, base_repo_dir=os.path.dirname(target))
            if args.json:
                print(json.dumps(catalog_res, ensure_ascii=False, indent=2))
            else:
                print("=" * 80)
                print(f" 🎯 基于原始使命的 Fleet Taxonomy Catalog 目标推演审计: {os.path.basename(target)}")
                print(f" • Total Audited:    {catalog_res['total_repositories_audited']}")
                print(f" • Aligned/Agreed:   {catalog_res['aligned_count']}")
                print(f" • Alignment Rate:   {catalog_res['alignment_rate_pct']}%")
                print(f" • Invariant Stable: {'PASS (>=85%)' if catalog_res['is_invariant_stable'] else 'FAIL'}")
                print("=" * 80)
            return 0
        elif os.path.isdir(target):
            verdict = RepoAnalyzer.analyze_path(target)
            if args.json:
                print(verdict.to_json())
            else:
                _print_verdict(verdict)
            return 0
        else:
            print(f"[ERROR] Path not recognized: {args.path}", file=sys.stderr)
            return 1

    # 2. Idea / Intent text evaluation
    idea_text = args.idea or (args.extra_args[0] if args.extra_args else "")
    if not idea_text:
        idea_text = "写一个全平台自动检测GitHub软件更新，扫描本地文件夹并一键批量静默安装更新包的命令行装具"

    verdict = GoalDrivenArbiter.deduce_from_goal(idea_text)

    if args.json:
        print(verdict.to_json())
    else:
        _print_verdict(verdict)
    return 0


def _print_verdict(v: GoalEvaluationVerdict):
    print("=" * 80)
    print(f" 🎯 基于核心目标的第一性原理架构形态裁决书 (Goal-Driven Arbiter Verdict)")
    print("=" * 80)
    print(f" • 原始输入陈述:     {v.target_goal}")
    print(f" • 纯粹问题域目标:   {v.pure_problem_goal}")
    if v.has_solution_bias:
        print(f" • 识别解域私货:     技术栈 {v.injected_tech_stack} | 架构声明 {v.injected_architecture_claims}")
    print(f" • 确定性裁定形态:   【 {v.archetype.value.upper()} 】 (标准前缀: {v.recommended_prefix})")
    print(f" • 推荐法定命名:     {v.suggested_name}")
    print(f" • 裁决置信度:       {v.confidence:.2%}")
    print(f" • 最小必要形态理由: {v.minimal_viable_rationale}")
    if v.anti_pattern_warning:
        print(f" ⚠️  过度设计反模式:  {v.anti_pattern_warning}")
    print("-" * 80)
    print(" 🔍 第一性原理推导逻辑链 (First-Principles Deduction Chain):")
    for i, step in enumerate(v.deduction_chain, 1):
        print(f"   {i}. {step}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="tool-taxonomy-arbiter: First-Principles Goal-Driven Architectural Decision Arbiter"
    )
    parser.add_argument("verb", nargs="?", default="run", choices=["setup", "run", "test", "health", "clean", "judge", "audit"])
    parser.add_argument("extra_args", nargs="*", help="Extra arguments or goal statement")
    parser.add_argument("--idea", "-i", type=str, help="Core goal or mission statement to deduce")
    parser.add_argument("--path", "-p", type=str, help="Local repo path or catalog markdown to deduce")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON format")

    args = parser.parse_args()

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
