"""
Email delivery for scheduled weekly briefs.
Configure via environment variables:
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM
"""

import os
import logging
from email.message import EmailMessage
import aiosmtplib
from typing import List

logger = logging.getLogger("focalpoint.email")

async def send_brief_email(to_emails: List[str], subject: str, body: str) -> bool:
    if not to_emails:
        logger.info("No recipient emails configured — skipping send")
        return False

    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    from_addr = os.getenv("SMTP_FROM", user or "noreply@focalpoint.local")

    if not host or not user:
        logger.warning("SMTP not configured — printing email instead")
        print("===== EMAIL (SMTP not configured) =====")
        print(f"To: {', '.join(to_emails)}")
        print(f"Subject: {subject}")
        print(body[:500] + "...")
        print("========================================")
        return True

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            msg,
            hostname=host,
            port=port,
            username=user,
            password=password,
            start_tls=True
        )
        logger.info(f"Brief email sent to {to_emails}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False
