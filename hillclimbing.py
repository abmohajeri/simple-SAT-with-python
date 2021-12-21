import re
from copy import deepcopy
from random import randrange


class Expression:
    def __init__(self, exp):
        self.expression = exp
        self.tokens = list(set(re.findall(r"[\w]+", exp)))  # Find all unique tokens
        self.clauses = exp.split('*')  # Find all unique clauses
        self.cur = 0

    def get_tokens(self):
        return self.tokens

    def get_clause_tokens(self, clause):
        return list(set(re.findall(r"[\w]+", clause)))

    def get_clauses(self):
        return self.clauses

    def generate_random_state(self):
        n = len(self.tokens)
        values = [int(x) for x in list('{0:0{width}b}'.format(randrange(n), width=n))]
        return dict(zip(self.tokens, values))

    def calculate_score(self, target):  # Calculate how many clause will be one
        cnt = 0
        clauses = self.get_clauses()
        for clause in clauses:
            mask = re.sub(r"([\w]+)", r"{\1}", clause)
            tokens = self.get_clause_tokens(clause)
            exp = {x: target[x] for x in tokens}  # Get each token target
            temp_mask = mask.format(**exp)
            temp_mask = temp_mask.replace('!', 'not ')
            temp_mask = temp_mask.replace('+', ' or ')
            temp_mask = temp_mask.replace('*', ' and ')
            if int(eval(temp_mask)):
                cnt += 1
        return cnt

    def get_next_target(self, target):  # Calculate how many clause will be one
        best_target = deepcopy(target)
        best_score = self.calculate_score(target)
        for x in target:
            target[x] = 1 - target[x]  # Toggle value
            temp = self.calculate_score(target)
            if temp > best_score:
                best_score = temp
                best_target = deepcopy(target)
            target[x] = 1 - target[x]
        return best_target, best_score

    def calculate(self, target, limit):  # Hill Climbing approach
        self.cur = self.cur + 1
        current_score = self.calculate_score(target)
        next_target, next_score = self.get_next_target(target)
        if next_score <= current_score:
            if self.cur < limit:
                return self.calculate(next_target, limit)
            else:
                return current_score
        else:
            return self.calculate(next_target, limit)


expressions = [
    "(x+y)*((!k)+(!p))",
    "(x+y+(!z))*(y+(!k)+(!p))*(p+(!k)+z)*(y+(!k)+z)",
    "(x)*(y)",
    "(x)*(!x)",
    "((!x)+y)*((!y)+z)*((!z)+x)*(x+y)*((!x)+(!y))"
]
for expression in expressions:
    print("Expression: {}".format(expression))
    expression = Expression(expression)
    start_target = expression.generate_random_state()
    clauses = expression.get_clauses()
    if expression.calculate(start_target, 500) == len(clauses):
        print("Satisfiable")
    else:
        print("Not Satisfiable")