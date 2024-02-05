from random import randint


class CauchyFakeCodec:
    def __init__(self, n=4, k=2, r=4):
        self.n = n
        self.k = k
        self.p = 2  # захардкожено для экспериментов
        self.r = r

    def encode(self, message):
        assert len(message) == self.k * self.r, 'message has invalid shape'
        return [randint(0, 1) for _ in range(self.n * self.r)]

    def decode(self, message, erasures):
        assert len(message) == self.n * self.r, 'message has invalid shape'
        assert len(erasures) == self.n * self.r, 'erasures has invalid shape'

        erasures_count = 0
        for i in range(self.n):
            field_symbol = erasures[i*self.r:(i+1)*self.r]
            is_erasured = sum(field_symbol) > 0
            if is_erasured:
                erasures_count += 1
        if self.n - erasures_count < self.k:
            return False
        return True
