import unittest
import subprocess
import sys
import re

class TestCalculatorTUI(unittest.TestCase):

    def run_tui_command(self, command):
        process = subprocess.Popen([sys.executable, 'calculator_tui.py'], 
                                   stdin=subprocess.PIPE, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   text=True)
        process.stdin.write(command + '\n')
        process.stdin.flush()
        process.stdin.write('q\n') # Quit after the command
        process.stdin.flush()
        output = process.communicate(timeout=5)[0]
        process.wait(timeout=5)
        self.assertEqual(process.returncode, 0)
        return output

    def extract_result(self, output):
        match = re.search(r'Result:\s*([\d\.\-]+|Error.+)', output)
        if match:
            return match.group(1)
        return None

    def test_tui_starts_and_quits(self):
        output = self.run_tui_command('q')
        self.assertIn("Calculator TUI", output)

    def test_addition(self):
        output = self.run_tui_command("2 + 3")
        result = self.extract_result(output)
        self.assertEqual(result, "5.0")

    def test_subtraction(self):
        output = self.run_tui_command("5 - 2")
        result = self.extract_result(output)
        self.assertEqual(result, "3.0")

    def test_multiplication(self):
        output = self.run_tui_command("4 * 6")
        result = self.extract_result(output)
        self.assertEqual(result, "24.0")

    def test_division(self):
        output = self.run_tui_command("10 / 2")
        result = self.extract_result(output)
        self.assertEqual(result, "5.0")

    def test_division_by_zero(self):
        output = self.run_tui_command("5 / 0")
        result = self.extract_result(output)
        self.assertEqual(result, "Error: Division by zero")

    def test_sqrt(self):
        output = self.run_tui_command("sqrt 9")
        result = self.extract_result(output)
        self.assertEqual(result, "3.0")

    def test_sqrt_negative(self):
        output = self.run_tui_command("sqrt -1")
        result = self.extract_result(output)
        self.assertEqual(result, "Error: Invalid input for sqrt")

    def test_power(self):
        output = self.run_tui_command("2 pow 3")
        result = self.extract_result(output)
        self.assertEqual(result, "8.0")


if __name__ == '__main__':
    unittest.main()
