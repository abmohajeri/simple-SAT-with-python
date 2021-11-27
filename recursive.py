import re


class Expression:
    def __init__(self, exp):
        self.expression = exp
        self.tokens = list(set(re.findall(r"[\w]+", exp)))  # Find all unique tokens

    def get_tokens(self):
        return self.tokens

    flat_permutation = []
    def get_permutation(self, n, list):
        if n == 0:
            self.flat_permutation.append(list)
            return list
        self.get_permutation(n - 1, list + ['0'])
        self.get_permutation(n - 1, list + ['1'])

    def calculate(self):
        mask = re.sub(r"([\w]+)", r"{\1}", self.expression)
        tokens = self.get_tokens()
        self.flat_permutation = []
        self.get_permutation(len(tokens), [])
        for permutation in self.flat_permutation:
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