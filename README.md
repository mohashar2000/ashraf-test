# Ashraf Test - Add Two Numbers

A simple Flask web application that adds two numbers. Includes a web form and a JSON API.

## Setup

### Using Python

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:8080 in your browser.

### Using Docker

```bash
docker build -t ashraf-test .
docker run -p 8080:8080 ashraf-test
```

## API

### Web Form

- `GET /` — Displays the form to enter two numbers

### JSON API

- `GET /api/add?num1=5&num2=3` — Returns JSON response:

```json
{
  "num1": 5.0,
  "num2": 3.0,
  "result": 8.0
}
```
