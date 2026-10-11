"""Self-contained Code Review Adapter (no Alibaba/AnyAgent dependency).

Employs static AST pattern matching to perform automated pre-flight security
and architectural reviews, verifying that code is free from exposed credentials,
eval/exec risks, and unsafe deserialization before VC or enterprise auditing.
Zero external dependencies (pure Python 3.9+ standard library only).
"""

from __future__ import annotations

import ast
import re
from typing import Any, Dict, List, Optional


class AlibabaCodeReviewAdapter:
    """Pre-flight code reviewer evaluating security hygiene and architectural quality."""

    DANGEROUS_CALLS = {"eval", "exec", "pickle.loads", "os.system", "subprocess.Popen"}

    def review_python_source(self, source_code: str, file_path: str = "main.py") -> Dict[str, Any]:
        """Parses Python AST and reports architectural findings."""
        findings: List[Dict[str, Any]] = []

        try:
            tree = ast.parse(source_code, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    func_name = ""
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                    elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                        func_name = f"{node.func.value.id}.{node.func.attr}"

                    if func_name in self.DANGEROUS_CALLS:
                        findings.append({
                            "severity": "HIGH",
                            "rule": "UNSAFE_DYNAMIC_EXECUTION",
                            "line": getattr(node, "lineno", 1),
                            "detail": f"Prohibited dynamic call detected: {func_name}",
                        })
        except SyntaxError as e:
            findings.append({
                "severity": "CRITICAL",
                "rule": "SYNTAX_ERROR",
                "line": e.lineno or 1,
                "detail": str(e),
            })

        # Regex scan for exposed hardcoded tokens
        token_pattern = re.compile(r"(ghp_[0-9a-zA-Z]{36}|sk-[0-9a-zA-Z]{32,}|AKIA[0-9A-Z]{16})")
        for match in token_pattern.finditer(source_code):
            findings.append({
                "severity": "CRITICAL",
                "rule": "HARDCODED_SECRET_LEAK",
                "line": source_code[:match.start()].count("\n") + 1,
                "detail": f"Hardcoded credential token pattern found: {match.group(0)[:6]}***",
            })

        critical_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
        high_count = sum(1 for f in findings if f["severity"] == "HIGH")
        review_passed = critical_count == 0 and high_count == 0

        return {
            "file_path": file_path,
            "total_findings": len(findings),
            "critical_count": critical_count,
            "high_count": high_count,
            "review_passed": review_passed,
            "findings": findings,
            "quality_grade": "A+" if review_passed else "FLAGGED",
        }
