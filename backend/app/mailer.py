import logging
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

from backend.app.config import settings
from backend.app.models import User

logger = logging.getLogger("rag.mailer")


def layout(title: str, intro: str, button: str, link: str, footer: str) -> tuple[str, str]:
    """Returns (text_body, html_body). HTML is a centred 480px card."""
    text_body = f"""{title}

{intro}

{button}: {link}

---
{footer}
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body style="margin: 0; padding: 24px 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f6f1e7; color: #1d2433;">
  <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width: 480px; background-color: #fffdf9; border: 1px solid #e3dac8; border-radius: 12px; padding: 32px; box-shadow: 0 4px 12px rgba(29, 36, 51, 0.06);" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td>
              <div style="font-size: 11px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: #9c7630; margin-bottom: 12px;">RAG Q&amp;A · THE LIBRARY</div>
              <h1 style="font-size: 24px; font-weight: 600; color: #1d2433; margin: 0 0 16px 0;">{title}</h1>
              <p style="font-size: 15px; line-height: 1.6; color: #5c6170; margin: 0 0 24px 0;">{intro}</p>
              
              <div style="text-align: center; margin: 28px 0;">
                <a href="{link}" style="display: inline-block; background-color: #7b1e2b; color: #fff8ef; padding: 12px 28px; font-size: 15px; font-weight: 600; text-decoration: none; border-radius: 8px; box-shadow: 0 2px 4px rgba(123, 30, 43, 0.2);">{button}</a>
              </div>
              
              <p style="font-size: 13px; line-height: 1.5; color: #8b8d95; margin: 20px 0 0 0; word-break: break-all;">
                Or copy and paste this link into your browser:<br>
                <a href="{link}" style="color: #7b1e2b;">{link}</a>
              </p>
              
              <hr style="border: 0; border-top: 1px solid #e3dac8; margin: 28px 0 16px 0;">
              
              <p style="font-size: 12px; line-height: 1.5; color: #8b8d95; margin: 0;">{footer}</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return text_body, html_body


def sendEmail(to: str, subject: str, text: str, html: str):
    """Send email via Resend HTTP API (works on cloud free tiers) or SMTP, fallback to outbox/log."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    # 1. Try Resend HTTP API (Port 443 HTTPS - never blocked by Render Free Tier firewall)
    if settings.RESEND_API_KEY.strip():
        try:
            import json
            import urllib.request
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {settings.RESEND_API_KEY.strip()}",
                "Content-Type": "application/json",
                "User-Agent": "rag-qa-app/1.0",
            }
            from_sender = settings.SMTP_FROM if "@" in settings.SMTP_FROM and "gmail.com" not in settings.SMTP_FROM else "RAG Q&A <onboarding@resend.dev>"
            payload = json.dumps({
                "from": from_sender,
                "to": [to],
                "subject": subject,
                "html": html,
                "text": text,
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status in (200, 201):
                    logger.info("Sent email via Resend to %s: %s", to, subject)
                    return
        except Exception as e:
            logger.error("Resend delivery failed to %s: %s", to, e)

    if not settings.SMTP_HOST.strip():
        outbox_dir = settings.resolve(Path("outbox"))
        outbox_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
        safe_to = to.replace("@", "_at_").replace(".", "_")
        eml_file = outbox_dir / f"{timestamp}-{safe_to}.eml"
        eml_file.write_bytes(msg.as_bytes())

        print(f"\n[EMAIL OUTBOX] To: {to} | Subject: {subject}")
        print(f"Saved: {eml_file}")
        print("-" * 50)
        print(text)
        print("-" * 50 + "\n")
        return

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
            if settings.SMTP_STARTTLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            logger.info("Sent email to %s: %s", to, subject)
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to, e)
        print(f"\n[EMAIL FALLBACK - SMTP FAILED] To: {to} | Subject: {subject} | Error: {e}")
        print("-" * 50)
        print(text)
        print("-" * 50 + "\n")


def sendVerification(user: User, token: str):
    """Send email verification link."""
    link = f"{settings.APP_URL}/verify-email?token={token}"
    subject = "Verify your email for RAG Q&A"
    title = "Verify your email"
    intro = f"Hello {user.name}, welcome to RAG Q&A. Please verify your email address to access the library."
    button = "Verify Email Address"
    footer = "This link expires in 24 hours. If you did not create this account, you can safely ignore this message."
    text, html = layout(title, intro, button, link, footer)
    sendEmail(user.email, subject, text, html)


def sendPasswordReset(user: User, token: str):
    """Send password reset link."""
    link = f"{settings.APP_URL}/reset-password?token={token}"
    subject = "Reset your RAG Q&A password"
    title = "Reset your password"
    intro = f"Hello {user.name}, we received a request to reset your password for RAG Q&A."
    button = "Reset Password"
    footer = "This link expires in 60 minutes and works once. If you did not request a password reset, your account is secure and you can ignore this email."
    text, html = layout(title, intro, button, link, footer)
    sendEmail(user.email, subject, text, html)

