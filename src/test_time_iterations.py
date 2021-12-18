import json
import random
from random import randint
from time import monotonic as now

from src.channel_codec import ChannelCodec


if __name__ == '__main__':
    cc = ChannelCodec(5, 10)
    erasure_count = 10

    # заменить на функцию генерации
    messages = list()
    erasures = list()
    for i in range(1000000):
        messages.append([randint(0, 1) for _ in range(5)])
        cur_erasures = [randint(0, 1) if i < 5 else 0 for i in range(10)]
        random.shuffle(cur_erasures)
        erasures.append(cur_erasures)

    global_start_time = now()
    times = list()
    mistakes = 0
    for mes, er in zip(messages, erasures):
        encoded = cc.encode(mes)
        start_time = now()
        decoded, message = cc.decode_hybrid(encoded, er)
        times.append(now() - start_time)
        if mes != decoded:
            mistakes += 1
    total_time = now() - global_start_time
    print(f'Hybrid: {total_time}, mistakes: {mistakes}')

    print(f'Begining: {times[:10]}')
    print(f'End: {times[-10:]}')
    print(f'Average: {sum(times) / len(times)}')

    with open('data/times.json', 'w') as file:
        json.dump(times, file)
