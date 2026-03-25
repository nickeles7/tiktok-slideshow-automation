# Hopecore TikTok Content System

## Session Start Checklist
Do this at the start of every new session. No sub-agents allowed for these steps — do them yourself directly.

1. Read these files:
   - `memory/MEMORY.md`
   - `system/post-log.json`
2. Check project state:
   - Are there drafts in `drafts/`? (pending work)
   - Are there rendered posts in `output/`?
   - Check `system/templates/grok-answer.md` freshness (see Grok Freshness below)
3. Follow the state machine:

| State | Action |
|-------|--------|
| Fresh Grok data + no drafts + no output | Auto-run Post Generation flow |
| Drafts exist + no output | Render with `render.py` |
| Output exists | Show what's ready, ask: post / revise / generate more |
| Stale or empty Grok data | Tell user to run Grok prompt and paste into `grok-answer.md` |
| User says "I posted" / "done posting" | Run Post-Posting Workflow |

4. Always greet with a brief status of where things stand

## Grok Freshness

`grok-answer.md` is **fresh** if it has NOT already been consumed into drafts this session.

To check: compare `grok-answer.md` content against the latest `grok-archive/` file.
- If `grok-answer.md` matches the latest archive → **stale** (already consumed)
- If `grok-answer.md` differs from latest archive OR no archive exists → **fresh**
- If `grok-answer.md` is empty → **no data**

When consuming fresh Grok data, archive it FIRST:
- `grok-answer.md` → `grok-archive/grok-answer-YYYY-MM-DD.md`
- Multi-pass: add `-N` suffix (`-1`, `-2`, etc.)

## Post Generation

When generating new drafts, you MUST read and execute `system/signal-interpreter.md` as a sequential procedure. Do not skip stages. Do not write slides before completing Stage 1. Stage 1 output requires user review before proceeding to Stage 2.

### What to read (and when)

**Always read at session start** (step 1):
- `memory/MEMORY.md`
- `system/post-log.json`

**Read when entering Stage 1** (only if generating):
- `system/signal-interpreter.md`
- `system/templates/grok-answer.md`
- `assets/images/image-tags.json`

**Read when entering Stage 2** (only if writing drafts):
- `system/templates/compare.json` or `listicle.json` (whichever was chosen)
- `system/config.json` (hashtag strategy)

Do NOT read everything up front. Read on demand.

## Draft Validation Checklist

Before writing ANY draft JSON to `drafts/`, verify ALL of the following. If any check fails, fix it before writing.

1. **Matrix fields present:** `hook_frame`, `story_engine`, `viewer_id`, `numeric_type`, `cta_angle` are all set to valid values (not empty, not placeholder)
2. **Differentiation rules pass:** No blocked values used (Section 3.5 of signal-interpreter.md)
3. **Images exist:** Every image path in the `images` array exists in `image-tags.json`
4. **Image count matches slides:** `images` array has exactly one entry per slide
5. **Image dedup:** No overlap with last 3 posted entries OR other drafts in this batch
6. **Required hashtags:** Caption contains `#usenextclip #nextclip #clippers #clipping`
7. **Caption length:** Max 4 lines including hashtags
8. **Hook format:** Uses `\n` for line breaks, max 3 lines, leads with a number
9. **Highlight markup:** `*...*` wraps only values, full money phrases as one unit
10. **CTA slide has image:** The last entry in `images` is a dark luxury image, NOT `"cta"`
11. **CTA angle rotated:** `cta_angle` differs from the previous post's `cta_angle`
12. **Naming convention:** `angle_id` follows `{template}-{YYYY-MM-DD}-{sequence}`

## Post-Posting Workflow

When the user says they posted (e.g., "posted", "done", "uploaded", "saved to TikTok drafts"):

1. **Ask for TikTok post IDs/URLs** — if the user provides them, use them. If not, leave `id` and `url` as `"pending"` (user can fill later).

2. **Update post-log.json** — for each posted draft, add an entry:
   ```json
   {
     "id": "<tiktok-id or pending>",
     "url": "<tiktok-url or pending>",
     "hook": "<hook text from blueprint>",
     "template": "<from blueprint>",
     "hook_frame": "<from blueprint>",
     "story_engine": "<from blueprint>",
     "viewer_id": "<from blueprint>",
     "numeric_type": "<from blueprint>",
     "cta_angle": "<from blueprint>",
     "account": "@m_d_o_p_s",
     "posted": true,
     "images": ["<from blueprint>"],
     "grok_batch": "<YYYY-MM-DD or YYYY-MM-DD-N>",
     "notes": "<brief description>"
   }
   ```

3. **Move blueprints:** `drafts/{file}.json` → `posts/{file}.json`

4. **Archive Grok data** (if not already archived this session):
   - Copy `grok-answer.md` → `grok-archive/grok-answer-YYYY-MM-DD.md`

5. **Clean output:** Ask user if they want `output/` cleared (it's re-renderable)

6. **Confirm** — show summary: what was logged, what was archived, what's left

## Key System Files
- `system/signal-interpreter.md` — two-stage generation with differentiation matrices
- `system/post-log.json` — tracks posts with angle tracking fields
- `system/config.json` — hashtag strategy, system settings
- `assets/images/image-tags.json` — source of truth for image zone/brightness

## Draft Lifecycle
```
drafts/                              ← hot: active blueprints, not yet posted
output/                              ← rendered PNGs (disposable, re-renderable)
posts/                               ← cold: blueprints moved here once posted
system/templates/grok-prompt.md      ← hot: current Grok prompt (editable)
system/templates/grok-answer.md      ← hot: current Grok signal data
system/templates/grok-archive/       ← cold: dated prompts + answers
```
- `output/` can be wiped anytime — re-render from `posts/` if needed
- `render.py` takes blueprint paths as CLI args, works from any directory
- When modifying `grok-prompt.md`, archive the current version first → `grok-archive/grok-prompt-YYYY-MM-DD.md`

## Rules
- Never overwrite original images — render.py outputs to `output/`
- Blueprint JSON is the input format for rendering posts
- Image paths in blueprints use category-relative format: `grind/g24a.jpg`, `luxury/p03b.jpg`, `flex/p08a.jpg`
- Always check `image-tags.json` when working with images — it's the source of truth for zone/brightness
- Keep memory files updated at end of sessions with meaningful progress
