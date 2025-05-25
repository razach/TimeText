from datetime import datetime, timedelta
import pytz
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_request_data():
    ny_tz = pytz.timezone('America/New_York')
    base_time = ny_tz.localize(datetime(2024, 3, 20, 9, 0))
    
    return {
        "selected_slots": [
            {
                "start": base_time.isoformat(),
                "end": (base_time + timedelta(hours=2)).isoformat()
            },
            {
                "start": (base_time + timedelta(days=1)).isoformat(),
                "end": (base_time + timedelta(days=1, hours=1)).isoformat()
            }
        ],
        "user_timezone": "America/New_York",
        "recipient_timezone": "America/Los_Angeles",
        "output_format": "continuous",
        "slot_granularity_minutes": 30
    }

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs_url" in data

def test_generate_availability_continuous(sample_request_data):
    response = client.post("/api/v1/availability/generate", json=sample_request_data)
    assert response.status_code == 200
    data = response.json()
    assert "text_output" in data
    assert "user_timezone" in data
    assert "recipient_timezone" in data
    assert "America/New_York" in data["text_output"]
    assert "America/Los_Angeles" in data["text_output"]

def test_generate_availability_chunks(sample_request_data):
    sample_request_data["output_format"] = "chunks"
    response = client.post("/api/v1/availability/generate", json=sample_request_data)
    assert response.status_code == 200
    data = response.json()
    assert "text_output" in data
    assert "9:00 AM" in data["text_output"]
    assert "9:30 AM" in data["text_output"]

def test_invalid_timezone():
    invalid_data = {
        "selected_slots": [
            {
                "start": "2024-03-20T09:00:00-04:00",
                "end": "2024-03-20T11:00:00-04:00"
            }
        ],
        "user_timezone": "Invalid/Timezone",
        "output_format": "continuous"
    }
    response = client.post("/api/v1/availability/generate", json=invalid_data)
    assert response.status_code == 400
    assert "Invalid timezone" in response.json()["detail"]

def test_invalid_output_format(sample_request_data):
    sample_request_data["output_format"] = "invalid_format"
    response = client.post("/api/v1/availability/generate", json=sample_request_data)
    assert response.status_code == 400
    assert "Invalid output_format" in response.json()["detail"] 