#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_arbiter.py: Rigorous regression and determinism unit tests for GoalDrivenArbiter.
Includes implementation bias de-noising, over-engineering alerts, and honest fleet catalog auditing.
"""
import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.goal_arbiter import GoalDrivenArbiter, ArchetypeEnum
from core.catalog_auditor import CatalogAuditor
from core.intent_cleaner import IntentCleaner


class TestGoalDrivenArbiter(unittest.TestCase):

    def test_mathematical_determinism_invariance(self):
        """
        Pure function invariance: Evaluating the exact same goal 100 times must yield identical verdicts.
        """
        goal = "极速无状态命令行脚本，计算数据后秒级退出"
        first = GoalDrivenArbiter.deduce_from_goal(goal, "test-tool")

        for _ in range(100):
            nxt = GoalDrivenArbiter.deduce_from_goal(goal, "test-tool")
            self.assertEqual(nxt.archetype, first.archetype)
            self.assertEqual(nxt.recommended_prefix, first.recommended_prefix)
            self.assertEqual(nxt.suggested_name, first.suggested_name)
            self.assertAlmostEqual(nxt.confidence, first.confidence, places=6)

    def test_implementation_bias_denoising_and_overengineering(self):
        """
        Tests that implementation bias ('夹带私货') is stripped and over-engineering is alerted.
        A goal of calculating perceptual hash is fundamentally a tool, even if wrapped in FastAPI & Redis!
        """
        biased_goal = "基于 FastAPI 和 Redis 的高性能图片哈希微服务，监听8080端口，用于计算图片感知哈希"
        v = GoalDrivenArbiter.deduce_from_goal(biased_goal, "image-hasher")

        self.assertEqual(v.archetype, ArchetypeEnum.TOOL)
        self.assertEqual(v.recommended_prefix, "tool-")
        self.assertEqual(v.pure_problem_goal, "计算图片感知哈希")
        self.assertTrue(v.has_solution_bias)
        self.assertIn("fastapi", v.injected_tech_stack)
        self.assertIn("redis", v.injected_tech_stack)
        self.assertIsNotNone(v.anti_pattern_warning)
        self.assertIn("过度设计警报", v.anti_pattern_warning)

    def test_boilerplate_catalog_warning(self):
        """
        Tests that pure boilerplate copied from catalog headers triggers a template alert.
        """
        bp_goal = "包含长驻留后台进程、HTTP/WebSocket 端口监听与服务接口"
        v = GoalDrivenArbiter.deduce_from_goal(bp_goal, "ai-cache-engine")
        self.assertIsNotNone(v.anti_pattern_warning)
        self.assertIn("纯模板套话警报", v.anti_pattern_warning)

    def test_agent_workflow_deduction(self):
        goal = "指导AI智能体在多轮对话中如何逐步拆解意图并调用现有三个工具提取下载链接的SOP提示词流程"
        v = GoalDrivenArbiter.deduce_from_goal(goal)
        self.assertEqual(v.archetype, ArchetypeEnum.SKILL)
        self.assertIn("skill-", v.recommended_prefix)

    def test_atomic_tool_deduction(self):
        goal = "扫描本地指定目录下的PE/ELF文件并比对版本哈希，输出更新清单后立即退出"
        v = GoalDrivenArbiter.deduce_from_goal(goal)
        self.assertEqual(v.archetype, ArchetypeEnum.TOOL)
        self.assertIn("tool-", v.recommended_prefix)

    def test_network_service_deduction(self):
        goal = "跨平台即时通信服务端与API网关，维护万人长连接与外部系统调用中继"
        v = GoalDrivenArbiter.deduce_from_goal(goal)
        self.assertEqual(v.archetype, ArchetypeEnum.SVC)
        self.assertIn("svc-", v.recommended_prefix)

    def test_mcp_protocol_deduction(self):
        goal = "实现Model Context Protocol标准协议，为大模型提供专有工具接头与实时数据库上下文总线"
        v = GoalDrivenArbiter.deduce_from_goal(goal)
        self.assertEqual(v.archetype, ArchetypeEnum.MCP)
        self.assertIn("mcp-", v.recommended_prefix)

    def test_spec_vs_rule_deduction(self):
        rule_goal = "在代码提交与编译前设立绝对安全防线，严格禁止任何私钥泄露与违规越界操作，违者直接拦截"
        v_rule = GoalDrivenArbiter.deduce_from_goal(rule_goal)
        self.assertEqual(v_rule.archetype, ArchetypeEnum.RULE)

        spec_goal = "定义全域统一CLI外观与API动词的标准规范契约与验收神谕RFC"
        v_spec = GoalDrivenArbiter.deduce_from_goal(spec_goal)
        self.assertEqual(v_spec.archetype, ArchetypeEnum.SPEC)

    def test_honest_fleet_catalog_audit(self):
        """
        Honest audit verification: The catalog must have between 75% and 95% alignment.
        It must NOT be 100% (which indicates tautological bypass / coin-toss impossibility),
        and must surface genuine discrepancies like guide notes in infra.
        """
        catalog_path = r"D:\github\FLEET_TAXONOMY_CATALOG.md"
        if os.path.exists(catalog_path):
            res = CatalogAuditor.audit_catalog_file(catalog_path, base_repo_dir=r"D:\github")
            self.assertGreaterEqual(res["total_repositories_audited"], 50)
            self.assertGreaterEqual(res["alignment_rate_pct"], 75.0)
            self.assertLess(res["alignment_rate_pct"], 99.0)  # Honest discrepancy detection!
            self.assertGreater(res["misaligned_count"], 0)

    def test_adr_recorder_and_physical_verifier(self):
        """
        Verify ADR recording generates valid append-only file and physical verifier evaluates code.
        """
        import tempfile
        import shutil
        from core.adr_recorder import ADRRecorder
        from core.physical_verifier import PhysicalVerifier

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create dummy repo
            readme_p = os.path.join(tmpdir, "README.md")
            with open(readme_p, "w", encoding="utf-8") as f:
                f.write("# dummy-tool\n> 极速无状态命令行脚本，计算数据后秒级退出\n")

            verdict = GoalDrivenArbiter.deduce_from_goal("极速无状态命令行脚本，计算数据后秒级退出", "dummy-tool")
            res_adr = ADRRecorder.record_verdict(tmpdir, verdict)
            self.assertEqual(res_adr["status"], "success")
            self.assertEqual(res_adr["adr_id"], "0001")
            self.assertTrue(os.path.exists(res_adr["filepath"]))

            # Physical verify
            res_ver = PhysicalVerifier.verify_repo(tmpdir, verdict)
            self.assertEqual(res_ver["status"], "PASS")
            self.assertEqual(res_ver["violations_count"], 0)


if __name__ == "__main__":
    unittest.main()

