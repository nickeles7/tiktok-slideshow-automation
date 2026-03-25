# Grok X Search — RAW Clipping + MMO Sentiment Mining (Evidence-First)

## Instructions
Paste this into Grok with X/Twitter search enabled. Run as one prompt.

---

## The Prompt

You have X/Twitter search enabled.

Goal: Collect REAL, recent posts about (A) short-form clipping/editing for creators AND (B) broader "make money online / side hustle" talk that touches clipping.

IMPORTANT RULES (DO NOT BREAK):
1) Do NOT summarize the overall situation.
2) Do NOT rewrite posts into "viral hooks."
3) Prefer VERBATIM quotes/excerpts. Avoid paraphrase unless the post is too long.
4) For every post, include a tweet URL. If you cannot provide a URL, skip that post.
5) Do NOT invent @handles, metrics, dates, or quotes. If unknown/not visible, write "unknown".

FOR EACH POST YOU RETURN, OUTPUT THIS STRUCTURE:
- URL:
- Date (if visible):
- Author / @handle:
- Engagement (likes/replies/reposts if visible):
- Verbatim quote/excerpt (exact wording; keep tone/slang):
- Platform/program mentioned (TikTok, YouTube, X, Creator Fund, Creativity Program, etc.):
- Numbers mentioned (money/views/time/etc.):
- Theme tag (choose 1): [pay-cuts | demonetized | earnings-cap | algorithm | client-acquisition | retainer-wins | pricing | workflow/tools | oversaturation | scams/agencies | outsider-discovery | other]
- Outsider-friendly? (yes/no)
- Why outsider-friendly or not (1 sentence; do NOT rewrite the quote):

QUALITY FILTERS (IMPORTANT):
- Prefer individual creators/editors over brand accounts.
- Avoid obvious course sellers / promo threads / engagement bait unless it's unusually high-engagement or highly specific.
- Prefer posts with concrete numbers, names, screenshots described, or specific programs.
- Avoid duplicates: do not include the same claim repeated by multiple accounts unless you label it as "repeated claim" and include only 1–2 examples.

RECENCY:
- First pull from last 30 days.
- If insufficient, extend to 90 days.

Now search and return posts in these 6 categories (8–12 posts per category):

1) FRUSTRATION ("getting screwed")
Search terms: clipping earnings, creativity program, creator fund, demonetized, capped earnings, denied submission, views but no money

2) FLEX/WINS ("look what I did")
Search terms: first retainer, landed a client, clipping income, $/month editing, quit my job, editing videos side hustle

3) QUESTIONS (beginners)
Search terms: how to start clipping, find creators to clip for, clipper portfolio, retainer deals, what to charge, beginners 2026

4) GAME/ADVICE (tactical)
Search terms: DM strategy clippers, how I got retainer, clipper advice, what agencies look for, editing workflow

5) CONTROVERSY (keep raw; no moralizing)
Search terms: clipping scam, agency scam, clipping oversaturated, whop clipping, creativity program scam

6) OUTSIDER DISCOVERY (most important)
Search terms: "people get paid to clip", "clipping side hustle", "making money editing videos", "no audience needed", "faceless tiktok money", "what is content clipping"

AFTER ALL CATEGORIES, OUTPUT:
A) Recurring names/entities (agencies, creators, tools, programs) — just a list
B) Repeated numeric claims (e.g., same payout story repeated) — list as "repeated claim: …"
C) Top 5 theme tag counts (just counts, no analysis)
