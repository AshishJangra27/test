# Game API (FastAPI)

This folder contains a minimal FastAPI server with three game endpoints:

- `GET /head-or-tail`
- `GET /roll-dice`
- `GET /draw-card`

It also includes a health endpoint:

- `GET /health`

---

## 1) How To Run The Server

### Prerequisites

- Python 3.10+
- Dependencies installed (`fastapi`, `uvicorn`, `numpy`)

If needed, install:

```bash
pip install fastapi uvicorn numpy
```

### Start the server

From project root (`mcp_servers`):

```bash
uvicorn game.app:app --reload
```

```bash
python -m uvicorn game.app:app --reload   
```


Expected output includes:

- `Uvicorn running on http://127.0.0.1:8000`

Server base URL:

- `http://127.0.0.1:8000`

---

## 2) How To Stop The Server

### If running in current terminal (foreground)

Press:

- `Ctrl + C`

### If running in background

Stop by process pattern:

```bash
pkill -f "uvicorn game.app:app"
```

Verify nothing is running:

```bash
pgrep -fl "uvicorn game.app:app"
```

---

## 3) Talk To The Server Via Docs Endpoint

FastAPI interactive docs endpoint is:

- `http://127.0.0.1:8000/docs`

Note: FastAPI uses `/docs` (not `/doc`).

### Steps

1. Start server.
2. Open `http://127.0.0.1:8000/docs` in browser.
3. Expand any endpoint (for example `/roll-dice`).
4. Click **Try it out**.
5. Click **Execute**.
6. Inspect response JSON and status code.

You can also use alternate docs UI:

- `http://127.0.0.1:8000/redoc`

---

## 4) Talk To The Server Via Python `requests` Library

Install requests if needed:

```bash
pip install requests
```

Example script:

```python
import requests

BASE = "http://127.0.0.1:8000"

endpoints = [
    "/health",
    "/head-or-tail",
    "/roll-dice",
    "/draw-card",
]

for ep in endpoints:
    r = requests.get(f"{BASE}{ep}", timeout=10)
    print(ep, r.status_code, r.json())
```

Expected sample output shape:

- `/health` -> `{ "status": "ok" }`
- `/head-or-tail` -> `{ "result": "Heads" }` or `{ "result": "Tails" }`
- `/roll-dice` -> `{ "roll": 1..6 }`
- `/draw-card` -> `{ "card": "Q of Diamonds" }`

---

## 5) Talk To The Server Via Postman

### Quick setup

1. Open Postman.
2. Create a new collection (optional), for example: `Game API`.
3. Add 4 requests with method `GET`:
   - `http://127.0.0.1:8000/health`
   - `http://127.0.0.1:8000/head-or-tail`
   - `http://127.0.0.1:8000/roll-dice`
   - `http://127.0.0.1:8000/draw-card`
4. Click **Send** on each request.
5. Verify JSON responses and `200 OK` status.

### Optional Postman Environment

Create an environment variable:

- `base_url = http://127.0.0.1:8000`

Then use URLs like:

- `{{base_url}}/roll-dice`

---

## Troubleshooting

- **Connection refused / timeout**:
  - Server may not be running. Start with `uvicorn game.app:app --reload`.
- **Wrong endpoint path**:
  - Confirm exact paths from `/docs`.
- **Port already in use**:
  - Run on another port:
    ```bash
    uvicorn game.app:app --reload --port 8001
    ```
  - Then use `http://127.0.0.1:8001`.
