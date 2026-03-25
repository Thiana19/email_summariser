# Email Summariser — AI-Powered Daily Inbox Briefing

Tired of waking up to 30 emails? This tool fetches your Gmail inbox every morning, filters out promotions and social noise, and uses an AI model to send you a single clean briefing — with a summary, per-email bullets, and a to-do list of anything that needs action.

---

## What it does

- Connects to your Gmail and fetches today's emails (skips promotions & social)
- Cleans and extracts plain text from each email
- Sends all emails to an AI model with a structured prompt
- Emails you back a daily briefing that looks like this:

```
The day's inbox theme is primarily focused on job application confirmations
from Jobstreet, with 9 out of 14 emails related to successful job submissions.
Additionally, there are security notifications from Google and Netflix
regarding account activity.

• thianz19@gmail.com — no subject or content provided [ACTION NEEDED]
• Google — security alert regarding allowed access to Google Account data [ACTION NEEDED]
• Google Cloud — welcomed to Google Cloud Free Trial [NO ACTION NEEDED]
• Netflix — new device using your account [ACTION NEEDED]
• Netflix — sign-in code provided [ACTION NEEDED]
• LinkedIn Premium — your profile is getting hits [NO ACTION NEEDED]

─── To-do ───
1. Review and respond to the email from thianz19@gmail.com
2. Address the security alert from Google
3. Review Netflix account activity and secure the account
4. Consider changing your Netflix password after reviewing device activity
5. Enter the Netflix sign-in code on the device if it was you
```

---

## AI provider options

You can choose which AI model powers the summarisation. Here's a comparison:

| Provider | Cost | Model | Sign up |
|---|---|---|---|
| **Groq** | **Free** | Llama 3.3 70B | [console.groq.com](https://console.groq.com) |
| OpenAI | Paid (fractions of a cent/run) | GPT-4o mini | [platform.openai.com](https://platform.openai.com) |
| Anthropic | Paid ($5 free credits on signup) | Claude Sonnet | [console.anthropic.com](https://console.anthropic.com) |

**Recommendation: start with Groq.** It's completely free, requires no credit card, and the Llama 3.3 70B model is excellent for this use case. If you want to upgrade to OpenAI or Anthropic later, see the [Switching AI providers](#switching-ai-providers) section below.

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/email-summariser.git
cd email-summariser
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values (see [AI provider options](#ai-provider-options) above for where to get keys).

### 5. Set up Gmail API

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and create a new project
2. Go to **APIs & Services → Library**, search for **Gmail API** and enable it
3. Go to **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID**
4. Choose **Desktop App**, download the JSON file
5. Rename it to `credentials.json` and place it in the project root
6. Go to **APIs & Services → OAuth consent screen → Audience → Add yourself as a test user**

### 6. Run it

```bash
python main.py
```

The first run will open a browser window asking you to authorise Gmail access. Do this once — it saves a `token.pickle` file so you never have to do it again.

---

## Switching AI providers

The `summarise.py` file contains the AI logic. Swap it out depending on which provider you want to use.

### Groq (free — default)

```bash
pip install groq
```

```python
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarise_emails(emails):
    # ... build prompt ...
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### OpenAI (paid)

Requires an OpenAI account with billing set up at [platform.openai.com/settings/billing](https://platform.openai.com/settings/billing). Costs fractions of a cent per run.

```bash
pip install openai
```

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarise_emails(emails):
    # ... build prompt ...
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### Anthropic (paid — $5 free credits on signup)

New Anthropic accounts get $5 in free API credits which is enough for months of daily runs. Sign up at [console.anthropic.com](https://console.anthropic.com).

```bash
pip install anthropic
```

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def summarise_emails(emails):
    # ... build prompt ...
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

---

## Schedule it to run automatically

### Mac / Linux (cron)

```bash
crontab -e
```

Add this line to run at 7:30am every day:

```
30 7 * * * /path/to/venv/bin/python /path/to/email-summariser/main.py
```

### Windows (Task Scheduler)

1. Open **Task Scheduler → Create Basic Task**
2. Set trigger to **Daily** at your preferred time
3. Set action to **Start a program**: `python` with argument `C:\path\to\main.py`

### GitHub Actions (free, runs in the cloud)

Create `.github/workflows/daily.yml`:

```yaml
name: Daily email briefing
on:
  schedule:
    - cron: "30 7 * * *"   # 7:30am UTC
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python main.py
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          EMAIL_RECIPIENT: ${{ secrets.EMAIL_RECIPIENT }}
```

Store your secrets in **GitHub repo → Settings → Secrets and variables → Actions**.

---

## Project structure

```
email-summariser/
├── auth.py              # Gmail OAuth authentication
├── fetch_emails.py      # Fetch and clean today's emails
├── summarise.py         # AI summarisation (swap provider here)
├── send_email.py        # Send the briefing to your inbox
├── main.py              # Entry point — runs everything
├── .env.example         # Template for your environment variables
├── .gitignore           # Keeps secrets out of git
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Security notes

- `credentials.json`, `.env`, and `token.pickle` are in `.gitignore` and will never be committed
- Your Gmail token only has read + send permissions — it cannot delete emails
- Never share your API keys or commit them to a public repo

---

## License

MIT
