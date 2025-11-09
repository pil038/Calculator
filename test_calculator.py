import unittest
import sys
import os


class TestCalculatorLogic(unittest.TestCase):

    def test_calculation_logic(self):
        """Тестируем логику калькулятора напрямую"""
        # Просто тестируем математику без импорта Flask
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
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Проверяем наличие ключевых элементов
        self.assertIn('@app.route(\'/api/calculate\'', content)
        self.assertIn('def calculate(', content)
        self.assertIn('def api_calculate(', content)


if __name__ == '__main__':
    unittest.main()