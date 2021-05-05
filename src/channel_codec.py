import numpy as np
from random import shuffle, sample
from sympy import Matrix


class ChannelCodec:
    def __init__(self, k, n):
        self.k = k
        self.n = n
        self._prepare_matrix()

    def encode(self, message):
        return np.dot(message, self.matrix) % 2

    def decode(self, message, erasures):
        # print('mes:', message)
        # print('erasures:', erasures)
        not_erasure_indexes = [i for i, (m, e) in enumerate(zip(message, erasures)) if not e]
        # print('indexes:', not_erasure_indexes)
        if len(not_erasure_indexes) < self.k:
            return list(), 'too much erasures'

        for _ in range(100):
            elements = sample(not_erasure_indexes, k=self.k)
            # print('elements:', elements)
            squared_matrix = self.matrix[:, elements]
            # print('matrix:', self.matrix)
            # print('squared:', squared_matrix)
            squared_matrix = Matrix(squared_matrix)
            det = squared_matrix.det()
            if det != 0:
                inv_m = squared_matrix.inv_mod(2)
                # print('inv_m', inv_m)
                inv_m = np.asarray(inv_m).astype(int)
                # print('inv:', inv_m)
                # print('mul:', np.matmul(squared_matrix, inv_m))
                # print('to_encode:', np.array(message)[elements].tolist())
                result = np.dot(np.array(message)[elements], inv_m).astype(np.uint8)
                # print('result:', result)
                result = result % 2
                return result.tolist(), 'ok'

        return list(), 'too much attempts'

    def _prepare_matrix(self):
        number_ones = self._calc_middle(self.k)
        columns = set()
        for i in range(self.n):
            # todo: добавить проверку, что это закончится
            while True:
                current = tuple(self._create_vector(number_ones, self.k))
                if current not in columns:
                    columns.add(current)
                    break

        self.matrix = np.array(list(columns), dtype=np.uint8).transpose()
        if np.linalg.matrix_rank(self.matrix) != self.k:
            self._prepare_matrix()

    @staticmethod
    def _create_vector(number_ones, length):
        column = [int(i < number_ones) for i in range(length)]
        shuffle(column)
        return column

    @staticmethod
    def _calc_middle(k):
        middle = k // 2
        middle = middle + 1 if middle % 2 == 0 else middle
        return middle
