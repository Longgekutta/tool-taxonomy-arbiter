#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_arbiter.py: Rigorous regression and determinism unit tests for GoalDrivenArbiter.
"""
import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.goal_arbiter import GoalDrivenArbiter, ArchetypeEnum
from core.catalog_auditor import CatalogAuditor


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
        goal = "在后台常驻运行并监听8080端口，接收客户端并发HTTP与WebSocket请求并转发的API网关微服务"
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

    def test_fleet_catalog_goal_deduction(self):
        catalog_path = r"D:\github\FLEET_TAXONOMY_CATALOG.md"
        if os.path.exists(catalog_path):
            res = CatalogAuditor.audit_catalog_file(catalog_path, base_repo_dir=r"D:\github")
            self.assertGreaterEqual(res["total_repositories_audited"], 50)
            self.assertGreaterEqual(res["alignment_rate_pct"], 85.0)


if __name__ == "__main__":
    unittest.main()
