"""Upload API tests - 3 tests."""

import os

import requests

BASE_URL = os.getenv("API_URL", "http://localhost:8000")


def test_upload_valid_csv():
    """Upload a valid CSV file - expect 201."""
    csv_content = "id,name,age\n1,Alice,30\n2,Bob,25\n"
    files = {"file": ("test.csv", csv_content.encode(), "text/csv")}
    resp = requests.post(f"{BASE_URL}/api/datasets/upload", files=files)
    assert resp.status_code == 201
    data = resp.json()
    assert data["file_type"] == "csv"
    assert data["row_count"] == 2


def test_upload_invalid_file_type():
    """Upload an unsupported file type - expect 400."""
    files = {"file": ("test.txt", b"hello world", "text/plain")}
    resp = requests.post(f"{BASE_URL}/api/datasets/upload", files=files)
    assert resp.status_code == 400


def test_upload_empty_file():
    """Upload an empty file - expect 400."""
    files = {"file": ("empty.csv", b"", "text/csv")}
    resp = requests.post(f"{BASE_URL}/api/datasets/upload", files=files)
    assert resp.status_code == 400
