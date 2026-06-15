# Converso API Usage Guide

Converso exposes a FastAPI backend at port `8000` to interact with the LLM chains programmatically. This guide details how to launch and query the API.

## Launching the API

To start the API server, run:
```bash
python endpoint/api.py
```
This starts a Uvicorn server listening on `http://localhost:8000`.

---

## Endpoint Details

### 1. `/chat` (POST)
Sends a message to the chatbot session and returns the AI generated response.

#### Request Schema
```json
{
  "content": "string",
  "chat_history_id": "string"
}
```

* `content` (required): The prompt text to send to the chatbot.
* `chat_history_id` (required): The unique session identifier to load chat memory and store history.

#### Response Schema
```json
{
  "content": "string",
  "chat_history_id": "string"
}
```

* `content`: The AI response.
* `chat_history_id`: The session identifier used.

---

## Example Usage

### Using Curl
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"content": "What is the capital of France?", "chat_history_id": "session-123"}'
```

### Using Python Requests
```python
import requests

url = "http://localhost:8000/chat"
data = {
    "content": "Hello! Introduce yourself.",
    "chat_history_id": "session-123"
}

response = requests.post(url, json=data)
print(response.json())
```
