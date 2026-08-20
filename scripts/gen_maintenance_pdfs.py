#!/usr/bin/env python3
"""Generate native, engine-specific Maintenance PDFs from the Markdown source."""

from __future__ import annotations

import os
import re
import subprocess
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

import markdown
import zensical
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from svglib.svglib import svg2rlg

ROOT = Path(__file__).parent.parent
SOURCE = ROOT / "docs" / "maintenance.md"
OUTPUT = ROOT / "docs" / "downloads" / "maintenance"
ICON_DIRECTORY = Path(zensical.__file__).parent / "templates" / ".icons" / "lucide"
ICON_VERTICAL_OFFSET = 2


def source_revision() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=8", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return os.environ.get("GITHUB_SHA", "unknown")[:8]


SOURCE_REVISION = source_revision()

ENGINE_FILES = {
    "5.7L GM": "5-7l-gm.pdf",
    "6.7LT PSI": "6-7lt-psi.pdf",
    "11LT PSI": "11lt-psi.pdf",
    "13LT PSI": "13lt-psi.pdf",
    "22LT Mesa": "22lt-mesa.pdf",
}

TYPE_COLORS = {
    "info": ("#00a6c0", "#e5f8fb"),
    "note": ("#3978e8", "#edf3ff"),
    "tip": ("#00a98f", "#e5faf6"),
    "success": ("#00ad49", "#e6f8ed"),
    "question": ("#58bd14", "#f0fae8"),
    "warning": ("#e98200", "#fff4e5"),
    "failure": ("#e64949", "#ffebeb"),
    "danger": ("#df143d", "#ffe7ec"),
    "example": ("#7044e6", "#f1edff"),
}

ICON_NAMES = {
    "info": "info",
    "note": "paperclip",
    "tip": "flame",
    "success": "check",
    "question": "circle-question-mark",
    "warning": "triangle-alert",
    "failure": "octagon-alert",
    "danger": "zap",
    "example": "flask-conical",
    "maintenance": "wrench",
    "task": "square",
}


@dataclass(frozen=True)
class ContentItem:
    kind: str
    markup: str


@dataclass(frozen=True)
class Admonition:
    kind: str
    icon_kind: str
    title: str
    content: tuple[ContentItem, ...]


@dataclass(frozen=True)
class MaintenanceDocument:
    title: str
    introduction: str
    fluids: dict[str, tuple[Admonition, ...]]
    checklists: dict[str, tuple[Admonition, ...]]


def strip_front_matter(source: str) -> str:
    if not source.startswith("---\n"):
        return source
    parts = source.split("---", 2)
    return parts[2].lstrip() if len(parts) == 3 else source


def class_names(element: ET.Element) -> set[str]:
    return set(element.attrib.get("class", "").split())


def direct_child_with_class(element: ET.Element, class_name: str) -> ET.Element:
    for child in element:
        if class_name in class_names(child):
            return child
    raise ValueError(f"Missing .{class_name} below <{element.tag}>")


def inline_markup(element: ET.Element) -> str:
    result = escape(element.text or "")
    wrappers = {
        "strong": ("<b>", "</b>"),
        "b": ("<b>", "</b>"),
        "em": ("<i>", "</i>"),
        "i": ("<i>", "</i>"),
        "sub": ("<sub>", "</sub>"),
        "sup": ("<super>", "</super>"),
        "code": ('<font name="Courier">', "</font>"),
    }

    for child in element:
        if child.tag == "input":
            child_markup = ""
        elif child.tag == "br":
            child_markup = "<br/>"
        elif child.tag == "a":
            href = escape(child.attrib.get("href", ""), {'"': "&quot;"})
            child_markup = f'<a href="{href}">{inline_markup(child)}</a>'
        else:
            opening, closing = wrappers.get(child.tag, ("", ""))
            child_markup = f"{opening}{inline_markup(child)}{closing}"
        result += child_markup + escape(child.tail or "")

    return " ".join(result.split())


def parse_admonition(element: ET.Element) -> Admonition:
    classes = element.attrib.get("class", "").split()
    kind = next((name for name in classes if name != "admonition"), "note")
    icon_kind = (
        "maintenance"
        if any(name.startswith("maintenance-") for name in classes)
        else kind
    )
    title = kind.title()
    content: list[ContentItem] = []

    for child in element:
        if "admonition-title" in class_names(child):
            title = "".join(child.itertext()).strip()
        elif child.tag == "p":
            content.append(ContentItem("paragraph", inline_markup(child)))
        elif child.tag in {"ul", "ol"}:
            for item in child.findall("./li"):
                item_kind = "task" if "task-list-item" in class_names(item) else "bullet"
                content.append(ContentItem(item_kind, inline_markup(item)))

    return Admonition(kind, icon_kind, title, tuple(content))


