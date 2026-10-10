"""Comprehensive unit and integration test suite for Apex_CapitalMatrix.

Verifies all core algorithms, adapters, orchestrator workflows, and CLI commands.
100% deterministic, zero external dependencies (pure Python standard library).
"""

import io
import json
import unittest
from contextlib import redirect_stdout

from apex_capitalmatrix.core.primitives import (
    GpuArchitecture,
    PoCApprovalVerdict,
    RiskClassification,
    TargetRegion,
)
from apex_capitalmatrix.core.hardware_saturation_verifier import HardwareSaturationVerifier
from apex_capitalmatrix.core.finops_atlas_actuary import FinOpsAtlasActuary
from apex_capitalmatrix.core.eu_ai_act_scanner import EuAiActScanner
from apex_capitalmatrix.core.airgap_sovereign_proxy import SovereignAirGapProxy
from apex_capitalmatrix.core.pan_asia_compliance_matrix import PanAsiaComplianceMatrix
from apex_capitalmatrix.adapters.clef_adapter import ClefEdgeReplicator
from apex_capitalmatrix.adapters.paperclip_adapter import PaperclipBudgetGovernor
from apex_capitalmatrix.adapters.control_plane_adapter import ControlPlaneFinOpsAdapter
from apex_capitalmatrix.adapters.integration_platform_adapter import FlowForgeSimulationReplayAdapter
from apex_capitalmatrix.adapters.aerial_6g_connector import Aerial6GConnector
from apex_capitalmatrix.adapters.alibaba_code_review_adapter import AlibabaCodeReviewAdapter
from apex_capitalmatrix.orchestrator import ApexCapitalMatrixOrchestrator
from apex_capitalmatrix.cli import main


