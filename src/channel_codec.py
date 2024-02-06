import numpy as np
from random import shuffle, sample
from itertools import combinations
from math import comb
from sympy import Matrix


class ChannelCodec:
    def __init__(self, k, n, with_identity=False):
        self.k = k
        self.n = n
        self._prepare_matrix(with_identity)

        self._helper = dict()

    def encode(self, message):
        return np.dot(message, self.matrix) % 2

    def decode(self, message, erasures):
        not_erasure_indexes = [i for i, (m, e) in enumerate(zip(message, erasures)) if not e]
        if len(not_erasure_indexes) < self.k:
            return list(), 'too much erasures'

        for elements in combinations(not_erasure_indexes, self.k):
            squared_matrix = self.matrix[:, elements]
            squared_matrix = Matrix(squared_matrix)
            det = squared_matrix.det()
            if det != 0:
                try:
                    inv_m = squared_matrix.inv_mod(2)
                except ValueError:
                    continue
                inv_m = np.asarray(inv_m).astype(int)
                result = np.dot(np.array(message)[list(elements)], inv_m).astype(np.uint8)
                result = result % 2
                return result.tolist(), 'ok'

        return list(), 'is not invertible'

    def decode_hybrid(self, message, erasures):
        not_erasure_indexes = [i for i, (m, e) in enumerate(zip(message, erasures)) if not e]
        if len(not_erasure_indexes) < self.k:
            return list(), 'too much erasures'

        for elements in combinations(not_erasure_indexes, self.k):
            fast_decoding = self._helper.get(elements, None)
            if fast_decoding:
                if fast_decoding == 'uninvertible':
                    continue
                else:
                    result = np.dot(np.array(message)[list(elements)], np.array(fast_decoding)).astype(np.uint8)
                    result = result % 2
                    return result.tolist(), 'fast'

            squared_matrix = self.matrix[:, elements]
            squared_matrix = Matrix(squared_matrix)
            det = squared_matrix.det()
            if det != 0:
                try:
                    inv_m = squared_matrix.inv_mod(2)
                except ValueError:
                    self._helper[elements] = 'uninvertible'
                    continue
                inv_m = np.asarray(inv_m).astype(int)
                self._helper[elements] = inv_m.tolist()
                result = np.dot(np.array(message)[list(elements)], inv_m).astype(np.uint8)
                result = result % 2
                return result.tolist(), 'ok'
            else:
                self._helper[elements] = 'uninvertible'

        return list(), 'is not invertible'

    def decode_belief_prop(self, message, erasures):
        erasure_indexes = [i for i, (m, e) in enumerate(zip(message, erasures)) if e]
        if len(erasure_indexes) > self.n - self.k:
            return list(), 'too much erasures'

        matrix = self.matrix.copy()
        # обнуляем стертые позиции
        matrix[:, erasure_indexes] = np.zeros(shape=(self.k, len(erasure_indexes)))
        message_inside = message.copy()
        result = np.zeros(self.k)
        counter = 0
        while matrix.sum() != 0:
            index_deg1 = np.where(matrix.sum(axis=0) == 1)
            if len(index_deg1[0]) == 0:
                return list(), 'no vector with deg 1'
            col_index = index_deg1[0][0]
            value = message_inside[col_index]
            cur_column = matrix[:, col_index]
            row_index = np.where(cur_column == 1)[0]
            result[row_index] = value
            xx = np.where(matrix[row_index, :] == 1)
            for x in xx:
                message_inside[x] += value
                message_inside[x] %= 2
                matrix[row_index, x] = 0
            counter += 1

        return result.tolist(), 'ok'







    def _prepare_matrix(self, with_identity):
        columns = self._prepare_common_columns(self.n) if not with_identity else self._prepare_identity_columns()
        self.matrix = np.array(list(columns), dtype=np.uint8).transpose()

        # перезапускаем процедуру генерации матрицы, если она получилась неполного ранга
        if np.linalg.matrix_rank(self.matrix) != self.k:
            self._prepare_matrix(with_identity)

    def _prepare_common_columns(self, count):
        number_ones = self._calc_middle(self.k)
        columns = set()
        for i in range(count):
            # todo: добавить проверку, что это закончится
            while True:
                current = tuple(self._create_vector(number_ones, self.k))
                if current not in columns:
                    columns.add(current)
                    break

        return columns

    def _prepare_identity_columns(self):
        columns = [tuple([0 if j != i else 1 for j in range(self.k)]) for i in range(self.k)]
        columns.extend(self._prepare_common_columns(count=self.n - self.k))
        return columns

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
