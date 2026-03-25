import base64, re
from datetime import date
from googleapiclient.discovery import build
from auth import get_credentials

def fetch_todays_emails(max_results=30):
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    today = date.today().strftime("%Y/%m/%d")

    results = service.users().messages().list(
        userId="me",
        q=f"after:{today} -category:promotions -category:social",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        full = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()

        headers = {h["name"]: h["value"] for h in full["payload"]["headers"]}
        subject = headers.get("Subject", "(no subject)")
        sender  = headers.get("From", "Unknown")
        body    = extract_body(full["payload"])

        emails.append({
            "subject": subject,
            "from":    sender,
            "body":    body[:2000]
        })

    return emails

def extract_body(payload):
    """Recursively find plain text body in the email payload."""
    if "parts" in payload:
        for part in payload["parts"]:
            result = extract_body(part)
            if result:
                return result
    if payload.get("mimeType") == "text/plain":
        data = payload["body"].get("data", "")
        text = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="ignore")
        return re.sub(r"\s+", " ", text).strip()
    return ""