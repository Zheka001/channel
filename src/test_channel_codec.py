from src.channel_codec import ChannelCodec
from random import randint

if __name__ == '__main__':
    cc = ChannelCodec(5, 10)

    for i in range(1000):
        mes = [randint(0, 1) for _ in range(5)]
        encoded = cc.encode(mes)
        erasures = [randint(0, 1) if i < 6 else 0 for i in range(5)]
        decoded, message = cc.decode(encoded, erasures)

        if mes != decoded:
            print(f'{i+1} mistake: {mes}, {decoded}, {message}')

        if i % 10 == 0:
            print(f'Processed {i} iterations')

    print('the end')
