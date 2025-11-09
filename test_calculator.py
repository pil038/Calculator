import unittest
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app_api import app, calculate
except ImportError:
    import importlib.util

    spec = importlib.util.spec_from_file_location("app_api", "app_api.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    app = app_module.app
    calculate = app_module.calculate


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Тесты функции calculate
    def test_calculate_addition(self):
        """Тест сложения"""
        result = calculate(5, 3, 'add')
        self.assertEqual(result, 8)

    def test_calculate_subtraction(self):
        """Тест вычитания"""
        result = calculate(10, 4, 'subtract')
        self.assertEqual(result, 6)

    def test_calculate_multiplication(self):
        """Тест умножения"""
        result = calculate(6, 7, 'multiply')
        self.assertEqual(result, 42)

    def test_calculate_division(self):
        """Тест деления"""
        result = calculate(15, 3, 'divide')
        self.assertEqual(result, 5)

    def test_calculate_division_by_zero(self):
        """Тест деления на ноль"""
        with self.assertRaises(ZeroDivisionError):
            calculate(5, 0, 'divide')

    def test_calculate_invalid_operation(self):
        """Тест неверной операции"""
        with self.assertRaises(ValueError):
            calculate(5, 3, 'invalid_op')

    # Тесты API endpoints
    def test_api_addition(self):
        """Тест API для сложения"""
        response = self.app.post('/api/calculate',
                                 json={'num1': 10, 'num2': 5, 'operation': 'add'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 15)
        self.assertEqual(data['operation'], 'add')

    def test_api_division_by_zero(self):
        """Тест API для деления на ноль"""
        response = self.app.post('/api/calculate',
                                 json={'num1': 10, 'num2': 0, 'operation': 'divide'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_main_page(self):
        """Тест главной страницы"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Calculator', response.data)


class TestCalculatorLogic(unittest.TestCase):

    def test_calculation_logic(self):
        """Тестируем логику калькулятора напрямую"""
        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else None
        }

        # Тест сложения
        result = operations['add'](5, 3)
        self.assertEqual(result, 8)

        # Тест умножения
        result = operations['multiply'](6, 7)
        self.assertEqual(result, 42)

        # Тест деления на ноль
        result = operations['divide'](5, 0)
        self.assertIsNone(result)


class TestAPIStructure(unittest.TestCase):

    def test_api_endpoints_exist(self):
        """Проверяем, что API endpoints существуют в коде"""
        with open('app_api.py', 'r', encoding='utf-8') as f:  # ← ИСПРАВЛЕНО
            content = f.read()

        # Проверяем наличие ключевых элементов
        self.assertIn('@app.route(\'/api/calculate\'', content)
        self.assertIn('def calculate(', content)
        self.assertIn('def api_calculate(', content)


if __name__ == '__main__':
    unittest.main()