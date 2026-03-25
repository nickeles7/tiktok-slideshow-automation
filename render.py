"""
render.py - Text overlay renderer for hopecore TikTok slideshow posts.

Reads a post blueprint JSON, composites text onto background images
using zone/brightness data from image-tags.json, and outputs finished
slides. Original images are never modified.

Usage:
    python render.py blueprint.json
"""

import json
import os
import random
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import cairo
import math

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
NEXTCLIP_DIR = ASSETS_DIR / "nextclip"
OUTPUT_DIR = BASE_DIR / "output"
TAGS_PATH = IMAGES_DIR / "image-tags.json"

# Font - Arial Bold on Windows
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"

# ---------------------------------------------------------------------------
# Sizing (relative to image dimensions, designed for 9:16 / 1080x1920)
# ---------------------------------------------------------------------------
HEADER_FONT_RATIO = 0.038      # header font size — reduced 10% for TikTok fit
BODY_FONT_RATIO = 0.026        # body font size — smaller for breathing room
HOOK_FONT_RATIO = 0.043        # hook slides — reduced 10% for TikTok fit
TEXT_WIDTH_RATIO = 0.82         # text width — keeps clear of right-side action buttons
LINE_SPACING_RATIO = 1.40      # line spacing multiplier

# TikTok safe zone — where text can actually live without UI overlap
SAFE_TOP = 0.19                # below search bar + pill overshoot clearance
SAFE_BOTTOM = 0.50             # above username/caption/sound bar (accounts for multi-line captions)
SAFE_LEFT = 0.06               # left padding
SAFE_RIGHT = 0.08              # right padding (action buttons)

# Shadow settings — multiple passes for organic glow instead of hard box
SHADOW_PASSES = [
    (0, 0, 12, 0.4),   # soft glow behind text (blur radius 12, 40% opacity)
    (2, 2, 3, 0.7),    # tight shadow (blur 3, 70% opacity)
    (0, 0, 0, 0.3),    # crisp outline pass
]

# Scrim settings — subtle darkening for bright/mixed images
SCRIM_ALPHA_MIXED = 60         # very subtle for mixed
SCRIM_ALPHA_BRIGHT = 110       # moderate for bright

# CTA product image sizing
CTA_IMAGE_WIDTH_RATIO = 0.58   # product screenshot width as fraction of image

# Highlight colors — auto-detected by content
MONEY_COLOR = (0, 160, 50, 255)        # rich green for dollar amounts / numbers
ACTION_COLOR = (250, 246, 5, 255)      # bright yellow for action / invitational words
HIGHLIGHT_STROKE_WIDTH = 4             # thick black outline on colored text
HIGHLIGHT_STROKE_COLOR = (0, 0, 0, 255)