def parse_tab_set(tab_set: ET.Element) -> dict[str, tuple[Admonition, ...]]:
    labels_element = direct_child_with_class(tab_set, "tabbed-labels")
    content_element = direct_child_with_class(tab_set, "tabbed-content")
    labels = ["".join(label.itertext()).strip() for label in labels_element.findall("./label")]
    blocks = [child for child in content_element if "tabbed-block" in class_names(child)]

    if len(labels) != len(blocks):
        raise ValueError(f"Tab label/content mismatch: {len(labels)} labels, {len(blocks)} blocks")

    parsed: dict[str, tuple[Admonition, ...]] = {}
    for label, block in zip(labels, blocks, strict=True):
        parsed[label] = tuple(
            parse_admonition(child)
            for child in block
            if "admonition" in class_names(child)
        )
    return parsed


def parse_document(source_path: Path) -> MaintenanceDocument:
    source = strip_front_matter(source_path.read_text(encoding="utf-8"))
    rendered = markdown.markdown(
        source,
        extensions=[
            "admonition",
            "pymdownx.tabbed",
            "pymdownx.tasklist",
            "pymdownx.tilde",
            "tables",
        ],
        extension_configs={"pymdownx.tabbed": {"alternate_style": True}},
    )

    # Python Markdown emits valid HTML boolean attributes, which need values
    # before the fragment can be consumed by ElementTree as XML.
    rendered = re.sub(
        r"(?<=\s)(disabled|checked)(?=[\s/>])",
        r'\1="\1"',
        rendered,
    )
    root = ET.fromstring(f"<root>{rendered}</root>")
    children = list(root)

    title_element = next(child for child in children if child.tag == "h1")
    title_index = children.index(title_element)
    intro_element = next(
        (child for child in children[title_index + 1 :] if child.tag == "p"),
        None,
    )
    tab_sets = [child for child in children if "tabbed-set" in class_names(child)]
    if len(tab_sets) != 2:
        raise ValueError(f"Expected two Maintenance tab sets, found {len(tab_sets)}")

    document = MaintenanceDocument(
        title="".join(title_element.itertext()).strip(),
        introduction=inline_markup(intro_element) if intro_element is not None else "",
        fluids=parse_tab_set(tab_sets[0]),
        checklists=parse_tab_set(tab_sets[1]),
    )

    expected = set(ENGINE_FILES)
    if set(document.fluids) != expected or set(document.checklists) != expected:
        raise ValueError("Maintenance tabs do not match the configured engine PDF names")
    return document


@lru_cache(maxsize=None)
def _svg_icon(kind: str, color_hex: str, size: float) -> Drawing:
    icon_name = ICON_NAMES.get(kind, ICON_NAMES["note"])
    source_path = ICON_DIRECTORY / f"{icon_name}.svg"
    if not source_path.exists():
        raise FileNotFoundError(f"Zensical icon not found: {source_path}")

    source = source_path.read_text(encoding="utf-8").replace("currentColor", color_hex)
    drawing = svg2rlg(BytesIO(source.encode("utf-8")))
    if drawing is None:
        raise ValueError(f"Could not parse SVG icon: {source_path}")

    scale = size / 24
    drawing.translate(0, ICON_VERTICAL_OFFSET)
    drawing.scale(scale, scale)
    drawing.width = size
    drawing.height = size
    return drawing


def status_icon(kind: str, color_hex: str, size: float = 14) -> Drawing:
    return deepcopy(_svg_icon(kind, color_hex, size))


def styles() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle(
            "Title",
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=HexColor("#17191c"),
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=HexColor("#4051b5"),
            spaceAfter=12,
        ),
        "heading": ParagraphStyle(
            "Heading2",
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=HexColor("#17191c"),
            spaceBefore=10,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=HexColor("#25282d"),
            spaceAfter=8,
        ),
        "box_title": ParagraphStyle(
            "BoxTitle",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=HexColor("#202328"),
        ),
        "box_body": ParagraphStyle(
            "BoxBody",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=HexColor("#25282d"),
        ),
    }


