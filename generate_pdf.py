from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─── PALETTE ────────────────────────────────────────────────────────────────
BG       = colors.HexColor("#0d0d0d")
SURFACE  = colors.HexColor("#161616")
SURFACE2 = colors.HexColor("#1e1e1e")
BORDER   = colors.HexColor("#2a2a2a")
TEXT     = colors.HexColor("#f0f0f0")
MUTED    = colors.HexColor("#666666")
YELLOW   = colors.HexColor("#e8ff47")
BLUE     = colors.HexColor("#47c4ff")
ORANGE   = colors.HexColor("#ff6b47")
GREEN    = colors.HexColor("#47ffb0")
WHITE    = colors.HexColor("#ffffff")

W, H = A4
MARGIN = 20 * mm

# ─── DOC ────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "/Users/doriangauthey/dashboard/dashboard_dorian.pdf",
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title="Dashboard Dorian Gauthey"
)

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.restoreState()

# ─── STYLES ─────────────────────────────────────────────────────────────────
def S(name, font="Helvetica", color=TEXT, **kw):
    return ParagraphStyle(name, fontName=font, textColor=color, **kw)

styles = {
    "title":       S("title",   font="Helvetica-Bold", color=WHITE,  fontSize=20, leading=26, spaceAfter=2*mm),
    "subtitle":    S("subtitle",                        color=MUTED,  fontSize=9,  leading=14, spaceAfter=6*mm, letterSpacing=1.5),
    "section":     S("section", font="Helvetica-Bold", color=MUTED,  fontSize=8,  leading=12, spaceBefore=6*mm, spaceAfter=3*mm, letterSpacing=1.8),
    "horizon":     S("horizon", font="Helvetica-Bold", color=WHITE,  fontSize=11, leading=16, spaceBefore=4*mm, spaceAfter=3*mm),
    "vision_text": S("vision",                         color=TEXT,   fontSize=11, leading=17, spaceAfter=2*mm),
    "body":        S("body",                           color=TEXT,   fontSize=10, leading=15),
    "muted":       S("muted",                          color=MUTED,  fontSize=9,  leading=13),
    "step":        S("step",                           color=TEXT,   fontSize=10, leading=15),
    "label":       S("label",   font="Helvetica-Bold", color=MUTED,  fontSize=8,  leading=12, letterSpacing=1.2),
}

def hr(color=BORDER, thickness=0.5, spaceB=2*mm, spaceA=2*mm):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=spaceA, spaceBefore=spaceB)

def pill(text, bg, fg):
    return Paragraph(
        f'<font color="#{bg[1:]}">{text}</font>',
        ParagraphStyle("pill", fontSize=8, fontName="Helvetica-Bold",
                       textColor=colors.HexColor(bg), leading=12, letterSpacing=1)
    )

def dot(color_hex):
    return f'<font color="{color_hex}">●</font> '

# ─── CONTENT ────────────────────────────────────────────────────────────────
story = []

# Header
story.append(Spacer(1, 4*mm))
story.append(Paragraph("DORIAN GAUTHEY", styles["title"]))
story.append(Paragraph("DASHBOARD STRATÉGIQUE · 2026 – 2031", styles["subtitle"]))
story.append(hr(BORDER, 0.5, 0, 4*mm))

# ── VISION ─────────────────────────────────────────────────────────────────
story.append(Paragraph("VISION — 5 ANS", styles["section"]))

vision_data = [[
    Paragraph('<font color="#e8ff47"><b>VISION 2031</b></font>',
              ParagraphStyle("vbadge", fontSize=8, fontName="Helvetica-Bold", textColor=YELLOW, leading=12)),
    Paragraph(
        "Freelance établi, <b>3 000 € net/mois</b>, 4 jours/semaine max — "
        "montage à domicile, tournages ponctuels, clients qui font voyager, "
        "mariage en niche complémentaire. Famille, santé, liberté.",
        ParagraphStyle("vtext", fontSize=10, textColor=TEXT, leading=15)
    )
]]
vision_table = Table(vision_data, colWidths=[28*mm, W - 2*MARGIN - 30*mm])
vision_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), SURFACE),
    ("ROUNDEDCORNERS", [6]),
    ("BOX",        (0,0), (-1,-1), 0.5, BORDER),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",(0,0), (-1,-1), 10),
    ("RIGHTPADDING",(0,0),(-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING",(0,0),(-1,-1), 10),
    ("LINEAFTER",  (0,0), (0,-1), 0.5, BORDER),
]))
story.append(vision_table)

