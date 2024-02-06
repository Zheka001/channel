from random import randint
from time import perf_counter

from src.channel_codec import ChannelCodec
from src.erasure_generator import ErasureGenerator

if __name__ == '__main__':
    k = 5
    n = 10
    attempts = 10000
    with_identity = True
    config = {
        'operation': 'simple',
        'simple_probability': 0.1,
    }
    codec = ChannelCodec(k, n, with_identity)
    gen = ErasureGenerator(config)

    successful_count_bp = 0
    successful_count_hybrid = 0
    total_time_bp = 0
    total_time_hybrid = 0

    for _ in range(attempts):
        message = [randint(0, 1) for _ in range(k)]
        encoded = codec.encode(message)
        erasures = gen.erase(encoded, op_type=config['operation'])

        start_time = perf_counter()
        decoded_bp, warning = codec.decode_belief_prop(encoded, erasures)
        total_time_bp += perf_counter() - start_time
        successful_count_bp += 1 if decoded_bp == message else 0

        start_time = perf_counter()
        decoded_hybrid, warning = codec.decode_hybrid(encoded, erasures)
        total_time_hybrid += perf_counter() - start_time
        successful_count_hybrid += 1 if decoded_hybrid == message else 0

    print(f'belief prop: {total_time_bp} s, {total_time_bp / attempts} s, {successful_count_bp}, '
          f'{successful_count_bp / attempts * 100.0}%')
    print(f'hybrid: {total_time_hybrid} s, {total_time_hybrid / attempts} s, {successful_count_hybrid}, '
          f'{successful_count_hybrid / attempts * 100.0}%')


