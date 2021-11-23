import json
import random
import concurrent.futures
from random import randint
from time import monotonic as now

from src.channel_codec import ChannelCodec
from src.erasure_generator import ErasureGenerator


# todo: переписать через класс
def experiment_iteration(config, verbose=False):
    codec = ChannelCodec(config['k'], config['n'], config['with_identity'])
    gen = ErasureGenerator(config['erasure_generator'])

    successful_count = 0
    total_experiments = 1000
    for i in range(total_experiments):
        message = [randint(0, 1) for _ in range(config['k'])]
        encoded = codec.encode(message)
        erasures = gen.erase(encoded, op_type=config['erasure_generator']['operation'])
        decode, _ = codec.decode_hybrid(encoded, erasures)

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
            'with_identity': False,
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


def run_random_experiment(n, k):
    start = now()
    length = 500
    result_filename = f'data/random_results_{n}_{k}.json'
    configs = generate_random_configs(n, k, length)

    results = list()
    start_time = now()

    # with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     futures = list()
    #     for cfg in configs:
    #         futures.append(executor.submit(run_experiment, cfg))
    #
    #     for future in concurrent.futures.as_completed(futures):
    #         results.append(future.result())

    for cfg in configs:
        results.append(run_experiment(cfg))

        if len(results) % 10 == 0:
            time_per_exp = round((now() - start_time) / len(results), 2)
            total = round(now() - start_time)
            estimated = (length - len(results) - 1) * time_per_exp
            print(f'Process {len(results)} experiments. '
                  f'Time per experiment: {time_per_exp} s, '
                  f'total: {int(total // 3600):02d}:{int(total % 3600 // 60):02d}:'
                  f'{int(total % 60):02d}, '
                  f'remained: {int(estimated // 3600):02d}:{int(estimated % 3600 // 60):02d}:'
                  f'{int(estimated % 60):02d}')
            write_results(results, result_filename)

    print(f'Full experiment took {round(now() - start, 2)} sec')

    write_results(results, result_filename)

    print('random experiment is done')


if __name__ == '__main__':
    for n, k in ((14, 7), (12, 6)):
        run_random_experiment(n, k)
    # run_random_experiment(10, 5)
