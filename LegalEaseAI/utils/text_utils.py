import re
import unicodedata


def sanitize_text(text: str) -> str:

    if not isinstance(text, str):
        raise TypeError(
            "text must be a string"
        )

    replacements = {

        "\u2018": "'",
        "\u2019": "'",

        "\u201c": '"',
        "\u201d": '"',

        "\u2013": "-",
        "\u2014": "-",

        "\u2026": "...",

        "\u00a0": " ",

        "\u2022": "-",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    text = unicodedata.normalize(
        "NFKC",
        text
    )

    text = text.replace(
        "\r\n",
        "\n"
    )

    text = text.replace(
        "\r",
        "\n"
    )

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )

    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text
    )

    return text.strip()


def parse_terms(terms: str):

    clean_terms = sanitize_text(
        terms
    )

    result = []

    for item in clean_terms.split(";"):

        item = item.strip(
            " -\t"
        )

        if item:
            result.append(item)

    return result


def safe_filename(
    document_type: str,
    extension: str
):

    name = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        document_type
    )

    name = name.strip("_")

    if not name:
        name = "legal_document"

    extension = extension.lstrip(".")

    return f"{name[:80]}.{extension}"