import json
import random
from random import randint
from time import monotonic as now

from src.channel_codec import ChannelCodec
from src.erasure_generator import ErasureGenerator


# todo: переписать через класс
def experiment_iteration(config):
    codec = ChannelCodec(config['k'], config['n'])
    gen = ErasureGenerator(config['erasure_generator'])

    successful_count = 0
    for i in range(1000):
        message = [randint(0, 1) for _ in range(5)]
        encoded = codec.encode(message)
        erasures = gen.erase(encoded, op_type=config['erasure_generator']['operation'])
        decode, _ = codec.decode(encoded, erasures)

        successful_count += 1 if decode == message else 0
        if i % 100 == 0:
            print(f'Processed {i} iterations ...')

    print(f'Success: {successful_count} of {1000}')
    print(f'group_probability: {gen.get_group_probability()}')
    return successful_count / 1000, gen.get_group_probability()


def run_experiment(config):
    res_group, g_p = experiment_iteration(config)
    config['erasure_generator']['operation'] = 'simple'
    config['erasure_generator']['simple_probability'] = g_p
    res_simple, _ = experiment_iteration(config)
    print(f'group - {res_group}, simple - {res_simple}')
    return {'group': res_group, 'simple': res_simple, 'probability': g_p,
            'b2g': config['erasure_generator']['bad_to_good'], 'g2b': config['erasure_generator']['good_to_bad']}


def generate_random_configs(n, k, length=1000):
    configs = list()
    for i in range(length):
        cfg = {
            'n': n,
            'k': k,
            'erasure_generator': {
                'operation': 'group',
                'simple_probability': 0,
                'group_probability': round(random.uniform(0.001, 0.6), 3),
                'bad_to_good': round(random.uniform(0.001, 0.3), 3),
                'good_to_bad': round(random.uniform(0.001, 0.3), 3),
            }
        }
        configs.append(cfg)
    return configs


def run_random_experiment():
    start_time = now()
    configs = generate_random_configs(10, 5, length=500)
    results = [run_experiment(cfg) for cfg in configs]

    print(f'experiment took {round(now() - start_time, 2)} sec')

    with open('random_results_500.json', 'w') as file:
        json.dump(results, file, indent=4)

    print('random experiment is done')


if __name__ == '__main__':
    run_random_experiment()