def load_tags():
    """Load image-tags.json and return the images dict."""
    with open(TAGS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["images"]


def load_blueprint(path):
    """Load a post blueprint JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_font(size):
    """Load Arial Bold at given pixel size."""
    return ImageFont.truetype(FONT_PATH, size)


def is_money_word(word):
    """Check if a word has actual currency symbols ($ or ¢). Strictly money only."""
    return '$' in word or '¢' in word


def get_highlight_color(word):
    """Return the right highlight color based on word content."""
    if is_money_word(word):
        return MONEY_COLOR
    return ACTION_COLOR


def parse_highlights(text):
    """Parse *highlighted* markup. Returns list of (word, is_highlight) tuples."""
    import re
    tokens = []
    parts = re.split(r'(\*[^*]+\*)', text)
    for part in parts:
        if part.startswith('*') and part.endswith('*'):
            for word in part[1:-1].split():
                tokens.append((word, True))
        else:
            for word in part.split():
                tokens.append((word, False))
    return tokens


def strip_highlights(text):
    """Remove * markers from text."""
    return text.replace('*', '')


def wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width pixels. Returns list of lines."""
    clean = strip_highlights(text)
    words = clean.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def wrap_tokens(tokens, font, max_width, draw):
    """Word-wrap tokens (with highlight flags) into lines.
    Returns list of lines, where each line is a list of (word, is_highlight) tuples."""
    lines = []
    current_line = []
    current_text = ""

    for word, hl in tokens:
        test_text = f"{current_text} {word}".strip()
        bbox = draw.textbbox((0, 0), test_text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append((word, hl))
            current_text = test_text
        else:
            if current_line:
                lines.append(current_line)
            current_line = [(word, hl)]
            current_text = word

    if current_line:
        lines.append(current_line)

    return lines


def calc_text_block_height(lines, font, line_spacing):
    """Calculate total height of a wrapped text block."""
    if not lines:
        return 0
    line_height = font.size * line_spacing
    return int(line_height * len(lines))


def get_zone_position(zone, img_width, img_height, block_width, block_height):
    """Return (x, y) top-left position for the text block based on TikTok safe zone."""
    left = int(img_width * SAFE_LEFT)
    right_edge = int(img_width * (1 - SAFE_RIGHT))
    top = int(img_height * SAFE_TOP)
    bottom_floor = int(img_height * SAFE_BOTTOM)

    positions = {
        "top":          (left, top),
        "top-left":     (left, top),
        "top-right":    (right_edge - block_width, top),
        "center":       (left, img_height // 2 - block_height // 2),
        "bottom":       (left, bottom_floor - block_height),
        "bottom-left":  (left, bottom_floor - block_height),
        "bottom-right": (right_edge - block_width, bottom_floor - block_height),
    }

    return positions.get(zone, positions["top"])


def apply_scrim(img, zone, alpha):
    """
    Apply a subtle top-down or bottom-up dark scrim instead of a boxy gradient.
    Feels more like natural vignetting than a PowerPoint shape.
    """
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    img_w, img_h = img.size

    if zone.startswith("bottom"):
        # Bottom scrim — gradient from bottom up
        scrim_h = int(img_h * 0.55)
        for y in range(scrim_h):
            progress = y / scrim_h  # 0 at top of scrim, 1 at bottom
            a = int(alpha * progress * progress)  # quadratic ease-in
            draw.line([(0, img_h - scrim_h + y), (img_w, img_h - scrim_h + y)],
                      fill=(0, 0, 0, a))
    else:
        # Top scrim — gradient from top down
        scrim_h = int(img_h * 0.55)
        for y in range(scrim_h):
            progress = 1.0 - (y / scrim_h)  # 1 at top, 0 at bottom
            a = int(alpha * progress * progress)
            draw.line([(0, y), (img_w, y)], fill=(0, 0, 0, a))

    return Image.alpha_composite(img, overlay)


def draw_text_with_shadow(draw, text, x, y, font, img_size):
    """
    Draw text with multi-pass shadow for organic look.
    No hard box — just soft glow + crisp shadow like IG stories.
    """
    img_w, img_h = img_size

    for dx, dy, blur_r, opacity in SHADOW_PASSES:
        shadow_alpha = int(255 * opacity)
        if blur_r > 0:
            # Create a temp image for this shadow pass, blur it
            tmp = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
            tmp_draw = ImageDraw.Draw(tmp)
            tmp_draw.text((x + dx, y + dy), text, font=font,
                          fill=(0, 0, 0, shadow_alpha))
            tmp = tmp.filter(ImageFilter.GaussianBlur(radius=blur_r))
            # Composite shadow onto a shared layer later — for now draw direct
            # We'll handle this at the slide level
            pass
        else:
            draw.text((x + dx, y + dy), text, font=font,
                      fill=(0, 0, 0, shadow_alpha))

    # Main white text
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))


def render_slide(image_path, header_text, body_text, zone, brightness,
                 role="tip", cta_image_path=None, url_text=None):
    """
    Render a single slide with organic text styling.
    """
    img = Image.open(image_path).convert("RGBA")
    img_w, img_h = img.size

    # Font sizes scaled to image — hooks get bigger text
    if role == "hook":
        header_size = max(36, int(img_h * HOOK_FONT_RATIO))
        body_size = max(20, int(img_h * BODY_FONT_RATIO))
    else:
        header_size = max(30, int(img_h * HEADER_FONT_RATIO))
        body_size = max(18, int(img_h * BODY_FONT_RATIO))

    header_font = get_font(header_size)
    body_font = get_font(body_size)

    max_text_w = int(img_w * TEXT_WIDTH_RATIO)

    temp_draw = ImageDraw.Draw(img)

    # Wrap text — header uses token-aware wrapping for highlight support
    # Hooks support \n for manual line breaks (author controls pacing)
    if header_text and role == "hook" and '\n' in header_text:
        header_token_lines = []
        for segment in header_text.split('\n'):
            seg_tokens = parse_highlights(segment.strip())
            if seg_tokens:
                # Auto-wrap within each segment if it's still too wide
                seg_lines = wrap_tokens(seg_tokens, header_font, max_text_w, temp_draw)
                header_token_lines.extend(seg_lines)
    else:
        header_tokens = parse_highlights(header_text) if header_text else []
        header_token_lines = wrap_tokens(header_tokens, header_font, max_text_w, temp_draw) if header_tokens else []
    header_lines = [" ".join(w for w, _ in tl) for tl in header_token_lines]
    body_lines = wrap_text(body_text, body_font, max_text_w, temp_draw) if body_text else []

    line_sp = LINE_SPACING_RATIO
    header_block_h = calc_text_block_height(header_lines, header_font, line_sp)
    body_block_h = calc_text_block_height(body_lines, body_font, line_sp)

    gap = int(body_size * 1.2) if header_lines and body_lines else 0
    url_gap = int(body_size * 0.8) if url_text and body_lines else 0
    url_block_h = int(body_font.size * line_sp) if url_text else 0
    total_text_h = header_block_h + gap + body_block_h + url_gap + url_block_h

    # Position text
    if cta_image_path:
        # CTA: text in safe zone top, phone below
        block_w = max_text_w
        tx = int(img_w * SAFE_LEFT)
        ty = int(img_h * SAFE_TOP)
    else:
        block_w = max_text_w
        block_h = total_text_h
        tx, ty = get_zone_position(zone, img_w, img_h, block_w, block_h)

    # Apply scrim for bright/mixed images (no boxy gradient)
    if brightness == "mixed":
        img = apply_scrim(img, zone, SCRIM_ALPHA_MIXED)
    elif brightness == "bright":
        img = apply_scrim(img, zone, SCRIM_ALPHA_BRIGHT)

    # Composite CTA product image BEFORE text so text can go on top if needed
    if cta_image_path:
        cta_img = Image.open(cta_image_path).convert("RGBA")
        cta_w = int(img_w * CTA_IMAGE_WIDTH_RATIO)
        cta_ratio = cta_w / cta_img.width
        cta_h = int(cta_img.height * cta_ratio)
        cta_img = cta_img.resize((cta_w, cta_h), Image.LANCZOS)

        # Place phone below text block with breathing room
        cta_x = int(img_w * 0.5 - cta_w * 0.45)
        text_bottom = ty + total_text_h + int(img_h * 0.03)
        cta_y = max(text_bottom, img_h - cta_h - int(img_h * 0.02))

        # Add subtle shadow behind phone frame
        phone_shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ps_draw = ImageDraw.Draw(phone_shadow)
        ps_draw.rounded_rectangle(
            [cta_x + 8, cta_y + 8, cta_x + cta_w + 8, cta_y + cta_h + 8],
            radius=24, fill=(0, 0, 0, 80)
        )
        phone_shadow = phone_shadow.filter(ImageFilter.GaussianBlur(radius=12))
        img = Image.alpha_composite(img, phone_shadow)

        img.paste(cta_img, (cta_x, cta_y), cta_img)

    # --- HEADER: IG-story-style per-line white pill stickers with black text ---
    # PYCAIRO — single vector path with exact same-radius concave interior corners.
    # No connectors, no hacks. One closed path traces the entire sticker outline
    # with arc() for convex exterior corners and arc_negative() for concave interior corners.
    cursor_y = ty
    sticker_pad_x = int(header_font.size * 0.28)
    sticker_pad_y = int(header_font.size * 0.08)
    pill_height = int(header_font.size + sticker_pad_y * 2)
    sticker_radius = int(header_font.size * 0.24)   # premium IG/TikTok rounding
    pill_gap = 0

    if header_lines:
        # Measure widths
        line_widths = []
        for line in header_lines:
            bbox = temp_draw.textbbox((0, 0), line, font=header_font)
            line_widths.append(bbox[2] - bbox[0])

        max_line_w = max(line_widths)
        if role == "hook":
            center_x = img_w // 2
        else:
            center_x = tx + max_line_w // 2 + sticker_pad_x

        # Build pill geometry
        pills = []
        for i, line_w in enumerate(line_widths):
            pill_w = line_w + sticker_pad_x * 2
            pill_x = center_x - pill_w // 2
            pill_y = cursor_y + i * (pill_height + pill_gap)
            pills.append((pill_x, pill_y, pill_w))

        n = len(pills)
        r = sticker_radius
        merge_threshold = r * 2  # if edges are closer than this, snap to same width

        # Snap near-equal edges so we don't draw tiny arcs for trivial differences
        lefts = [px for px, py, pw in pills]
        rights = [px + pw for px, py, pw in pills]
        for j in range(n - 1):
            if abs(rights[j] - rights[j+1]) < merge_threshold:
                shared = max(rights[j], rights[j+1])
                rights[j] = shared
                rights[j+1] = shared
            if abs(lefts[j] - lefts[j+1]) < merge_threshold:
                shared = min(lefts[j], lefts[j+1])
                lefts[j] = shared
                lefts[j+1] = shared

        tops = [py for px, py, pw in pills]
        bottoms = [py + pill_height for px, py, pw in pills]

        # Determine hook highlight style before drawing pill
        has_highlights = any(hl for tl in header_token_lines for _, hl in tl)
        unified_color = None
        skip_pill = False
        if role == "hook" and has_highlights:
            hl_words = [w for tl in header_token_lines for w, hl in tl if hl]
            has_money = any(is_money_word(w) for w in hl_words)
            unified_color = MONEY_COLOR if has_money else ACTION_COLOR
            # Yellow hooks: no white pill, just stroked text on image
            if not has_money:
                skip_pill = True

        if not skip_pill:
            # Cairo vector surface — white pill sticker
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_w, img_h)
            ctx = cairo.Context(surface)
            ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
            ctx.new_path()

            # === TOP EDGE ===
            ctx.arc(lefts[0] + r, tops[0] + r, r, math.pi, 3*math.pi/2)        # top-left
            ctx.arc(rights[0] - r, tops[0] + r, r, 3*math.pi/2, 2*math.pi)     # top-right

            # === RIGHT SIDE (going down) ===
            for j in range(n - 1):
                jy = bottoms[j]
                if rights[j] > rights[j+1] + 1:
                    ctx.arc(rights[j] - r, jy - r, r, 0, math.pi/2)
                    ctx.line_to(rights[j+1] + r, jy)
                    ctx.arc_negative(rights[j+1] + r, jy + r, r, 3*math.pi/2, math.pi)
                elif rights[j+1] > rights[j] + 1:
                    ctx.arc_negative(rights[j] + r, jy - r, r, math.pi, math.pi/2)
                    ctx.line_to(rights[j+1] - r, jy)
                    ctx.arc(rights[j+1] - r, jy + r, r, 3*math.pi/2, 2*math.pi)

            # === BOTTOM EDGE ===
            ctx.arc(rights[-1] - r, bottoms[-1] - r, r, 0, math.pi/2)          # bottom-right
            ctx.arc(lefts[-1] + r, bottoms[-1] - r, r, math.pi/2, math.pi)     # bottom-left

            # === LEFT SIDE (going up) ===
            for j in range(n - 2, -1, -1):
                jy = bottoms[j]
                if lefts[j] < lefts[j+1] - 1:
                    ctx.arc_negative(lefts[j+1] - r, jy + r, r, 0, 3*math.pi/2)
                    ctx.line_to(lefts[j] + r, jy)
                    ctx.arc(lefts[j] + r, jy - r, r, math.pi/2, math.pi)
                elif lefts[j+1] < lefts[j] - 1:
                    ctx.arc(lefts[j+1] + r, jy + r, r, math.pi, 3*math.pi/2)
                    ctx.line_to(lefts[j] - r, jy)
                    ctx.arc_negative(lefts[j] - r, jy - r, r, math.pi/2, 0)

            ctx.close_path()
            ctx.fill()

            # Composite Cairo → Pillow
            sticker_bytes = surface.get_data()
            sticker_img = Image.frombytes("RGBA", (img_w, img_h), sticker_bytes, "raw", "BGRA", 0, 1)
            img = Image.alpha_composite(img, sticker_img)

        # Text on pills — word-by-word for highlight color support
        draw = ImageDraw.Draw(img)

        for i, (token_line, line_w) in enumerate(zip(header_token_lines, line_widths)):
            pill_w = line_w + sticker_pad_x * 2
            pill_x = center_x - pill_w // 2
            pill_y = cursor_y + i * (pill_height + pill_gap)
            lx = pill_x + sticker_pad_x
            ly = pill_y + sticker_pad_y

            if role == "hook" and has_highlights and skip_pill:
                # Yellow action hook: no pill, all words yellow with stroke
                cx = lx
                for wi, (word, hl) in enumerate(token_line):
                    draw.text((cx, ly), word, font=header_font,
                              fill=ACTION_COLOR,
                              stroke_width=HIGHLIGHT_STROKE_WIDTH,
                              stroke_fill=HIGHLIGHT_STROKE_COLOR)
                    word_w = draw.textbbox((0, 0), word + " ", font=header_font)[2]
                    cx += word_w
            elif role == "hook" and has_highlights:
                # Money hook: white pill, currency=green, stats=yellow, rest=black
                cx = lx
                for wi, (word, hl) in enumerate(token_line):
                    if hl and is_money_word(word):
                        # Currency — green with stroke
                        draw.text((cx, ly), word, font=header_font,
                                  fill=MONEY_COLOR,
                                  stroke_width=HIGHLIGHT_STROKE_WIDTH,
                                  stroke_fill=HIGHLIGHT_STROKE_COLOR)
                    elif hl:
                        # Stats/non-money highlight — yellow with stroke
                        draw.text((cx, ly), word, font=header_font,
                                  fill=ACTION_COLOR,
                                  stroke_width=HIGHLIGHT_STROKE_WIDTH,
                                  stroke_fill=HIGHLIGHT_STROKE_COLOR)
                    else:
                        draw.text((cx, ly), word, font=header_font,
                                  fill=(0, 0, 0, 255))
                    word_w = draw.textbbox((0, 0), word + " ", font=header_font)[2]
                    cx += word_w
            elif has_highlights:
                # Non-hook: per-word coloring (green for money, gold for action)
                cx = lx
                for wi, (word, hl) in enumerate(token_line):
                    if hl:
                        color = get_highlight_color(word)
                        draw.text((cx, ly), word, font=header_font,
                                  fill=color,
                                  stroke_width=HIGHLIGHT_STROKE_WIDTH,
                                  stroke_fill=HIGHLIGHT_STROKE_COLOR)
                    else:
                        draw.text((cx, ly), word, font=header_font,
                                  fill=(0, 0, 0, 255))
                    word_w = draw.textbbox((0, 0), word + " ", font=header_font)[2]
                    cx += word_w
            else:
                line_text = " ".join(w for w, _ in token_line)
                draw.text((lx, ly), line_text, font=header_font, fill=(0, 0, 0, 255))

        total_pills_h = len(header_lines) * (pill_height + pill_gap) - pill_gap
        cursor_y += total_pills_h + gap

    # --- BODY: white text with transparent dark underlay ---
    if body_lines:
        line_height = int(body_font.size * line_sp)

        # Dark rounded rectangle behind body text
        body_pad_x = int(body_font.size * 0.4)
        body_pad_y = int(body_font.size * 0.35)
        body_block_top = cursor_y - body_pad_y
        body_block_bottom = cursor_y + len(body_lines) * line_height + body_pad_y
        body_block_left = tx - body_pad_x
        body_block_right = tx + max_text_w + body_pad_x
        body_bg = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        body_bg_draw = ImageDraw.Draw(body_bg)
        body_bg_draw.rounded_rectangle(
            [body_block_left, body_block_top, body_block_right, body_block_bottom],
            radius=int(body_font.size * 0.3),
            fill=(0, 0, 0, 120),
        )
        img = Image.alpha_composite(img, body_bg)

        # White glow behind text so it pops off the dark underlay
        glow_layer = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        for i, line in enumerate(body_lines):
            ly = cursor_y + i * line_height
            lx = tx if role != "hook" else img_w // 2 - (temp_draw.textbbox((0, 0), line, font=body_font)[2] - temp_draw.textbbox((0, 0), line, font=body_font)[0]) // 2
            glow_draw.text((lx, ly), line, font=body_font, fill=(255, 255, 255, 200))
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=3))
        img = Image.alpha_composite(img, glow_layer)

        # Crisp body text
        draw = ImageDraw.Draw(img)
        for i, line in enumerate(body_lines):
            ly = cursor_y + i * line_height
            if role == "hook":
                bbox = draw.textbbox((0, 0), line, font=body_font)
                text_w = bbox[2] - bbox[0]
                lx = img_w // 2 - text_w // 2
            else:
                lx = tx
            draw.text((lx, ly), line, font=body_font, fill=(255, 255, 255, 255))

    # --- URL: colored link text below body (CTA slides only) ---
    if url_text:
        url_y = cursor_y
        if body_lines:
            line_height = int(body_font.size * line_sp)
            url_y = cursor_y + len(body_lines) * line_height + url_gap

        url_color = (0, 200, 255, 255)  # cyan — readable on dark and light

        # Shadow for URL
        url_shadow = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
        url_shadow_draw = ImageDraw.Draw(url_shadow)
        url_shadow_draw.text((tx, url_y), url_text, font=body_font, fill=(0, 0, 0, 180))
        url_shadow = url_shadow.filter(ImageFilter.GaussianBlur(radius=8))
        img = Image.alpha_composite(img, url_shadow)

        # Crisp URL text
        draw = ImageDraw.Draw(img)
        draw.text((tx + 2, url_y + 2), url_text, font=body_font, fill=(0, 0, 0, 160))
        draw.text((tx, url_y), url_text, font=body_font, fill=url_color)

    return img.convert("RGB")


