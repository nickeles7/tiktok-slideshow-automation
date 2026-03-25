# Claude Signal Interpreter — Two-Stage Translation Layer

## Purpose

Sits BETWEEN raw Grok mining output and slideshow draft generation.

Grok = raw signal extraction
Claude (this prompt) = signal interpretation + strategic framing

Prevents bias contamination from Grok. Hook selection, template choice, and narrative direction are based on clustered signal — not random loud posts.

---

# STAGE 1 — SIGNAL INTERPRETATION (NO SLIDES YET)

You are analyzing raw mined X/Twitter posts about clipping, side hustles, and make money online conversations.

Do NOT write slides yet.

## 1. Cluster the Posts

Group posts into themes such as:

- Platform pay cuts
- Earnings caps
- Retainer wins
- Client acquisition (DM strategy)
- Oversaturation
- Agency drama
- Scam skepticism
- Outsider discovery ("wait people get paid for this?")
- Lifestyle freedom
- Low barrier / no audience required

List each cluster and how many posts fall into it.

**Outsider filter:** For each cluster, note how many posts would make sense to someone who has NEVER heard of clipping. Clusters with high outsider-friendly counts get priority — they produce hooks that work for broad audiences.

---

## 2. Frequency & Signal Strength

Identify:

- Most common pain point
- Most common win pattern
- Most common outsider discovery angle
- Whether frustration > wins
- Whether controversy is rising
- Whether big money claims are common or rare

If dates are visible, determine if a topic appears to be increasing in frequency.

---

## 3. Extract Structural Drivers

For the dominant cluster(s), extract:

- Primary Emotion
- Core Driver (WHY they feel this way)
- Supporting numbers (money, views, time)
- Any repeated specific names (agencies, platforms, tools)

---

## 3.5 Narrative Differentiation Check

Before choosing any angle, you MUST check what's been used and force rotation. This prevents structurally identical posts even when numbers change.

### Matrix 1: Hook Frame

What psychological lever does the hook pull? (Replaces the old "Hook Class" system.)

