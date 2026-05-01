---
description: Read and post to the PriceBot Bluesky account (pricebot.bsky.social) via the AT Protocol API.
allowed-tools: Read Edit Bash(curl *)
---

Interact with the PriceBot Bluesky account using the AT Protocol REST API.

## Setup

1. Read `.env` and look for lines starting with `BLUESKY_USERNAME=` and `BLUESKY_PASSWORD=`.

2. If either is **not present**, ask the user for the missing value(s), append them to `.env`, and confirm they were saved.

3. Extract both values from those lines.

## Authenticate (get an access token)

All write operations require a session token. Authenticate first:

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.server.createSession" \
  -H "Content-Type: application/json" \
  -d '{"identifier": "BLUESKY_USERNAME", "password": "BLUESKY_PASSWORD"}'
```

Save the `accessJwt` and `did` values from the response — you'll need both for subsequent requests.

## Post plain text

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.repo.createRecord" \
  -H "Authorization: Bearer ACCESS_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "DID",
    "collection": "app.bsky.feed.post",
    "record": {
      "$type": "app.bsky.feed.post",
      "text": "Your post text here",
      "createdAt": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"
    }
  }'
```

## Post with an external link card embed

First, fetch the article's OG tags to get title, description, and image URL:

```bash
curl -sL "ARTICLE_URL" | grep -o '<meta[^>]*property="og:[^>]*>' 
```

Then upload the thumbnail image as a blob:

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.repo.uploadBlob" \
  -H "Authorization: Bearer ACCESS_JWT" \
  -H "Content-Type: image/jpeg" \
  --data-binary @<(curl -sL "IMAGE_URL")
```

Save the `blob` object from the response. Then create the post with the embed:

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.repo.createRecord" \
  -H "Authorization: Bearer ACCESS_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "DID",
    "collection": "app.bsky.feed.post",
    "record": {
      "$type": "app.bsky.feed.post",
      "text": "Your post text here",
      "createdAt": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'",
      "embed": {
        "$type": "app.bsky.embed.external",
        "external": {
          "uri": "ARTICLE_URL",
          "title": "ARTICLE_TITLE",
          "description": "ARTICLE_DESCRIPTION",
          "thumb": BLOB_OBJECT
        }
      }
    }
  }'
```

## Read recent posts from the account

```bash
curl -s "https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor=BLUESKY_USERNAME&limit=10" \
  -H "Authorization: Bearer ACCESS_JWT"
```

## Delete a post

Requires the `rkey` (the last segment of the post's AT URI, e.g. `at://did:.../app.bsky.feed.post/RKEY`):

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.repo.deleteRecord" \
  -H "Authorization: Bearer ACCESS_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "DID",
    "collection": "app.bsky.feed.post",
    "rkey": "RKEY"
  }'
```

## Notes

- Session tokens expire after ~2 hours. Re-authenticate if you get a 401.
- Bluesky posts have a 300 grapheme limit.
- Surface any API errors clearly to the user.
