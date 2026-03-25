import base64, os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from auth import get_credentials
from dotenv import load_dotenv

load_dotenv()

def send_briefing(summary: str):
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    recipient = os.getenv("EMAIL_RECIPIENT")
    html_body = summary.replace("\n", "<br>").replace("**", "<b>").replace("**", "</b>")

    message = MIMEText(f"""
    <html><body style="font-family:sans-serif;max-width:600px;margin:auto;padding:20px">
    <h2 style="color:#333">Your daily inbox briefing</h2>
    <hr/>
    {html_body}
    </body></html>
    """, "html")

    message["to"] = recipient
    message["subject"] = "Daily inbox briefing"

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"Briefing sent to {recipient}")