import logging

from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)


logger = logging.getLogger(__name__)

router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    payload: DocumentRequest
):

    try:

        content = generator.generate_document(
            document_type=payload.document_type,
            parties=payload.parties,
            terms=payload.terms,
            effective_date=payload.effective_date,
        )

        return DocumentResponse(
            document_type=payload.document_type,
            content=content,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception:

        logger.exception(
            "Document generation failed"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "The AI document-generation service "
                "could not complete the request."
            )
        )