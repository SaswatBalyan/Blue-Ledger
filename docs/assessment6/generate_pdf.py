# -*- coding: utf-8 -*-
"""
Generates Assessment_6_Project_Proposal.pdf for BCSE302P - Database Systems Lab.

Project: BlueLedger (Android / Kotlin / Jetpack Compose mangrove-reforestation
carbon-credit tracker). This script renders the Project Proposal & Database
Design Document, including vector ER and architecture diagrams, entirely with
reportlab so the output is a real, print-quality PDF (not a Markdown export).

Run:  python docs/assessment6/generate_pdf.py
Output: <repo-root>/Assessment_6_Project_Proposal.pdf
"""

import os
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    NextPageTemplate, PageBreak, Preformatted, KeepTogether, FrameBreak,
    ListFlowable, ListItem, HRFlowable
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Group, Ellipse, Circle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_PDF = os.path.join(REPO_ROOT, "Assessment_6_Project_Proposal.pdf")

# ---------------------------------------------------------------------------
# Palette (lifted from the app's own brand colors in SPLASH_IMPLEMENTATION.md)
# ---------------------------------------------------------------------------
PRIMARY_DARK = colors.HexColor("#0B3042")   # BlueLedger title color
ACCENT       = colors.HexColor("#2494C3")   # BlueLedger tagline color
ACCENT_DARK  = colors.HexColor("#2C5262")   # BlueLedger button color
LIGHT_BG     = colors.HexColor("#EAF4F9")
LIGHT_BG2    = colors.HexColor("#F5FAFC")
LINE_BLUE    = colors.HexColor("#B5D8E7")
TEXT_GREY    = colors.HexColor("#2A2A2A")
MUTED_GREY   = colors.HexColor("#6B7A80")
WHITE        = colors.white
WARN_BG      = colors.HexColor("#FFF6E5")
WARN_BORDER  = colors.HexColor("#E8A93B")
CODE_BG      = colors.HexColor("#0B3042")
CODE_TEXT    = colors.HexColor("#EAF4F9")

DOC_TITLE = "Project Proposal & Database Design Document"
DOC_SUB   = "BlueLedger — Mangrove Carbon-Credit Ledger"
COURSE    = "BCSE302P – Database Systems Lab"
SUBMIT_DATE = "29 September 2026"

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
ss = getSampleStyleSheet()

def style(name, parent, **kw):
    base = ss[parent].__dict__.copy() if isinstance(parent, str) else parent.__dict__.copy()
    base.update(kw)
    base.pop('name', None)
    return ParagraphStyle(name, **base)

H1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=17, leading=21,
                     textColor=PRIMARY_DARK, spaceBefore=4, spaceAfter=10)
H2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=12.5, leading=16,
                     textColor=ACCENT_DARK, spaceBefore=12, spaceAfter=6)
H3 = ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=10.5, leading=14,
                     textColor=PRIMARY_DARK, spaceBefore=8, spaceAfter=4)
BODY = ParagraphStyle('BODY', fontName='Times-Roman', fontSize=10, leading=14.5,
                       textColor=TEXT_GREY, alignment=TA_JUSTIFY, spaceAfter=6)
BODY_L = ParagraphStyle('BODY_L', parent=BODY, alignment=TA_LEFT)
SMALL = ParagraphStyle('SMALL', fontName='Times-Roman', fontSize=8.6, leading=11.5,
                        textColor=MUTED_GREY, alignment=TA_LEFT)
CAPTION = ParagraphStyle('CAPTION', fontName='Helvetica-Oblique', fontSize=8.6,
                          leading=11, textColor=MUTED_GREY, alignment=TA_CENTER,
                          spaceBefore=4, spaceAfter=10)
BULLET = ParagraphStyle('BULLET', parent=BODY, alignment=TA_LEFT, spaceAfter=3,
                         leftIndent=0)
CELL = ParagraphStyle('CELL', fontName='Helvetica', fontSize=8.6, leading=11.5,
                       textColor=TEXT_GREY, alignment=TA_LEFT)
CELL_HDR = ParagraphStyle('CELL_HDR', fontName='Helvetica-Bold', fontSize=8.8,
                           leading=11.5, textColor=WHITE, alignment=TA_LEFT)
CELL_MONO = ParagraphStyle('CELL_MONO', fontName='Courier', fontSize=8.2,
                            leading=11, textColor=TEXT_GREY, alignment=TA_LEFT)
TOC_TITLE = ParagraphStyle('TOC_TITLE', fontName='Helvetica-Bold', fontSize=18, leading=22,
                            textColor=PRIMARY_DARK, spaceAfter=14)

def P(text, s=BODY):
    return Paragraph(text, s)

def cell(text, mono=False):
    return Paragraph(text, CELL_MONO if mono else CELL)

def hcell(text):
    return Paragraph(text, CELL_HDR)

