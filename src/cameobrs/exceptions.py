from __future__ import absolute_import, print_function


class IncompatibleTargets(Exception):
    def __init__(self, target1, target2):
        super(IncompatibleTargets, self).__init__(
            "Incompatible targets %s and %s" % (target1, target2)
        )
        self.target1 = target1
        self.target2 = target2
