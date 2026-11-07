"""Create a concise Markdown/JSON report from pytest JUnit XML."""
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

def summarize(xml_path: Path):
    root = ET.parse(xml_path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    cases = []
    for suite in suites:
        for case in suite.findall("testcase"):
            failure = case.find("failure")
            error = case.find("error")
            skipped = case.find("skipped")
            status = "FAILED" if failure is not None else "ERROR" if error is not None else "SKIPPED" if skipped is not None else "PASSED"
            detail_node = failure if failure is not None else error if error is not None else skipped
            detail = (detail_node.get("message", "") or (detail_node.text or "")).strip() if detail_node is not None else ""
            cases.append({"name": case.get("name", "unknown"), "classname": case.get("classname", ""), "time_seconds": float(case.get("time", 0) or 0), "status": status, "detail": detail[:1200]})
    counts = {key: sum(1 for c in cases if c["status"] == key) for key in ["PASSED", "FAILED", "ERROR", "SKIPPED"]}
    return {"generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "total": len(cases), **{k.lower(): v for k,v in counts.items()}, "cases": cases}

def main():
    xml_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("reports/junit.xml")
    if not xml_path.exists():
        print(f"JUnit report not found: {xml_path}", file=sys.stderr); return 2
    report = summarize(xml_path)
    out_dir = xml_path.parent
    (out_dir / "summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["# Test Execution Summary", "", f"- Generated (UTC): {report['generated_at_utc']}", f"- Total: {report['total']}", f"- Passed: {report['passed']}", f"- Failed: {report['failed']}", f"- Errors: {report['error']}", f"- Skipped: {report['skipped']}", "", "## Failed / Error Cases"]
    failures = [c for c in report["cases"] if c["status"] in ("FAILED", "ERROR")]
    if failures:
        for case in failures:
            lines += [f"### {case['classname']}::{case['name']}", "", case["detail"] or "No failure detail was recorded.", ""]
    else:
        lines += ["No failed or error cases were reported.", ""]
    (out_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Total={report['total']} | Passed={report['passed']} | Failed={report['failed']} | Errors={report['error']} | Skipped={report['skipped']}")
    return 0 if report["failed"] == 0 and report["error"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
