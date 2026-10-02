#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/adr_recorder.py: 架构决策记录 (ADR) 权威不可变状态机写入器
对标 npryce/adr-tools 规范，将形态仲裁与选型结论固化为 Append-Only DAG 账本。
"""
import os
import re
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from core.goal_arbiter import GoalEvaluationVerdict


class ADRRecorder:
    """
    负责在目标仓库的 docs/adr 目录下创建或追加单调递增的架构决策记录。
    确保系统架构决策有据可查、历史不可篡改。
    """

    @classmethod
    def record_verdict(cls, repo_path: str, verdict: GoalEvaluationVerdict) -> Dict[str, Any]:
        repo_dir = Path(repo_path).resolve()
        if not repo_dir.exists():
            raise FileNotFoundError(f"Repository directory does not exist: {repo_path}")

        adr_dir = repo_dir / "docs" / "adr"
        adr_dir.mkdir(parents=True, exist_ok=True)

        # 1. 扫描现有 ADR，计算单调递增编号
        existing_adrs = sorted(adr_dir.glob("[0-9][0-9][0-9][0-9]-*.md"))
        next_id = 1
        if existing_adrs:
            last_file = existing_adrs[-1].name
            match = re.match(r"^(\d{4})-", last_file)
            if match:
                next_id = int(match.group(1)) + 1

        id_str = f"{next_id:04d}"
        slug = re.sub(r"[^\w\-]+", "-", verdict.suggested_name.lower()).strip("-")
        filename = f"{id_str}-architectural-archetype-{slug}.md"
        target_file = adr_dir / filename

        today_str = datetime.date.today().isoformat()

        content = f"""# {id_str}. 架构形态仲裁决策：{verdict.suggested_name}

* **决策状态**：Accepted (已批准)
* **决策日期**：{today_str}
* **仲裁法典**：`tool-taxonomy-arbiter` (第一性原理确定性推导)
* **法定形态**：`{verdict.archetype.value.upper()}` (前缀契约: `{verdict.recommended_prefix}`)
* **置信度**：{verdict.confidence:.2%}

---

## 一、 原始诉求与核心问题域

* **原始输入陈述**：
  > {verdict.target_goal}

* **脱敏后纯粹问题域目标**：
  > {verdict.pure_problem_goal}

{f"⚠️ **识别并剥离解域私货**：技术栈 {verdict.injected_tech_stack} | 架构声明 {verdict.injected_architecture_claims}" if verdict.has_solution_bias else "✓ 意图验真：纯粹问题域目标，无解域实现私货污染。"}

---

## 二、 架构形态判定与最小必要理由

* **裁决形态**：**【 {verdict.archetype.value.upper()} 】**
* **最小必要性论证**：
  {verdict.minimal_viable_rationale}

{f"⚠️ **过度设计与防腐警报**：{verdict.anti_pattern_warning}" if verdict.anti_pattern_warning else ""}

---

## 三、 第一性原理推导逻辑链 (Deduction Chain)

{chr(10).join(f"{i}. {step}" for i, step in enumerate(verdict.deduction_chain, 1))}

---

## 四、 架构后果与不变量契约 (Consequences & Invariants)

1. **正向收益**：彻底杜绝架构形态漂移，以最小运行时代价实现全部功能。
2. **负向红线**：严禁在后续迭代中私自引入不属于本形态的重型冗余。
3. **不可变状态说明**：本 ADR 遵循 Append-only 线性化法则，未来若架构演进，必须通过新增 ADR 显式声明 `Supersedes {id_str}`，禁止直接篡改本文件。
"""

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "status": "success",
            "adr_id": id_str,
            "filename": filename,
            "filepath": str(target_file),
            "verdict": verdict.to_dict()
        }
