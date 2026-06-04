from odl_quality.models.result import QualityReport

def print_report(report: QualityReport) -> None:
    """Print a quality report to the console."""
    status = "PASSED" if report.passed else "FAILED"
    print(f"\nQuality Report: {report.dataset} / {report.resource} [{status}]")
    print("-" * 60)
    for result in report.results:
        mark = "✓" if result.passed else "✗"
        print(f"{mark} {result.check_name}: {result.message}")
    print("-" * 60)
