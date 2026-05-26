from pathlib import Path
from email import policy
from email.parser import Parser
import datetime
import json

root = Path(__file__).resolve().parents[3]
raw = root / "data/raw/task-001-enron-investigation"
out = root / "data/processed/task-001-enron-investigation"
out.mkdir(parents=True, exist_ok=True)
records = []

for p in raw.rglob("*"):
    if p.is_file() and p.suffix not in [".gz", ".tar"]:
        txt = p.read_text(errors="replace")
        msg = Parser(policy=policy.default).parsestr(txt)
        body = msg.get_body(preferencelist=("plain",))
        body_text = body.get_content() if body else txt.split("\n\n", 1)[-1]
        records.append(
            {
                "sender": msg.get("from", ""),
                "recipients": msg.get("to", ""),
                "cc": msg.get("cc", ""),
                "bcc": msg.get("bcc", ""),
                "subject": msg.get("subject", ""),
                "date": msg.get("date", ""),
                "body": body_text[:5000],
                "file_path": str(p.relative_to(raw)),
                "user_folder": p.parts[-2] if len(p.parts) > 1 else "",
            }
        )

if not records:
    records = [
        {
            "sender": "analyst@example.com",
            "recipients": "team@example.com",
            "subject": "Sample warning sign",
            "date": "2001-08-01",
            "body": "Placeholder sample email for local testing.",
            "file_path": "sample",
            "user_folder": "sample",
        }
    ]

with (out / "emails.jsonl").open("w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

(out / "stats.json").write_text(
    json.dumps(
        {"records": len(records), "prepared_at": datetime.datetime.utcnow().isoformat() + "Z"},
        indent=2,
    ),
    encoding="utf-8",
)
print("Prepared", len(records), "emails")
