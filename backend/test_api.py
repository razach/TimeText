import requests
import json
from datetime import datetime, timedelta
import pytz

# API Configuration
BASE_URL = "https://timetext-1d1c.onrender.com/api/v1"
API_KEY = "who-knows-if-this-is-going-to-work-!"
ENDPOINT = "/availability/"

def test_api():
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    # Test Case 1: Valid Continuous Output
    print("\nTest Case 1: Valid Continuous Output")
    payload = {
        "selected_slots": [
            {"start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00"},
            {"start": "2024-03-21T09:00:00-04:00", "end": "2024-03-21T10:00:00-04:00"}
        ],
        "user_timezone": "America/New_York",
        "recipient_timezone": "America/Los_Angeles",
        "output_format": "continuous"
    }
    response = requests.post(f"{BASE_URL}{ENDPOINT}", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test Case 2: Valid Chunks Output
    print("\nTest Case 2: Valid Chunks Output")
    payload = {
        "selected_slots": [
            {"start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00"}
        ],
        "user_timezone": "America/New_York",
        "recipient_timezone": "America/Los_Angeles",
        "output_format": "chunks",
        "slot_granularity_minutes": 30
    }
    response = requests.post(f"{BASE_URL}{ENDPOINT}", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test Case 3: Invalid Timezone
    print("\nTest Case 3: Invalid Timezone")
    payload = {
        "selected_slots": [
            {"start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00"}
        ],
        "user_timezone": "Invalid/Timezone",
        "output_format": "continuous"
    }
    response = requests.post(f"{BASE_URL}{ENDPOINT}", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test Case 4: Invalid Output Format
    print("\nTest Case 4: Invalid Output Format")
    payload = {
        "selected_slots": [
            {"start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00"}
        ],
        "user_timezone": "America/New_York",
        "output_format": "invalid_format"
    }
    response = requests.post(f"{BASE_URL}{ENDPOINT}", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test Case 5: Start Time After End Time
    print("\nTest Case 5: Start Time After End Time")
    payload = {
        "selected_slots": [
            {"start": "2024-03-20T11:00:00-04:00", "end": "2024-03-20T09:00:00-04:00"}
        ],
        "user_timezone": "America/New_York",
        "output_format": "continuous"
    }
    response = requests.post(f"{BASE_URL}{ENDPOINT}", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test Case 6: Missing Required Fields
    print("\nTest Case 6: Missing Required Fields")
    payload = {
        "user_timezone": "America/New_York",
        "output_format": "continuous"
    }
    response = requests.post(f"{BASE_URL}{ENDPOINT}", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test Case 7: Invalid API Key
    print("\nTest Case 7: Invalid API Key")
    invalid_headers = headers.copy()
    invalid_headers["X-API-Key"] = "invalid-key"
    payload = {
        "selected_slots": [
            {"start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00"}
        ],
        "user_timezone": "America/New_York",
        "output_format": "continuous"
    }
    response = requests.post(f"{BASE_URL}{ENDPOINT}", headers=invalid_headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_api() 