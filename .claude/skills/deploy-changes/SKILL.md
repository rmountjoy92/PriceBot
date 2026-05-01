---
description: Deploy latest changes to PythonAnywhere by triggering a git pull in the hosted console.
allowed-tools: Read Bash(curl *)
---

Deploy the latest changes to PythonAnywhere.

## Steps

1. Read `.env` and look for a line starting with `PYTHONANYWHERE_API_KEY=`.

2. If the key is **not present**, ask the user: "Please enter your PythonAnywhere API token:" then append `PYTHONANYWHERE_API_KEY=<value>` to `.env` and confirm it was saved.

3. Extract the API key value from that line.

4. Run this bash command, substituting the real key for `YOUR_API_KEY`:

```bash
curl -s -X POST "https://www.pythonanywhere.com/api/v0/user/blueskypricebot/consoles/43114787/send_input/" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "cd ~/PriceBot && git pull\n"}'
```

5. Report the response. A successful call returns `{}`. Surface any errors clearly.
