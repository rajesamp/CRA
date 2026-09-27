"""Generate one incident-summary document per record in data/incidents.json.

Run from the repo root:  uv run python scripts/build_incident_summaries.py
Output: corpus/incidents/<incident_id>.md (overwritten on each run).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCIDENTS = json.loads((ROOT / "data" / "incidents.json").read_text())
OUT = ROOT / "corpus" / "incidents"

SOURCE_NOTE = {
    "course_sample": "Course sample data (Sep-Projects change_risk_sample.xlsx).",
    "postmortem_table+synthetic_root_cause": (
        "Service, date, change type and severity from the INC-2201 postmortem's "
        "related-incident table; root cause written as synthetic data."
    ),
    "synthetic": "Synthetic record written for the CRA dataset (task #6).",
}


def related(incident):
    """Other incidents on the same service or with the same change type."""
    same_service = [
        i["incident_id"] for i in INCIDENTS
        if i["service"] == incident["service"] and i["incident_id"] != incident["incident_id"]
    ]
    same_type = [
        i["incident_id"] for i in INCIDENTS
        if i["change_type"] == incident["change_type"]
        and i["service"] != incident["service"]
    ]
    return same_service, same_type


def render(i):
    same_service, same_type = related(i)
    lines = [
        f"---",
        f"doc_type: incident_summary",
        f"incident_id: {i['incident_id']}",
        f"service: {i['service']}",
        f"change_type: {i['change_type']}",
        f"severity: {i['severity']}",
        f"date: {i['date']}",
        f"source: {i['source']}",
        f"---",
        "",
        f"# {i['incident_id']}: {i['service']} {i['change_type'].lower()} ({i['severity']})",
        "",
        f"On {i['date']}, a {i['change_type'].lower()} to {i['service']} caused a "
        f"{i['severity']} incident. Root cause: {i['root_cause']}.",
        "",
        f"Change type: {i['change_type']}. Service: {i['service']}. Severity: {i['severity']}.",
        "",
    ]
    if same_service:
        lines.append(f"Other incidents on {i['service']}: {', '.join(same_service)}.")
    if same_type:
        lines.append(f"Other {i['change_type'].lower()} incidents on other services: {', '.join(same_type)}.")
    lines += ["", f"Source: {SOURCE_NOTE[i['source']]}", ""]
    return "\n".join(lines)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("INC-*.md"):
        old.unlink()
    for i in INCIDENTS:
        (OUT / f"{i['incident_id']}.md").write_text(render(i))
    print(f"wrote {len(INCIDENTS)} incident summaries to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
