import numpy as np


class agent():
    def __init__(self, x):
        self.X = x
        self.Y = None

    def mutate(self, strange, chast):
        if np.random.rand() <= chast:
            if np.random.rand() > 0.5:
                self.X -= strange
            else:
                self.X -= strange

    def calculate(self, fun):
        self.Y = fun(self.X)

    def print(self):
        print(self.X, self.Y)

    def rX(self):
        return self.X

    def rY(self):
        return self.Y