def section_table(data, colWidths, header=True, zebra=True):
    t = Table(data, colWidths=colWidths, repeatRows=1 if header else 0)
    cmds = [
        ('GRID', (0, 0), (-1, -1), 0.6, LINE_BLUE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    if header:
        cmds.append(('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK))
    if zebra:
        start = 1 if header else 0
        for i in range(start, len(data)):
            if (i - start) % 2 == 1:
                cmds.append(('BACKGROUND', (0, i), (-1, i), LIGHT_BG))
    t.setStyle(TableStyle(cmds))
    return t

def code_block(text):
    pre = Preformatted(text, ParagraphStyle('code', fontName='Courier', fontSize=7.8,
                                             leading=10.4, textColor=CODE_TEXT))
    t = Table([[pre]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def note_box(text):
    p = Paragraph(text, ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=8.8,
                                        leading=12, textColor=PRIMARY_DARK))
    t = Table([[p]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), WARN_BG),
        ('BOX', (0, 0), (-1, -1), 0.8, WARN_BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t

def bullets(items, style_=BULLET, bullet_char='•'):
    return ListFlowable(
        [ListItem(Paragraph(it, style_), leftIndent=0) for it in items],
        bulletType='bullet', bulletChar=bullet_char, leftIndent=14, bulletFontSize=8,
        spaceBefore=2, spaceAfter=6,
    )

def divider():
    return HRFlowable(width="100%", thickness=0.7, color=LINE_BLUE, spaceBefore=2, spaceAfter=10)

CONTENT_W = PAGE_W - 2 * MARGIN

def fit_drawing(d, target_width=None):
    """Uniformly scale a Drawing (built in its own coordinate space) so its
    reported width exactly matches the text frame width. Prevents wrap()
    width mismatches that make BaseDocTemplate.multiBuild fail to converge."""
    if target_width is None:
        target_width = CONTENT_W
    factor = target_width / float(d.width)
    d.scale(factor, factor)
    d.width = target_width
    d.height = d.height * factor
    return d


# ---------------------------------------------------------------------------
# ER Diagram (vector) -- entities, attributes, relationships, crow's-foot
# cardinality notation. Layout is computed from row counts (never hand-tuned
# pixel positions) so boxes can never overflow their attribute lists, and
# every relationship is a single straight segment aligned to a shared grid
# so no connector ever has to cross another entity's body.
# ---------------------------------------------------------------------------
HEAD_H = 21
ROW_H = 15.2
PAD_T = 9
PAD_B = 8

def ent_h(n):
    return HEAD_H + n * ROW_H + PAD_T + PAD_B

def draw_entity(d, x, y, w, h, title, attrs):
    """attrs: list of (name, descriptor, kind) where kind in {'pk','fk','plain'}."""
    shadow = Rect(x + 3.5, y - 3.5, w, h, fillColor=PRIMARY_DARK, strokeColor=None, rx=7, ry=7)
    shadow.fillOpacity = 0.12
    d.add(shadow)
    d.add(Rect(x, y, w, h, fillColor=WHITE, strokeColor=PRIMARY_DARK, strokeWidth=1.1, rx=7, ry=7))
    d.add(Rect(x, y + h - HEAD_H, w, HEAD_H, fillColor=PRIMARY_DARK, strokeColor=PRIMARY_DARK, rx=7, ry=7))
    d.add(Rect(x, y + h - HEAD_H, w, HEAD_H / 2.0, fillColor=PRIMARY_DARK, strokeColor=PRIMARY_DARK))
    d.add(Line(x + 3, y + h - HEAD_H, x + w - 3, y + h - HEAD_H, strokeColor=ACCENT, strokeWidth=1.6))
    d.add(String(x + w / 2.0, y + h - HEAD_H + 6.5, title, fontName='Helvetica-Bold',
                 fontSize=9.4, fillColor=WHITE, textAnchor='middle'))

    fsize = 7.5
    dsize = 6.7
    ry_ = y + h - HEAD_H - PAD_T - 6.5
    for name, descr, kind in attrs:
        bx = x + 13
        tx = x + 21
        if kind == 'pk':
            d.add(Circle(bx, ry_ + 2.3, 2.1, fillColor=PRIMARY_DARK, strokeColor=None))
            nfont, ncol = 'Helvetica-Bold', PRIMARY_DARK
        elif kind == 'fk':
            d.add(Polygon([bx, ry_ + 4.6, bx + 2.5, ry_ + 2.3, bx, ry_ + 0.0, bx - 2.5, ry_ + 2.3],
                          fillColor=colors.white, strokeColor=ACCENT, strokeWidth=0.9))
            nfont, ncol = 'Helvetica-Oblique', ACCENT_DARK
        else:
            nfont, ncol = 'Helvetica', TEXT_GREY
        d.add(String(tx, ry_, name, fontName=nfont, fontSize=fsize, fillColor=ncol))
        nw = stringWidth(name, nfont, fsize)
        if kind == 'pk':
            d.add(Line(tx, ry_ - 1.8, tx + nw, ry_ - 1.8, strokeColor=PRIMARY_DARK, strokeWidth=0.7))
        d.add(String(tx + nw + 4, ry_, descr, fontName='Helvetica', fontSize=dsize, fillColor=MUTED_GREY))
        ry_ -= ROW_H
    return d

def _unit(dx, dy):
    l = math.hypot(dx, dy) or 1.0
    return dx / l, dy / l

def one_tick(d, x, y, dx, dy, size=5.5, offset=10, color=ACCENT_DARK, width=1.3):
    """Crow's-foot 'one' notation: a single perpendicular tick near the entity border."""
    dx, dy = _unit(dx, dy)
    px, py = -dy, dx
    cx_, cy_ = x + dx * offset, y + dy * offset
    d.add(Line(cx_ - px * size, cy_ - py * size, cx_ + px * size, cy_ + py * size,
               strokeColor=color, strokeWidth=width))

def crows_foot(d, x, y, dx, dy, spread=6.2, length=13, color=ACCENT_DARK, width=1.3):
    """Crow's-foot 'many' notation: a three-pronged fork converging on the entity border."""
    dx, dy = _unit(dx, dy)
    px, py = -dy, dx
    base_x, base_y = x + dx * length, y + dy * length
    left = (x + dx * length * 0.5 + px * spread, y + dy * length * 0.5 + py * spread)
    right = (x + dx * length * 0.5 - px * spread, y + dy * length * 0.5 - py * spread)
    d.add(Line(x, y, base_x, base_y, strokeColor=color, strokeWidth=width))
    d.add(Line(x, y, left[0], left[1], strokeColor=color, strokeWidth=width))
    d.add(Line(x, y, right[0], right[1], strokeColor=color, strokeWidth=width))

def rel_label(d, x, y, text, color=MUTED_GREY, anchor='start'):
    d.add(String(x, y - 2.6, text, fontName='Helvetica-Oblique', fontSize=7.6,
                 fillColor=color, textAnchor=anchor))

def relationship(d, x1, y1, x2, y2, one_dir, many_dir, label, label_pos, label_anchor='start', color=ACCENT_DARK):
    """A single straight connector (no elbow) between a 'one' endpoint (x1,y1)
    and a 'many' endpoint (x2,y2), decorated with crow's-foot notation."""
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.2))
    one_tick(d, x1, y1, *one_dir, color=color)
    crows_foot(d, x2, y2, *many_dir, color=color)
    rel_label(d, label_pos[0], label_pos[1], label, anchor=label_anchor)

def build_er_diagram():
    community_attrs = [
        ("community_id", ": INTEGER", 'pk'),
        ("name", ": TEXT · UNIQUE, NOT NULL", 'plain'),
        ("region", ": TEXT", 'plain'),
        ("enrolled_at", ": DATETIME", 'plain'),
    ]
    user_attrs = [
        ("user_id", ": INTEGER", 'pk'),
        ("email", ": TEXT · UNIQUE, NOT NULL", 'plain'),
        ("username", ": TEXT · NOT NULL", 'plain'),
        ("phone", ": TEXT", 'plain'),
        ("password_hash", ": TEXT · NOT NULL", 'plain'),
        ("community_id", ": INTEGER · NULL", 'fk'),
        ("created_at", ": DATETIME", 'plain'),
    ]
    species_attrs = [
        ("species_id", ": INTEGER", 'pk'),
        ("common_name", ": TEXT · UNIQUE", 'plain'),
        ("credit_rate_per_ha", ": DECIMAL(5,2)", 'plain'),
        ("description", ": TEXT", 'plain'),
    ]
    project_attrs = [
        ("project_id", ": INTEGER", 'pk'),
        ("plot_id", ": TEXT · NOT NULL", 'plain'),
        ("user_id", ": INTEGER · NOT NULL", 'fk'),
        ("species_id", ": INTEGER · NOT NULL", 'fk'),
        ("hectares", ": DECIMAL(6,2)", 'plain'),
        ("gps_lat", ": DECIMAL(9,6)", 'plain'),
        ("gps_lng", ": DECIMAL(9,6)", 'plain'),
        ("image_uri", ": TEXT · NULL", 'plain'),
        ("status", ": TEXT · CHECK", 'plain'),
        ("created_at", ": DATETIME", 'plain'),
    ]
    txn_attrs = [
        ("transaction_id", ": INTEGER", 'pk'),
        ("project_id", ": INTEGER · NULL", 'fk'),
        ("user_id", ": INTEGER · NOT NULL", 'fk'),
        ("txn_type", ": TEXT · CHECK", 'plain'),
        ("credit_amount", ": INTEGER · CHECK<>0", 'plain'),
        ("bonus_multiplier", ": DECIMAL(3,2)", 'plain'),
        ("txn_timestamp", ": DATETIME", 'plain'),
    ]

    # ---- layout: two aligned columns + a centered bottom entity, spaced on
    # ---- one consistent 40pt grid gutter both horizontally and vertically.
    W = 500
    GUTTER = 40
    col1_x, col1_w = 12, 208
    col2_x, col2_w = col1_x + col1_w + GUTTER, 220
    txn_w = 236

    community_h, species_h = ent_h(len(community_attrs)), ent_h(len(species_attrs))
    user_h, project_h = ent_h(len(user_attrs)), ent_h(len(project_attrs))
    txn_h = ent_h(len(txn_attrs))

    txn_y = 14
    row_b_top = txn_y + txn_h + GUTTER + project_h  # shared top edge of USER & PROJECT
    project_y = row_b_top - project_h
    user_y = row_b_top - user_h
    row_a_y = row_b_top + GUTTER  # shared bottom edge of COMMUNITY & SPECIES
    community_y = species_y = row_a_y
    H = row_a_y + max(community_h, species_h) + 16

    community_x, species_x = col1_x, col2_x
    user_x, project_x = col1_x, col2_x
    txn_x = (W - txn_w) / 2.0

    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=LIGHT_BG2, strokeColor=None))

    draw_entity(d, community_x, community_y, col1_w, community_h, "COMMUNITY", community_attrs)
    draw_entity(d, species_x, species_y, col2_w, species_h, "SPECIES", species_attrs)
    draw_entity(d, user_x, user_y, col1_w, user_h, "USER", user_attrs)
    draw_entity(d, project_x, project_y, col2_w, project_h, "PROJECT", project_attrs)
    draw_entity(d, txn_x, txn_y, txn_w, txn_h, "CREDIT_TRANSACTION", txn_attrs)

    # COMMUNITY (1) -> USER (M), straight vertical, shared column
    ex = community_x + 46
    relationship(d, ex, community_y, ex, user_y + user_h,
                 one_dir=(0, -1), many_dir=(0, 1), label="enrolls",
                 label_pos=(ex + 10, (community_y + user_y + user_h) / 2.0))

    # USER (1) -> PROJECT (M), straight horizontal, shared row-top band
    uy_line = row_b_top - 24
    relationship(d, user_x + col1_w, uy_line, project_x, uy_line,
                 one_dir=(1, 0), many_dir=(-1, 0), label="uploads",
                 label_pos=((user_x + col1_w + project_x) / 2.0, uy_line + 9), label_anchor='middle')

    # SPECIES (1) -> PROJECT (M), straight vertical, shared column
    sx = species_x + col2_w - 40
    relationship(d, sx, species_y, sx, project_y + project_h,
                 one_dir=(0, -1), many_dir=(0, 1), label="classified as",
                 label_pos=(sx + 10, (species_y + project_y + project_h) / 2.0))

    # PROJECT (1) -> CREDIT_TRANSACTION (M), straight vertical, overlapping x-range
    px_ = max(project_x + 40, txn_x + 30)
    relationship(d, px_, project_y, px_, txn_y + txn_h,
                 one_dir=(0, -1), many_dir=(0, 1), label="generates",
                 label_pos=(px_ + 10, (project_y + txn_y + txn_h) / 2.0))

    # USER (1) -> CREDIT_TRANSACTION (M), straight vertical, overlapping x-range
    ux_ = min(user_x + col1_w - 30, txn_x + 30)
    relationship(d, ux_, user_y, ux_, txn_y + txn_h,
                 one_dir=(0, -1), many_dir=(0, 1), label="owns",
                 label_pos=(ux_ + 10, (user_y + txn_y + txn_h) / 2.0))

    # Legend: draw the actual notation marks rather than describing them in words
    lx, ly = 14, H - 12
    d.add(Line(lx, ly, lx + 16, ly, strokeColor=ACCENT_DARK, strokeWidth=1.2))
    one_tick(d, lx, ly, 1, 0, offset=8)
    d.add(String(lx + 22, ly - 3, "one", fontName='Helvetica', fontSize=7.4, fillColor=MUTED_GREY))
    lx2 = lx + 56
    d.add(Line(lx2, ly, lx2 + 16, ly, strokeColor=ACCENT_DARK, strokeWidth=1.2))
    crows_foot(d, lx2 + 16, ly, 1, 0)
    d.add(String(lx2 + 40, ly - 3, "many", fontName='Helvetica', fontSize=7.4, fillColor=MUTED_GREY))
    lx3 = lx2 + 88
    d.add(Circle(lx3, ly + 0.3, 2.1, fillColor=PRIMARY_DARK, strokeColor=None))
    d.add(String(lx3 + 7, ly - 3, "PK (underlined)", fontName='Helvetica-Oblique', fontSize=7.4,
                 fillColor=MUTED_GREY))
    lx4 = lx3 + 92
    d.add(Polygon([lx4, ly + 2.3, lx4 + 2.5, ly, lx4, ly - 2.3, lx4 - 2.5, ly],
                  fillColor=colors.white, strokeColor=ACCENT, strokeWidth=0.9))
    d.add(String(lx4 + 7, ly - 3, "FK (italic)", fontName='Helvetica-Oblique', fontSize=7.4,
                 fillColor=MUTED_GREY))
    return d

# ---------------------------------------------------------------------------
# System Architecture Diagram (vector) -- a left-to-right pipeline matching
# the assessment's required flow (Users -> Application/System -> Database ->
# Output), drawn as the real mechanism rather than a generic stack of equal
# boxes: each stage carries the icon/detail that shows what it actually does.
# ---------------------------------------------------------------------------
def arrow_head(d, x, y, direction='right', color=ACCENT_DARK, size=5):
    if direction == 'right':
        pts = [x - size, y - size, x - size, y + size, x, y]
    elif direction == 'left':
        pts = [x + size, y - size, x + size, y + size, x, y]
    elif direction == 'down':
        pts = [x - size, y + size, x + size, y + size, x, y]
    else:
        pts = [x - size, y - size, x + size, y - size, x, y]
    d.add(Polygon(pts, fillColor=color, strokeColor=color))

def stage_shell(d, x, y, w, h, title, fill=LIGHT_BG):
    shadow = Rect(x + 3, y - 3, w, h, fillColor=PRIMARY_DARK, strokeColor=None, rx=8, ry=8)
    shadow.fillOpacity = 0.10
    d.add(shadow)
    d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=PRIMARY_DARK, strokeWidth=1.2, rx=8, ry=8))
    d.add(String(x + w / 2.0, y + h - 15, title, fontName='Helvetica-Bold', fontSize=8.6,
                 fillColor=PRIMARY_DARK, textAnchor='middle'))
    d.add(Line(x + 12, y + h - 20, x + w - 12, y + h - 20, strokeColor=ACCENT, strokeWidth=1.1))

