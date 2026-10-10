"""Apex_CapitalMatrix package.

Sovereign NVIDIA VC Alliance Diligence & Enterprise Connect Air-Gapped PoC Operating System.
Zero external dependencies (pure Python 3.9+ standard library only).
"""

__version__ = "1.0.0"
__author__ = "Ahmed Hassan"
__license__ = "Apache-2.0"

from apex_capitalmatrix.orchestrator import ApexCapitalMatrixOrchestrator
from apex_capitalmatrix.core.primitives import (
    AirGapEnclaveStatus,
    AtlasFinOpsAudit,
    CapitalConnectDiligencePacket,
    EnterpriseConnectPoCCertificate,
    EuAiActVerdict,
    GpuArchitecture,
    HardwareProfile,
    MFUMetrics,
    PanAsiaComplianceVerdict,
    PoCApprovalVerdict,
    RiskClassification,
    TargetRegion,
)

__all__ = [
    "__version__",
    "ApexCapitalMatrixOrchestrator",
    "AirGapEnclaveStatus",
    "AtlasFinOpsAudit",
    "CapitalConnectDiligencePacket",
    "EnterpriseConnectPoCCertificate",
    "EuAiActVerdict",
    "GpuArchitecture",
    "HardwareProfile",
    "MFUMetrics",
    "PanAsiaComplianceVerdict",
    "PoCApprovalVerdict",
    "RiskClassification",
    "TargetRegion",
]
