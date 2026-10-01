from utils.exporters import (
    format_docx,
    format_pdf,
    format_txt
)

from utils.text_utils import (
    parse_terms,
    sanitize_text,
    safe_filename
)


def test_sanitize_text():

    result = sanitize_text(
        "“Hello” — world…"
    )

    assert result == (
        '"Hello" - world...'
    )


def test_parse_terms():

    result = parse_terms(
        "A; B ; ; C"
    )

    assert result == [
        "A",
        "B",
        "C"
    ]


def test_safe_filename():

    result = safe_filename(
        "Employment Contract",
        "pdf"
    )

    assert (
        result
        == "Employment_Contract.pdf"
    )


def test_txt_export():

    result = format_txt(
        "Hello"
    )

    assert result == b"Hello"


def test_docx_export():

    result = format_docx(
        "EMPLOYMENT CONTRACT\n\nHello",
        "Employment Contract"
    )

    assert result[:2] == b"PK"


def test_pdf_export():

    result = format_pdf(
        "EMPLOYMENT CONTRACT\n\nHello",
        "Employment Contract"
    )

    assert result.startswith(
        b"%PDF"
    )