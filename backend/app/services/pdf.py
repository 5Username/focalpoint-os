"""
Server-side PDF generation for Weekly Briefs and Travel Risk Packs.
Uses ReportLab for reliable, dependency-light PDFs.
"""

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, Any

def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleCustom', parent=styles['Title'], fontSize=16, spaceAfter=8, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='HeadingCustom', parent=styles['Heading2'], fontSize=12, spaceBefore=12, spaceAfter=4, textColor=colors.HexColor('#312e81')))
    styles.add(ParagraphStyle(name='BodyCustom', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6))
    styles.add(ParagraphStyle(name='Small', parent=styles['Normal'], fontSize=8, textColor=colors.grey))
    return styles

def generate_brief_pdf(data: Dict[str, Any]) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=15*mm, bottomMargin=15*mm)
    styles = _styles()
    story = []

    story.append(Paragraph(data.get('title', 'Weekly Security Brief'), styles['TitleCustom']))
    story.append(Paragraph(f"Region: {data.get('region', '')} | Week of: {data.get('week_of', '')}", styles['Small']))
    story.append(Spacer(1, 8))

    sections = data.get('sections', {})
    for key, value in sections.items():
        if key == 'sources_used':
            continue
        heading = key.replace('_', ' ').title()
        story.append(Paragraph(heading, styles['HeadingCustom']))
        if isinstance(value, list):
            items = [ListItem(Paragraph(str(item), styles['BodyCustom'])) for item in value]
            story.append(ListFlowable(items, bulletType='bullet', start='•'))
        else:
            story.append(Paragraph(str(value), styles['BodyCustom']))

    story.append(Spacer(1, 12))
    story.append(Paragraph(data.get('disclaimer', ''), styles['Small']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def generate_travel_pdf(data: Dict[str, Any]) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=15*mm, bottomMargin=15*mm)
    styles = _styles()
    story = []

    story.append(Paragraph(f"Travel Risk Pack — {data.get('destination', '')}", styles['TitleCustom']))
    story.append(Paragraph(f"{data.get('period', '')} | {data.get('organization', '')}", styles['Small']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"<b>Overall Recommendation:</b> {data.get('overall_recommendation', '')}", styles['BodyCustom']))
    story.append(Spacer(1, 8))

    # Risks table
    story.append(Paragraph('Key Risks', styles['HeadingCustom']))
    risk_data = [['Category', 'Level', 'Notes']]
    for r in data.get('key_risks', []):
        risk_data.append([r.get('category', ''), r.get('level', ''), r.get('notes', '')])
    t = Table(risk_data, colWidths=[45*mm, 30*mm, 90*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#312e81')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph('Mitigations', styles['HeadingCustom']))
    for m in data.get('mitigations', []):
        story.append(Paragraph(f"• {m}", styles['BodyCustom']))

    story.append(Paragraph('Go / No-Go Checklist', styles['HeadingCustom']))
    for c in data.get('go_no_go_checklist', []):
        mark = '✓' if c.get('status') else '✗'
        story.append(Paragraph(f"{mark}  {c.get('item', '')}", styles['BodyCustom']))

    story.append(Spacer(1, 12))
    story.append(Paragraph(data.get('disclaimer', ''), styles['Small']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
