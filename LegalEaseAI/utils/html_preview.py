import html

from utils.text_utils import sanitize_text


def format_html_preview(
    text: str,
    title: str = "Document Preview"
):

    clean_text = sanitize_text(text)

    blocks = []

    for raw_block in clean_text.split(
        "\n\n"
    ):

        block = raw_block.strip()

        if not block:
            continue

        escaped = html.escape(
            block
        )

        is_heading = (
            len(block) < 100
            and (
                block.isupper()
                or block.lower().startswith(
                    (
                        "section ",
                        "article ",
                        "clause "
                    )
                )
                or block.endswith(":")
            )
        )

        if is_heading:

            blocks.append(
                f"<h3>{escaped}</h3>"
            )

        else:

            blocks.append(
                "<p>"
                + escaped.replace(
                    "\n",
                    "<br>"
                )
                + "</p>"
            )

    body = "\n".join(
        blocks
    )

    return f"""
    <div style="
        background:#111827;
        color:#f3f4f6;
        border:1px solid #374151;
        border-radius:14px;
        padding:24px;
        max-height:650px;
        overflow:auto;
        font-family:Georgia, 'Times New Roman', serif;
        line-height:1.65;
    ">

        <div style="
            font-family:Arial,sans-serif;
            font-size:13px;
            color:#9ca3af;
            margin-bottom:16px;
        ">
            {html.escape(title)}
        </div>

        {body}

    </div>
    """