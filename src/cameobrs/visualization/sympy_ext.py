from sympy import And, Or


def _str_or(self):
    return "(" + " OR ".join([str(v) for v in self.args]) + ")"


Or.__str__ = _str_or


def _str_and(self):
    return "(" + " AND ".join([str(v) for v in self.args]) + ")"


And.__str__ = _str_and
