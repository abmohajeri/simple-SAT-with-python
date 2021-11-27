import re


class Expression:
    def __init__(self, exp):
        self.expression = exp
        self.tokens = list(set(re.findall(r"[\w]+", exp)))  # Find all unique tokens

    def get_tokens(self):
        return self.tokens

    def get_permutation(self, n):
        return ['{0:0{width}b}'.format(v, width=n) for v in range(2**n)]  # All permutation of 0 & 1

    def calculate(self):
        mask = re.sub(r"([\w]+)", r"{\1}", self.expression)
        tokens = self.get_tokens()
        permutations = self.get_permutation(len(tokens))
        for permutation in permutations:
            exp = dict(zip(tokens, list(permutation)))
            temp_mask = mask.format(**exp)
            temp_mask = temp_mask.replace('!', 'not ')
            temp_mask = temp_mask.replace('+', ' or ')
            temp_mask = temp_mask.replace('*', ' and ')
            if int(eval(temp_mask)):
                return True
        return False


expressions = [
    "(!x)+y+z",
    "(x+y)*((!x)+(!y))",
    "x*(!x)"
]
for expression in expressions:
    print("Expression: {}".format(expression))
    expression = Expression(expression)
    if expression.calculate():
        print("Satisfiable")
    else:
        print("Not Satisfiable")