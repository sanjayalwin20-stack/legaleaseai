import pytest

from fastapi.testclient import TestClient

from backend.main import app


class FakeGenerator:

    def generate_document(
        self,
        **kwargs
    ):

        return (
            f"{kwargs['document_type']}\n\n"
            f"Parties: {kwargs['parties']}\n"
            f"Effective Date: "
            f"{kwargs['effective_date']}\n\n"
            f"Terms: {kwargs['terms']}\n\n"
            "Drafting Notice: "
            "AI-generated draft for "
            "professional review."
        )


@pytest.fixture
def client(
    monkeypatch
):

    monkeypatch.setattr(
        "backend.routes.generator",
        FakeGenerator()
    )

    return TestClient(
        app
    )