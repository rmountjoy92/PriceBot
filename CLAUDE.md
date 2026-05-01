# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Skills — what you can ask Claude to do

This repo has three built-in skills. You don't need to invoke them manually — just describe what you want and Claude will use the right one.

### Managing the post schedule (Airtable)
The bot posts once per day. Each day of the month is assigned a topic. To manage the schedule, say things like:

- "Show me all the scheduled posts"
- "What's posting on the 15th?"
- "Add a new post for day 8 tracking the price of oranges"
- "Update the article link for the Eggs post"
- "Delete the post scheduled for day 31"

Claude will use the **airtable skill** to read and write the `Posts` table directly.

### Viewing and managing Bluesky posts
To interact with the bot's Bluesky account (@pricebot.bsky.social), say things like:

- "Show me the last 10 posts"
- "Did today's post go out?"
- "Delete the post from April 29th that had an error"
- "Post a test message to Bluesky"

Claude will use the **bluesky skill** to authenticate and interact with the account.

### Deploying code changes
After a developer has pushed a code change, to deploy it to the live server say:

- "Deploy the latest changes"

Claude will use the **deploy-changes skill** to pull the update on PythonAnywhere.

---

## Running the bot

```bash
source .venv/bin/activate
python main.py
```

The bot is hosted on PythonAnywhere and runs on a scheduled task. To deploy changes after committing and pushing, use `/deploy-changes`.

## Architecture

`main.py` is the entry point. It:
1. Reads all rows from the Airtable `Posts` table
2. Finds the row whose `Day` field matches today's day-of-month
3. Dispatches to either `FREDClient` or `BLSClient` based on the `Source` field
4. Posts the result to Bluesky via `BlueskyClient`

### Airtable schema (`Posts` table)
Each row represents one scheduled post. Key fields:
- `Day` — integer day-of-month when this post should run
- `Source` — `"FRED"` or `"BLS"`
- `Series ID` — the data series identifier passed to the respective API
- `Series Name` — human-readable source label used in the post footer
- `Name` — display name for the item being tracked (e.g. `"Rent"`)
- `Type` — `"Price"`, `"Percent"`, or `"Index"` (FRED only; affects formatting)
- `article` — optional URL to embed as a link card in the Bluesky post

### Data clients
- **`FREDClient`** — fetches from the St. Louis Fed FRED API. Supports `Price`, `Percent`, and `Index` display types. Calculates year-over-year change by matching the same month from the prior year.
- **`BLSClient`** — fetches from the BLS public API v2. Always formats values as dollar prices. Assumes data index `[0]` is latest and `[12]` is 12 months prior (monthly data).

### Bluesky posting
`BlueskyClient.post()` accepts optional `article_url`. When provided, it scrapes OG tags (`og:title`, `og:description`, `og:image`) using `cloudscraper` + `BeautifulSoup` to build a link card embed.

## Environment variables

Required in `.env`:
- `AIRTABLE_KEY` — Airtable personal access token
- `AIRTABLE_BASE_ID` — Airtable base ID
- `FRED_API_KEY` — St. Louis Fed API key
- `BLUESKY_USERNAME` / `BLUESKY_PASSWORD` — Bluesky credentials
- `PYTHONANYWHERE_API_KEY` — used only by the `/deploy-changes` skill
