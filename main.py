import json
import os
import requests
from holidays import is_non_working_day
from datetime import date, datetime
from requests.auth import HTTPBasicAuth
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
import pytz

# Load .env
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# 🔒 Safety check (IMPORTANT)
missing = []

if not JIRA_URL:
    missing.append("JIRA_URL")
if not JIRA_EMAIL:
    missing.append("JIRA_EMAIL")
if not JIRA_API_TOKEN:
    missing.append("JIRA_API_TOKEN")

if missing:
    raise Exception(f"❌ Missing env vars: {', '.join(missing)}")

# Timezone
TIMEZONE = pytz.timezone("Europe/Sofia")

# Load config safely (absolute path fix)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")

with open(config_path, "r") as f:
    config = json.load(f)


def log_work(issue_key, hours):
    print(f"➡️ Logging {hours}h to {issue_key}")

    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/worklog"

    payload = {
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": "Automated daily work log",
                            "type": "text"
                        }
                    ]
                }
            ]
        },
        "timeSpentSeconds": int(float(hours) * 3600)
    }

    response = requests.post(
        url,
        json=payload,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 201:
        print(f"✅ SUCCESS: {issue_key} ({hours}h)")
    else:
        print(f"❌ ERROR: {issue_key}")
        print(response.text)


def daily_job():
    today = date.today()

    if is_non_working_day(today):
        print(f"🛑 Skipping Jira logging (non-working day: {today})")
        return

    print(f"\n[{datetime.now()}] Running Jira Auto Logger...\n")

    for task in config["tasks"]:
        log_work(task["ticket"], task["hours"])


# Scheduler
scheduler = BlockingScheduler(timezone=TIMEZONE)

scheduler.add_job(
    daily_job,
    trigger="cron",
    day_of_week="mon-fri",
    hour=17,
    minute=0
)

print("🚀 Jira Auto Logger started")
print("⏰ Runs every weekday at 17:00 (Europe/Sofia)")

scheduler.start()
