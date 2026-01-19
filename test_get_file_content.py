import unittest
from functions.get_file_content import get_file_content


class TestGetFileContent(unittest.TestCase):
    def setUp(self):
        self.get_file_content = get_file_content

    def test_calculator(self):
        result = self.get_file_content("calculator", "./lorem.txt")
        print("Result for lorem:")
        print("result", result)
        self.assertEqual(len(result), 10053)

    def test_calculator_main(self):
            result = self.get_file_content("calculator", "main.py")
            print("Result for 'main.py':")
            print("result", result)
            self.assertEqual(result, """import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output


def main():
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        if result is not None:
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()""")

    def test_calculator_pkg(self):
            result = self.get_file_content("calculator", "pkg/calculator.py")
            print("Result for 'pkg/calculator.py':")
            print("result", result)
            self.assertEqual(result, """# calculator/pkg/calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))""")
    
    def test_calculator_bin_cat(self):
        result = self.get_file_content("calculator", "./bin/cat")
        print("Result for lorem:")
        print(result)
        self.assertEqual(result, 'Error: File not found or is not a regular file: "./bin/cat"')
    
    def test_calculator_not_exists(self):
        result = self.get_file_content("calculator", "pkg/does_not_exist.py")
        print("Result for lorem:")
        print(result)
        self.assertEqual(result, 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"')
if __name__ == "__main__":
    unittest.main()