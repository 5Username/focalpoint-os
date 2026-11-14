"""
Background scheduler + HTML email delivery + analytics counters.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import asyncio

from app.services.workspaces import get_all_enabled_schedules, increment_brief_counter
from app.services.osint import build_brief_sections
from app.services.email import send_brief_email, render_brief_html

logger = logging.getLogger("focalpoint.scheduler")
scheduler = BackgroundScheduler()

def _run_brief_job(workspace: dict, notify_emails: list):
    try:
        region = workspace.get("region", "Kenya")
        name = workspace.get("name", "Unknown NGO")
        sections = build_brief_sections(region)

        data = {
            "title": f"Weekly Security Brief — {name}",
            "region": region,
            "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            "sections": sections
        }

        # Plain text fallback
        text_lines = [
            data["title"],
            f"Region: {region}",
            f"Generated: {data['generated_at']}",
            "",
            "EXECUTIVE SUMMARY",
            sections.get("executive_summary", ""),
            "",
            "RECOMMENDATIONS"
        ]
        for r in sections.get("recommendations", []):
            text_lines.append(f"• {r}")
        text_lines.append("")
        text_lines.append("This is a research and coordination product compiled from public sources.")
        text_body = "\n".join(text_lines)

        html_body = render_brief_html(data)
        subject = f"[FocalPoint] Weekly Security Brief — {name} ({region})"

        asyncio.run(send_brief_email(notify_emails, subject, text_body, html_body))

        # Update analytics
        increment_brief_counter(workspace["id"])

        logger.info(f"[Scheduler] Brief generated + emailed for {name}")
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
        logger.info(f"Registered job {job_id} → {ws['name']}")

def start_scheduler():
    if not scheduler.running:
        reload_schedules()
        scheduler.start()
        logger.info("FocalPoint scheduler started")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