def admonition_table(admonition: Admonition, available_width: float, style: dict[str, ParagraphStyle]) -> Table:
    accent_hex, background_hex = TYPE_COLORS.get(admonition.kind, TYPE_COLORS["note"])
    accent = HexColor(accent_hex)
    background = HexColor(background_hex)
    rows: list[list[object]] = [
        [status_icon(admonition.icon_kind, accent_hex), Paragraph(escape(admonition.title), style["box_title"])],
    ]

    for item in admonition.content:
        if item.kind == "task":
            icon: object = status_icon("task", "#6b7178", 12)
        elif item.kind == "bullet":
            icon = Paragraph("&#8226;", style["box_body"])
        else:
            icon = ""
        rows.append([icon, Paragraph(item.markup, style["box_body"])])

    table = Table(
        rows,
        colWidths=[0.27 * inch, available_width - 0.27 * inch],
        hAlign="LEFT",
        splitByRow=1,
        repeatRows=1,
        cornerRadii=[6, 6, 6, 6],
    )
    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.5, accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, -1), 8),
        ("RIGHTPADDING", (0, 0), (0, -1), 2),
        ("LEFTPADDING", (1, 0), (1, -1), 2),
        ("RIGHTPADDING", (1, 0), (1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ("TOPPADDING", (0, 1), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 3),
    ]
    if len(rows) > 1:
        commands.append(("NOSPLIT", (0, 0), (-1, 1)))
    table.setStyle(TableStyle(commands))
    return table


def draw_page_frame(canvas, document, engine: str) -> None:
    width, height = LETTER
    canvas.saveState()
    canvas.setTitle(f"Maintenance - {engine}")
    canvas.setAuthor("Upstream Data Inc")

    canvas.setFillColor(HexColor("#4051b5"))
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(document.leftMargin, height - 0.38 * inch, "UPSTREAM DATA")
    canvas.setFillColor(HexColor("#6b7178"))
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(width - document.rightMargin, height - 0.38 * inch, f"MAINTENANCE | {engine}")

    canvas.setStrokeColor(HexColor("#d9dce1"))
    canvas.line(document.leftMargin, 0.42 * inch, width - document.rightMargin, 0.42 * inch)
    canvas.setFillColor(HexColor("#6b7178"))
    canvas.setFont("Helvetica", 7)
    canvas.drawString(
        document.leftMargin,
        0.25 * inch,
        f"2026 / UPSTREAM DATA INC. / REV {SOURCE_REVISION}",
    )
    canvas.drawRightString(width - document.rightMargin, 0.25 * inch, f"Page {document.page}")
    canvas.restoreState()


def generate_pdf(document: MaintenanceDocument, engine: str, destination: Path) -> None:
    style = styles()
    pdf = SimpleDocTemplate(
        str(destination),
        pagesize=LETTER,
        leftMargin=0.62 * inch,
        rightMargin=0.62 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.55 * inch,
        title=f"Maintenance - {engine}",
        author="Upstream Data Inc",
        subject=f"Engine maintenance requirements and checklist for {engine}",
    )
    available_width = LETTER[0] - pdf.leftMargin - pdf.rightMargin

    def interval_table(admonition: Admonition) -> Table:
        table = admonition_table(admonition, available_width, style)
        _, table_height = table.wrap(available_width, pdf.height)
        if table_height + 7 > pdf.height:
            raise ValueError(
                f"{engine}: service interval {admonition.title!r} exceeds one PDF page"
            )
        return table

    story: list[object] = [
        Paragraph(escape(document.title), style["title"]),
        Paragraph(escape(engine), style["subtitle"]),
    ]
    if document.introduction:
        story.append(Paragraph(document.introduction, style["body"]))
    story.append(Paragraph("Engine fluid requirements", style["heading"]))

    for admonition in document.fluids[engine]:
        story.extend([admonition_table(admonition, available_width, style), Spacer(1, 7)])

    checklist = document.checklists[engine]
    first_interval = [
        Paragraph("Engine Maintenance Checklist", style["heading"]),
        interval_table(checklist[0]),
        Spacer(1, 7),
    ]
    story.append(KeepTogether(first_interval))
    for admonition in checklist[1:]:
        story.append(
            KeepTogether(
                [interval_table(admonition), Spacer(1, 7)]
            )
        )

    page_frame = lambda canvas, doc: draw_page_frame(canvas, doc, engine)
    pdf.build(story, onFirstPage=page_frame, onLaterPages=page_frame)


def main() -> None:
    document = parse_document(SOURCE)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for engine, filename in ENGINE_FILES.items():
        destination = OUTPUT / filename
        generate_pdf(document, engine, destination)
        print(f"Generated {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
