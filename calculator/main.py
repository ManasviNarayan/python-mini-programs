import argparse
from calculator import Calculator

parser = argparse.ArgumentParser(description='A simple mathematical expression Calculator')
parser.add_argument('expression', help='Mathematical expression to be evaluated inside double quotes')

try:
    # Note input expression in double quotes
    # main.py "2+3-2"
    args = parser.parse_args()
    calculator = Calculator(args.expression)
    print(f'{args.expression} = {calculator.parse_expression()}')
except Exception as e:
    print(f'Error: {str(e)}')


