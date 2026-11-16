import pytest
from app import app, submissions

VALID = {
    "name": "Amber Fateh Khan",
    "reg_no": "SP23-BCS-062",
    "title": "DevOps Lab Mid",
    "url": "https://github.com/test/repo",
}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    submissions.clear()
    with app.test_client() as c:
        yield c


def test_valid_submission_is_saved(client):
    r = client.post("/", data=VALID)
    assert r.status_code == 200
    assert len(submissions) == 1
    assert "SP23-BCS-062" in r.get_data(as_text=True)


def test_missing_registration_number_is_rejected(client):
    r = client.post("/", data={**VALID, "reg_no": ""})
    assert r.status_code == 400
    assert "Registration number is required" in r.get_data(as_text=True)
    assert len(submissions) == 0


def test_invalid_submission_url_is_rejected(client):
    r = client.post("/", data={**VALID, "url": "not-a-url"})
    assert r.status_code == 400
    assert len(submissions) == 0