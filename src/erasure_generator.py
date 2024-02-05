from random import random
from functools import partial


class ErasureGenerator:
    def __init__(self, config):
        self._config = config
        self._simple_probability = self._config['simple_probability']
        self._factory = {
            'simple': self._simple_erasure,
            'group': self._group_erasure,
        }
        self._init_group_erasures()

    def erase(self, message, op_type='simple'):
        return partial(self._factory[op_type], message)()

    def get_group_probability(self):
        return self._g_prob * self._g2b / (self._b2g + self._g2b)

    def _simple_erasure(self, message):
        return [random() < self._simple_probability for _ in message]

    def _group_erasure(self, message):
        return [self._g_erase_for_symbol() for _ in message]

    def _init_group_erasures(self):
        self._state = 0
        self._b2g = self._config.get('bad_to_good', None)
        self._g2b = self._config.get('good_to_bad', None)
        self._transitions = [self._g2b, self._b2g]
        self._g_prob = self._config.get('group_probability', None)

    def _update_state(self):
        sample = random()
        if sample < self._transitions[self._state]:
            self._state = (self._state + 1) % 2

    def _g_erase_for_symbol(self):
        self._update_state()
        if self._state == 1 and random() < self._g_prob:
            return 1
        return 0
