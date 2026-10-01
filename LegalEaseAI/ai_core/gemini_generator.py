import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI-assisted legal document drafting system.

Your job is to create a clear, structured FIRST DRAFT of a legal document from
the user's supplied facts.

Important rules:

1. Do not invent names, dates, prices, addresses, jurisdictions, obligations,
   or other material facts.

2. If important information is missing, use:
   [MISSING: information required]
   instead of inventing information.

3. Use professional legal-document structure.

4. Include:
   - Document title
   - Parties
   - Effective date
   - Background or recitals where appropriate
   - Numbered sections
   - Relevant clauses
   - Signature blocks

5. Preserve all important user-provided terms.

6. Do not claim that the generated document is legally valid or suitable for
   every jurisdiction.

7. Do not fabricate jurisdiction-specific laws.

8. End the document with a short drafting notice explaining that it is an
   AI-generated draft that should be reviewed by a qualified legal professional.

9. Return plain text only.

10. Do not provide hidden reasoning or analysis.
"""


class GeminiDocumentGenerator:
    """
    Handles communication with Google's Gemini API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        client=None,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        self.model = model or os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        self._client = client

        if self._client is None and self.api_key:
            from google import genai

            self._client = genai.Client(
                api_key=self.api_key
            )

    @staticmethod
    def build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:

        return f"""
Create a first-draft {document_type} using ONLY the information supplied below.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{effective_date}

Formatting requirements:

- Use a clear document title.
- Use numbered headings and clauses.
- Include the supplied terms as substantive clauses.
- Add signature blocks appropriate to the document.
- Mark missing material information with [MISSING: ...].
- Do not fabricate jurisdiction-specific legal requirements.
- End with a brief drafting notice.

Create a professional and readable legal-document draft.
""".strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:

        if not self.api_key and self._client is None:
            raise ValueError(
                "GEMINI_API_KEY is not configured. "
                "Please add it to your .env file."
            )

        if self._client is None:
            from google import genai

            self._client = genai.Client(
                api_key=self.api_key
            )

        from google.genai import types

        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
        )

        response = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.25,
                max_output_tokens=12000,
            ),
        )

        generated_text = getattr(
            response,
            "text",
            None
        )

        if not generated_text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return generated_text.strip()