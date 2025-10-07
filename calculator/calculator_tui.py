import sys
import math

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    return x / y

def sqrt(x):
    if x < 0:
        return "Error: Invalid input for sqrt"
    return math.sqrt(x)

def power(x, y):
    return x ** y


def main():
    print("Calculator TUI")
    print("----------------")
    print("\nAvailable operations: + - * / sqrt pow\n")

    while True:
        expression = input("Enter expression (or 'q' to quit): ")
        if expression.lower() == 'q':
            break

        try:
            parts = expression.split()
            if len(parts) == 3:
                op = parts[1]
                num1 = float(parts[0])
                num2 = float(parts[2])

                if op == '+':
                    result = add(num1, num2)
                elif op == '-':
                    result = subtract(num1, num2)
                elif op == '*':
                    result = multiply(num1, num2)
                elif op == '/':
                    result = divide(num1, num2)
                elif op == 'pow':
                    result = power(num1, num2)
                else:
                    result = "Error: Invalid operator"

            elif len(parts) == 2:
                op = parts[0]
                num = float(parts[1])

                if op == 'sqrt':
                    result = sqrt(num)
                else:
                    result = "Error: Invalid operator"
            else:
                result = "Error: Invalid expression"

            print(f"Result: {result}")

        except ValueError:
            print("Error: Invalid input")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
