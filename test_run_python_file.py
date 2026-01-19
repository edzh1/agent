import unittest
from functions.run_python_file import run_python_file


class TestGetFileContent(unittest.TestCase):
    def setUp(self):
        self.run_python_file = run_python_file

    def test_calculator(self):
        result = self.run_python_file("calculator", "main.py")
        print("Result for main.py:")
        print("result", result)
        self.assertEqual(result, """STDOUT: Calculator App
Usage: python main.py "<expression>"
Example: python main.py "3 + 5"
STDERR: """)

    def test_calculator_addition(self):
        result = self.run_python_file("calculator", "main.py", ["3 + 5"])
        print("Result for main.py addition:")
        print("result", result)
        self.assertEqual(result, """STDOUT: {
  "expression": "3 + 5",
  "result": 8
}
STDERR: """)
        
    
    def test_calculator_tests(self):
        result = self.run_python_file("calculator", "tests.py")
        print("Result for tests")
        print("result")
        print(result)
        self.assertEqual(result, """STDOUT: STDERR: .........
----------------------------------------------------------------------
Ran 9 tests in 0.000s

OK
""")
    def test_calculator_error(self):
        result = self.run_python_file("calculator", "../main.py")
        print("Result for main.py error:")
        print("result", result)
        self.assertEqual(result, """Error: Cannot execute "../main.py" as it is outside the permitted working directory""")
    
    def test_calculator_error_non_exists(self):
        result = self.run_python_file("calculator", "nonexistent.py")
        print("Result for nonexistent.py error:")
        print("result", result)
        self.assertEqual(result, """Error: "nonexistent.py" does not exist or is not a regular file""")
    
    def test_calculator_error_py_file(self):
        result = self.run_python_file("calculator", "lorem.txt")
        print("Result for not py file error:")
        print("result", result)
        self.assertEqual(result, """Error: "lorem.txt" is not a Python file""")

if __name__ == "__main__":
    unittest.main()