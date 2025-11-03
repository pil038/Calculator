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

# ... фронтенд часть остается без изменений ...