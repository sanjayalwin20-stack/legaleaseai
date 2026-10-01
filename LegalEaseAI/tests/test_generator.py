from ai_core.gemini_generator import (
    GeminiDocumentGenerator
)


def test_prompt_contains_inputs():

    prompt = (
        GeminiDocumentGenerator
        .build_prompt(

            "NDA",

            "Alice and Bob",

            "Keep information confidential",

            "2026-10-01"
        )
    )


    assert "NDA" in prompt

    assert (
        "Alice and Bob"
        in prompt
    )

    assert (
        "Keep information confidential"
        in prompt
    )

    assert (
        "2026-10-01"
        in prompt
    )


def test_missing_key_raises():

    generator = (
        GeminiDocumentGenerator(
            api_key=None,
            client=None
        )
    )

    generator.api_key = None


    try:

        generator.generate_document(

            "NDA",

            "A and B",

            "Confidentiality",

            "2026-10-01"
        )

    except ValueError as exc:

        assert (
            "GEMINI_API_KEY"
            in str(exc)
        )

    else:

        raise AssertionError(
            "Expected ValueError"
        )