# ── LONG TERME ─────────────────────────────────────────────────────────────
story.append(Spacer(1, 5*mm))
story.append(Paragraph("OBJECTIFS LONG TERME — 3 À 5 ANS", styles["section"]))

lt_data = [
    [Paragraph("<b>PRO</b>", styles["label"]),
     Paragraph(
         dot("#e8ff47") + "Client ancrage corporate — montage domicile majoritaire<br/>"
         + dot("#e8ff47") + "4 à 5 mariages/an — niche complémentaire, peut monter à 50% CA<br/>"
         + dot("#e8ff47") + "Clients qui font voyager<br/>"
         + dot("#e8ff47") + "3 000 € net/mois, 4 jours/semaine max<br/>"
         + dot("#e8ff47") + "Présence LinkedIn active — visibilité B2B continue",
         styles["body"])],
    [Paragraph("<b>CRÉATIF</b>", styles["label"]),
     Paragraph(
         dot("#ff6b47") + "Court métrage terminé et diffusé<br/>"
         + dot("#ff6b47") + "Présence Instagram incarnée — se mettre en scène",
         styles["body"])],
    [Paragraph("<b>PERSO</b>", styles["label"]),
     Paragraph(
         dot("#47ffb0") + "Versailles + pied-à-terre en Bourgogne avec la conjointe<br/>"
         + dot("#47ffb0") + "Famille, enfants, vie paisible<br/>"
         + dot("#47ffb0") + "Santé physique — sport régulier, nature, voyages",
         styles["body"])],
]

lt_table = Table(lt_data, colWidths=[28*mm, W - 2*MARGIN - 30*mm])
lt_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), SURFACE),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("LINEAFTER",     (0,0), (0,-1), 0.5, BORDER),
    ("LINEBELOW",     (0,0), (-1,-2), 0.5, BORDER),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 9),
    ("BOTTOMPADDING", (0,0), (-1,-1), 9),
    ("TEXTCOLOR",     (0,0), (0,-1), MUTED),
]))
story.append(lt_table)

# ── ANNUEL 2026 ─────────────────────────────────────────────────────────────
story.append(Spacer(1, 5*mm))
story.append(Paragraph("OBJECTIFS ANNUELS — 2026", styles["section"]))

an_data = [
    [Paragraph("<b>PRO</b>", styles["label"]),
     Paragraph(
         dot("#e8ff47") + "Client ancrage corporate signé avant fin août — 2 500 € net/mois<br/>"
         + dot("#e8ff47") + "1 mariage booké via démarchage actif<br/>"
         + dot("#e8ff47") + "Page mariage.net créée<br/>"
         + dot("#e8ff47") + "2 posts LinkedIn par semaine — visibilité B2B",
         styles["body"])],
    [Paragraph("<b>CRÉATIF</b>", styles["label"]),
     Paragraph(
         dot("#ff6b47") + "Documentaire île de Ré — monté et exporté avant le 31 décembre<br/>"
         + dot("#ff6b47") + "Instagram perso lancé",
         styles["body"])],
    [Paragraph("<b>PERSO</b>", styles["label"]),
     Paragraph(dot("#47ffb0") + "Blocs sport + nature verrouillés dans l'agenda — intouchables", styles["body"])],
]