def render_post(blueprint):
    """
    Render all slides for a post blueprint.
    blueprint dict with keys: angle_id, images[], slides[], cta_image (optional)
    """
    tags = load_tags()
    angle_id = blueprint["angle_id"]
    slides = blueprint["slides"]
    images = blueprint["images"]
    cta_image_name = blueprint.get("cta_image")

    out_dir = OUTPUT_DIR / angle_id
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, slide in enumerate(slides):
        role = slide["role"]

        if role == "hook":
            header_text = slide.get("text", "")
            body_text = ""
        else:
            header_text = slide.get("header", "")
            body_text = slide.get("body", "")

        img_key = images[i] if i < len(images) else images[-1]

        img_path = IMAGES_DIR / img_key
        if not img_path.exists():
            # Fallback: pick a random image from the same category folder
            category = img_key.split("/")[0]
            category_dir = IMAGES_DIR / category
            available = [f.name for f in category_dir.iterdir()
                         if f.suffix.lower() in (".jpg", ".jpeg", ".png")]
            fallback = random.choice(available)
            print(f"  WARNING: {img_key} not found, using {category}/{fallback}")
            img_key = f"{category}/{fallback}"
            img_path = IMAGES_DIR / img_key

        img_tags = tags.get(img_key, {"zone": "top", "brightness": "dark"})
        zone = img_tags.get("zone", "top")
        brightness = img_tags.get("brightness", "dark")

        cta_path = None
        if role == "cta" and cta_image_name:
            cta_path = NEXTCLIP_DIR / f"{cta_image_name}.png"

        print(f"  Slide {i+1} ({role}): {img_key} [zone={zone}, brightness={brightness}]")

        result = render_slide(
            image_path=str(img_path),
            header_text=header_text,
            body_text=body_text,
            zone=zone,
            brightness=brightness,
            role=role,
            cta_image_path=str(cta_path) if cta_path else None,
            url_text=slide.get("url"),
        )

        out_path = out_dir / f"slide-{i+1}.png"
        result.save(str(out_path), "PNG")
        print(f"    -> {out_path}")

    print(f"\nDone! {len(slides)} slides saved to {out_dir}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python render.py <blueprint.json>")
        sys.exit(1)

    bp_path = sys.argv[1]
    print(f"Loading blueprint: {bp_path}")
    blueprint = load_blueprint(bp_path)
    print(f"Rendering post: {blueprint['angle_id']}")
    render_post(blueprint)


if __name__ == "__main__":
    main()
