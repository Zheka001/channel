from random import randint
from time import monotonic as now

from src.channel_codec import ChannelCodec


if __name__ == '__main__':
    cc = ChannelCodec(5, 10)
    erasure_count = 10
    messages = list()
    erasures = list()
    for i in range(100000):
        messages.append([randint(0, 1) for _ in range(5)])
        erasures.append([randint(0, 1) for _ in range(10)])

    start_time = now()
    mistakes = 0
    for mes, er in zip(messages, erasures):
        encoded = cc.encode(mes)
        decoded, message = cc.decode(encoded, er)
        if mes != decoded:
            mistakes += 1
    total_time = now() - start_time
    print(f'Common: {total_time}, mistakes: {mistakes}')

    start_time = now()
    mistakes = 0
    for mes, er in zip(messages, erasures):
        encoded = cc.encode(mes)
        decoded, message = cc.decode_hybrid(encoded, er)
        if mes != decoded:
            mistakes += 1
    total_time = now() - start_time
    print(f'Hybrid: {total_time}, mistakes: {mistakes}')