| Code | Frame | Viewer Reaction | Hook Shape |
|------|-------|-----------------|------------|
| `envy` | Envy Trigger | "Wait, THEY made that much?" | Someone else's specific result: `*$450* in *4* hours — she's 19` |
| `gap` | Gap Reveal | "I'm doing it wrong" | Two numbers in tension: `*54M* views = *¢28*\nthe kid editing clips made *$1,500*` |
| `ease` | Ease Shock | "That's way simpler than I thought" | Lead with what you DON'T need, money second: `no audience. no product.\njust a laptop and *$2,300/week*` |
| `proof` | Proof Stack | "Too consistent to be fake" | Multiple data points compressed: `*3* retainers. *$4,200/month*.\nstarted *47* days ago` |

### Matrix 2: Story Engine

What narrative arc do the slides follow? Independent of template — a compare and a listicle can use the same engine, but the slides will shape differently.

| Code | Engine | Arc Summary |
|------|--------|-------------|
| `broken-system` | The System Is Broken | Platform/old way fails you → here's what replaced it |
| `hidden-path` | The Hidden Path | Most people don't know this exists → discovery → proof |
| `upgrade` | The Upgrade | You're already doing the work for free → here's how to get paid |
| `origin` | The Origin Story | One person went from $0 to $X → how they did it |

### Matrix 3: Viewer Identity

Who is the post speaking to? This shapes language, assumptions, and what slides 1-2 address.

| Code | Identity | Who They Are | Language Signals |
|------|----------|-------------|------------------|
| `dreamer` | The Dreamer | No online income yet, browses make-money content | "no experience", "from your phone", "zero followers" |
| `stuck` | The Stuck Creator | Already edits/creates but earns nothing from it | "you're already editing", "doing it for free", "your skills are worth more" |
| `skeptic` | The Skeptic | Seen too many scams, needs proof before engaging | stats-heavy, multiple data points, "real numbers", no hype language |
| `searcher` | The Searcher | Actively comparing side hustle options | comparison framing, "instead of X", "while others do Y" |

### Matrix 4: Numeric Type

What kind of number anchors the hook? Prevents every hook from being "$X/month."

| Code | Type | Example |
|------|------|---------|
| `money` | Dollar amount | `*$5k/month*`, `*$450*` |
| `time` | Time leverage | `*3* hours/day`, `*47* days` |
| `count` | Quantity | `*3* clients`, `*10* accounts` |
| `zero` | Zero barrier | `*0* followers`, `no audience` |
| `ratio` | Tension ratio | `*54M* views → *¢28*` |

Every hook still needs a number — this controls WHICH TYPE of number leads.

### Differentiation Procedure

1. Read `system/post-log.json`. Extract `hook_frame`, `story_engine`, `viewer_id`, `numeric_type` from the last 4 entries where `"posted": true`. Skip entries marked `"legacy"`.

2. Count occurrences of each value across those entries.

3. **BLOCK** any value appearing 2+ times. You CANNOT use it for this batch.

4. **DEPRIORITIZE** any value appearing exactly 1 time. Prefer unused values first.

5. List the AVAILABLE options for each matrix with reasoning.

6. **Batch diversity rules:**
   - **2 drafts:** Must differ on at least 2 of the 4 matrices.
   - **3-5 drafts:** No `hook_frame` more than twice. No `story_engine` more than twice. No `viewer_id` more than twice. No `numeric_type` more than twice. At least 3 distinct values across each matrix.

7. **Combination uniqueness:** The triplet `{hook_frame}-{story_engine}-{viewer_id}` must not repeat within the last 8 posts.

Output your available/blocked status and selected values BEFORE proceeding to Section 4.

---

## 4. Determine Hook Frame

Choose ONE hook frame from the AVAILABLE options identified in Section 3.5.

Every hook frame MUST produce a hook that includes a concrete number or dollar amount. No emotion-only hooks. No vague provocations. If the data doesn't support the frame's required hook shape, the frame isn't ready.

**Hook shape requirements by frame:**
- `envy`: Must reference a specific person's result (age, timeframe, or circumstance that triggers "why not me?")
- `gap`: Must contain TWO numbers — the bad outcome AND the good outcome in the same hook
- `ease`: Must lead with barriers removed (no audience, no product, no startup cost) THEN the money
- `proof`: Must stack 2+ independent data points (clients, income, timeframe) in a single hook

Explain WHY this hook frame is most supported by the Grok data AND why it's available per Section 3.5.

### Numeric Type

Choose ONE numeric type from the AVAILABLE options in Section 3.5. This determines what KIND of number leads the hook — not just which number.

The numeric type and hook frame work together:
- `envy` + `money` = "$450 in 4 hours — she's 19"
- `envy` + `time` = "47 days in and she's booked 3 retainers"
- `gap` + `ratio` = "54M views = ¢28 — the kid editing clips made $1,500"
- `ease` + `zero` = "0 followers. 0 startup cost. $2,300/week"
- `proof` + `count` = "3 retainers. $4,200/month. started 47 days ago"

---

## 5. Choose Template + Story Engine

### Template

Choose:

- **Compare** (old vs new / broken vs better) — 6 slides
- **Listicle** (3 reasons / 3 patterns / 3 mistakes) — 5 slides

Explain why this template fits the dominant signal.

### Story Engine

Choose ONE story engine from the AVAILABLE options identified in Section 3.5. Explain how this engine shapes the slide flow for your chosen template.

| Engine | Compare Flow | Listicle Flow |
|--------|-------------|---------------|
| `broken-system` | Old way (platform) → pain (it fails) → new way (retainers) → why it works → CTA | Tips expose why old way fails, tip 3 = the fix → CTA |
| `hidden-path` | Obvious hustle → why nobody talks about this one → the hidden method → proof it works → CTA | 3 things nobody told you → each tip is a discovery → CTA |
| `upgrade` | Free work (editing for fun) → pain (you're not getting paid) → same skill, paid → how to start → CTA | 3 upgrades that turned free work into income → CTA |
| `origin` | Before ($0, no direction) → turning point → after (retainers, income) → what they did → CTA | 3 steps one person took from $0 to $X → CTA |

---

## 6. Output Narrative Direction

Provide:

- **Selected codes:** `hook_frame`, `story_engine`, `viewer_id`, `numeric_type` (with codes)
- **Viewer address:** 1 sentence on how slides 1-2 speak to this viewer identity
- 1 paragraph core narrative angle
- 3 hook candidates (must follow the hook shape for the selected frame — not just dollar amounts)
- 3 possible slide flow outlines (must follow the arc for the selected engine)

STOP HERE.

Do NOT write final slide copy yet.

---

# STAGE 2 — SLIDESHOW GENERATION

Generate the draft JSON blueprint using:

- The selected hook frame, story engine, and viewer identity
- The selected template
- Real numbers pulled from mined data
- Progressive reveal funnel logic:
  - Slide 1 = Broad money/hustle hook (no clipping jargon)
  - Slide 2-3 = Reveal the niche (editing clips for creators)
  - Final slide = CTA framing NextClip as logical solution

## Content Rules

- Do NOT exaggerate beyond raw data
- Use real numbers if available
- Avoid repetitive $X/month phrasing if data suggests alternative framing
- Maintain outsider clarity before revealing niche
- No problem-stack framing ("are you struggling?", "you're getting ignored")

## CTA Framing Rotation

The CTA slide always points to NextClip.me, but the FRAMING must rotate. Do not reuse the same CTA angle as the previous post in `post-log.json`.

Pick one framing per post:

| Code | CTA Angle | Header Example | Body Example |
|------|-----------|----------------|--------------|
| `proof-page` | Build your proof | "Build Your Proof Page" | "Show creators your reach in one link." |
| `no-screenshots` | Kill the screenshots | "Stop Sending Screenshots" | "One link. All your stats. No back-and-forth." |
| `dm-weapon` | Win the DM | "Attach This to Every DM" | "Creators get 50 DMs a day. This is how you stand out." |
| `undeniable` | Make it undeniable | "Make Your Numbers Undeniable" | "Real stats. One link. No trust issues." |
| `one-link` | One link wins | "One Link Beats 50 DMs" | "Everyone sends clips. You send proof." |

Store the selected code as `cta_angle` in the blueprint JSON.

## Hook Formatting Rules

- Use `\n` for line breaks — each beat of the hook gets its own line
- Line 1 = the punch (money, stat, shock value)
- Line 2+ = context (what you're doing, the contrast)
- Max 3 lines
- Must lead with a concrete number or dollar amount

## Highlight Markup Rules

Wrap highlighted words in `*...*` — the renderer auto-detects color:

- **Green**: words containing `$` or `¢` (actual currency)
- **Yellow**: stats, view counts, non-currency numbers
- **Black**: everything else

Rules:
- Wrap the FULL money phrase as one unit: `*$5k/month*` NOT `*$5k*/month`
- Only wrap the value, not surrounding words: `*$1,500/mo* to edit videos` NOT `*$1,500/mo to edit videos*`
- Use `¢` format for cents: `*¢.28*` not `*28 cents*`

## Image Assignment

- Assign images from `assets/images/` using category-relative paths: `grind/g24a.jpg`, `luxury/p03b.jpg`, `flex/p08a.jpg`
- Check `image-tags.json` for zone/brightness data — ONLY use images that exist in this file
- No image should repeat within a post
- **Every slide needs a background image, including the CTA slide** — use a dark luxury/city image for CTA
- The `images` array must have one entry per slide. Do NOT use `"cta"` as an image path.

### Slide Role → Image Category Guide

| Slide Role | Preferred Category | Why |
|---|---|---|
| **hook** | `flex/` (cash, cars, lifestyle) | Stops the scroll — aspirational punch |
| **method-1 / tip-1** | `grind/` (desks, laptops, setups) | "The work" energy |
| **pain / tip-2** | `grind/` (night desks, editing setups) | Grinding in the dark vibe |
| **method-2 / tip-3** | `grind/` or `luxury/` (creator desk or nice room) | Leveling up, proof of results |
| **why-it-works** | `luxury/` (rooms, pools, skylines) | Reward energy, lifestyle payoff |
| **cta** | `luxury/` dark (night skylines, city lights) | Clean dark background for product screenshot |

Prefer `brightness: "dark"` images — they render text cleanest with no gradient needed.

### Image Deduplication

Before assigning images, check `system/post-log.json` for the `images` arrays of recent posts.

**Rules:**
1. **Within a single post:** No image repeats (already enforced).
2. **Within the same batch:** If generating multiple drafts in one session, lock the first draft's images before picking the second. Zero overlap between drafts in the same batch.
3. **Across recent posts:** Do not reuse any image from the last 3 posted entries in post-log.json. After 3 posts of cooldown, an image can be reused.
4. **Never duplicate a full permutation:** No two posts should ever have the exact same image lineup, even after cooldown.
5. **Log images:** Every draft must include an `images` array in the blueprint JSON so it gets tracked when moved to post-log.json.

With 59 images and ~6 per post, this gives ~10 fully unique posts before cooldown recycling kicks in.

## Caption Rules

- **Max 4 lines** including hashtags — longer captions push TikTok's overlay higher and cover slide content
- Required hashtags (every post): `#usenextclip #nextclip #clippers #clipping`
- Add discovery hashtags after required: `#grindset #hopecore #monetize #motivationslideshow #facelesstiktok`
- Line 1 = short punchy caption. Line 2 = hashtags. That's it.

