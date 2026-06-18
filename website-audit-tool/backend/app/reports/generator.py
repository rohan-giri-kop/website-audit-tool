
from io import BytesIO
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.graphics.shapes import (
Circle,
Drawing,
Rect,
String
)

from reportlab.platypus import (
Paragraph,
SimpleDocTemplate,
Spacer,
Table,
TableStyle,
Image,
PageBreak
)

def _build_logo() -> Drawing:

    drawing = Drawing(120, 36)

    drawing.add(
        Rect(
            0, 0, 36, 36,
            rx=12,
            ry=12,
            fillColor=colors.HexColor("#2563EB"),
            strokeColor=colors.HexColor("#2563EB")
        )
    )

    drawing.add(
        Circle(
            18, 18, 10,
            fillColor=colors.HexColor("#7C3AED"),
            strokeColor=None
        )
    )

    drawing.add(
        String(
            48,
            13,
            "AI Audit",
            fontName="Helvetica-Bold",
            fontSize=14,
            fillColor=colors.HexColor("#0F172A")
        )
    )

    return drawing

def build_pdf_report(audit, findings: list) -> bytes:

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=40,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        textColor=colors.HexColor("#2563EB"),
        fontSize=22,
        leading=26
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["BodyText"],
        textColor=colors.HexColor("#475569"),
        fontSize=10,
        leading=13
    )

    story = [

        _build_logo(),

        Spacer(1, 0.12 * inch),

        Paragraph(
            "AI Website Audit Report",
            title_style
        ),

        Spacer(1, 0.12 * inch),

        Paragraph(
            f"Website: {audit.website_url}",
            subtitle_style
        ),

    Paragraph(
        f"Audit Date: {audit.created_at}",
        subtitle_style
    ),

    Paragraph(
        f"Overall Grade: {audit.grade} | Overall Score: {audit.overall_score}",
        subtitle_style
    ),

    Spacer(1, 0.2 * inch)
]

    score_table = Table(
        [
            [
                "SEO",
                "Performance",
                "Accessibility",
                "Security",
                "Mobile",
                "Overall"
            ],
            [
                audit.seo_score,
                audit.performance_score,
                audit.accessibility_score,
                audit.security_score,
                audit.mobile_score,
                audit.overall_score
            ]
        ],
        colWidths=[0.95 * inch] * 6
    )

    score_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EFF6FF")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10)
        ])
    )

    story.extend([
        score_table,
        Spacer(1, 0.2 * inch),

        Paragraph(
            "Executive Summary",
            styles["Heading2"]
        ),

        Paragraph(
            audit.summary or "",
            styles["BodyText"]
        ),

        Spacer(1, 0.2 * inch)
    ])

# WEBSITE SCREENSHOT

    if audit.screenshot_path:

        screenshot_path = os.path.abspath(
            audit.screenshot_path
        )

        if os.path.exists(
            screenshot_path
        ):

            story.extend([

                Paragraph(
                    "Website Screenshot",
                    styles["Heading2"]
                ),

                Spacer(1, 0.1 * inch),

                Image(
                    screenshot_path,
                    width=5.8 * inch,
                    height=3.5 * inch
                ),

                Spacer(1, 0.2 * inch)

            ])

    story.append(PageBreak())

    # AI RECOMMENDATIONS

    story.append(
        Paragraph(
            "AI Recommendations",
            styles["Heading1"]
        )
    )

    story.append(
        Spacer(1, 0.1 * inch)
    )

    for rec in (audit.recommendations or []):

        story.append(
            Paragraph(
                f"<b>{rec.get('priority','')}</b> - "
                f"{rec.get('recommendation','')}",
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 0.08 * inch)
        )

    story.append(PageBreak())

    # FINDINGS

    rows = [
        [
            "Category",
            "Issue",
            "Recommendation",
            "Priority"
        ]
    ]

    for finding in findings:

        rows.append([
            finding.category,
            finding.issue,
            finding.recommendation,
            finding.priority
        ])

    findings_table = Table(
        rows,
        colWidths=[
            0.9 * inch,
            1.9 * inch,
            2.7 * inch,
            0.8 * inch
        ],
        repeatRows=1
    )

    findings_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7C3AED")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.white,
                colors.HexColor("#F8FAFC")
            ]),
            ("FONTSIZE", (0, 0), (-1, -1), 8)
        ])
    )

    story.extend([
        Paragraph(
            "Detailed Findings",
            styles["Heading2"]
        ),
        findings_table
    ])

    document.build(story)

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes
