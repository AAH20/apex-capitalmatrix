"""FinOps Atlas Actuary & GPU Lease Liability Auditor.

Integrates the GAAP ASC 606 revenue audit models from 'project-atlas-due-diligence'
and the compute lease liability models from 'tech-balance-sheet' & 'ma_vdr_diligence_os'.
Evaluates True Token-per-Dollar, unabsorbed GPU lease drag, and EBITDA valuation haircuts.
Zero external dependencies (pure Python 3.9+ standard library only).
"""

from __future__ import annotations

from typing import Dict, Optional
from apex_capitalmatrix.core.primitives import AtlasFinOpsAudit


class FinOpsAtlasActuary:
    """Actuarial due diligence engine auditing ARR, GPU lease drag, and EBITDA haircuts."""

    def __init__(self, default_ev_multiple: float = 8.5):
        self.default_ev_multiple = default_ev_multiple

    def audit_target_finances(
        self,
        reported_arr_usd: float = 50_000_000.0,
        services_misclassified_pct: float = 0.18,  # 18% of ARR is actually one-off services
        committed_gpu_instances: int = 128,         # Contracted H100 nodes (8 GPUs each = 1024 chips)
        hourly_gpu_rate_usd: float = 3.25,
        target_workload_absorption_pct: float = 0.42,  # Only 42% of reserved capacity is absorbed
        reported_ebitda_usd: float = 12_500_000.0,
        unhedged_cyber_debt_usd: float = 1_250_000.0,
    ) -> AtlasFinOpsAudit:
        """Computes GAAP ASC 606 adjustments, unabsorbed GPU lease drag, and EBITDA haircuts.
        
        Mathematical Formulation:
          1. ASC 606 Services Drag = reported_arr_usd * services_misclassified_pct
          2. Reconciled ARR = reported_arr_usd - services_drag
          3. Total Annual GPU Lease Cost = committed_gpu_instances * 8 * hourly_rate * 8760
          4. Unabsorbed GPU Drag = Total Annual Lease Cost * (1.0 - absorption_pct)
          5. Adjusted EBITDA = reported_ebitda - services_drag - unabsorbed_gpu_drag
          6. EBITDA Haircut % = (reported_ebitda - adjusted_ebitda) / reported_ebitda * 100
          7. Compute ROIC = Reconciled ARR / Total Annual GPU Lease Cost
          8. Reps & Warranties Escrow = max(10% EV haircut, unhedged_cyber_debt + unabsorbed_gpu_drag * 0.25)
        """
        # 1. GAAP ASC 606 Reconciled Revenue
        services_misclass_usd = reported_arr_usd * services_misclassified_pct
        reconciled_arr_usd = max(0.0, reported_arr_usd - services_misclass_usd)

        # 2. Unabsorbed GPU Lease Commitments
        total_chips = committed_gpu_instances * 8
        annual_hours = 8760.0
        total_gpu_lease_annual = total_chips * hourly_gpu_rate_usd * annual_hours
        unabsorbed_pct = max(0.0, 1.0 - target_workload_absorption_pct)
        unabsorbed_gpu_drag_usd = total_gpu_lease_annual * unabsorbed_pct

        # 3. Adjusted EBITDA & Haircut
        adjusted_ebitda_usd = reported_ebitda_usd - (services_misclass_usd * 0.40) - unabsorbed_gpu_drag_usd
        if reported_ebitda_usd > 0:
            haircut_pct = max(0.0, ((reported_ebitda_usd - adjusted_ebitda_usd) / reported_ebitda_usd) * 100.0)
        else:
            haircut_pct = 100.0

        # 4. Compute ROIC
        compute_roic = reconciled_arr_usd / max(1.0, total_gpu_lease_annual)

        # 5. Reps & Warranties Escrow Holdback
        ev_haircut_impact = (reported_arr_usd - reconciled_arr_usd) * self.default_ev_multiple
        escrow_holdback_usd = max(
            unhedged_cyber_debt_usd + (unabsorbed_gpu_drag_usd * 0.20),
            ev_haircut_impact * 0.12,
        )

        return AtlasFinOpsAudit(
            reported_arr_usd=round(reported_arr_usd, 2),
            gaap_asc_606_reconciled_arr_usd=round(reconciled_arr_usd, 2),
            services_misclassification_usd=round(services_misclass_usd, 2),
            unabsorbed_gpu_lease_drag_usd=round(unabsorbed_gpu_drag_usd, 2),
            reported_ebitda_usd=round(reported_ebitda_usd, 2),
            adjusted_ebitda_usd=round(adjusted_ebitda_usd, 2),
            ebitda_haircut_pct=round(haircut_pct, 2),
            compute_roic=round(compute_roic, 3),
            reps_warranties_escrow_holdback_usd=round(escrow_holdback_usd, 2),
        )
