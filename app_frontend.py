from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница с формой"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calculator</title>
        <style>
            body { font-family: Arial; max-width: 400px; margin: 50px auto; }
            input, select, button { width: 100%; padding: 8px; margin: 5px 0; }
            #result { margin-top: 15px; padding: 10px; }
        </style>
    </head>
    <body>
        <h2>Your calculator</h2>
        <input type="number" id="num1" placeholder="First number" step="any">
        <select id="operation">
            <option value="add">+</option>
            <option value="subtract">-</option>
            <option value="multiply">×</option>
            <option value="divide">÷</option>
        </select>
        <input type="number" id="num2" placeholder="Second number" step="any">
        <button onclick="calculate()">Сalculate</button>
        <div id="result"></div>

        <script>
            async function calculate() {
                const num1 = parseFloat(document.getElementById('num1').value);
                const num2 = parseFloat(document.getElementById('num2').value);
                const operation = document.getElementById('operation').value;

                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ num1, num2, operation })
                });

                const data = await response.json();
                const resultDiv = document.getElementById('result');

                if (response.ok) {
                    resultDiv.innerHTML = `<strong>Result:</strong> ${data.result}`;
                    resultDiv.style.color = 'green';
                } else {
                    resultDiv.innerHTML = `<strong>ERROR:</strong> ${data.error}`;
                    resultDiv.style.color = 'red';
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)