an_table = Table(an_data, colWidths=[28*mm, W - 2*MARGIN - 30*mm])
an_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), SURFACE),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("LINEAFTER",     (0,0), (0,-1), 0.5, BORDER),
    ("LINEBELOW",     (0,0), (-1,-2), 0.5, BORDER),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 9),
    ("BOTTOMPADDING", (0,0), (-1,-1), 9),
    ("TEXTCOLOR",     (0,0), (0,-1), MUTED),
]))
story.append(an_table)

# ── TRIMESTRIEL ─────────────────────────────────────────────────────────────
story.append(Spacer(1, 5*mm))
story.append(Paragraph("OBJECTIFS TRIMESTRIELS — MAI → JUILLET 2026", styles["section"]))

tr_headers = [
    Paragraph("<b>PRIORITÉ</b>", ParagraphStyle("th", fontSize=8, fontName="Helvetica-Bold", textColor=MUTED, leading=12)),
    Paragraph("<b>DEADLINE</b>", ParagraphStyle("th", fontSize=8, fontName="Helvetica-Bold", textColor=MUTED, leading=12, alignment=TA_RIGHT)),
]
tr_rows = [
    [Paragraph(dot("#e8ff47") + "Showreel finalisé", styles["body"]),
     Paragraph('<font color="#666666">31 mai</font>', ParagraphStyle("dd", fontSize=10, textColor=MUTED, leading=15, alignment=TA_RIGHT))],
    [Paragraph(dot("#47c4ff") + "Site en ligne", styles["body"]),
     Paragraph('<font color="#666666">30 juin</font>', ParagraphStyle("dd", fontSize=10, textColor=MUTED, leading=15, alignment=TA_RIGHT))],
    [Paragraph(dot("#47c4ff") + "Vidéo mariage montée + mariage.net créé", styles["body"]),
     Paragraph('<font color="#666666">30 juin</font>', ParagraphStyle("dd", fontSize=10, textColor=MUTED, leading=15, alignment=TA_RIGHT))],
    [Paragraph(dot("#e8ff47") + "15 contacts corporate par mois", styles["body"]),
     Paragraph('<font color="#666666">Continu</font>', ParagraphStyle("dd", fontSize=10, textColor=MUTED, leading=15, alignment=TA_RIGHT))],
    [Paragraph(dot("#ff6b47") + "Instagram : 1 post / semaine", styles["body"]),
     Paragraph('<font color="#666666">Continu</font>', ParagraphStyle("dd", fontSize=10, textColor=MUTED, leading=15, alignment=TA_RIGHT))],
    [Paragraph(dot("#47ffb0") + "Emploi du temps perso verrouillé", styles["body"]),
     Paragraph('<font color="#666666">Cette semaine</font>', ParagraphStyle("dd", fontSize=10, textColor=MUTED, leading=15, alignment=TA_RIGHT))],
]

tr_col = W - 2*MARGIN
tr_table = Table([tr_headers] + tr_rows, colWidths=[tr_col*0.75, tr_col*0.25])
tr_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1, 0), SURFACE2),
    ("BACKGROUND",    (0,1), (-1,-1), SURFACE),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("LINEBELOW",     (0,0), (-1,-2), 0.5, BORDER),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 9),
    ("BOTTOMPADDING", (0,0), (-1,-1), 9),
]))
story.append(tr_table)

# ── PAGE BREAK ──────────────────────────────────────────────────────────────
from reportlab.platypus import PageBreak
story.append(PageBreak())

# ── SEMAINE TYPE ─────────────────────────────────────────────────────────────
story.append(Spacer(1, 4*mm))
story.append(Paragraph("SEMAINE TYPE", styles["section"]))

def blk(text, color_hex):
    return Paragraph(
        f'<font color="{color_hex}">■</font> {text}',
        ParagraphStyle("blk", fontSize=9, textColor=TEXT, leading=13)
    )

