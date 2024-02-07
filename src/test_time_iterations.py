import json
import random
from random import randint
from time import monotonic as now

import numpy as np

from src.channel_codec import ChannelCodec


if __name__ == '__main__':
    cc = ChannelCodec(5, 10)
    messages_count = 10000

    # заменить на функцию генерации
    messages = list()
    erasures = list()
    for i in range(messages_count):
        messages.append([randint(0, 1) for _ in range(5)])
        cur_erasures = [randint(0, 1) if i < 5 else 0 for i in range(10)]
        random.shuffle(cur_erasures)
        erasures.append(cur_erasures)

    global_start_time = now()
    times_hybrid = list()
    mistakes = 0
    for mes, er in zip(messages, erasures):
        encoded = cc.encode(mes)
        start_time = now()
        decoded, message = cc.decode_hybrid(encoded, er)
        times_hybrid.append(now() - start_time)
        if mes != decoded:
            mistakes += 1
    total_time = now() - global_start_time
    print(f'Hybrid: {total_time}, mistakes: {mistakes}, per second: {messages_count / sum(times_hybrid)}')

    global_start_time = now()
    times = list()
    mistakes = 0
    for mes, er in zip(messages, erasures):
        encoded = cc.encode(mes)
        start_time = now()
        decoded, message = cc.decode(encoded, er)
        times.append(now() - start_time)
        if mes != decoded:
            mistakes += 1
    total_time = now() - global_start_time
    print(f'Common: {total_time}, mistakes: {mistakes}, per second: {messages_count / sum(times)}')

    # print(f'Begining: {times[:10]}')
    # print(f'End: {times[-10:]}')
    # print(f'Average: {sum(times) / len(times)}')

    data = {
        'hybrid_times': times_hybrid,
        'common_times': times,
    }
    ratio = sum(times) / sum(times_hybrid)
    print(f'ratio: {ratio}')

    with open('data/times.json', 'w') as file:
        json.dump(data, file)
