import sys
import re
from tqdm import tqdm

class Item:
    def __init__(
            self,
            initial_worry_level,
            ):
        self._worry = initial_worry_level
        self._mod = 1

    def __repr__(self):
        return f'Item(worry={self.worry})'

    @property
    def worry(self):
        return self._worry

    def set_worry(self, x):
        self._worry = x

    def set_mod(self, m):
        self._mod = m

    def relieve(self):
        self._worry = self._worry % self._mod

class Monkey:
    def __init__(
            self,
            mid,
            operator,
            operand,
            test,
            cond_true,
            cond_false
            ):
        self.mid = mid
        self.items = []

        self.operator = operator
        self.operand = operand if operand == 'old' else int(operand)

        if self.operator == '+':
            self._fn_lambda = lambda x,y: x + y
        elif self.operator == '*':
            self._fn_lambda = lambda x,y: x * y
        else:
            raise ValueError(f'Invalid operator {self.operator}')

        self.test = test
        self.cond_true = cond_true
        self.cond_false = cond_false

        self.monkey_business = 0

        self.debug = False

    def __repr__(self):
        return f"Monkey {self.mid} ({self.operator}{self.operand}, {self.test}/{self.cond_true}/{self.cond_false})"

    def _inspection_fn(self, x):
        y = x if self.operand == 'old' else self.operand
        return self._fn_lambda(x,y)

    def _test_fn(self, x):
        return self.cond_true if x % self.test == 0 else self.cond_false

    @property
    def has_items(self):
        return (len(self.items) > 0)

    def give_item(self, item: Item):
        self.items.append(item)

    def get_next_item(self):
        return self.items.pop(0)

    def inspect(self, item: Item):

        self.monkey_business += 1

        if self.debug:
            print(f'{self} inspects {item}')

        item.set_worry(self._inspection_fn(item.worry))
        if self.debug:
            print(f'{self} upated worry level of {item}')

        item.relieve()
        if self.debug:
            print(f'{item} relieved')

        monkeyTo = self._test_fn(item.worry)
        if self.debug:
            print(f'{self} threw {item} to Monkey {monkeyTo}')
            print('=====')

        return monkeyTo

    @classmethod
    def factory(cls, reMatch):
        mid = int(reMatch[0])
        items = [int(i) for i in reMatch[1].split(', ')]
        operator = reMatch[2]
        operand = reMatch[3]
        test = int(reMatch[4])
        cond_true = int(reMatch[5])
        cond_false = int(reMatch[6])
        m = Monkey(
                mid,
                operator,
                operand,
                test,
                cond_true,
                cond_false
                )
        for i in items:
            m.give_item(Item(int(i)))
        return m

DEBUG = False
N_ROUNDS = 10000

# Create Monkeys
monkeyDict = {}
monkeyRegex = r"Monkey (\d+):\n  Starting items: (.*)\n  Operation: new = old ([+|*]) (.*)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)"

with open(sys.argv[1],'r') as f:
    monkeyMatches = re.findall(monkeyRegex, f.read())

mod_counter = 1
for mM in monkeyMatches:
    monkey = Monkey.factory(mM)
    monkey.debug = DEBUG
    mod_counter *= monkey.test
    monkeyDict[monkey.mid] = monkey
n_monkeys = max(monkeyDict.keys())

for monkey in monkeyDict.values():
    for item in monkey.items:
        item.set_mod(mod_counter)

# Main Loop
for nrnd in range(N_ROUNDS):
    for mid in range(n_monkeys+1):
        monkey = monkeyDict[mid]

        while monkey.has_items:
            it = monkey.get_next_item()
            throw_to = monkey.inspect(it)
            monkeyDict[throw_to].give_item(it)

    if DEBUG:
        print(f'After Round {nrnd+1}')
        for monkey in monkeyDict.values():
            print(monkey, monkey.items)
        print('')

sortedMonkeys = sorted(monkeyDict.values(), key = lambda x: x.monkey_business)
topTwo = sortedMonkeys[-2:]
monkeyBusiness = topTwo[0].monkey_business * topTwo[1].monkey_business
print(monkeyBusiness)
