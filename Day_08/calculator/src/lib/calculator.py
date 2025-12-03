import operator

class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass

class InvalidExpressionError(CalculatorError):
    """Raised when an expression is syntactically invalid."""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when division by zero occurs."""
    pass

def _tokenize(expression: str) -> list[str]:
    """
    Tokenizes an arithmetic expression into numbers and operators.
    """
    tokens = []
    current_number = ""
    
    i = 0
    while i < len(expression):
        char = expression[i]
        
        if char.isdigit() or char == '.':
            current_number += char
        elif char in ['+', '-', '*', '/']:
            if current_number:
                tokens.append(current_number)
                current_number = ""
            
            # Handle unary minus (e.g., "-5", "2*-5")
            if char == '-' and (not tokens or tokens[-1] in ['+', '-', '*', '/']):
                # Look ahead for a number
                j = i + 1
                temp_number = ""
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    temp_number += expression[j]
                    j += 1
                if temp_number:
                    tokens.append(char + temp_number) # Append as a negative number token
                    i = j - 1 # Adjust index to skip processed number
                else:
                    tokens.append(char) # It's a binary minus
            else:
                tokens.append(char)
        elif char.isspace():
            if current_number:
                tokens.append(current_number)
                current_number = ""
        else: # Unsupported character
            if current_number:
                tokens.append(current_number)
            raise InvalidExpressionError(f"Unsupported character: '{char}'")
        i += 1

    if current_number:
        tokens.append(current_number)
            
    # Post-tokenization validation for operator sequences and leading/trailing operators
    if not tokens:
        raise InvalidExpressionError("Empty expression.")

    # Simplified check for leading/trailing operators, consider unary minus
    if tokens[0] in ['+', '*', '/'] or (tokens[0] == '-' and len(tokens) > 1 and tokens[1] in ['+', '*', '/']):
        raise InvalidExpressionError("Expression cannot start with invalid operator.")
    if tokens[-1] in ['+', '-', '*', '/'] and not tokens[-1].startswith('-'): # Allow negative numbers at end
        raise InvalidExpressionError("Expression cannot end with an operator.")
            
    for k in range(len(tokens) - 1):
        # Check for consecutive operators. Allow unary minus if it forms a negative number.
        if tokens[k] in ['+', '-', '*', '/'] and tokens[k+1] in ['+', '*', '/']:
            raise InvalidExpressionError("Consecutive operators are not allowed.")
        # Ensure that if a token is a number, the next is an operator (unless end of expr)
        if tokens[k].replace('.', '', 1).isdigit() and tokens[k+1].replace('.', '', 1).isdigit():
             raise InvalidExpressionError("Numbers must be separated by an operator.")

    return tokens


def _evaluate_rpn(tokens: list[str]) -> float:
    """Evaluates a list of tokens in Reverse Polish Notation (RPN)."""
    op_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    
    stack = []
    for token in tokens:
        try:
            # Handle potentially negative numbers that are tokenized as '-N'
            stack.append(float(token))
        except ValueError:
            # If it's not a number, it must be an operator
            if token in op_map:
                if len(stack) < 2:
                    raise InvalidExpressionError("Insufficient operands for operator.")
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '/' and operand2 == 0:
                    raise DivisionByZeroError("Cannot divide by zero.")
                stack.append(op_map[token](operand1, operand2))
            else:
                raise InvalidExpressionError(f"Unexpected token in RPN evaluation: '{token}'")

    if len(stack) != 1:
        raise InvalidExpressionError("Invalid expression format.")
    return stack[0]

def _infix_to_rpn(tokens: list[str]) -> list[str]:
    """Converts an infix expression token list to Reverse Polish Notation (RPN)."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    op_stack = []
    rpn_output = []

    for token in tokens:
        try:
            # Numbers (including negative numbers)
            float(token) 
            rpn_output.append(token)
        except ValueError:
            # Operators
            if token in precedence:
                while op_stack and op_stack[-1] in precedence and precedence[op_stack[-1]] >= precedence[token]:
                    rpn_output.append(op_stack.pop())
                op_stack.append(token)
            else: 
                # This should ideally not be reached if _tokenize is robust
                raise InvalidExpressionError(f"Unexpected token during RPN conversion: '{token}'")
    
    while op_stack:
        rpn_output.append(op_stack.pop())
        
    return rpn_output

def evaluate_expression(expression: str) -> float:
    """
    Evaluates a basic arithmetic expression.

    Args:
        expression: The arithmetic expression as a string.

    Returns:
        The numerical result of the expression.

    Raises:
        InvalidExpressionError: If the expression is invalid or contains unsupported operations.
        DivisionByZeroError: If the expression involves division by zero.
    """
    # Remove spaces before tokenization for cleaner handling
    expression = expression.replace(" ", "")
    tokens = _tokenize(expression)
    
    rpn_tokens = _infix_to_rpn(tokens)
    result = _evaluate_rpn(rpn_tokens)
    return result