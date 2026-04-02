from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Calculator</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 24px;
            padding: 40px 32px;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4);
        }

        h2 {
            color: #fff;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 28px;
            background: linear-gradient(90deg, #ff6fd8, #3813c2, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        input, select {
            padding: 14px 16px;
            margin: 8px 0;
            width: 100%;
            border: 2px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
            font-size: 1rem;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        input::placeholder { color: rgba(255, 255, 255, 0.4); }

        input:focus, select:focus {
            border-color: #ff6fd8;
            box-shadow: 0 0 0 3px rgba(255, 111, 216, 0.25);
        }

        select option { background: #302b63; color: #fff; }

        button {
            margin-top: 16px;
            padding: 14px;
            width: 100%;
            border: none;
            border-radius: 12px;
            background: linear-gradient(90deg, #ff6fd8, #7b2ff7, #00d4ff);
            color: #fff;
            font-size: 1rem;
            font-weight: 700;
            font-family: inherit;
            cursor: pointer;
            letter-spacing: 0.5px;
            transition: opacity 0.2s, transform 0.1s;
        }

        button:hover { opacity: 0.88; transform: translateY(-1px); }
        button:active { transform: translateY(0); }

        .result {
            margin-top: 20px;
            padding: 16px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(123, 47, 247, 0.15));
            border: 1px solid rgba(0, 212, 255, 0.3);
            font-size: 1.3em;
            font-weight: 700;
            color: #00d4ff;
            text-align: center;
        }

        .error {
            margin-top: 20px;
            padding: 16px;
            border-radius: 12px;
            background: rgba(255, 0, 110, 0.12);
            border: 1px solid rgba(255, 0, 110, 0.4);
            font-size: 1.1em;
            color: #ff006e;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="card">
    <h2>Calculator ✨</h2>
    <form method="POST" action="/calculate">
        <input type="number" name="num1" placeholder="Enter first number" step="any" required>
        <select name="operation">
            <option value="add">Add (+)</option>
            <option value="subtract">Subtract (-)</option>
            <option value="multiply">Multiply (*)</option>
            <option value="divide">Divide (/)</option>
        </select>
        <input type="number" name="num2" placeholder="Enter second number" step="any" required>
        <button type="submit">Calculate</button>
    </form>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% elif result is not none %}
    <div class="result">Result: {{ result }}</div>
    {% endif %}
</div>
</body>
</html>
"""


OPERATIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b,
}


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, result=None, error=None)


@app.route("/calculate", methods=["POST"])
def calculate():
    num1 = float(request.form["num1"])
    num2 = float(request.form["num2"])
    operation = request.form["operation"]
    if operation == "divide" and num2 == 0:
        return render_template_string(HTML_TEMPLATE, result=None, error="Cannot divide by zero")
    result = OPERATIONS[operation](num1, num2)
    return render_template_string(HTML_TEMPLATE, result=result, error=None)


@app.route("/api/<operation>")
def api_calculate(operation):
    if operation not in OPERATIONS:
        return jsonify({"error": "Invalid operation. Use: add, subtract, multiply, divide"}), 400
    num1 = float(request.args["num1"])
    num2 = float(request.args["num2"])
    if operation == "divide" and num2 == 0:
        return jsonify({"error": "Cannot divide by zero"}), 400
    result = OPERATIONS[operation](num1, num2)
    return jsonify({"num1": num1, "num2": num2, "operation": operation, "result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
