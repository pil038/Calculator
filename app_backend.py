from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate(num1, num2, operation):
    """Функция для вычислений"""
    operations = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else None
    }
    if operation in operations:
        return operations[operation](num1, num2)
    return None

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for calculations"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        num1 = float(data.get('num1', 0))
        num2 = float(data.get('num2', 0))
        operation = data.get('operation', 'add')

        result = calculate(num1, num2, operation)

        if result is None:
            return jsonify({'error': 'Invalid operation or division by zero'}), 400

        return jsonify({
            'num1': num1,
            'num2': num2,
            'operation': operation,
            'result': result
        })

    except ValueError:
        return jsonify({'error': 'Invalid number format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)