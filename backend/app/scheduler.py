"""
Background scheduler using APScheduler.
Loads enabled workspace schedules and registers weekly brief jobs.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

from app.services.workspaces import get_all_enabled_schedules
from app.services.osint import build_brief_sections

logger = logging.getLogger("focalpoint.scheduler")
scheduler = BackgroundScheduler()

def _run_brief_job(workspace: dict):
    """Job that generates a weekly brief for a workspace."""
    try:
        region = workspace.get("region", "Kenya")
        name = workspace.get("name", "Unknown NGO")
        sections = build_brief_sections(region)
        logger.info(f"[Scheduler] Generated weekly brief for {name} ({region}) at {datetime.utcnow().isoformat()}")
        # In production: save to DB, email, or push notification
        # For now we just log that it ran successfully
        print(f"[FocalPoint Scheduler] Brief generated for workspace: {name}")
    except Exception as e:
        logger.error(f"[Scheduler] Failed for {workspace.get('name')}: {e}")

def reload_schedules():
    """Clear existing jobs and re-register from current workspace schedules."""
    scheduler.remove_all_jobs()
    for item in get_all_enabled_schedules():
        ws = item["workspace"]
        sched = item["schedule"]
        day = sched.get("day_of_week", "monday")
        hour = int(sched.get("hour", 7))
        # Map day name to cron day_of_week (mon=0 ... sun=6)
        day_map = {"monday": "mon", "tuesday": "tue", "wednesday": "wed",
                   "thursday": "thu", "friday": "fri", "saturday": "sat", "sunday": "sun"}
        cron_day = day_map.get(day, "mon")

        trigger = CronTrigger(day_of_week=cron_day, hour=hour, minute=0)
        job_id = f"brief_{ws['id']}"
        scheduler.add_job(
            _run_brief_job,
            trigger=trigger,
            id=job_id,
            args=[ws],
            replace_existing=True,
            name=f"Weekly brief for {ws['name']}"
        )
        logger.info(f"Registered job {job_id} for {ws['name']} ({cron_day} {hour}:00)")

def start_scheduler():
    if not scheduler.running:
        reload_schedules()
        scheduler.start()
        logger.info("FocalPoint scheduler started")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
