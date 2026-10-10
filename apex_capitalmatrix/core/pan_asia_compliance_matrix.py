"""Pan-Asia Sovereign Regulatory Compliance Matrix.

Evaluates AI agent deployments across 5 major Asian jurisdictions:
  1. Japan: APPI & METI AI Governance Guidelines
  2. Singapore: MAS TRM Guidelines & IMDA Model AI Governance Framework (FEAT)
  3. Saudi Arabia / GCC: SDAIA NDMO & UAE Federal Data Protection Law
  4. South Korea: PIPA & National AI Ethics Standards
  5. India: Digital Personal Data Protection (DPDP) Act 2023
Zero external dependencies (pure Python 3.9+ standard library only).
"""

from __future__ import annotations

from typing import Dict, List, Optional
from apex_capitalmatrix.core.primitives import PanAsiaComplianceVerdict


class PanAsiaComplianceMatrix:
    """Evaluates regulatory posture across Asian sovereign jurisdictions."""

    def evaluate_compliance(
        self,
        has_local_data_residency: bool = True,
        has_model_explainability_audit: bool = True,
        has_consent_management: bool = True,
        has_air_gapped_encryption_at_rest: bool = True,
        has_audit_logging_sha256: bool = True,
        is_cross_border_egress_prevented: bool = True,
    ) -> PanAsiaComplianceVerdict:
        """Calculates jurisdictional compliance scores (0.0 to 1.0)."""

        # 1. Japan (APPI & METI)
        # Emphasizes cross-border transfer control, consent, and explainability
        japan_score = 0.0
        if is_cross_border_egress_prevented:
            japan_score += 0.35
        if has_model_explainability_audit:
            japan_score += 0.35
        if has_consent_management:
            japan_score += 0.30

        # 2. Singapore (MAS TRM & IMDA FEAT)
        # Emphasizes cyber risk management, auditability, and fairness/transparency
        singapore_score = 0.0
        if has_air_gapped_encryption_at_rest:
            singapore_score += 0.30
        if has_audit_logging_sha256:
            singapore_score += 0.35
        if has_model_explainability_audit:
            singapore_score += 0.35

        # 3. Saudi Arabia / GCC (SDAIA & UAE PDP)
        # Strictly requires sovereign data residency and zero external egress
        saudi_score = 0.0
        if has_local_data_residency:
            saudi_score += 0.45
        if is_cross_border_egress_prevented:
            saudi_score += 0.35
        if has_air_gapped_encryption_at_rest:
            saudi_score += 0.20

        # 4. South Korea (PIPA)
        # Focuses on consent, de-identification, and security safeguards
        korea_score = 0.0
        if has_consent_management:
            korea_score += 0.35
        if has_air_gapped_encryption_at_rest:
            korea_score += 0.35
        if is_cross_border_egress_prevented:
            korea_score += 0.30

        # 5. India (DPDP Act 2023)
        # Mandates consent mechanisms, audit logs, and data security
        india_score = 0.0
        if has_consent_management:
            india_score += 0.40
        if has_audit_logging_sha256:
            india_score += 0.35
        if has_local_data_residency:
            india_score += 0.25

        scores = [japan_score, singapore_score, saudi_score, korea_score, india_score]
        passed_count = sum(1 for s in scores if s >= 0.80)
        all_passed = passed_count == 5

        return PanAsiaComplianceVerdict(
            japan_appi_score=round(japan_score, 2),
            singapore_mas_score=round(singapore_score, 2),
            saudi_sdaia_score=round(saudi_score, 2),
            korea_pipa_score=round(korea_score, 2),
            india_dpdp_score=round(india_score, 2),
            jurisdictions_passed=passed_count,
            all_passed=all_passed,
        )
