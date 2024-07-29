from typing import List
from collections import namedtuple 

class Solution:
    Element = namedtuple("Element", "parent size factor")
    def __init__(self):
        self._elms = {} # name -> Element

    def init_elm(self, equation):
        for e in equation:
            if e not in self._elms:
                # point to self, size of connected elements, factor = e.value / parent.value
                elm = Solution.Element(parent=e, size=1, factor=1.0)
                self._elms[e] = elm

    def update_root(self, e1, e2, value):
        r1 = self.root(e1)
        r2 = self.root(e2)

        if r1 is not r2:
            if self._elms[r1].size > self._elms[r2].size:
                r1, r2 = r2, r1
                e1, e2 = e2, e1
                value = 1/value

            factor1 = self.factor_root(e1)
            factor2 = self.factor_root(e2)
            new_factor = factor2 / factor1 * value
            
            self._elms[r1] = self._elms[r1]._replace(parent = r2,
                    factor = new_factor)

            self._elms[r2] = self._elms[r2]._replace( size = self._elms[r1].size + self._elms[r2].size)

    def factor_root(self, e):
        factor = 1.0
        while self._elms[e].parent != e:
            factor *= self._elms[e].factor
            e = self._elms[e].parent
        return factor

    def root(self, e):
        if e not in self._elms:
            return None
        while self._elms[e].parent != e:
            e = self._elms[e].parent
        return e

    def union(self, equations, values):
        self._elms = {} # name -> Element
        for i, equation in enumerate(equations):
            self.init_elm(equation)
            self.update_root(equation[0], equation[1], values[i])


    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        self.union(equations, values)
        print(self._elms)

        ret = [-1.0] * len(queries)
        for i, q in enumerate(queries):
            if self.root(q[0]) and (self.root(q[0]) is self.root(q[1])):
                f0 = self.factor_root(q[0])
                f1 = self.factor_root(q[1])

                ret[i] = f0 / f1

        return ret





if __name__ == "__main__":
    sol = Solution()
    equations = [["a","b"],["b","c"]]
    values = [2.0,3.0]
    queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
    print(sol.calcEquation(equations, values, queries))

    equations = [["a","b"],["b","c"],["bc","cd"]]
    values = [1.5,2.5,5.0]
    queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
    print(sol.calcEquation(equations, values, queries))
    equations = [["a","b"]]
    values = [0.5]
    queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
    print(sol.calcEquation(equations, values, queries))

    equations = [["a","b"],["b","c"],["bc","cd"]]
    values = [1.5,2.5,5.0]
    queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
    print(sol.calcEquation(equations, values, queries))
# sol.generateParenthesis(8)
