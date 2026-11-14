"""
Background scheduler using APScheduler + email delivery.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import asyncio

from app.services.workspaces import get_all_enabled_schedules
from app.services.osint import build_brief_sections
from app.services.email import send_brief_email

logger = logging.getLogger("focalpoint.scheduler")
scheduler = BackgroundScheduler()

def _run_brief_job(workspace: dict, notify_emails: list):
    try:
        region = workspace.get("region", "Kenya")
        name = workspace.get("name", "Unknown NGO")
        sections = build_brief_sections(region)

        # Build plain-text body
        lines = [
            f"Weekly Security Brief — {name}",
            f"Region: {region}",
            f"Generated: {datetime.utcnow().isoformat()}Z",
            "",
            "EXECUTIVE SUMMARY",
            sections.get("executive_summary", ""),
            "",
            "RECOMMENDATIONS"
        ]
        for r in sections.get("recommendations", []):
            lines.append(f"• {r}")
        lines.append("")
        lines.append("This is a research and coordination product compiled from public sources.")
        lines.append("It is not licensed security advice.")

        body = "\n".join(lines)
        subject = f"[FocalPoint] Weekly Security Brief — {name} ({region})"

        # Send email (run async from sync job)
        asyncio.run(send_brief_email(notify_emails, subject, body))

        logger.info(f"[Scheduler] Brief generated and emailed for {name}")
        print(f"[FocalPoint Scheduler] Brief generated for: {name}")
    except Exception as e:
        logger.error(f"[Scheduler] Failed for {workspace.get('name')}: {e}")

def reload_schedules():
    scheduler.remove_all_jobs()
    for item in get_all_enabled_schedules():
        ws = item["workspace"]
        sched = item["schedule"]
        day = sched.get("day_of_week", "monday")
        hour = int(sched.get("hour", 7))
        emails = sched.get("notify_emails", [])

        day_map = {"monday": "mon", "tuesday": "tue", "wednesday": "wed",
                   "thursday": "thu", "friday": "fri", "saturday": "sat", "sunday": "sun"}
        cron_day = day_map.get(day, "mon")

        trigger = CronTrigger(day_of_week=cron_day, hour=hour, minute=0)
        job_id = f"brief_{ws['id']}"
        scheduler.add_job(
            _run_brief_job,
            trigger=trigger,
            id=job_id,
            args=[ws, emails],
            replace_existing=True,
            name=f"Weekly brief for {ws['name']}"
        )
        logger.info(f"Registered job {job_id} → {ws['name']} ({cron_day} {hour}:00) emails={emails}")

def start_scheduler():
    if not scheduler.running:
        reload_schedules()
        scheduler.start()
        logger.info("FocalPoint scheduler started")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
