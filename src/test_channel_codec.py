from src.channel_codec import ChannelCodec
from random import randint

if __name__ == '__main__':
    cc = ChannelCodec(5, 10)
    erasure_count = 10
    for i in range(100000):
        mes = [randint(0, 1) for _ in range(5)]
        encoded = cc.encode(mes)
        erasures = [randint(0, 1) for _ in range(10)]
        decoded, message = cc.decode_hybrid(encoded, erasures)

        if mes != decoded:
            erasure_count = min(erasure_count, len([i for i in erasures if i == 1]))
            print(f'{i+1} mistake: {mes}, {decoded}, {message}, {len([i for i in erasures if i == 1])}')

        if i % 10 == 0:
            print(f'Processed {i} iterations')

    print('min erasures with mistake:', erasure_count)
