import json
import os
from datetime import datetime

DB_FILE = "jobs.json"


def get_jobs():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE) as f:
        return json.load(f)


def create_job(data):
    jobs = get_jobs()
    data["timestamp"] = datetime.now().isoformat()
    jobs.append(data)

    with open(DB_FILE, "w") as f:
        json.dump(jobs, f, indent=2)
