def evaluate_rpn(expression: str) -> float:
    """
    Evaluate a Reverse Polish Notation (RPN) expression.

    params:
        expression (str): The RPN expression as a space-separated string.

    returns:
        float: The result of the evaluation.

    raises:
        ValueError: If the expression is invalid.
    """
    stack = []
    tokens = expression.strip().split()

    operators = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    for token in tokens:
        if token in operators:
            if len(stack) < 2:
                raise ValueError("Insufficient operands for operation")
            b = stack.pop()
            a = stack.pop()
            result = operators[token](a, b)
            stack.append(result)
        else:
            try:
                stack.append(float(token))
            except ValueError:
                raise ValueError(f"Invalid token: {token}")

    if len(stack) != 1:
        raise ValueError("Invalid RPN expression")

    return stack[0]
