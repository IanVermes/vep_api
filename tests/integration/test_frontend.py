import pytest
from bs4 import BeautifulSoup


def test_index_page_title(client):
    response = client.get("/")

    soup = BeautifulSoup(response.content, "html.parser")
    tag = soup.select_one("title")

    assert tag is not None
    assert "Variant Effect Predictor - VEP WebApp" in tag.text


def test_index_page_content(client):
    response = client.get("/")

    assert "VEP Uploader" in str(response.content)


def test_index_page_status(client):
    response = client.get("/")
    assert response.status_code == 200
