from flask import Flask, request, jsonify

app = Flask(__name__)


def calculate(num1, num2, operation):
    """Функция для вычислений с улучшенной обработкой ошибок"""
    operations = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else None
    }

    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")

    if operation == 'divide' and num2 == 0:
        raise ZeroDivisionError("Division by zero is not allowed")

    return operations[operation](num1, num2)


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint with enhanced error handling"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Проверка обязательных полей
        required_fields = ['num1', 'num2', 'operation']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            num1 = float(data['num1'])
            num2 = float(data['num2'])
        except (TypeError, ValueError):
            return jsonify({'error': 'Invalid number format'}), 400

        operation = data['operation']

        # Валидация операции
        valid_operations = ['add', 'subtract', 'multiply', 'divide']
        if operation not in valid_operations:
            return jsonify({'error': f'Invalid operation. Must be one of: {valid_operations}'}), 400

        result = calculate(num1, num2, operation)

        return jsonify({
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'result': result
        })

    except ZeroDivisionError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
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