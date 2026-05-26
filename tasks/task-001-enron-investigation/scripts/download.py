import argparse
import urllib.request
from pathlib import Path

URL = "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz"
root = Path(__file__).resolve().parents[3]
out = root / "data/raw/task-001-enron-investigation"
parser = argparse.ArgumentParser()
parser.add_argument("--sample-only", action="store_true")
parser.add_argument("--force", action="store_true")
args = parser.parse_args()
out.mkdir(parents=True, exist_ok=True)

if args.sample_only:
    sample = out / "sample_emails.txt"
    sample.write_text(
        "From: analyst@example.com\n"
        "To: team@example.com\n"
        "Subject: Sample warning sign\n"
        "Date: 2001-08-01\n\n"
        "Placeholder Enron sample for local validation.\n",
        encoding="utf-8",
    )
    print("Wrote sample", sample)
    raise SystemExit

print(
    "Ethics notice: Enron emails contain personal communications. "
    "Use responsibly and do not republish unnecessary personal data."
)
target = out / "enron_mail_20150507.tar.gz"
if target.exists() and not args.force:
    print("Already exists", target)
else:
    urllib.request.urlretrieve(URL, target)
    print("Downloaded", target)
