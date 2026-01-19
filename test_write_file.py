import unittest
from functions.write_file import write_file


class TestGetFileContent(unittest.TestCase):
    def setUp(self):
        self.write_file = write_file

    def test_calculator(self):
        result = self.write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print("Result for lorem.txt:")
        print("result", result)
        self.assertEqual(result, """Successfully wrote to "lorem.txt" (28 characters written)""")

    def test_calculator_more(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print("Result for pkg/morelorem.txt:")
        print("result", result)
        self.assertEqual(result, 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)')

    def test_calculator_not_allowed(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print("Result for /tmp/temp.txt")
        print("result", result)
        self.assertEqual(result, 'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory')

if __name__ == "__main__":
    unittest.main()