sw_headers = [
    Paragraph("<b>JOUR</b>",   ParagraphStyle("swh", fontSize=8, fontName="Helvetica-Bold", textColor=MUTED, leading=12)),
    Paragraph("<b>MATIN</b>",  ParagraphStyle("swh", fontSize=8, fontName="Helvetica-Bold", textColor=MUTED, leading=12)),
    Paragraph("<b>APRÈS-MIDI</b>", ParagraphStyle("swh", fontSize=8, fontName="Helvetica-Bold", textColor=MUTED, leading=12)),
    Paragraph("<b>17H – 20H</b>",  ParagraphStyle("swh", fontSize=8, fontName="Helvetica-Bold", textColor=MUTED, leading=12)),
]

sw_rows = [
    [Paragraph("<b>Lundi</b>",   ParagraphStyle("day", fontSize=10, fontName="Helvetica-Bold", textColor=MUTED, leading=15)),
     blk("Démarchage corporate", "#e8ff47"),
     blk("Admin léger / réponses", "#666666"),
     blk("Docu perso", "#ff6b47")],
    [Paragraph("<b>Mardi</b>",   ParagraphStyle("day", fontSize=10, fontName="Helvetica-Bold", textColor=MUTED, leading=15)),
     blk("Production / Montage", "#e8ff47"),
     blk("LinkedIn / Instagram", "#47c4ff"),
     blk("Gym", "#47ffb0")],
    [Paragraph("<b>Mercredi</b>", ParagraphStyle("day", fontSize=10, fontName="Helvetica-Bold", textColor=MUTED, leading=15)),
     Paragraph(
         '<font color="#47ffb0"><b>NATURE — Rando / Bivouac / Training · INTOUCHABLE</b></font>',
         ParagraphStyle("nat", fontSize=9, textColor=GREEN, leading=13)
     ), Paragraph(""), Paragraph("")],
    [Paragraph("<b>Jeudi</b>",   ParagraphStyle("day", fontSize=10, fontName="Helvetica-Bold", textColor=MUTED, leading=15)),
     blk("Mariage — montage / démarche", "#47c4ff"),
     blk("Site web / Showreel", "#e8ff47"),
     blk("Court métrage", "#ff6b47")],
    [Paragraph("<b>Vendredi</b>", ParagraphStyle("day", fontSize=10, fontName="Helvetica-Bold", textColor=MUTED, leading=15)),
     Paragraph(blk("Weekly Review (30 min)", "#666666").text + "<br/>" + blk("Instagram / Contenu", "#47c4ff").text,
               ParagraphStyle("fri", fontSize=9, textColor=TEXT, leading=14)),
     blk("Libre / Rattrapage", "#666666"),
     blk("Gym", "#47ffb0")],
    [Paragraph("<b>Week-end</b>", ParagraphStyle("day", fontSize=10, fontName="Helvetica-Bold", textColor=MUTED, leading=15)),
     Paragraph(
         '<font color="#47ffb0">■</font> Famille · Perso · Récupération · Gym (1 séance)',
         ParagraphStyle("we", fontSize=9, textColor=TEXT, leading=13)
     ), Paragraph(""), Paragraph("")],
]

cw = W - 2*MARGIN
sw_table = Table([sw_headers] + sw_rows, colWidths=[cw*0.13, cw*0.29, cw*0.29, cw*0.29])
sw_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1, 0), SURFACE2),
    ("BACKGROUND",    (0,1), (-1,-1), SURFACE),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("LINEBELOW",     (0,0), (-1,-2), 0.5, BORDER),
    ("LINEBEFORE",    (1,0), (-1,-1), 0.5, BORDER),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("SPAN",          (1,3), (3,3)),  # Mercredi spans
    ("SPAN",          (1,6), (3,6)),  # Week-end spans
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))
story.append(sw_table)

# ── WEEKLY REVIEW ──────────────────────────────────────────────────────────
story.append(Spacer(1, 6*mm))
story.append(Paragraph("RITUEL WEEKLY REVIEW — VENDREDI MATIN (30 MIN)", styles["section"]))

wr_steps = [
    ("1", "Vider",   "Tout ce qui est dans ta tête ou ton carnet → Trello INBOX"),
    ("2", "Trier",   "Chaque carte reçoit une étiquette : Client / Visibilité / Créatif / Perso / Parking"),
    ("3", "Choisir", "3 priorités max pour la semaine suivante — pas plus"),
    ("4", "Bloquer", "Placer ces 3 priorités dans Google Calendar"),
]