## Naming Convention

Files and `angle_id` use: `{template}-{grok-date}-{sequence}`

Examples: `compare-2026-02-27-1`, `listicle-2026-02-27-2`

- **template** = compare or listicle
- **grok-date** = date of the Grok batch that produced it
- **sequence** = global order across all drafts that day (1, 2, 3...)

**Multi-pass days:** If the user runs Grok more than once in a day, archives are numbered:
- `grok-answer-2026-02-27-1.md` (pass 1)
- `grok-answer-2026-02-27-2.md` (pass 2)
- Post-log `grok_batch` becomes `"2026-02-27-2"` to distinguish which pass

Draft sequence continues across passes: if pass 1 produced drafts 1-2, pass 2 starts at 3.

This links: draft filename → grok archive → post-log `grok_batch`. Everything traces by date + pass.

## Output Format

Return valid JSON matching this structure:

```json
{
  "angle_id": "{template}-{YYYY-MM-DD}-{sequence}",
  "template": "compare|listicle",
  "hook_frame": "envy|gap|ease|proof",
  "story_engine": "broken-system|hidden-path|upgrade|origin",
  "viewer_id": "dreamer|stuck|skeptic|searcher",
  "numeric_type": "money|time|count|zero|ratio",
  "cta_angle": "proof-page|no-screenshots|dm-weapon|undeniable|one-link",
  "cta_image": "profile-stats",
  "caption": "...",
  "images": ["category/file.jpg", ...],
  "slides": [
    {"role": "hook", "text": "..."},
    {"role": "...", "header": "...", "body": "..."},
    {"role": "cta", "header": "...", "body": "...", "url": "https://nextclip.me"}
  ]
}
```

No commentary outside JSON.
