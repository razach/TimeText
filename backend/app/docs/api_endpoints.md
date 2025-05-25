# Availability Calendar API Documentation

## Base URL

- Local development: `http://localhost:8000/api/v1`

---

## Endpoints

### 1. Generate Availability Text

- **URL:** `/availability/generate`
- **Method:** `POST`
- **Headers:**
  - `X-API-Key`: Required. The API key for authentication.
- **Request Body:**

```
{
  "selected_slots": [
    { "start": "YYYY-MM-DDTHH:mm:ss±hh:mm", "end": "YYYY-MM-DDTHH:mm:ss±hh:mm" },
    // ... more slots
  ],
  "user_timezone": "America/Los_Angeles",
  "recipient_timezone": "America/New_York", // optional
  "output_format": "continuous", // "continuous" or "chunks"
  "slot_granularity_minutes": 30 // used if output_format is "chunks"
}
```

- **Success Response:**
    - **Status:** `200 OK`
    - **Content-Type:** `application/json`
    - **Body:**
    ```json
    {
      "text_output": "...plain text table...",
      "user_timezone": "America/Los_Angeles",
      "recipient_timezone": "America/New_York"
    }
    ```

- **Error Responses:**
    - **Status:** `400 Bad Request`
    - **Body:**
    ```json
    { "detail": "Descriptive error message" }
    ```
    - **Status:** `401 Unauthorized`
    - **Body:**
    ```json
    { "detail": "Invalid API key" }
    ```
    - **Status:** `500 Internal Server Error`
    - **Body:**
    ```json
    { "detail": "An error occurred: ..." }
    ```

---

## Example Test Scenarios

### Scenario 1: Valid Continuous Output
- **Request:**
    ```json
    {
      "selected_slots": [
        { "start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00" },
        { "start": "2024-03-21T09:00:00-04:00", "end": "2024-03-21T10:00:00-04:00" }
      ],
      "user_timezone": "America/New_York",
      "recipient_timezone": "America/Los_Angeles",
      "output_format": "continuous",
      "slot_granularity_minutes": 30
    }
    ```
- **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
- **Expected Response:**
    - Status: 200
    - `text_output` contains both timezones and both dates.

### Scenario 2: Valid Chunks Output
- **Request:**
    ```json
    {
      "selected_slots": [
        { "start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00" }
      ],
      "user_timezone": "America/New_York",
      "recipient_timezone": "America/Los_Angeles",
      "output_format": "chunks",
      "slot_granularity_minutes": 30
    }
    ```
- **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
- **Expected Response:**
    - Status: 200
    - `text_output` contains 30-minute intervals for the slot.

### Scenario 3: Invalid Timezone
- **Request:**
    ```json
    {
      "selected_slots": [
        { "start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00" }
      ],
      "user_timezone": "Invalid/Timezone",
      "output_format": "continuous"
    }
    ```
- **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
- **Expected Response:**
    - Status: 400
    - `detail` contains "Invalid timezone"

### Scenario 4: Invalid Output Format
- **Request:**
    ```json
    {
      "selected_slots": [
        { "start": "2024-03-20T09:00:00-04:00", "end": "2024-03-20T11:00:00-04:00" }
      ],
      "user_timezone": "America/New_York",
      "output_format": "invalid_format"
    }
    ```
- **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
- **Expected Response:**
    - Status: 400
    - `detail` contains "Invalid output_format"

### Scenario 5: Start Time After End Time
- **Request:**
    ```json
    {
      "selected_slots": [
        { "start": "2024-03-20T11:00:00-04:00", "end": "2024-03-20T09:00:00-04:00" }
      ],
      "user_timezone": "America/New_York",
      "output_format": "continuous"
    }
    ```
- **Headers:**
    ```
    X-API-Key: your-api-key-here
    ```
- **Expected Response:**
    - Status: 400
    - `detail` contains "Start time must be before end time"

---

## See Also
- Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc docs: [http://localhost:8000/redoc](http://localhost:8000/redoc) 