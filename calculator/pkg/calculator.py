import re
import math

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "sqrt": lambda a: math.sqrt(a),
            "pow": lambda a, b: a ** b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "sqrt": 3,
            "pow": 3,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = re.findall(r'(\d+\.?\d*)|([+\-*/()])|(sqrt)|(pow)', expression)
        tokens = [token for group in tokens for token in group if token]
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
        if operator == "sqrt":
            if not values:
                raise ValueError(f"not enough operands for operator {operator}")
            a = values.pop()
            values.append(self.operators[operator](a))
        elif operator == "pow":
            if len(values) < 2:
                raise ValueError(f"not enough operands for operator {operator}")

            b = values.pop()
            a = values.pop()
            values.append(self.operators[operator](a, b))
        else:
            if len(values) < 2:
                raise ValueError(f"not enough operands for operator {operator}")

            b = values.pop()
            a = values.pop()
            if operator == '/' and b == 0:
                raise ValueError("division by zero")
            values.append(self.operators[operator](a, b))
