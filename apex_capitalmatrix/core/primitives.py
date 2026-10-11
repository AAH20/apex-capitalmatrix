"""Foundational primitives and data contracts for Apex_CapitalMatrix.

Sovereign NVIDIA VC Alliance Diligence & Enterprise Connect Air-Gapped PoC Operating System.
Zero external dependencies (pure Python 3.9+ standard library only).
"""

from __future__ import annotations

import enum
import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


class TargetRegion(str, enum.Enum):
    US_CAPITAL_CONNECT = "US_CAPITAL_CONNECT"
    EU_CAPITAL_CONNECT = "EU_CAPITAL_CONNECT"
    ASIA_ENTERPRISE_CONNECT = "ASIA_ENTERPRISE_CONNECT"
    GLOBAL_OMNI = "GLOBAL_OMNI"


class GpuArchitecture(str, enum.Enum):
    GB200_NVL72 = "GB200_NVL72"
    H100_SXM5 = "H100_SXM5"
    H200_SXM5 = "H200_SXM5"
    L40S = "L40S"
    A100_SXM4 = "A100_SXM4"


class RiskClassification(str, enum.Enum):
    MINIMAL_RISK = "MINIMAL_RISK"
    SPECIFIC_TRANSPARENCY = "SPECIFIC_TRANSPARENCY"
    HIGH_RISK = "HIGH_RISK"
    PROHIBITED = "PROHIBITED"


class PoCApprovalVerdict(str, enum.Enum):
    GREENLIGHT_48H = "GREENLIGHT_48H"
    CONDITIONAL_REVIEW = "CONDITIONAL_REVIEW"
    REJECTED_EGRESS_RISK = "REJECTED_EGRESS_RISK"


@dataclass(frozen=True)
class HardwareProfile:
    architecture: GpuArchitecture
    chip_count: int
    theoretical_fp8_tflops_per_chip: float
    memory_bandwidth_gbps_per_chip: float
    power_watts_per_chip: float
    lease_cost_usd_per_hour_per_chip: float

    @property
    def total_theoretical_tflops(self) -> float:
        return self.chip_count * self.theoretical_fp8_tflops_per_chip

    @property
    def total_lease_cost_hourly(self) -> float:
        return self.chip_count * self.lease_cost_usd_per_hour_per_chip


@dataclass
class MFUMetrics:
    achieved_tflops: float
    theoretical_tflops: float
    mfu_percentage: float
    tokens_per_second: float
    tokens_per_dollar: float
    kv_cache_hit_rate: float
    memory_bandwidth_utilization_pct: float
    wrapper_suspicion_score: float  # 0.0 (Pure Deep Tech) to 1.0 (API Wrapper)
    is_deep_tech_verified: bool
    simulated: bool = False  # True when figures derive from a synthetic profile, not a GPU measurement


@dataclass
class AtlasFinOpsAudit:
    reported_arr_usd: float
    gaap_asc_606_reconciled_arr_usd: float
    services_misclassification_usd: float
    unabsorbed_gpu_lease_drag_usd: float
    reported_ebitda_usd: float
    adjusted_ebitda_usd: float
    ebitda_haircut_pct: float
    compute_roic: float  # Return on Invested Capital per Compute Dollar
    reps_warranties_escrow_holdback_usd: float


@dataclass
class EuAiActVerdict:
    risk_classification: RiskClassification
    article_50_transparency_pass: bool
    article_53_copyright_pass: bool
    copyleft_contamination_found: bool
    contaminated_licenses: List[str] = field(default_factory=list)
    carbon_intensity_gco2_per_kwh: float = 38.5
    audit_passed: bool = True


@dataclass
class AirGapEnclaveStatus:
    zero_egress_verified: bool
    pii_token_leakage_detected: bool
    outbound_socket_blocks: int
    credential_isolation_verified: bool
    synthetic_twin_active: bool
    sovereign_vpc_digest: str


@dataclass
class PanAsiaComplianceVerdict:
    japan_appi_score: float      # Japan APPI / METI (0.0 to 1.0)
    singapore_mas_score: float   # Singapore MAS TRM / PDPC
    saudi_sdaia_score: float     # Saudi Arabia / GCC SDAIA NDMO
    korea_pipa_score: float      # South Korea PIPA
    india_dpdp_score: float      # India DPDP Act
    jurisdictions_passed: int
    all_passed: bool


@dataclass
class CapitalConnectDiligencePacket:
    packet_id: str
    timestamp: float
    startup_name: str
    target_region: TargetRegion
    gpu_architecture: str
    mfu_metrics: MFUMetrics
    atlas_finops: AtlasFinOpsAudit
    eu_compliance: EuAiActVerdict
    vc_readiness_score: float  # 0.0 to 100.0
    action_ledger_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def compute_hash(self) -> str:
        payload = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass
class EnterpriseConnectPoCCertificate:
    certificate_id: str
    timestamp: float
    startup_name: str
    enterprise_client: str
    airgap_status: AirGapEnclaveStatus
    pan_asia_compliance: PanAsiaComplianceVerdict
    flowforge_simulation_passed: bool
    reps_warranties_escrow_holdback_usd: float
    approval_verdict: PoCApprovalVerdict
    audit_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def compute_hash(self) -> str:
        payload = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
