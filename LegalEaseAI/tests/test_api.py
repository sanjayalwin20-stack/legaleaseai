def test_root(client):

    response = client.get("/")

    assert response.status_code == 200

    assert (
        response.json()["service"]
        == "LegalEase API"
    )


def test_health(client):

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_generate(client):

    payload = {

        "document_type": "NDA",

        "parties":
            "Alice (Disclosing), "
            "Bob (Receiving)",

        "terms":
            "Confidentiality; "
            "30 day termination notice",

        "effective_date":
            "2026-10-01"
    }


    response = client.post(
        "/generate",
        json=payload
    )


    assert response.status_code == 200


    body = response.json()


    assert (
        body["document_type"]
        == "NDA"
    )


    assert (
        "Confidentiality"
        in body["content"]
    )


def test_generate_validation(client):

    payload = {

        "document_type": "",

        "parties": "Alice",

        "terms":
            "Confidentiality",

        "effective_date":
            "2026-10-01"
    }


    response = client.post(
        "/generate",
        json=payload
    )


    assert (
        response.status_code
        == 422
    )