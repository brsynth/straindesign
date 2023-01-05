from __future__ import absolute_import, print_function

from copy import copy


class MultipleChromosomeGenome(object):
    def __init__(self, keys=[], *args, **kwargs):
        super(MultipleChromosomeGenome, self).__init__(*args, **kwargs)
        self.chromosomes = {k: [] for k in keys}
        self.keys = keys

    def __getitem__(self, key):
        return self.chromosomes[key]

    def __delitem__(self, key):
        del self.chromosomes[key]

    def __setitem__(self, key, value):
        self.chromosomes[key] = sorted(value)

    def copy(self):
        new_genome = MultipleChromosomeGenome(self.keys)
        for key in self.keys:
            new_genome[key] = copy(self[key])
        return new_genome

    def __repr__(self):
        return "| ".join(["%s: %s" % (k, list(v)) for k, v in self.chromosomes.items()])
