import datetime
import json
import os
import urllib.request
import xml.etree.ElementTree as ET

root = ET.parse("results.xml").getroot()
tests = []

for tc in root.iter("testcase"):
    result, msg = "passed", None
    bad = tc.find("failure")
    if bad is None:
        bad = tc.find("error")
    if bad is not None:
        result = "failed"
        msg = bad.get("message", "")
    tests.append({"name": tc.get("name"), "result": result, "failure_message": msg})

passed = sum(1 for t in tests if t["result"] == "passed")
failed = len(tests) - passed

report = {
    "repository": os.getenv("GITHUB_REPOSITORY", "local-run"),
    "branch": os.getenv("GITHUB_REF_NAME", "local"),
    "commit_sha": os.getenv("GITHUB_SHA", "local"),
    "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "local"),
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "tests": tests,
    "total": len(tests),
    "passed": passed,
    "failed": failed,
    "overall_status": "passed" if failed == 0 else "failed",
}

with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

url = os.getenv("REPORT_URL", "http://localhost:9000/report")
req = urllib.request.Request(
    url,
    data=json.dumps(report).encode(),
    headers={"Content-Type": "application/json", "User-Agent": "ci-report/1.0"},
    method="POST",
)
print("Server response:", urllib.request.urlopen(req, timeout=15).read().decode())