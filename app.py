from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Add Two Numbers</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 80px auto; }
        input, button { padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        .result { margin-top: 15px; font-size: 1.2em; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Add Two Numbers</h2>
    <form method="POST" action="/add">
        <input type="number" name="num1" placeholder="Enter first number" step="any" required>
        <input type="number" name="num2" placeholder="Enter second number" step="any" required>
        <button type="submit">Add</button>
    </form>
    {% if result is not none %}
    <div class="result">Result: {{ result }}</div>
    {% endif %}
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, result=None)


@app.route("/add", methods=["POST"])
def add():
    num1 = float(request.form["num1"])
    num2 = float(request.form["num2"])
    result = num1 + num2
    return render_template_string(HTML_TEMPLATE, result=result)


@app.route("/api/add")
def api_add():
    num1 = float(request.args["num1"])
    num2 = float(request.args["num2"])
    return jsonify({"num1": num1, "num2": num2, "result": num1 + num2})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
