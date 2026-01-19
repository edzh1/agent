import unittest
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        self.get_files_info = get_files_info

    def test_calculator(self):
        result = self.get_files_info("calculator", ".")
        print("Result for current directory:")
        self.assertEqual(result, """- tests.py: file_size=1353 bytes, is_dir=False
- main.py: file_size=718 bytes, is_dir=False
- pkg: file_size=160 bytes, is_dir=True""")

    def test_calculator_pkg(self):
            result = self.get_files_info("calculator", "pkg")
            print("Result for 'pkg' directory:")
            self.assertEqual(result, """- render.py: file_size=403 bytes, is_dir=False
- __pycache__: file_size=128 bytes, is_dir=True
- calculator.py: file_size=1752 bytes, is_dir=False""")

    def test_calculator_bin(self):
            result = self.get_files_info("calculator", "/bin")
            print("Result for '/bin' directory:")
            self.assertEqual(result, """Error: Cannot list "/bin" as it is outside the permitted working directory""")


    def test_calculator_parent(self):
            result = self.get_files_info("calculator", "../")
            print("Result for '../' directory:")
            self.assertEqual(result, """Error: Cannot list "../" as it is outside the permitted working directory""")

if __name__ == "__main__":
    unittest.main()