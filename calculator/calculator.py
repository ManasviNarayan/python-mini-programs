import re
class Calculator():

    def __init__(self, expression):
        expression = self.format_expression(expression)
        self.tokens = self.tokenize(expression)

    def format_expression(self,expression):
        # remove whitespace
        expression = re.sub(r'\s', "", expression)
        # explicit multiplication between paranthesis
        # ()() --> ()*()
        expression = re.sub(r'\)\(',r')*(', expression)
        # explicit multiplication between number and brackets
        # 2(3) --> 2*(3)
        expression = re.sub(r'(\d)\(', r'\1*(', expression)
        #(3)2 --> (3)*2
        expression = re.sub(r'\)(\d)', r')*\1', expression)
        # check for invalid characters
        if re.search(r'[^\d+*/()-]', expression):
            raise Exception('Invalid expression. Valid symbols: +-/*()')
        return expression

    def tokenize(self,expression):
        # split into tokens
        pattern = re.compile(r"\d+|[-+*/()]")
        lst = re.findall(pattern, expression)
        return lst
    
    # expression -> term + expression | term - expression | term
    # term -> factor * term | factor / term | factor
    # factor -> ( expression ) | number
    def parse_expression(self):
        left = self.parse_term()
        while self.tokens and self.tokens[0] in '+-':
            operator = self.tokens.pop(0)
            right = self.parse_term()
            if operator == "+":
                left += right
            else:
                left -= right
        return left
    
    def parse_term(self):
        left = self.parse_factor()
        while self.tokens and self.tokens[0] in '*/':
            operator = self.tokens.pop(0)
            right = self.parse_factor()
            if operator == '*':
                left *= right
            elif operator == '/':
                left /= right
        return left
    
    def parse_factor(self):
        token = self.tokens.pop(0)
        if token == '(':
            result = self.parse_expression()
            self.tokens.pop(0) # remove ) after expression has been evaluated
            return result
        else:
            return float(token)
