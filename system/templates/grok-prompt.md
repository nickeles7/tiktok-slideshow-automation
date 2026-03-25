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

EXCLUSION LIST:
Skip any posts from these URLs or @handles — I already have them:
- https://x.com/FoxyhitsW/status/2015382768600145982
- https://x.com/armourtheeditor/status/2026361996829143219
- https://x.com/rejoice_archie/status/2026929601201528854
- https://x.com/TheCliptic/status/2026815299387854888
- https://x.com/TheCliptic/status/2027443642210607191
- https://x.com/RezzaShahab/status/2026628287221408099
- https://x.com/RezzaShahab/status/2027407202579829174
- https://x.com/jessieclipping/status/2023018166301913125
- https://x.com/jessieclipping/status/2026251029679898793
- https://x.com/danvsI/status/2022292985501598062
- https://x.com/0x_beni_/status/2027466630859477028
- https://x.com/Rubencitopaa/status/2027483711495680414
- https://x.com/Mshartistry/status/2026663193179992559
- https://x.com/gambler_steven/status/2026216722730991886
- https://x.com/SimonDezX/status/2027435118676066596
- https://x.com/Duranwilliams22/status/2027493373171454124
- https://x.com/0xDepressionn/status/2027074872048836817
- https://x.com/ripchillpill/status/2014621863595422074
- https://x.com/yo/status/2021546944901136434

If most results in a category overlap with exclusions, expand time range or try these adjacent search terms:
- "clipping" → "content creation income", "faceless pages", "UGC money"
- "retainer" → "monthly client", "recurring editing income"
- "creator fund" → "platform payouts", "TikTok money"
- "side hustle" → "online income no audience", "phone only business", "zero startup cost"
