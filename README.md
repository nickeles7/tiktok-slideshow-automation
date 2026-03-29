# TikTok Slideshow Automation

Python rendering engine that turns JSON blueprints into TikTok-ready hopecore slideshow PNGs. Built to promote NextClip.me.

## Problem

Posting consistently on TikTok means making a lot of slideshows. Doing them manually in Canva is slow and they start looking the same. I needed a pipeline that could take raw content direction, generate structured slide blueprints, and render finished images automatically. Also needed a system to prevent posts from getting repetitive even when the underlying topics overlap.

## How It Works

Three-stage pipeline. Signal mining, blueprint generation, rendering.

**Signal mining.** A structured prompt goes into Grok with X/Twitter search enabled. It pulls real posts about clipping, editing, side hustles. Verbatim quotes, real URLs, engagement metrics. Raw material.

**Blueprint generation.** Claude processes the raw signals through a signal interpreter that clusters themes, picks narrative direction, and generates JSON blueprints following template schemas (compare or listicle format). A differentiation matrix system tracks the last 4 posts across 4 dimensions (hook frame, story engine, viewer identity, numeric type) and blocks any repeated combination. Keeps posts structurally distinct even when the numbers are similar.

**Rendering.** `render.py` takes a blueprint JSON and composites text overlays onto background images using Pillow and PyCairo.
- TikTok safe zone handling (avoids UI overlap from search bar, action buttons, caption area)
- Zone-aware text positioning based on per-image metadata (where text goes depends on the image)
- Brightness-aware dark scrims for mixed/bright backgrounds
- PyCairo vector stickers for headers with concave interior corners on multi-line layouts
- Highlight markup: green for money, yellow for stats, black for everything else
- CTA slides with product screenshot compositing

## Stack

Python, Pillow, PyCairo, Grok (signal mining), Claude (blueprint generation)
