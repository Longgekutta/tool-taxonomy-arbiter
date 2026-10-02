#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/repo_resolver.py: 通用仓库解析与定位适配器 (Universal Repository Resolver)
支持对本地目录、远程 Git/GitHub URL 或短名 Slug 的统一无感解析。
"""

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


class RepoResolver:
    """
    通用工业母机仓库定位解析器。
    将任何本地路径、远程 Git 地址或仓库短名解析为本地有效且可进行物理静态分析的绝对路径。
    """

    CACHE_DIR = Path.home() / ".cache" / "industrial_meta_tools" / "repos"

    @classmethod
    def resolve(cls, target_input: str, search_roots: Optional[list] = None) -> Tuple[str, Dict[str, Any]]:
        raw = target_input.strip()
        metadata = {
            "input": raw,
            "type": "UNKNOWN",
            "is_temporary": False,
            "resolved_path": ""
        }

        if not raw:
            raise ValueError("Repository target input cannot be empty.")

        # 1. 直接本地路径
        local_p = Path(raw).expanduser().resolve()
        if local_p.exists() and local_p.is_dir():
            metadata["type"] = "LOCAL_DIR"
            metadata["resolved_path"] = str(local_p)
            return str(local_p), metadata

        # 2. 候选搜索目录
        candidate_roots = search_roots or [
            Path(r"D:\github"),
            Path.cwd(),
            Path.cwd().parent
        ]
        for root in candidate_roots:
            p = (Path(root) / raw).resolve()
            if p.exists() and p.is_dir():
                metadata["type"] = "LOCAL_NAMED_DIR"
                metadata["resolved_path"] = str(p)
                return str(p), metadata

        # 3. 远程 Git URL
        if raw.startswith("http://") or raw.startswith("https://") or raw.startswith("git@") or raw.endswith(".git"):
            metadata["type"] = "REMOTE_GIT_URL"
            cached_path = cls._clone_or_update_git_repo(raw)
            metadata["resolved_path"] = str(cached_path)
            return str(cached_path), metadata

        # 4. GitHub Slug (owner/repo)
        if re.match(r"^[\w\-\.]+/[\w\-\.]+$", raw):
            github_url = f"https://github.com/{raw}.git"
            metadata["type"] = "GITHUB_SLUG"
            cached_path = cls._clone_or_update_git_repo(github_url)
            metadata["resolved_path"] = str(cached_path)
            return str(cached_path), metadata

        raise FileNotFoundError(f"Cannot resolve target repository: '{target_input}'")

    @classmethod
    def _clone_or_update_git_repo(cls, git_url: str) -> Path:
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = re.sub(r"[^\w\-]", "_", git_url.replace("https://", "").replace("http://", "").replace("git@", "").replace(".git", ""))
        target_dir = cls.CACHE_DIR / safe_name

        if target_dir.exists() and (target_dir / ".git").exists():
            try:
                subprocess.run(["git", "pull", "--depth", "1"], cwd=target_dir, capture_output=True, timeout=15)
            except Exception:
                pass
            return target_dir

        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)

        cmd = ["git", "clone", "--depth", "1", git_url, str(target_dir)]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to clone remote repository {git_url}: {res.stderr}")

        return target_dir
