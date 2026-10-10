"""Command-Line Interface for Apex_CapitalMatrix.

Institutional CLI for NVIDIA Capital Connect VC Diligence and Enterprise Connect PoC execution.
Zero external dependencies (pure Python 3.9+ standard library only).
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from apex_capitalmatrix.core.primitives import GpuArchitecture, TargetRegion
from apex_capitalmatrix.orchestrator import ApexCapitalMatrixOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="capitalmatrix",
        description="Apex_CapitalMatrix: Sovereign NVIDIA VC Alliance Diligence & Enterprise Connect PoC Engine",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command 1: benchmark
    bench_parser = subparsers.add_parser("benchmark", help="Run local hardware saturation and MFU benchmark")
    bench_parser.add_argument("--arch", choices=[a.value for a in GpuArchitecture], default=GpuArchitecture.H100_SXM5.value)
    bench_parser.add_argument("--iterations", type=int, default=10, help="Benchmark iteration count")

    # Command 2: audit-vc
    audit_parser = subparsers.add_parser("audit-vc", help="Execute complete Capital Connect VC due diligence audit")
    audit_parser.add_argument("--startup", type=str, default="Apex Growth Systems LLC", help="Target startup name")
    audit_parser.add_argument("--region", choices=[r.value for r in TargetRegion], default=TargetRegion.US_CAPITAL_CONNECT.value)
    audit_parser.add_argument("--arch", choices=[a.value for a in GpuArchitecture], default=GpuArchitecture.H100_SXM5.value)
    audit_parser.add_argument("--arr", type=float, default=18000000.0, help="Reported ARR in USD")
    audit_parser.add_argument("--ebitda", type=float, default=4200000.0, help="Reported EBITDA in USD")

    # Command 3: poc-verify
    poc_parser = subparsers.add_parser("poc-verify", help="Execute Asian Enterprise Connect air-gap PoC verification")
    poc_parser.add_argument("--startup", type=str, default="Apex Growth Systems LLC", help="Target startup name")
    poc_parser.add_argument("--client", type=str, default="Singtel Enterprise Asia", help="Enterprise customer name")
    poc_parser.add_argument("--erp-action", type=str, default="CREATE_PURCHASE_ORDER", help="Sample ERP action")

    # Command 4: finops
    subparsers.add_parser("finops", help="Display Kubernetes GPU FinOps cluster spend telemetry")

    # Command 5: report
    subparsers.add_parser("report", help="Generate and print full executive markdown diligence memo")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    orchestrator = ApexCapitalMatrixOrchestrator()

    if args.command == "benchmark":
        arch_enum = GpuArchitecture(args.arch)
        print(f"Executing Hardware Saturation Benchmark on {arch_enum.value}...")
        metrics = orchestrator.hardware_verifier.run_synthetic_benchmark(arch=arch_enum, iterations=args.iterations)
        print("Hardware Benchmark Results:")
        print(f"  Achieved TFLOPS     : {metrics.achieved_tflops} TFLOPS")
        print(f"  Theoretical TFLOPS  : {metrics.theoretical_tflops} TFLOPS")
        print(f"  MFU Percentage      : {metrics.mfu_percentage}%")
        print(f"  Throughput          : {metrics.tokens_per_second} tokens/sec")
        print(f"  Token Economics     : {metrics.tokens_per_dollar} tokens/USD")
        print(f"  Wrapper Suspicion   : {metrics.wrapper_suspicion_score} / 1.0 (Deep Tech: {metrics.is_deep_tech_verified})")
        return 0

    elif args.command == "audit-vc":
        packet = orchestrator.run_capital_connect_diligence(
            startup_name=args.startup,
            target_region=TargetRegion(args.region),
            gpu_arch=GpuArchitecture(args.arch),
            reported_arr_usd=args.arr,
            reported_ebitda_usd=args.ebitda,
        )
        print(f"Capital Connect Diligence Completed: [{packet.packet_id}]")
        print(f"  Startup Name        : {packet.startup_name}")
        print(f"  VC Readiness Score  : {packet.vc_readiness_score} / 100.0")
        print(f"  Achieved MFU        : {packet.mfu_metrics.mfu_percentage}%")
        print(f"  Reconciled ARR      : ${packet.atlas_finops.gaap_asc_606_reconciled_arr_usd:,.2f}")
        print(f"  GPU Lease Drag      : ${packet.atlas_finops.unabsorbed_gpu_lease_drag_usd:,.2f}")
        print(f"  Adjusted EBITDA     : ${packet.atlas_finops.adjusted_ebitda_usd:,.2f} (Haircut: {packet.atlas_finops.ebitda_haircut_pct}%)")
        print(f"  EU AI Act Audit     : {'PASSED' if packet.eu_compliance.audit_passed else 'FLAGGED'}")
        print(f"  ActionLedger Digest : {packet.action_ledger_sha256}")
        return 0

    elif args.command == "poc-verify":
        cert = orchestrator.run_enterprise_connect_poc(
            startup_name=args.startup,
            enterprise_client=args.client,
            sample_erp_action=args.erp_action,
        )
        print(f"Enterprise Connect PoC Verified: [{cert.certificate_id}]")
        print(f"  Enterprise Client   : {cert.enterprise_client}")
        print(f"  Approval Verdict    : {cert.approval_verdict.value}")
        print(f"  Zero-Egress State   : {'VERIFIED' if cert.airgap_status.zero_egress_verified else 'FAILED'}")
        print(f"  FlowForge Replay    : {'SAFE IDEMPOTENT' if cert.flowforge_simulation_passed else 'FAILED'}")
        print(f"  Pan-Asia Compliance : {'5/5 PASSED' if cert.pan_asia_compliance.all_passed else 'CONDITIONAL'}")
        print(f"  Escrow Holdback     : ${cert.reps_warranties_escrow_holdback_usd:,.2f}")
        print(f"  Audit Digest        : {cert.audit_sha256}")
        return 0

    elif args.command == "finops":
        orchestrator.control_plane.record_gpu_finops_allocation(
            node_pool="default-dgx-h100-pool",
            gpu_count=16,
            gpu_model="H100_SXM5",
            allocated_hours=24.0,
            hourly_rate_usd=3.25,
        )
        summary = orchestrator.control_plane.get_cluster_spend_summary()
        print("Kubernetes GPU FinOps Summary:")
        print(f"  Cluster Name        : {summary['cluster_name']}")
        print(f"  Total Allocation Log: {summary['total_records']}")
        print(f"  Cumulative GPU Hours: {summary['cumulative_gpu_hours']} hrs")
        print(f"  Cumulative Spend    : ${summary['cumulative_spend_usd']:,.2f}")
        return 0

    elif args.command == "report":
        packet = orchestrator.run_capital_connect_diligence()
        poc = orchestrator.run_enterprise_connect_poc()
        report_md = orchestrator.generate_executive_markdown_report(packet, poc)
        print(report_md)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
