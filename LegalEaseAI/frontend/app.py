import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv

from utils.exporters import (
    format_docx,
    format_pdf,
    format_txt
)

from utils.html_preview import (
    format_html_preview
)

from utils.text_utils import (
    safe_filename
)


load_dotenv()


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


if "generated_text" not in st.session_state:

    st.session_state[
        "generated_text"
    ] = ""


if "edited_text" not in st.session_state:

    st.session_state[
        "edited_text"
    ] = ""


if "document_type" not in st.session_state:

    st.session_state[
        "document_type"
    ] = "Non-Disclosure Agreement"


st.markdown(
    """
    <style>

    .main-title {

        text-align:center;

        font-size:42px;

        font-weight:700;

        margin-bottom:0;

    }

    .subtitle {

        text-align:center;

        color:#6b7280;

        margin-top:4px;

        margin-bottom:28px;

    }

    .notice {

        padding:12px 16px;

        border-radius:10px;

        background:#fff7ed;

        border:1px solid #fed7aa;

    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="main-title">'
    '⚖️ LegalEase'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-assisted legal document drafting and export'
    '</div>',
    unsafe_allow_html=True
)


with st.sidebar:

    st.header(
        "Document Settings"
    )

    document_type = st.selectbox(
        "Document Type",

        [
            "Non-Disclosure Agreement",
            "Employment Contract",
            "Lease Agreement",
            "Employment Offer Letter",
            "Service Agreement",
            "Freelance Work Contract",
            "Business Agreement",
            "Custom Legal Document"
        ]
    )

    st.session_state[
        "document_type"
    ] = document_type


    logo = st.file_uploader(
        "Optional Logo",

        type=[
            "png",
            "jpg",
            "jpeg"
        ],

        help=(
            "The logo will be added "
            "to DOCX and PDF exports."
        )
    )


    st.caption(
        f"Backend: `{BACKEND_URL}`"
    )


    if st.button(
        "Check Backend",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{BACKEND_URL}/health",
                timeout=5
            )

            response.raise_for_status()

            st.success(
                "Backend is reachable."
            )

        except requests.RequestException as exc:

            st.error(
                f"Backend unavailable: {exc}"
            )


st.subheader(
    "Document Information"
)


with st.form(
    "document_form"
):

    parties = st.text_area(
        "Parties Involved",

        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),

        height=90
    )


    terms = st.text_area(
        "Terms & Conditions",

        placeholder=(
            "Payment to be made within "
            "30 days of invoice; "
            "Confidentiality must be maintained; "
            "Either party may terminate with "
            "15 days notice"
        ),

        height=150,

        help=(
            "Separate terms using semicolons."
        )
    )


    effective_date = st.date_input(
        "Effective Date",
        value=date.today()
    )


    submitted = st.form_submit_button(
        "Generate Document",
        type="primary",
        use_container_width=True
    )


if submitted:

    if not parties.strip():

        st.error(
            "Please enter the parties."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "effective_date":
                effective_date.isoformat()
        }


        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                generated_text = (
                    result["content"]
                )

                st.session_state[
                    "generated_text"
                ] = generated_text

                st.session_state[
                    "edited_text"
                ] = generated_text

                st.success(
                    "Document generated successfully."
                )

            except requests.HTTPError:

                try:

                    detail = (
                        response.json()
                        .get(
                            "detail",
                            response.text
                        )
                    )

                except Exception:

                    detail = response.text

                st.error(
                    f"Generation failed: {detail}"
                )

            except requests.RequestException as exc:

                st.error(
                    f"Could not connect to backend: {exc}"
                )


if st.session_state[
    "generated_text"
]:

    st.divider()

    st.subheader(
        "Document Preview"
    )


    current_text = (
        st.session_state[
            "edited_text"
        ]
    )


    st.components.v1.html(

        format_html_preview(
            current_text,
            document_type
        ),

        height=680,

        scrolling=True
    )


    st.subheader(
        "Edit Document"
    )


    edited_text = st.text_area(

        "Edit the generated document",

        value=current_text,

        height=500,

        label_visibility="collapsed"
    )


    st.session_state[
        "edited_text"
    ] = edited_text


    logo_bytes = (
        logo.getvalue()
        if logo
        else None
    )


    txt_data = format_txt(
        edited_text
    )


    docx_data = format_docx(

        edited_text,

        document_type,

        terms=terms,

        logo_bytes=logo_bytes
    )


    pdf_data = format_pdf(

        edited_text,

        document_type,

        logo_bytes=logo_bytes
    )


    filename_base = safe_filename(
        document_type,
        ""
    ).rstrip(".")


    st.subheader(
        "Download Document"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.download_button(

            "Download TXT",

            data=txt_data,

            file_name=(
                f"{filename_base}.txt"
            ),

            mime="text/plain",

            use_container_width=True
        )


    with col2:

        st.download_button(

            "Download DOCX",

            data=docx_data,

            file_name=(
                f"{filename_base}.docx"
            ),

            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            use_container_width=True
        )


    with col3:

        st.download_button(

            "Download PDF",

            data=pdf_data,

            file_name=(
                f"{filename_base}.pdf"
            ),

            mime="application/pdf",

            use_container_width=True
        )


    st.markdown(
        """
        <div class="notice">

        <strong>Drafting Notice:</strong>

        This application generates AI-assisted
        drafts for informational and drafting
        purposes. Important legal documents
        should be reviewed by a qualified legal
        professional before signing or relying
        on them.

        </div>
        """,

        unsafe_allow_html=True
    )

else:

    st.info(
        "Enter the document information "
        "and click Generate Document."
    )