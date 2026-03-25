from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarise_emails(emails: list[dict]) -> str:
    if not emails:
        return "No emails to summarise today."

    email_block = ""
    for i, e in enumerate(emails, 1):
        email_block += f"""
--- Email {i} ---
From: {e['from']}
Subject: {e['subject']}
Body: {e['body']}
"""

    prompt = f"""You are a sharp executive assistant. Below are today's emails.

Your job:
1. Write a 2-3 sentence overall summary of the day's inbox theme.
2. List each email as a bullet: bold the sender name, one line on what they want or said, and flag if any action is needed (use [ACTION NEEDED]).
3. At the end, list ONLY the action items in a separate "To-do" section.

Be concise. Skip pleasantries. Today's emails:

{email_block}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content