def draw_phone_icon(d, cx, cy, h=42):
    w = h * 0.5
    x, y = cx - w / 2.0, cy - h / 2.0
    d.add(Rect(x, y, w, h, fillColor=WHITE, strokeColor=PRIMARY_DARK, strokeWidth=1.3, rx=4, ry=4))
    d.add(Rect(x + w * 0.10, y + h * 0.13, w * 0.80, h * 0.68, fillColor=LIGHT_BG,
               strokeColor=PRIMARY_DARK, strokeWidth=0.6, rx=1.5, ry=1.5))
    d.add(Circle(cx, y + h * 0.06, h * 0.03, fillColor=PRIMARY_DARK, strokeColor=None))

def draw_cylinder(d, x, y, w, h, fill=ACCENT_DARK, border=PRIMARY_DARK, bw=1.3):
    rx, ry = w / 2.0, h * 0.16
    cx = x + w / 2.0
    bot_cy, top_cy = y + ry, y + h - ry
    d.add(Rect(x, bot_cy, w, top_cy - bot_cy, fillColor=fill, strokeColor=None))
    d.add(Ellipse(cx, bot_cy, rx, ry, fillColor=fill, strokeColor=border, strokeWidth=bw))
    d.add(Line(x, bot_cy, x, top_cy, strokeColor=border, strokeWidth=bw))
    d.add(Line(x + w, bot_cy, x + w, top_cy, strokeColor=border, strokeWidth=bw))
    d.add(Ellipse(cx, top_cy, rx, ry, fillColor=fill, strokeColor=border, strokeWidth=bw))

def draw_barchart_icon(d, cx, cy, w=34, h=26, color=ACCENT):
    heights = [0.35, 0.65, 1.0, 0.5]
    n = len(heights)
    bw = w / (n * 1.6)
    x0 = cx - w / 2.0
    base = cy - h / 2.0
    for i, f in enumerate(heights):
        bx = x0 + i * (w / n)
        d.add(Rect(bx, base, bw, h * f, fillColor=color, strokeColor=None, rx=0.8, ry=0.8))
    d.add(Line(x0 - 2, base, x0 + w + 2, base, strokeColor=PRIMARY_DARK, strokeWidth=0.9))

def flow_arrow(d, x1, x2, y, label_top=None, label_bottom=None, color=ACCENT_DARK, two_way=False):
    d.add(Line(x1, y, x2, y, strokeColor=color, strokeWidth=1.4))
    arrow_head(d, x2, y, 'right', color, size=4.6)
    if two_way:
        d.add(Line(x1, y - 13, x2, y - 13, strokeColor=MUTED_GREY, strokeWidth=1.0))
        arrow_head(d, x1, y - 13, 'left', MUTED_GREY, size=3.8)
    if label_top:
        d.add(String((x1 + x2) / 2.0, y + 7, label_top, fontName='Helvetica-Oblique',
                     fontSize=6.1, fillColor=color, textAnchor='middle'))
    if label_bottom:
        d.add(String((x1 + x2) / 2.0, y - 25, label_bottom, fontName='Helvetica-Oblique',
                     fontSize=6.1, fillColor=MUTED_GREY, textAnchor='middle'))