class TestApexCapitalMatrix(unittest.TestCase):

    def setUp(self):
        self.orchestrator = ApexCapitalMatrixOrchestrator(default_budget_usd=10.00)

    # 1. Hardware Saturation & MFU Verifier Tests
    def test_hardware_saturation_verifier(self):
        verifier = HardwareSaturationVerifier()
        metrics = verifier.verify_workload(
            arch=GpuArchitecture.H100_SXM5,
            model_params_billions=70.0,
            batch_size=32,
            tokens_per_second=2400.0,
            kv_cache_hit_rate=0.88,
            reported_http_latency_jitter_ms=2.5,
        )
        self.assertGreater(metrics.achieved_tflops, 100.0)
        self.assertGreater(metrics.mfu_percentage, 0.0)
        self.assertLess(metrics.wrapper_suspicion_score, 0.50)
        self.assertTrue(metrics.is_deep_tech_verified)

    def test_synthetic_benchmark_execution(self):
        verifier = HardwareSaturationVerifier()
        metrics = verifier.run_synthetic_benchmark(arch=GpuArchitecture.GB200_NVL72, iterations=5)
        self.assertGreater(metrics.tokens_per_dollar, 1000.0)
        self.assertGreater(metrics.memory_bandwidth_utilization_pct, 50.0)

    # 2. FinOps Atlas Actuary Tests
    def test_finops_atlas_actuary_revenue_reconciliation(self):
        actuary = FinOpsAtlasActuary(default_ev_multiple=8.0)
        audit = actuary.audit_target_finances(
            reported_arr_usd=100_000_000.0,
            services_misclassified_pct=0.20,
            committed_gpu_instances=64,
            hourly_gpu_rate_usd=3.25,
            target_workload_absorption_pct=0.80,
            reported_ebitda_usd=25_000_000.0,
            unhedged_cyber_debt_usd=1_000_000.0,
        )
        self.assertEqual(audit.services_misclassification_usd, 20_000_000.0)
        self.assertEqual(audit.gaap_asc_606_reconciled_arr_usd, 80_000_000.0)
        self.assertGreater(audit.ebitda_haircut_pct, 0.0)
        self.assertGreater(audit.compute_roic, 0.0)

    def test_finops_unabsorbed_gpu_lease_drag(self):
        actuary = FinOpsAtlasActuary()
        audit = actuary.audit_target_finances(
            reported_arr_usd=20_000_000.0,
            services_misclassified_pct=0.10,
            committed_gpu_instances=128,  # 1024 H100s
            hourly_gpu_rate_usd=3.25,
            target_workload_absorption_pct=0.25,  # 75% unabsorbed drag
            reported_ebitda_usd=5_000_000.0,
        )
        self.assertGreater(audit.unabsorbed_gpu_lease_drag_usd, 5_000_000.0)
        self.assertGreater(audit.ebitda_haircut_pct, 50.0)
        self.assertGreater(audit.reps_warranties_escrow_holdback_usd, 0.0)

    # 3. EU AI Act & IP Scanner Tests
    def test_eu_ai_act_clean_project(self):
        scanner = EuAiActScanner()
        verdict = scanner.scan_project(
            dependencies=["torch==2.5.1", "fastapi==0.115.0"],
            system_capabilities=["text_summarization"],
        )
        self.assertEqual(verdict.risk_classification, RiskClassification.MINIMAL_RISK)
        self.assertFalse(verdict.copyleft_contamination_found)
        self.assertTrue(verdict.audit_passed)

    def test_eu_ai_act_copyleft_and_prohibited_detection(self):
        scanner = EuAiActScanner()
        verdict = scanner.scan_project(
            dependencies=["some-lib-agpl-3.0", "torch==2.5.1"],
            system_capabilities=["social_scoring_citizen_risk"],
        )
        self.assertEqual(verdict.risk_classification, RiskClassification.PROHIBITED)
        self.assertTrue(verdict.copyleft_contamination_found)
        self.assertFalse(verdict.audit_passed)

    # 4. Sovereign Air-Gap Proxy Tests
    def test_airgap_proxy_pii_redaction(self):
        proxy = SovereignAirGapProxy()
        sample_text = "Customer email is ceo@enterprise.com with card 4111-2222-3333-4444 and key AKIAIOSFODNN7EXAMPLE."
        sanitized, blocked, violations = proxy.inspect_and_filter_payload(sample_text, target_destination="127.0.0.1")
        self.assertFalse(blocked)
        self.assertIn("[REDACTED_EMAIL_ADDRESS]", sanitized)
        self.assertIn("[REDACTED_CREDIT_CARD]", sanitized)
        self.assertIn("[REDACTED_AWS_OR_CLOUD_KEY]", sanitized)
        self.assertGreaterEqual(len(violations), 3)

    def test_airgap_proxy_unauthorized_egress_block(self):
        proxy = SovereignAirGapProxy()
        _, blocked, violations = proxy.inspect_and_filter_payload("test query", target_destination="api.openai.com")
        self.assertTrue(blocked)
        self.assertIn("UNAUTHORIZED_EXTERNAL_EGRESS_ATTEMPT", violations[0])
        status = proxy.get_enclave_status()
        self.assertGreaterEqual(status.outbound_socket_blocks, 1)

    # 5. Pan-Asia Compliance Matrix Tests
    def test_pan_asia_compliance_full_pass(self):
        matrix = PanAsiaComplianceMatrix()
        verdict = matrix.evaluate_compliance(
            has_local_data_residency=True,
            has_model_explainability_audit=True,
            has_consent_management=True,
            has_air_gapped_encryption_at_rest=True,
            has_audit_logging_sha256=True,
            is_cross_border_egress_prevented=True,
        )
        self.assertEqual(verdict.jurisdictions_passed, 5)
        self.assertTrue(verdict.all_passed)
        self.assertGreaterEqual(verdict.japan_appi_score, 0.80)
        self.assertGreaterEqual(verdict.singapore_mas_score, 0.80)
        self.assertGreaterEqual(verdict.saudi_sdaia_score, 0.80)

    # 6. Adapter Tests
    def test_clef_edge_consensus_replication(self):
        clef = ClefEdgeReplicator()
        record = clef.broadcast_diligence_packet(
            packet_id="pkt-100",
            packet_sha256="abc123sha",
            metadata={"status": "APPROVED"},
        )
        self.assertEqual(record["consensus_status"], "COMMITTED_SUB_100US")
        self.assertTrue(clef.verify_edge_consensus("pkt-100"))
        self.assertEqual(clef.get_ledger_size(), 1)

    def test_paperclip_budget_governor_deductions_and_exhaustion(self):
        governor = PaperclipBudgetGovernor(default_budget_usd=0.50)
        receipt = governor.charge_audit_step("TEST_STEP", 100_000.0, {"key": "val"})  # $0.10
        self.assertEqual(receipt["heartbeat_state"], "ACTIVE_HEALTHY")
        self.assertAlmostEqual(governor.get_remaining_budget(), 0.40, places=4)

        # Trigger exhaustion
        with self.assertRaises(RuntimeError):
            governor.charge_audit_step("EXCESS_STEP", 500_000.0, {})

    def test_control_plane_finops_accounting(self):
        adapter = ControlPlaneFinOpsAdapter(cluster_name="test-cluster")
        adapter.record_gpu_finops_allocation(
            node_pool="gpu-pool",
            gpu_count=8,
            gpu_model="H100_SXM5",
            allocated_hours=10.0,
            hourly_rate_usd=3.25,
        )
        summary = adapter.get_cluster_spend_summary()
        self.assertEqual(summary["cumulative_gpu_hours"], 80.0)
        self.assertEqual(summary["cumulative_spend_usd"], 260.0)

    def test_flowforge_simulation_replay_safety(self):
        flowforge = FlowForgeSimulationReplayAdapter()
        rec = flowforge.simulate_agent_action("POST_JOURNAL_ENTRY", "SAP_GL", {"amount": 5000})
        self.assertTrue(rec["rollback_guaranteed"])
        self.assertEqual(rec["production_impact"], "ZERO_MUTATION_DRY_RUN_ISOLATED")

    def test_aerial_6g_urllc_decision_sla(self):
        connector = Aerial6GConnector(max_sla_ms=5.0)
        connector.record_decision_event("INFERENCE_STEP_1", 2.1)
        connector.record_decision_event("INFERENCE_STEP_2", 3.4)
        summary = connector.get_urllc_summary()
        self.assertEqual(summary["status"], "URLLC_COMPLIANT")
        self.assertEqual(summary["compliance_rate_pct"], 100.0)

    def test_alibaba_code_review_adapter(self):
        reviewer = AlibabaCodeReviewAdapter()
        # Clean code
        clean_res = reviewer.review_python_source("def add(a, b):\n    return a + b\n")
        self.assertTrue(clean_res["review_passed"])
        self.assertEqual(clean_res["quality_grade"], "A+")

        # Dirty code (dangerous call)
        dirty_res = reviewer.review_python_source("eval('2 + 2')\n")
        self.assertFalse(dirty_res["review_passed"])
        self.assertEqual(dirty_res["findings"][0]["rule"], "UNSAFE_DYNAMIC_EXECUTION")

    # 7. Orchestrator End-to-End Tests
    def test_orchestrator_capital_connect_diligence(self):
        packet = self.orchestrator.run_capital_connect_diligence(
            startup_name="Apex Growth Systems LLC",
            target_region=TargetRegion.US_CAPITAL_CONNECT,
            gpu_arch=GpuArchitecture.H100_SXM5,
            reported_arr_usd=25_000_000.0,
            reported_ebitda_usd=6_000_000.0,
        )
        self.assertGreater(packet.vc_readiness_score, 50.0)
        self.assertGreater(packet.mfu_metrics.mfu_percentage, 0.0)
        self.assertIsNotNone(packet.action_ledger_sha256)
        self.assertTrue(self.orchestrator.clef_replicator.verify_edge_consensus(packet.packet_id))

    def test_orchestrator_enterprise_connect_poc(self):
        cert = self.orchestrator.run_enterprise_connect_poc(
            startup_name="Apex Growth Systems LLC",
            enterprise_client="Singtel Enterprise Asia",
        )
        self.assertEqual(cert.approval_verdict, PoCApprovalVerdict.GREENLIGHT_48H)
        self.assertTrue(cert.airgap_status.zero_egress_verified)
        self.assertTrue(cert.flowforge_simulation_passed)
        self.assertTrue(cert.pan_asia_compliance.all_passed)

    def test_orchestrator_markdown_report_generation(self):
        packet = self.orchestrator.run_capital_connect_diligence()
        poc = self.orchestrator.run_enterprise_connect_poc()
        report = self.orchestrator.generate_executive_markdown_report(packet, poc)
        self.assertIn("# CapitalMatrix Institutional Diligence & PoC Memo", report)
        self.assertIn("Hardware Saturation", report)
        self.assertIn("Atlas FinOps", report)
        self.assertIn("Enterprise Connect Air-Gapped PoC", report)

    # 8. CLI Tests
    def test_cli_subcommands(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ret_bench = main(["benchmark", "--iterations", "2"])
            self.assertEqual(ret_bench, 0)

            ret_audit = main(["audit-vc", "--startup", "Apex", "--arr", "10000000"])
            self.assertEqual(ret_audit, 0)

            ret_poc = main(["poc-verify", "--client", "NTT Communications"])
            self.assertEqual(ret_poc, 0)

            ret_finops = main(["finops"])
            self.assertEqual(ret_finops, 0)

            ret_report = main(["report"])
            self.assertEqual(ret_report, 0)


if __name__ == "__main__":
    unittest.main()
