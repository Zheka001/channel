# import cv2
# import mediapipe as mp

# from time import monotonic as now
import numpy as np
from random import randint
from math import floor, factorial, comb
from itertools import product
from tqdm import tqdm

# todo: скопировать в нужный проект по каналу
class TestCombinations:
    def __init__(self, q, n, d, e):
        self.q = q
        self.n = n
        self.d = d
        self.e = e
        self.errors_decoding = floor((d - 1) / 2)
        print(f'code: F_{q}, length - {n}, minimal code distance - {d}, erasures - {e}, '
              f'errors_decoding - {self.errors_decoding}')

        self.original_codeword = None
        self.erased_codeword = None
        self.erased_positions = None

    def run(self):
        self.original_codeword = [randint(0, self.q - 1) for _ in range(self.n)]

        self.erased_codeword, self.erased_positions = self.erase(self.original_codeword)

        print(self.original_codeword, self.erased_codeword, self.erased_positions)
        self.test_formula()
        # self.test_permutations()

    def erase(self, codeword):
        erased_codeword = codeword.copy()
        positions = set()
        while len(positions) < self.e:
            cur_pos = randint(0, self.n - 1)
            positions.add(cur_pos)

        for pos in positions:
            erased_codeword[pos] = '*'
        return erased_codeword, positions

    def test_permutations(self):
        comb_list = product(range(self.q), repeat=self.e)
        comb_list = list(comb_list)
        total = 0
        good_counter = 0
        for comb in tqdm(comb_list):
            current = self.erased_codeword.copy()
            for elem, pos in zip(comb, self.erased_positions):
                current[pos] = elem

            differences = 0
            for i in range(self.n):
                if current[i] != self.original_codeword[i]:
                    differences += 1

            good_counter += 1 if differences <= self.errors_decoding else 0
            total += 1

        print(f'total: {total}')
        print(f'good: {good_counter}')
        print(f'ratio: {good_counter / total}')

    def test_formula(self):
        good = 0
        for i in range(self.errors_decoding, self.e + 1):
            good += pow(self.q - 1, self.e - i) * comb(self.e, i)

        total = pow(self.q, self.e)
        print(f'formula value = {good / total}')
        print(f'total = {total}, good = {good}')

        print('full probabilities: ')
        mult_result = 1
        i = 0
        while total > good:
            cur_prob = good / total
            mult_result *= (1 - cur_prob)
            result = 1 - mult_result
            total = total - 1
            i += 1
            print(i, round(result, 3))

            if result > 0.97:
                break


if __name__ == '__main__':
    TestCombinations(q=9, n=31, d=10, e=9).run()