def build_architecture_diagram():
    W, H = 580, 300
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=LIGHT_BG2, strokeColor=None))

    stage_w, stage_h, gap = 104, 195, 48
    total = 4 * stage_w + 3 * gap
    x0 = (W - total) / 2.0
    y0 = 70
    xs = [x0 + i * (stage_w + gap) for i in range(4)]
    mid_y = y0 + stage_h * 0.55

    # ---- Stage 1: USER ----
    stage_shell(d, xs[0], y0, stage_w, stage_h, "USER")
    draw_phone_icon(d, xs[0] + stage_w / 2.0, y0 + stage_h * 0.56)
    d.add(String(xs[0] + stage_w / 2.0, y0 + 18, "Field agent /", fontName='Helvetica',
                 fontSize=6.6, fillColor=MUTED_GREY, textAnchor='middle'))
    d.add(String(xs[0] + stage_w / 2.0, y0 + 9, "planter", fontName='Helvetica',
                 fontSize=6.6, fillColor=MUTED_GREY, textAnchor='middle'))

    # ---- Stage 2: APPLICATION / SYSTEM (shows its internal layers) ----
    stage_shell(d, xs[1], y0, stage_w, stage_h, "APPLICATION")
    inner = [("Presentation", "Compose UI"), ("State", "ViewModels"), ("Data access", "Repositories")]
    row_h, row_gap = 34, 6
    top = y0 + stage_h - 26
    for i, (t, s) in enumerate(inner):
        ry = top - i * (row_h + row_gap) - row_h
        d.add(Rect(xs[1] + 9, ry, stage_w - 18, row_h, fillColor=WHITE, strokeColor=LINE_BLUE,
                   strokeWidth=1, rx=4, ry=4))
        d.add(String(xs[1] + stage_w / 2.0, ry + row_h - 12, t, fontName='Helvetica-Bold',
                     fontSize=6.8, fillColor=PRIMARY_DARK, textAnchor='middle'))
        d.add(String(xs[1] + stage_w / 2.0, ry + 6, s, fontName='Helvetica',
                     fontSize=6.0, fillColor=MUTED_GREY, textAnchor='middle'))
        if i > 0:
            ay = ry + row_h + row_gap
            d.add(Line(xs[1] + stage_w / 2.0, ay, xs[1] + stage_w / 2.0, ay - row_gap + 1,
                       strokeColor=ACCENT_DARK, strokeWidth=1))
            arrow_head(d, xs[1] + stage_w / 2.0, ay - row_gap + 1, 'down', ACCENT_DARK, size=2.6)

    # ---- Stage 3: DATABASE (cylinder + table chips = the real schema) ----
    stage_shell(d, xs[2], y0, stage_w, stage_h, "DATABASE")
    cyl_w, cyl_h = 64, 78
    cyl_x = xs[2] + (stage_w - cyl_w) / 2.0
    cyl_y = y0 + stage_h - 26 - cyl_h
    draw_cylinder(d, cyl_x, cyl_y, cyl_w, cyl_h, fill=ACCENT_DARK, border=PRIMARY_DARK)
    d.add(String(cyl_x + cyl_w / 2.0, cyl_y + cyl_h / 2.0 - 3, "SQLite", fontName='Helvetica-Bold',
                 fontSize=7.2, fillColor=WHITE, textAnchor='middle'))
    chips = ["User", "Community", "Species", "Project", "CreditTxn"]
    chip_y = cyl_y - 14
    for i, c in enumerate(chips):
        cy_ = chip_y - i * 11
        d.add(Circle(xs[2] + 12, cy_ + 2, 1.6, fillColor=ACCENT_DARK, strokeColor=None))
        d.add(String(xs[2] + 18, cy_ - 1, c, fontName='Helvetica', fontSize=6.3,
                     fillColor=TEXT_GREY, textAnchor='start'))

    # ---- Stage 4: OUTPUT ----
    stage_shell(d, xs[3], y0, stage_w, stage_h, "OUTPUT")
    draw_barchart_icon(d, xs[3] + stage_w / 2.0, y0 + stage_h * 0.60)
    for i, t in enumerate(["Dashboard", "Wallet ledger", "Reports"]):
        d.add(String(xs[3] + stage_w / 2.0, y0 + 34 - i * 10, t, fontName='Helvetica',
                     fontSize=6.6, fillColor=TEXT_GREY, textAnchor='middle'))

    # ---- Flow arrows between stages, each labeled with the real mechanism ----
    flow_arrow(d, xs[0] + stage_w, xs[1], mid_y,
               label_top="submits data", label_bottom="renders UI", two_way=True)
    flow_arrow(d, xs[1] + stage_w, xs[2], mid_y,
               label_top="writes (txn)", label_bottom="reads (SQL)", two_way=True)
    flow_arrow(d, xs[2] + stage_w, xs[3], mid_y,
               label_top="results", two_way=False)

    # ---- Device inputs feeding the Application stage from below ----
    in_w, in_h = 150, 34
    in_x = xs[1] + stage_w / 2.0 - in_w / 2.0
    in_y = 10
    d.add(Rect(in_x, in_y, in_w, in_h, fillColor=WHITE, strokeColor=LINE_BLUE, strokeWidth=1, rx=5, ry=5))
    d.add(String(in_x + in_w / 2.0, in_y + in_h - 13, "Device inputs", fontName='Helvetica-Bold',
                 fontSize=6.8, fillColor=ACCENT_DARK, textAnchor='middle'))
    d.add(String(in_x + in_w / 2.0, in_y + 6, "GPS fix  ·  plot photo", fontName='Helvetica',
                 fontSize=6.2, fillColor=MUTED_GREY, textAnchor='middle'))
    d.add(Line(xs[1] + stage_w / 2.0, in_y + in_h, xs[1] + stage_w / 2.0, y0 - 6,
               strokeColor=LINE_BLUE, strokeWidth=1.2))
    arrow_head(d, xs[1] + stage_w / 2.0, y0 - 6, 'up', LINE_BLUE, size=4)
    d.add(String(xs[1] + stage_w / 2.0 + 8, (in_y + in_h + y0) / 2.0 - 3, "captured on upload",
                 fontName='Helvetica-Oblique', fontSize=6.2, fillColor=MUTED_GREY, textAnchor='start'))

    return d


# ---------------------------------------------------------------------------
# Header / Footer + TOC-aware document template
# ---------------------------------------------------------------------------
class DocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        self._bm = 0

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            txt = flowable.getPlainText()
            sname = flowable.style.name
            if sname == 'H1':
                key = 'bm-%s' % abs(hash(txt))
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(txt, key, level=0, closed=False)
                self.notify('TOCEntry', (0, txt, self.page))
            elif sname == 'H2':
                key = 'bm-%s' % abs(hash(txt))
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(txt, key, level=1, closed=False)
                self.notify('TOCEntry', (1, txt, self.page))


def draw_chrome(canv, doc, is_cover=False, is_toc=False):
    canv.saveState()
    if is_cover:
        canv.restoreState()
        return
    # Header
    canv.setStrokeColor(LINE_BLUE)
    canv.setLineWidth(0.8)
    canv.line(MARGIN, PAGE_H - 14 * mm, PAGE_W - MARGIN, PAGE_H - 14 * mm)
    canv.setFont('Helvetica-Bold', 8.2)
    canv.setFillColor(PRIMARY_DARK)
    canv.drawString(MARGIN, PAGE_H - 12.2 * mm, COURSE)
    canv.setFont('Helvetica', 8.2)
    canv.setFillColor(MUTED_GREY)
    canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 12.2 * mm, DOC_TITLE)
    # Footer
    canv.setStrokeColor(LINE_BLUE)
    canv.line(MARGIN, 13 * mm, PAGE_W - MARGIN, 13 * mm)
    canv.setFont('Helvetica', 8)
    canv.setFillColor(MUTED_GREY)
    canv.drawString(MARGIN, 9.5 * mm, "BlueLedger — Assessment 6")
    canv.drawCentredString(PAGE_W / 2.0, 9.5 * mm, "Page %d" % canv.getPageNumber())
    canv.drawRightString(PAGE_W - MARGIN, 9.5 * mm, SUBMIT_DATE)
    canv.restoreState()


def on_cover(canv, doc):
    draw_chrome(canv, doc, is_cover=True)


def on_page(canv, doc):
    draw_chrome(canv, doc)


