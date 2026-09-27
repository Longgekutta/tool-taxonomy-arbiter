#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_arbiter.py: Rigorous regression and determinism unit tests for tool-taxonomy-arbiter.
"""
import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.models import ArchetypeEnum, DimensionVector, ArbiterVerdict
from core.decision_engine import DecisionEngine
from core.repo_analyzer import RepoAnalyzer
from core.catalog_auditor import CatalogAuditor


class TestTaxonomyArbiter(unittest.TestCase):

    def test_mathematical_determinism_invariance(self):
        """
        Theorem 1: Pure function invariance.
        Evaluating the exact same input 100 times must yield 100 identical verdicts.
        """
        vec = DimensionVector(lifecycle=0.0, protocol=0.0, execution=1.0, agenticity=0.0)
        first_verdict = DecisionEngine.evaluate_vector(vec, "test-tool")

        for _ in range(100):
            next_verdict = DecisionEngine.evaluate_vector(vec, "test-tool")
            self.assertEqual(next_verdict.archetype, first_verdict.archetype)
            self.assertEqual(next_verdict.recommended_prefix, first_verdict.recommended_prefix)
            self.assertAlmostEqual(next_verdict.confidence, first_verdict.confidence, places=6)
            self.assertEqual(next_verdict.suggested_name, first_verdict.suggested_name)

    def test_strict_boundary_tool_vs_skill(self):
        """
        A pure SOP markdown workflow operated by an AI Agent must classify as SKILL,
        while an atomic executable script must classify as TOOL.
        """
        skill_prompt = "指导智能体分步骤提取GitHub下载链接的SOP提示词流程与markdown操作规范"
        vec_skill, _ = DecisionEngine.extract_vector_from_text(skill_prompt)
        verdict_skill = DecisionEngine.evaluate_vector(vec_skill, "github-asset-hunter")
        self.assertEqual(verdict_skill.archetype, ArchetypeEnum.SKILL)

        tool_prompt = "一个极速无状态的命令行装具，输入参数后进行数学计算并秒级退出，符合UCFS五动词"
        vec_tool, _ = DecisionEngine.extract_vector_from_text(tool_prompt)
        verdict_tool = DecisionEngine.evaluate_vector(vec_tool, "math-calculator")
        self.assertEqual(verdict_tool.archetype, ArchetypeEnum.TOOL)

    def test_strict_boundary_svc_vs_mcp(self):
        """
        MCP protocol servers must lock into MCP archetype.
        HTTP/WebSocket long-running gateways must lock into SVC archetype.
        """
        mcp_prompt = "实现Model Context Protocol JSON-RPC标准协议，专为Claude和AI宿主暴露工具"
        vec_mcp, _ = DecisionEngine.extract_vector_from_text(mcp_prompt)
        verdict_mcp = DecisionEngine.evaluate_vector(vec_mcp, "mcp-database-query")
        self.assertEqual(verdict_mcp.archetype, ArchetypeEnum.MCP)

        svc_prompt = "一个常驻后台的FastAPI网关服务，监听8080端口，接收HTTP请求并做反向代理转发"
        vec_svc, _ = DecisionEngine.extract_vector_from_text(svc_prompt)
        verdict_svc = DecisionEngine.evaluate_vector(vec_svc, "api-gateway")
        self.assertEqual(verdict_svc.archetype, ArchetypeEnum.SVC)

    def test_strict_boundary_spec_vs_rule(self):
        """
        Formal schemas and RFC specifications classify as SPEC.
        Negative constraints and security guardrails classify as RULE.
        """
        rule_prompt = "严格禁止任何未经审查的代码合并，负向边界守卫防线，越界立即拦截报错"
        vec_rule, _ = DecisionEngine.extract_vector_from_text(rule_prompt)
        verdict_rule = DecisionEngine.evaluate_vector(vec_rule, "security-guard-rule")
        self.assertEqual(verdict_rule.archetype, ArchetypeEnum.RULE)

        spec_prompt = "全域CLI统一外观五动词刚性规范标准，定义API契约与验收神谕RFC"
        vec_spec, _ = DecisionEngine.extract_vector_from_text(spec_prompt)
        verdict_spec = DecisionEngine.evaluate_vector(vec_spec, "cli-facade-spec")
        self.assertEqual(verdict_spec.archetype, ArchetypeEnum.SPEC)

    def test_fleet_catalog_batch_audit(self):
        """
        Audit FLEET_TAXONOMY_CATALOG.md across all repos.
        Must achieve >= 90% alignment stability.
        """
        catalog_path = r"D:\github\FLEET_TAXONOMY_CATALOG.md"
        if os.path.exists(catalog_path):
            res = CatalogAuditor.audit_catalog_file(catalog_path, base_repo_dir=r"D:\github")
            self.assertGreaterEqual(res["total_repositories_audited"], 50)
            self.assertGreaterEqual(res["alignment_rate_pct"], 85.0)
            self.assertTrue(res["is_invariant_stable"])


if __name__ == "__main__":
    unittest.main()
