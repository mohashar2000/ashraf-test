from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 80px auto; }
        input, select, button { padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        .result { margin-top: 15px; font-size: 1.2em; font-weight: bold; }
        .error { margin-top: 15px; font-size: 1.1em; color: red; }
    </style>
</head>
<body>
    <h2>Calculator</h2>
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