def build():
    doc = DocTemplate(OUT_PDF, pagesize=A4,
                       leftMargin=MARGIN, rightMargin=MARGIN,
                       topMargin=22 * mm, bottomMargin=18 * mm,
                       title=DOC_TITLE, author="BCSE302P Student Submission")

    frame_cover = Frame(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN, id='cover')
    frame_normal = Frame(MARGIN, 18 * mm, PAGE_W - 2 * MARGIN, PAGE_H - 22 * mm - 18 * mm, id='normal')

    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[frame_cover], onPage=on_cover),
        PageTemplate(id='Normal', frames=[frame_normal], onPage=on_page),
    ])

    story = []

    # ---------------- COVER PAGE ----------------
    story.append(Spacer(1, 18 * mm))
    cover_band = Table([['']], colWidths=[PAGE_W - 2 * MARGIN], rowHeights=[3])
    cover_band.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), ACCENT)]))
    story.append(cover_band)
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(COURSE, ParagraphStyle('c1', fontName='Helvetica-Bold', fontSize=14, leading=18,
                                                    textColor=MUTED_GREY, alignment=TA_CENTER, spaceAfter=6)))
    story.append(Paragraph("D2 Slot – L11+L12", ParagraphStyle('c1b', fontName='Helvetica', fontSize=10.5, leading=14,
                                                    textColor=MUTED_GREY, alignment=TA_CENTER, spaceAfter=26)))
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph("BlueLedger", ParagraphStyle('c2', fontName='Helvetica-Bold', fontSize=34, leading=40,
                                                          textColor=PRIMARY_DARK, alignment=TA_CENTER, spaceAfter=8)))
    story.append(Paragraph("Community Mangrove Reforestation &amp; Carbon-Credit Ledger",
                            ParagraphStyle('c2b', fontName='Helvetica-Oblique', fontSize=13, leading=17,
                                           textColor=ACCENT, alignment=TA_CENTER, spaceAfter=30)))
    story.append(Spacer(1, 18 * mm))
    story.append(Paragraph(DOC_TITLE, ParagraphStyle('c3', fontName='Helvetica-Bold', fontSize=19, leading=24,
                                                       textColor=WHITE, alignment=TA_CENTER, spaceAfter=0,
                                                       backColor=PRIMARY_DARK, borderPadding=12)))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Assessment 6  —  10 Marks", ParagraphStyle('c4', fontName='Helvetica-Bold',
                                                       fontSize=11.5, leading=15, textColor=ACCENT_DARK, alignment=TA_CENTER,
                                                       spaceAfter=40)))

    meta_rows = [
        [Paragraph('<b>Course</b>', CELL), Paragraph('BCSE302P – Database Systems Lab', CELL)],
        [Paragraph('<b>Submission</b>', CELL), Paragraph('1 of 3 — Project Proposal &amp; Database Design Document', CELL)],
        [Paragraph('<b>Submission Date</b>', CELL), Paragraph(SUBMIT_DATE, CELL)],
        [Paragraph('<b>Repository</b>', CELL), Paragraph('Blue-Ledger (GitHub) — Android / Kotlin / Jetpack Compose', CELL)],
        [Paragraph('<b>Student Name</b>', CELL), Paragraph('[ To be filled by student ]', CELL)],
        [Paragraph('<b>Registration Number</b>', CELL), Paragraph('[ To be filled by student ]', CELL)],
        [Paragraph('<b>Faculty In-Charge</b>', CELL), Paragraph('[ To be filled by student ]', CELL)],
    ]
    meta_tbl = Table(meta_rows, colWidths=[45 * mm, PAGE_W - 2 * MARGIN - 45 * mm])
    meta_tbl.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, LINE_BLUE),
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_BG),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 14 * mm))
    story.append(Paragraph(
        "This document has been generated by analysing the actual BlueLedger Android codebase "
        "(Kotlin, Jetpack Compose, DataStore) and proposes the database design required to satisfy "
        "BCSE302P Assessment 6. Fields shown in brackets are left for the student to complete.",
        ParagraphStyle('disc', fontName='Times-Italic', fontSize=9, textColor=MUTED_GREY,
                       alignment=TA_CENTER)))

    story.append(NextPageTemplate('Normal'))
    story.append(PageBreak())

    # ---------------- TABLE OF CONTENTS ----------------
    story.append(Paragraph("Table of Contents", TOC_TITLE))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle('TOC1', fontName='Helvetica-Bold', fontSize=10.5, leading=16,
                       textColor=PRIMARY_DARK, leftIndent=0),
        ParagraphStyle('TOC2', fontName='Helvetica', fontSize=9.5, leading=14,
                       textColor=TEXT_GREY, leftIndent=14),
    ]
    story.append(toc)
    story.append(PageBreak())

    # ================= 1. PROJECT TITLE =================
    story.append(Paragraph("1. Project Title", H1))
    story.append(note_box(
        "<b>BlueLedger: A Relational Database System for Verified Mangrove Reforestation "
        "Tracking and Carbon-Credit Accounting</b>"))
    story.append(P(
        "BlueLedger is an existing offline-first Android application (Kotlin, Jetpack Compose) that lets "
        "field users record mangrove-planting plots and automatically computes carbon credits for them. "
        "This document proposes adapting its ad-hoc local storage into a proper relational database so the "
        "same real-world workflow gains referential integrity, auditable transactions, and queryable history."))
    story.append(divider())

    # ================= 2. INTRODUCTION =================
    story.append(Paragraph("2. Introduction and Background", H1))
    story.append(P(
        "Mangrove forests are among the most effective natural carbon sinks, and community-driven "
        "reforestation programs increasingly rely on digital tools to record planting activity and convert "
        "verified effort into tradable carbon credits. <b>BlueLedger</b> (this repository) is an Android "
        "application built for exactly this purpose: field users log in, record a planting plot (GPS location, "
        "species, area in hectares, photo evidence), and the app computes a carbon-credit amount using a "
        "species-specific per-hectare rate with area-based bonus multipliers."))
    story.append(P(
        "The application already implements a working mobile UI (splash, onboarding, login/signup, a four-tab "
        "home screen – Dashboard, Upload, Wallet, Profile), device GPS capture, an image picker for plot "
        "evidence, and a deterministic carbon-credit formula. However, as documented in the project's own "
        "development notes, it has <b>no real database</b>: all data is serialized into unstructured text and "
        "held in the device's local application storage. This document treats that gap as the starting point for "
        "the required database design work."))
    story.append(divider())

    # ================= 3. PROBLEM STATEMENT =================
    story.append(Paragraph("3. Problem Statement", H1))
    story.append(P(
        "Community reforestation programs need a trustworthy, auditable record of who planted what, where, "
        "and how many carbon credits that effort is worth. In the current BlueLedger implementation this record "
        "is fragile by construction:"))
    story.append(bullets([
        "<b>No relational structure.</b> The application currently keeps the entire list of planting projects as "
        "one block of unstructured text, and the current user's details as another single block. There is no "
        "per-record identity the storage understands, no foreign keys, and no way to query a subset of records "
        "without loading everything into memory first.",
        "<b>Unsafe concurrent writes.</b> Adding a new plot means reading the whole project list, appending one "
        "entry in memory, and writing the whole list back. Two near-simultaneous submissions can race and "
        "silently overwrite each other — there is no transactional guarantee.",
        "<b>Business rules hidden in code, not data.</b> The species-to-carbon-rate mapping (Rhizophora = 14, "
        "Avicennia = 12, Bruguiera = 10 credits/hectare) is hardcoded into the app's logic rather than stored as "
        "data. Adding a species or correcting a rate requires a new app release, and there is no historical "
        "record of which rate was in effect when a given credit was minted.",
        "<b>No audit trail for credits.</b> The minted-credit amount is baked directly into each project record "
        "at upload time. There is no separate ledger of mint/redeem events, so a future credit-redemption feature "
        "cannot be implemented safely.",
        "<b>Single-user, unauthenticated storage.</b> Login/signup currently accepts any non-empty credentials "
        "and stores exactly one user record per device — there is no user table, no password verification, and "
        "no way for a plot to be attributed to a specific verified contributor.",
    ]))
    story.append(P(
        "A structured database directly addresses each of these problems: it gives every plot, user, species "
        "rate, and credit event a durable, constrained, queryable identity, and lets the minting rule live as "
        "data rather than as compiled logic."))
    story.append(divider())

    # ================= 4. OBJECTIVES =================
    story.append(Paragraph("4. Objectives", H1))
    story.append(bullets([
        "Replace the current unstructured, single-block storage of user and project data with a normalized "
        "relational schema (five tables) accessed through a proper embedded database, without changing the "
        "app's existing screens, navigation, or carbon-credit formula.",
        "Enforce referential integrity with primary/foreign-key constraints so no <i>Project</i> can reference a "
        "non-existent <i>User</i> or <i>Species</i>, and no <i>CreditTransaction</i> can reference a non-existent "
        "<i>Project</i>.",
        "Externalize the species-to-credit-rate mapping (currently hardcoded into the app's logic) into a "
        "queryable <i>Species</i> reference table.",
        "Introduce an append-only <i>CreditTransaction</i> ledger so minted and (future) redeemed credits form an "
        "auditable history, independent of the current wallet balance shown on screen.",
        "Support indexed, filterable queries (by user, species, status, date range) so the Dashboard and Wallet "
        "screens no longer need to load the entire upload history into memory on every screen open.",
        "Document the schema to at least Third Normal Form (3NF) with a concrete example drawn from this "
        "project's own data (the species-rate transitive dependency).",
    ]))
    story.append(divider())

    # ================= 5. SCOPE =================
    story.append(Paragraph("5. Scope of the Project", H1))

    scope_data = [
        [hcell("Category"), hcell("Items")],
        [cell("<b>Already implemented</b><br/>(existing application, unchanged)"),
         cell("Mobile UI: splash, onboarding, login/signup, Dashboard/Upload/Wallet/Profile screens · "
              "in-app navigation · GPS capture for plot location · image picker for plot photos · the "
              "carbon-credit calculation formula (species rate × hectares × area bonus) · saved “remember me” "
              "and language preference")],
        [cell("<b>Included in this proposal</b><br/>(database-design scope)"),
         cell("Relational schema for User, Community, Species, Project and CreditTransaction · a proper "
              "database layer replacing the current unstructured local storage · CRUD operations backed by SQL · "
              "aggregate queries for Dashboard/Wallet totals · project verification status field")],
        [cell("<b>Existing features that the new schema must not break</b>"),
         cell("The species-selection dropdown on the Upload screen, the bonus-multiplier rule "
              "(&ge;10 ha &rarr; 1.2×, &ge;5 ha &rarr; 1.1×), and the wallet-summary figures shown on the "
              "Wallet screen")],
        [cell("<b>Excluded from current scope</b>"),
         cell("Cloud/server backend and network sync · blockchain-based credit minting · real payment or "
              "credit-redemption processing · a dedicated admin/verifier screen (the schema reserves a status "
              "field for this, but building the review screen is future work) · multi-device data "
              "synchronization")],
    ]
    story.append(section_table(scope_data, colWidths=[42 * mm, PAGE_W - 2 * MARGIN - 42 * mm]))
    story.append(divider())

    # ================= 6. REQUIREMENT ANALYSIS =================
    story.append(Paragraph("6. Requirement Analysis", H1))
    story.append(Paragraph("6.1 Functional Requirements", H2))

    story.append(Paragraph("User roles", H3))
    story.append(bullets([
        "<b>Registered Contributor</b> (implemented today as a mock login): creates an account, submits planting "
        "projects, views their own dashboard and wallet.",
        "<b>Verifier / Admin</b> (proposed, enabled by a status field on each project but out of scope to build "
        "a screen for in this phase): would approve or reject submitted projects before credits are minted.",
    ]))

    story.append(Paragraph("Data to be stored", H3))
    story.append(bullets([
        "User accounts (email, username, phone, credentials, optional community membership)",
        "Communities/cooperatives enrolled in the program",
        "Reference data for mangrove species and their carbon-credit rate per hectare",
        "Planting projects (plot id, species, hectares, GPS coordinates, photo evidence, verification status)",
        "An append-only ledger of credit-minting and credit-redemption events",
    ]))

    story.append(Paragraph("CRUD operations required", H3))
    crud_data = [
        [hcell("Entity"), hcell("Create"), hcell("Read"), hcell("Update"), hcell("Delete")],
        [cell("User"), cell("Sign up"), cell("Login / profile view"), cell("Edit profile"), cell("Not exposed (retain audit trail)")],
        [cell("Community"), cell("Program admin enrolls a community"), cell("Dashboard “total communities” stat"), cell("Update region/name"), cell("Rare / admin-only")],
        [cell("Species"), cell("Seed reference rows"), cell("Populate species dropdown"), cell("Adjust credit rate"), cell("Not exposed (rates are historical)")],
        [cell("Project"), cell("Upload screen → new plot"), cell("Dashboard / Wallet history"), cell("Edit before verification"), cell("Delete a draft/pending project")],
        [cell("CreditTransaction"), cell("System-generated on mint / redeem"), cell("Wallet ledger view"), cell("Immutable (append-only)"), cell("Never deleted (audit requirement)")],
    ]
    story.append(section_table(crud_data, colWidths=[26*mm, 32*mm, 32*mm, 32*mm, 32*mm]))

    story.append(Paragraph("Data retrieval, filtering, relationships and reporting", H3))
    story.append(bullets([
        "Filter a user's projects by species, verification status, or date range.",
        "Sort a user's credit-transaction history chronologically (Wallet screen).",
        "Look up a project's species rate <i>at the time it was planted</i> via the Species reference table, "
        "rather than recomputing it from constants buried in application logic.",
        "Insert a Project and its initial MINT CreditTransaction as a single atomic transaction so credits can "
        "never exist without a backing project.",
        "Aggregate totals: SUM(credit_amount) per user (wallet balance), SUM(hectares) per user or per species, "
        "COUNT(projects) per community, for the Dashboard's headline metrics.",
    ]))

    story.append(Paragraph("6.2 Non-Functional Requirements", H2))
    nfr_data = [
        [hcell("Quality"), hcell("Requirement, tied to an observed gap in the current system")],
        [cell("<b>Performance</b>"), cell("Indexed foreign keys give fast, targeted lookups for wallet/dashboard queries, replacing the "
                                          "current approach of loading the entire upload history into memory on every screen open.")],
        [cell("<b>Data integrity</b>"), cell("NOT NULL, CHECK and foreign-key constraints replace today's unchecked fields — e.g. nothing "
                                             "currently stops a negative hectares value or an arbitrary species name from being stored.")],
        [cell("<b>Security</b>"), cell("A password-hash column and real credential verification replace the current mock login, which "
                                       "accepts any non-empty password.")],
        [cell("<b>Scalability</b>"), cell("A relational table scales to thousands of rows per user without the "
                                          "read-entire-list-then-rewrite-entire-list pattern the app currently uses for every single "
                                          "upload.")],
        [cell("<b>Reliability</b>"), cell("Database transactions remove the race condition in the current upload flow (read-then-write "
                                          "is not atomic today), where two concurrent uploads could overwrite each other.")],
    ]
    story.append(section_table(nfr_data, colWidths=[30*mm, PAGE_W - 2*MARGIN - 30*mm]))
    story.append(divider())

    # ================= 7. DATABASE SELECTION =================
    story.append(Paragraph("7. Database Selection and Justification", H1))
    story.append(note_box(
        "<b>Selected technology: SQLite, accessed through the Android Room Persistence Library</b> "
        "&mdash; an embedded relational database."))
    story.append(P(
        "<b>Why Room/SQLite fits this specific project</b> (not chosen by default, but because the project's own "
        "characteristics point to it):"))
    story.append(bullets([
        "<b>Already the intended direction for this app.</b> The project's build configuration already lists the "
        "Room persistence library as a dependency, and the codebase documents it as \"prepared for future use.\" "
        "Adopting it is the change with the least unnecessary restructuring, matching the assessment's "
        "instruction to prioritise modifications with the most DBMS relevance for the least disruption.",
        "<b>The app is offline-first by design.</b> BlueLedger is explicitly built around local, offline data "
        "persistence with no backend server. A cloud document store (Firestore, MongoDB Realm) would introduce a "
        "network dependency the product does not currently have; an embedded relational engine keeps that design "
        "intact.",
        "<b>The data is inherently relational, not document-shaped.</b> A User has many Projects; a Project "
        "references exactly one Species; a Project generates many CreditTransactions. These are clean one-to-many "
        "foreign-key relationships with a fixed, shallow shape &mdash; not deeply nested or schema-varying "
        "documents that would benefit from a document model.",
        "<b>Aggregation is a core requirement.</b> The Dashboard/Wallet screens need SUM and GROUP BY-style "
        "aggregates (total hectares, total credits, per-species totals). SQL expresses these directly; a "
        "key-value or document store would require pulling every record into the application to aggregate them, "
        "which is exactly the current (broken) approach.",
        "<b>Transactional guarantees protect the credit ledger.</b> Minting a credit must never happen without a "
        "backing project. A relational database's built-in transaction support gives that guarantee for free; the "
        "app's current local-storage mechanism has no transaction concept.",
        "<b>Drop-in fit with the existing reactive architecture.</b> The screens already update reactively from "
        "the data layer, so a database that can stream live query results back to the UI (as Room does) requires "
        "no change to how screens observe and display data — only the storage layer underneath changes.",
    ]))

    story.append(Paragraph("7.1 Comparison with alternatives", H2))
    cmp_data = [
        [hcell("Option"), hcell("Type"), hcell("Verdict for BlueLedger")],
        [cell("<b>SQLite / Room</b> (selected)"), cell("Embedded relational"),
         cell("Fits offline-first design, relational data shape, existing Flow-based architecture, and an "
              "already-declared dependency. Chosen.")],
        [cell("Firebase Firestore / MongoDB"), cell("Cloud document"),
         cell("Would suit a future multi-device sync feature, but adds a network dependency and cost the "
              "current offline-first product does not need; harder to enforce a single source of truth for "
              "species rates. Reasonable Phase-2 addition (see Future Enhancements), not a replacement now.")],
        [cell("DataStore Preferences (current)"), cell("Key-value"),
         cell("Already tried in this repository and shown to be insufficient: no querying, no relations, one "
              "overwritable blob per record type, no concurrency safety.")],
        [cell("Server-side PostgreSQL/MySQL"), cell("Client-server relational"),
         cell("Appropriate once a backend for project verification and a credit marketplace exists (already "
              "identified as a known gap). Out of scope until that backend is built.")],
        [cell("Graph database (e.g. Neo4j)"), cell("Graph"),
         cell("No multi-hop relationship-traversal use case exists in this domain (no social graph, no "
              "path-finding); not justified.")],
    ]
    story.append(section_table(cmp_data, colWidths=[38*mm, 26*mm, PAGE_W - 2*MARGIN - 64*mm]))

    story.append(Paragraph("7.2 Advantages and limitations", H2))
    story.append(bullets([
        "<b>Advantages:</b> zero network dependency, ACID transactions, compile-time-checked SQL via Room "
        "annotations, native Flow support, mature Android tooling (Database Inspector), no additional cost.",
        "<b>Limitations (acknowledged honestly):</b> SQLite is a single-writer, file-based engine local to one "
        "device — it has no built-in multi-device replication. If BlueLedger later needs data shared across a "
        "contributor's devices or a server-side verification workflow, a sync layer or a migration to a "
        "client-server database (PostgreSQL) would be required; this is listed under Future Enhancements rather "
        "than solved here, to avoid unnecessary restructuring in this phase.",
    ]))

    story.append(Paragraph("7.3 Integration with the existing stack", H2))
    story.append(P(
        "The proposed database slots directly underneath the app's existing data layer, which already separates "
        "the screens from how data is stored. The behavior the screens currently rely on — logging in, "
        "submitting a plot, and reading back totals — stays the same; only the storage mechanism behind it "
        "changes, from unstructured local text to a structured, constrained database. As a result, no visible "
        "screen or navigation flow needs to change for this migration."))
    story.append(divider())
    story.append(PageBreak())

    # ================= 8. DATA MODEL =================
    story.append(Paragraph("8. Data Model / Database Design", H1))
    story.append(P(
        "This is the core design section (4 of 10 assessment marks). It presents the ER diagram, per-entity "
        "attribute definitions, the relational schema as SQL DDL, key/constraint reasoning, and the normalization "
        "argument, all derived from the entities identified above."))

    story.append(Paragraph("8.A  Entity-Relationship Diagram", H2))
    er = fit_drawing(build_er_diagram())
    story.append(KeepTogether([er, Paragraph(
        "Figure 1. ER diagram for the proposed BlueLedger schema — 5 entities, all one-to-many "
        "relationships, surrogate integer primary keys.", CAPTION)]))

    story.append(Paragraph("8.B  Entity Descriptions", H2))

    def entity_table(title, rows, desc):
        story.append(Paragraph(title, H3))
        story.append(P(desc))
        data = [[hcell("Attribute"), hcell("Data Type"), hcell("Constraint")]] + rows
        story.append(section_table(data, colWidths=[52*mm, 40*mm, PAGE_W-2*MARGIN-92*mm]))
        story.append(Spacer(1, 6))

    entity_table("COMMUNITY", [
        [cell("community_id", True), cell("INTEGER"), cell("PRIMARY KEY, AUTOINCREMENT")],
        [cell("name", True), cell("TEXT"), cell("NOT NULL, UNIQUE")],
        [cell("region", True), cell("TEXT"), cell("NULLable")],
        [cell("enrolled_at", True), cell("DATETIME"), cell("NOT NULL, DEFAULT CURRENT_TIMESTAMP")],
    ], "Represents a village or cooperative enrolled in the program. Newly proposed: the current Dashboard "
       "screen already displays a “total communities enrolled” figure with no underlying record to back it.")

    entity_table("USER", [
        [cell("user_id", True), cell("INTEGER"), cell("PRIMARY KEY, AUTOINCREMENT")],
        [cell("email", True), cell("TEXT"), cell("NOT NULL, UNIQUE")],
        [cell("username", True), cell("TEXT"), cell("NOT NULL")],
        [cell("phone", True), cell("TEXT"), cell("NULLable")],
        [cell("password_hash", True), cell("TEXT"), cell("NOT NULL")],
        [cell("community_id", True), cell("INTEGER"), cell("FOREIGN KEY → COMMUNITY(community_id), NULLable")],
        [cell("created_at", True), cell("DATETIME"), cell("NOT NULL, DEFAULT CURRENT_TIMESTAMP")],
    ], "Evolves the current, minimal user record (email, phone, username only) into a real account record with "
       "credential storage and optional community membership.")

    entity_table("SPECIES", [
        [cell("species_id", True), cell("INTEGER"), cell("PRIMARY KEY, AUTOINCREMENT")],
        [cell("common_name", True), cell("TEXT"), cell("NOT NULL, UNIQUE")],
        [cell("credit_rate_per_ha", True), cell("DECIMAL(5,2)"), cell("NOT NULL, CHECK (credit_rate_per_ha > 0)")],
        [cell("description", True), cell("TEXT"), cell("NULLable")],
    ], "Reference/lookup table. Replaces the hardcoded species-to-rate mapping currently built into the app's "
       "credit-calculation logic with queryable, editable data. Seed rows: Rhizophora (14), Avicennia (12), "
       "Bruguiera (10) — the rates already used by the app today.")

    entity_table("PROJECT", [
        [cell("project_id", True), cell("INTEGER"), cell("PRIMARY KEY, AUTOINCREMENT")],
        [cell("plot_id", True), cell("TEXT"), cell("NOT NULL")],
        [cell("user_id", True), cell("INTEGER"), cell("FOREIGN KEY → USER(user_id), NOT NULL")],
        [cell("species_id", True), cell("INTEGER"), cell("FOREIGN KEY → SPECIES(species_id), NOT NULL")],
        [cell("hectares", True), cell("DECIMAL(6,2)"), cell("NOT NULL, CHECK (hectares > 0)")],
        [cell("gps_lat", True), cell("DECIMAL(9,6)"), cell("NOT NULL")],
        [cell("gps_lng", True), cell("DECIMAL(9,6)"), cell("NOT NULL")],
        [cell("image_uri", True), cell("TEXT"), cell("NULLable")],
        [cell("status", True), cell("TEXT"), cell("NOT NULL, CHECK IN ('PENDING','VERIFIED','REJECTED'), DEFAULT 'PENDING'")],
        [cell("created_at", True), cell("DATETIME"), cell("NOT NULL, DEFAULT CURRENT_TIMESTAMP")],
    ], "Direct evolution of the existing project record. The free-text species field becomes a validated "
       "foreign key, and a new status column formalizes a verification workflow that today does not exist "
       "(credits are minted instantly and unconditionally).")

    entity_table("CREDIT_TRANSACTION", [
        [cell("transaction_id", True), cell("INTEGER"), cell("PRIMARY KEY, AUTOINCREMENT")],
        [cell("project_id", True), cell("INTEGER"), cell("FOREIGN KEY → PROJECT(project_id), NULLable")],
        [cell("user_id", True), cell("INTEGER"), cell("FOREIGN KEY → USER(user_id), NOT NULL")],
        [cell("txn_type", True), cell("TEXT"), cell("NOT NULL, CHECK IN ('MINT','REDEEM')")],
        [cell("credit_amount", True), cell("INTEGER"), cell("NOT NULL, CHECK (credit_amount <> 0)")],
        [cell("bonus_multiplier", True), cell("DECIMAL(3,2)"), cell("NOT NULL, DEFAULT 1.00")],
        [cell("txn_timestamp", True), cell("DATETIME"), cell("NOT NULL, DEFAULT CURRENT_TIMESTAMP")],
    ], "An append-only ledger. The minted-credit amount is no longer stored solely on the Project record; "
       "instead every mint (and, later, every redemption) is its own row. project_id is nullable because a "
       "REDEEM transaction draws from a user's pooled balance rather than a single project. Wallet balance = "
       "SUM(credit_amount) grouped by user.")

    story.append(Paragraph("8.C  Relational Schema (SQL DDL)", H2))
    story.append(P("The Room persistence library generates SQL equivalent to this from the entity definitions; "
                    "it is shown directly here for clarity and portability."))
    ddl = """CREATE TABLE community (
    community_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    region        TEXT,
    enrolled_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user (
    user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    email          TEXT NOT NULL UNIQUE,
    username       TEXT NOT NULL,
    phone          TEXT,
    password_hash  TEXT NOT NULL,
    community_id   INTEGER,
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (community_id) REFERENCES community(community_id)
);

CREATE TABLE species (
    species_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    common_name          TEXT NOT NULL UNIQUE,
    credit_rate_per_ha   DECIMAL(5,2) NOT NULL CHECK (credit_rate_per_ha > 0),
    description          TEXT
);

CREATE TABLE project (
    project_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    plot_id      TEXT NOT NULL,
    user_id      INTEGER NOT NULL,
    species_id   INTEGER NOT NULL,
    hectares     DECIMAL(6,2) NOT NULL CHECK (hectares > 0),
    gps_lat      DECIMAL(9,6) NOT NULL,
    gps_lng      DECIMAL(9,6) NOT NULL,
    image_uri    TEXT,
    status       TEXT NOT NULL DEFAULT 'PENDING'
                 CHECK (status IN ('PENDING','VERIFIED','REJECTED')),
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)    REFERENCES user(user_id),
    FOREIGN KEY (species_id) REFERENCES species(species_id)
);

CREATE TABLE credit_transaction (
    transaction_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id        INTEGER,
    user_id           INTEGER NOT NULL,
    txn_type          TEXT NOT NULL CHECK (txn_type IN ('MINT','REDEEM')),
    credit_amount     INTEGER NOT NULL CHECK (credit_amount <> 0),
    bonus_multiplier  DECIMAL(3,2) NOT NULL DEFAULT 1.00,
    txn_timestamp     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project(project_id),
    FOREIGN KEY (user_id)    REFERENCES user(user_id),
    CHECK ((txn_type = 'MINT' AND project_id IS NOT NULL) OR txn_type = 'REDEEM')
);

CREATE INDEX idx_project_user     ON project(user_id);
CREATE INDEX idx_project_species  ON project(species_id);
CREATE INDEX idx_txn_user         ON credit_transaction(user_id);
CREATE INDEX idx_txn_project      ON credit_transaction(project_id);"""
    story.append(code_block(ddl))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Representative queries", H3))
    q_ddl = """-- Wallet balance and total hectares for the signed-in user (Wallet / Dashboard screens)
SELECT COALESCE(SUM(ct.credit_amount), 0) AS wallet_balance
FROM   credit_transaction ct
WHERE  ct.user_id = :userId;

SELECT COALESCE(SUM(p.hectares), 0) AS total_hectares
FROM   project p
WHERE  p.user_id = :userId;

-- Per-species totals for an analytics/report view
SELECT s.common_name, COUNT(p.project_id) AS plots, SUM(p.hectares) AS hectares
FROM   project p JOIN species s ON s.species_id = p.species_id
GROUP  BY s.common_name;

-- Community leaderboard by total credits minted
SELECT c.name, SUM(ct.credit_amount) AS total_credits
FROM   credit_transaction ct
JOIN   user u ON u.user_id = ct.user_id
JOIN   community c ON c.community_id = u.community_id
WHERE  ct.txn_type = 'MINT'
GROUP  BY c.name
ORDER  BY total_credits DESC;"""
    story.append(code_block(q_ddl))

    story.append(Paragraph("8.D  Keys and Constraints", H2))
    keys_data = [
        [hcell("Constraint type"), hcell("Where applied"), hcell("Purpose")],
        [cell("PRIMARY KEY"), cell("*_id on every table"), cell("Uniquely identifies each row; SQLite auto-generates a monotonic surrogate key.")],
        [cell("FOREIGN KEY"), cell("user.community_id, project.user_id, project.species_id, credit_transaction.project_id/user_id"), cell("Guarantees every reference points to a row that actually exists — an integrity check the current unstructured storage cannot make.")],
        [cell("UNIQUE"), cell("user.email, community.name, species.common_name"), cell("Prevents duplicate accounts, duplicate community records, and duplicate species reference rows.")],
        [cell("NOT NULL"), cell("email, username, password_hash, hectares, gps_lat/lng, txn_type, credit_amount, etc."), cell("Blocks incomplete records — today nothing stops an empty species name from being saved.")],
        [cell("CHECK"), cell("hectares &gt; 0, credit_rate_per_ha &gt; 0, credit_amount &lt;&gt; 0, status/txn_type enumerations, MINT&rarr;project_id required"), cell("Encodes domain rules directly in the schema instead of relying on UI-side validation alone.")],
    ]
    story.append(section_table(keys_data, colWidths=[24*mm, 62*mm, PAGE_W-2*MARGIN-86*mm]))

    story.append(Paragraph("8.E  Normalization", H2))
    story.append(Paragraph("1NF — fixing the current violation", H3))
    story.append(P(
        "The existing storage is not even in First Normal Form: the entire list of projects is held as one "
        "serialized block of text under a single stored value &mdash; a repeating group packed into a single "
        "atomic field. The proposed schema gives every project its own row with atomic columns, satisfying 1NF."))
    story.append(Paragraph("2NF — trivially satisfied", H3))
    story.append(P(
        "Every table in the design uses a single-column surrogate primary key "
        "(<font face='Courier'>*_id</font>), so there are no composite keys and therefore no possibility of a "
        "partial-key dependency. 2NF holds by construction."))
    story.append(Paragraph("3NF — the species-rate example", H3))
    story.append(P(
        "This is the concrete anomaly the redesign removes. If a credit-rate column were added directly onto "
        "the project table instead of extracting species into its own table, it would depend on the project's "
        "species rather than on the project's own primary key &mdash; a transitive dependency "
        "(project &rarr; species &rarr; credit rate) that violates 3NF. The practical symptom is exactly the "
        "situation already present in the app today: the rate is duplicated in application logic rather than "
        "being looked up once. Extracting SPECIES as its own table with a foreign key from PROJECT removes the "
        "transitive dependency and the update anomaly it would otherwise cause (correcting Rhizophora's rate "
        "would no longer require touching every historical project row)."))
    story.append(divider())
    story.append(PageBreak())

    # ================= 9. SYSTEM ARCHITECTURE =================
    story.append(Paragraph("9. System Architecture / Workflow Diagram", H1))
    story.append(P(
        "The diagram below follows the required Users &rarr; Application/System &rarr; Database &rarr; Output "
        "flow, mapped onto BlueLedger's actual application layering."))
    arch = fit_drawing(build_architecture_diagram())
    story.append(KeepTogether([arch, Paragraph(
        "Figure 2. BlueLedger system architecture with the proposed SQLite persistence layer. Solid arrows are "
        "write/request calls; the lighter return arrows are the live data updates that refresh the screens.",
        CAPTION)]))
    story.append(PageBreak())

    # ================= A. EXISTING VS PROPOSED =================
    story.append(Paragraph("A. Existing vs Proposed System", H1))
    comp_data = [
        [hcell("Aspect"), hcell("Existing (today)"), hcell("Proposed")],
        [cell("Storage"), cell("Two unstructured text blocks in local device storage"), cell("5-table relational schema in an embedded SQLite database")],
        [cell("User model"), cell("Single overwritable user record, mock authentication"), cell("USER table, unique email, password hash, multi-account capable")],
        [cell("Species rates"), cell("Hardcoded in application logic"), cell("SPECIES reference table, editable without a rebuild")],
        [cell("Credit history"), cell("Baked into each project's single credit-amount field"), cell("Append-only CREDIT_TRANSACTION ledger, supports future redemption")],
        [cell("Integrity"), cell("None — any value accepted"), cell("Primary-key, foreign-key, NOT NULL and CHECK constraints enforced by the database engine")],
        [cell("Queries"), cell("Full-list loading into memory, then in-app filtering"), cell("Indexed SQL queries and aggregates (SUM, GROUP BY)")],
        [cell("Concurrency"), cell("Read-then-write race during upload"), cell("Atomic database transactions on insert")],
    ]
    story.append(section_table(comp_data, colWidths=[26*mm, 65*mm, PAGE_W-2*MARGIN-91*mm]))
    story.append(divider())

    # ================= B. IMPLEMENTATION ROADMAP =================
    story.append(Paragraph("B. Proposed Implementation Plan", H1))
    phase_data = [
        [hcell("Phase"), hcell("Work"), hcell("Outcome")],
        [cell("1. Database setup"), cell("Introduce the embedded database and its configuration into the application."), cell("A working, empty database ready to hold data")],
        [cell("2. Schema / model implementation"), cell("Define the five entities (User, Community, Species, Project, CreditTransaction) with the constraints in §8.D; seed the Species reference rows."), cell("The full schema created and seeded")],
        [cell("3. Data-access integration"), cell("Implement the queries needed to create, read, update, and delete records, equivalent to today's data-access methods."), cell("All required database operations available")],
        [cell("4. Application integration"), cell("Connect the existing data layer to the new database instead of the current unstructured local storage, keeping the same behavior visible to the screens."), cell("Screens read/write through the new database transparently")],
        [cell("5. Reference-data wiring"), cell("Point the species-selection dropdown at the live Species table instead of a fixed list."), cell("Species list becomes data-driven")],
        [cell("6. Testing and validation"), cell("Test all CRUD operations against a test database; verify constraint violations are rejected; verify wallet totals match manually computed values."), cell("Verified, constraint-correct database behavior")],
    ]
    story.append(section_table(phase_data, colWidths=[38*mm, 82*mm, PAGE_W-2*MARGIN-120*mm]))
    story.append(divider())

    # ================= C. CHECKLIST =================
    story.append(Paragraph("C. Assessment Readiness Checklist", H1))
    chk_data = [
        [hcell("Assessment 6 requirement"), hcell("Status"), hcell("Where addressed")],
        [cell("1. Project Title"), cell("Done"), cell("Section 1")],
        [cell("2. Introduction and Background"), cell("Done"), cell("Section 2")],
        [cell("3. Problem Statement"), cell("Done"), cell("Section 3")],
        [cell("4. Objectives"), cell("Done"), cell("Section 4")],
        [cell("5. Scope of the Project"), cell("Done"), cell("Section 5")],
        [cell("6. Requirement Analysis (functional + non-functional)"), cell("Done"), cell("Section 6")],
        [cell("7. Database Selection and Justification"), cell("Done"), cell("Section 7")],
        [cell("8. Data Model / Database Design (ER diagram, entities, schema, keys, normalization)"), cell("Done"), cell("Section 8")],
        [cell("9. System Architecture / Workflow Diagram"), cell("Done"), cell("Section 9")],
        [cell("Distinguishes implemented vs proposed features"), cell("Done"), cell("Sections 2, 3, 5, Appendix A")],
        [cell("Implementation not yet performed on the live codebase"), cell("Confirmed — no source files were modified"), cell("This document is a proposal only")],
    ]
    story.append(section_table(chk_data, colWidths=[86*mm, 30*mm, PAGE_W-2*MARGIN-116*mm]))
    story.append(divider())

    # ================= D. FUTURE ENHANCEMENTS =================
    story.append(Paragraph("D. Future Enhancements", H1))
    story.append(bullets([
        "<b>Verifier role and review screen:</b> build the screen that lets a second role transition a "
        "project's status from PENDING to VERIFIED/REJECTED before a credit-mint transaction is allowed to fire.",
        "<b>Cloud sync:</b> once multi-device access is needed, add a thin sync layer (or move to a server-backed "
        "relational database) rather than switching the local model — the existing foreign-key-based schema maps "
        "cleanly onto a server-side PostgreSQL schema if that becomes necessary.",
        "<b>Credit redemption workflow:</b> implement the already-planned “Sell Credits” action on the Wallet "
        "screen using REDEEM rows in the credit-transaction ledger.",
        "<b>Historical rate versioning:</b> if species credit rates change over time, add an effective-date range "
        "to the Species table (or a separate rate-history table) so past mints remain reproducible.",
    ]))
    story.append(P(
        "These are explicitly out of scope for the current submission and are listed only to show the schema "
        "was designed with room to grow, per the assessment's request for realistic future extensions."))

    doc.multiBuild(story)


if __name__ == "__main__":
    build()
    print("Wrote", OUT_PDF)
