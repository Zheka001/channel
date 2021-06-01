import json
import random
from random import randint
from time import monotonic as now

from src.channel_codec import ChannelCodec
from src.erasure_generator import ErasureGenerator


# todo: переписать через класс
def experiment_iteration(config, verbose=False):
    codec = ChannelCodec(config['k'], config['n'])
    gen = ErasureGenerator(config['erasure_generator'])

    successful_count = 0
    total_experiments = 1000
    for i in range(total_experiments):
        message = [randint(0, 1) for _ in range(5)]
        encoded = codec.encode(message)
        erasures = gen.erase(encoded, op_type=config['erasure_generator']['operation'])
        decode, _ = codec.decode(encoded, erasures)

        successful_count += 1 if decode == message else 0

    if verbose:
        print(f'Success: {successful_count} of {total_experiments}')
        print(f'group_probability: {gen.get_group_probability()}')
    return successful_count / total_experiments, gen.get_group_probability()


def run_experiment(config):
    res_group, g_p = experiment_iteration(config)
    config['erasure_generator']['operation'] = 'simple'
    config['erasure_generator']['simple_probability'] = g_p
    res_simple, _ = experiment_iteration(config)
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
                'group_probability': round(random.uniform(0.001, 0.7), 3),
                'bad_to_good': round(random.uniform(0.001, 0.45), 3),
                'good_to_bad': round(random.uniform(0.001, 0.45), 3),
            }
        }
        configs.append(cfg)
    return configs


def write_results(results, filename):
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4)


def run_random_experiment():
    start = now()
    length = 500
    result_filename = 'data/random_results_500.json'
    configs = generate_random_configs(10, 5, length)

    results = list()
    start_time = now()

    # todo: для ускорения можно заменить на ThreadPoolExecutor
    for i, cfg in enumerate(configs):
        results.append(run_experiment(cfg))

        if i % 10 == 0 and i != 0:
            time_per_exp = round((now() - start_time) / 10, 2)
            estimated = (length - i - 1) * time_per_exp
            print(f'Process {i} experiments. Time per experiment: {time_per_exp} s, '
                  f'remained: {estimated / 3600:02f}:{estimated % 3600 / 60:02f}:{estimated % 60:02f}')
            write_results(results, result_filename)

    print(f'Full experiment took {round(now() - start, 2)} sec')

    write_results(results, result_filename)

    print('random experiment is done')


if __name__ == '__main__':
    run_random_experiment()