wr_data = [
    [Paragraph(f'<font color="#666666"><b>{n}</b></font>',
               ParagraphStyle("sn", fontSize=11, fontName="Helvetica-Bold", textColor=MUTED, leading=14, alignment=TA_CENTER)),
     Paragraph(f'<b>{title}</b> — {desc}', styles["body"])]
    for n, title, desc in wr_steps
]

wr_table = Table(wr_data, colWidths=[12*mm, W - 2*MARGIN - 14*mm])
wr_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), SURFACE),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("LINEBELOW",     (0,0), (-1,-2), 0.5, BORDER),
    ("LINEAFTER",     (0,0), (0,-1), 0.5, BORDER),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 9),
    ("BOTTOMPADDING", (0,0), (-1,-1), 9),
]))
story.append(wr_table)

# ── TRELLO ──────────────────────────────────────────────────────────────────
story.append(Spacer(1, 6*mm))
story.append(Paragraph("STRUCTURE TRELLO", styles["section"]))

tr_cols = [
    ("INBOX",        "Tout ce qui entre — non trié. Vider ici d'abord."),
    ("Cette semaine","3 cartes max. Choisies le vendredi. Pas plus."),
    ("En cours",     "WIP actif. Une seule tâche à la fois idéalement."),
    ("Fait",         "Archive de la semaine. Se vide chaque vendredi."),
    ("Parking",      "Un jour peut-être. Pas ce trimestre."),
]

trel_data = [[
    Paragraph(f'<b>{t}</b><br/><font color="#666666">{d}</font>',
              ParagraphStyle("tc", fontSize=9, textColor=TEXT, leading=13))
    for t, d in tr_cols
]]

trel_table = Table(trel_data, colWidths=[(W - 2*MARGIN) / 5] * 5)
trel_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), SURFACE),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("LINEBEFORE",    (1,0), (-1,-1), 0.5, BORDER),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 9),
    ("RIGHTPADDING",  (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
]))
story.append(trel_table)

# Étiquettes
story.append(Spacer(1, 4*mm))
labels_data = [[
    Paragraph('<font color="#e8ff47"><b>■ Client</b></font>', ParagraphStyle("l", fontSize=9, textColor=TEXT, leading=12)),
    Paragraph('<font color="#47c4ff"><b>■ Visibilité</b></font>', ParagraphStyle("l", fontSize=9, textColor=TEXT, leading=12)),
    Paragraph('<font color="#ff6b47"><b>■ Créatif</b></font>', ParagraphStyle("l", fontSize=9, textColor=TEXT, leading=12)),
    Paragraph('<font color="#47ffb0"><b>■ Perso</b></font>', ParagraphStyle("l", fontSize=9, textColor=TEXT, leading=12)),
    Paragraph('<font color="#666666"><b>■ Parking</b></font>', ParagraphStyle("l", fontSize=9, textColor=TEXT, leading=12)),
]]
labels_table = Table(labels_data, colWidths=[(W - 2*MARGIN) / 5] * 5)
labels_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), SURFACE2),
    ("BOX",           (0,0), (-1,-1), 0.5, BORDER),
    ("LINEBEFORE",    (1,0), (-1,-1), 0.5, BORDER),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
]))
story.append(labels_table)

# ── FOOTER ──────────────────────────────────────────────────────────────────
story.append(Spacer(1, 8*mm))
story.append(hr(BORDER, 0.5, 0, 3*mm))
story.append(Paragraph(
    "Dorian Gauthey · Dashboard Stratégique · Mis à jour avril 2026",
    ParagraphStyle("footer", fontSize=8, textColor=MUTED, leading=12, alignment=TA_CENTER)
))

# ─── BUILD ──────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("PDF généré : /Users/doriangauthey/dashboard/dashboard_dorian.pdf")
