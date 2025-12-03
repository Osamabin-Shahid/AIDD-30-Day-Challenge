import sys
import os

# Add the project root to the sys.path to enable imports from the 'src' directory
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.lib.calculator import evaluate_expression, CalculatorError

def main():
    if len(sys.argv) < 2:
        print("Usage: python calculator.py <expression>")
        sys.exit(1)

    expression = " ".join(sys.argv[1:])
    try:
        result = evaluate_expression(expression)
        print(f"Result: {result}")
    except CalculatorError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
