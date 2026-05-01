---
description: Read and write records in the PriceBot Airtable base (apprylPNW7FXPyY9h).
allowed-tools: Read Edit Bash(curl *)
---

Interact with the PriceBot Airtable base (`apprylPNW7FXPyY9h`).

## Setup

1. Read `.env` and look for a line starting with `AIRTABLE_KEY=`.

2. If the key is **not present**, ask the user: "Please enter your Airtable personal access token:" then append `AIRTABLE_KEY=<value>` to `.env` and confirm it was saved.

3. Extract the API key value from that line.

## Reading records

To list all records from a table (e.g. `Posts`):

```bash
curl -s "https://api.airtable.com/v0/apprylPNW7FXPyY9h/Posts" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Paginate using the `offset` query param if the response includes an `"offset"` field:

```bash
curl -s "https://api.airtable.com/v0/apprylPNW7FXPyY9h/Posts?offset=OFFSET_VALUE" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Creating a record

```bash
curl -s -X POST "https://api.airtable.com/v0/apprylPNW7FXPyY9h/Posts" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Field Name": "value"}}'
```

## Updating a record

Requires the record ID (e.g. `recXXXXXXXXXXXXXX`). Use PATCH to update only specified fields:

```bash
curl -s -X PATCH "https://api.airtable.com/v0/apprylPNW7FXPyY9h/Posts/RECORD_ID" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"Field Name": "new value"}}'
```

## Deleting a record

```bash
curl -s -X DELETE "https://api.airtable.com/v0/apprylPNW7FXPyY9h/Posts/RECORD_ID" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Notes

- Replace `Posts` with any table name in the base.
- Record IDs are returned in the `id` field of each record in list/create responses.
- Surface any API errors clearly to the user.
