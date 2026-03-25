from fetch_emails import fetch_todays_emails
from summarise import summarise_emails
from send_email import send_briefing

def run():
    print("Fetching emails...")
    emails = fetch_todays_emails(max_results=30)
    print(f"Found {len(emails)} emails. Summarising...")
    summary = summarise_emails(emails)
    print(summary)
    send_briefing(summary)
    print("Done.")

if __name__ == "__main__":
    run()