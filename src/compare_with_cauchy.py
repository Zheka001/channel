import random
import json
from pathlib import Path
from random import randint

from tqdm import tqdm

from src.channel_codec import ChannelCodec
from src.cauchy_fake import CauchyFakeCodec
from src.erasure_generator import ErasureGenerator


def simple_erasures():
    for k in range(12, 20, 2):
        n = k * 2
        total_experiments = 1000
        cc = ChannelCodec(k, n)
        cauchy_codec = CauchyFakeCodec(r=k//2)

        results_list = list()
        for erasure_count in range(1, k + 1):
            erasures = [1] * erasure_count + [0] * (n - erasure_count)
            print(f'experiments for {erasure_count} erasures')

            cc_success = 0
            cauchy_success = 0
            for i in tqdm(range(total_experiments)):
                random.shuffle(erasures)
                mes = [randint(0, 1) for _ in range(k)]
                encoded = cc.encode(mes)
                decoded, message = cc.decode_hybrid(encoded, erasures)
                if mes == decoded:
                    cc_success += 1

                status = cauchy_codec.decode(encoded, erasures)
                if status:
                    cauchy_success += 1

            print(f'cc: {cc_success}, cauchy: {cauchy_success}, total: {total_experiments}')
            results_list.append({
                'erasure_count': erasure_count,
                'ours': cc_success,
                'cauchy': cauchy_success,
                'total': total_experiments,
            })
            with open(f'data/cauchy/results_cauchy_{k}_{n}.json', 'w') as file:
                json.dump(results_list, file, indent=4)


def complex_erasures():
    path_to_save = Path('data/cauchy_complex')
    path_to_save.mkdir(parents=True, exist_ok=True)

    for k in range(8, 17, 8):
        n = k * 2
        total_experiments = 1000
        cc = ChannelCodec(k, n)
        cauchy_codec = CauchyFakeCodec(r=k//2)

        results_list = list()
        for erasure_count in range(1, 3):
            erasures_complex = [1] * erasure_count + [0] * (4 - erasure_count)
            print(f'experiments for {erasure_count} erasures')
            cc_success = 0
            cauchy_success = 0
            for i in tqdm(range(total_experiments)):
                random.shuffle(erasures_complex)
                erasures_lists = [[i] * (k // 2) for i in erasures_complex]
                erasures = list()
                for el in erasures_lists:
                    erasures.extend(el)
                mes = [randint(0, 1) for _ in range(k)]
                encoded = cc.encode(mes)
                decoded, message = cc.decode_hybrid(encoded, erasures)
                if mes == decoded:
                    cc_success += 1

                status = cauchy_codec.decode(encoded, erasures)
                if status:
                    cauchy_success += 1

            print(f'cc: {cc_success}, cauchy: {cauchy_success}, total: {total_experiments}')
            results_list.append({
                'erasure_count': erasure_count,
                'ours': cc_success,
                'cauchy': cauchy_success,
                'total': total_experiments,
            })
            with open(path_to_save / f'results_cauchy_{k}_{n}.json', 'w') as file:
                json.dump(results_list, file, indent=4)


def generate_random_configs_for_simple(length=500):
    configs = list()
    for i in range(length):
        cfg = {
            'operation': 'simple',
            'simple_probability': round(random.uniform(0.001, 0.5), 3),
        }
        configs.append(cfg)
    return configs


def probability_erasures():
    path_to_save = Path('data/cauchy_probability')
    path_to_save.mkdir(parents=True, exist_ok=True)

    erasure_configs = generate_random_configs_for_simple(length=500)

    for k in range(8, 17, 8):
        n = k * 2
        total_experiments = 1000
        cc = ChannelCodec(k, n)
        cauchy_codec = CauchyFakeCodec(r=k//2)
        print(f'process ({n}, {k}) codes ...')
        results_list = list()
        for erasure_config in tqdm(erasure_configs):
            erasure_generator = ErasureGenerator(config=erasure_config)

            cc_success = 0
            cauchy_success = 0
            for i in range(total_experiments):
                mes = [randint(0, 1) for _ in range(k)]
                encoded = cc.encode(mes)
                erasures = erasure_generator.erase(encoded, op_type='simple')
                decoded, message = cc.decode_hybrid(encoded, erasures)
                if mes == decoded:
                    cc_success += 1

                status = cauchy_codec.decode(encoded, erasures)
                if status:
                    cauchy_success += 1

            print(f'cc: {cc_success}, cauchy: {cauchy_success}, total: {total_experiments}')
            results_list.append({
                'erasure_prob': erasure_config['simple_probability'],
                'ours': cc_success,
                'cauchy': cauchy_success,
                'total': total_experiments,
            })
        with open(path_to_save / f'results_cauchy_{k}_{n}.json', 'w') as file:
            json.dump(results_list, file, indent=4)


def generate_random_configs_for_group(length=500):
    configs = list()
    for i in range(length):
        cfg = {
            'operation': 'group',
            'simple_probability': 0,
            'group_probability': round(random.uniform(0.001, 0.7), 3),
            'bad_to_good': round(random.uniform(0.001, 0.45), 3),
            'good_to_bad': round(random.uniform(0.001, 0.45), 3),
        }
        configs.append(cfg)
    return configs


def probability_group_erasures():
    path_to_save = Path('data/cauchy_probability_group')
    path_to_save.mkdir(parents=True, exist_ok=True)

    erasure_configs = generate_random_configs_for_group(length=500)

    for k in range(8, 17, 8):
        n = k * 2
        total_experiments = 1000
        cc = ChannelCodec(k, n)
        cauchy_codec = CauchyFakeCodec(r=k//2)
        print(f'process ({n}, {k}) codes ...')
        results_list = list()
        for erasure_config in tqdm(erasure_configs):
            erasure_generator = ErasureGenerator(config=erasure_config)

            cc_success = 0
            cauchy_success = 0
            for i in range(total_experiments):
                mes = [randint(0, 1) for _ in range(k)]
                encoded = cc.encode(mes)
                erasures = erasure_generator.erase(encoded, op_type='simple')
                decoded, message = cc.decode_hybrid(encoded, erasures)
                if mes == decoded:
                    cc_success += 1

                status = cauchy_codec.decode(encoded, erasures)
                if status:
                    cauchy_success += 1

            print(f'cc: {cc_success}, cauchy: {cauchy_success}, total: {total_experiments}')
            results_list.append({
                'erasure_prob': erasure_config['simple_probability'],
                'ours': cc_success,
                'cauchy': cauchy_success,
                'total': total_experiments,
            })
        with open(path_to_save / f'results_cauchy_{k}_{n}.json', 'w') as file:
            json.dump(results_list, file, indent=4)


if __name__ == '__main__':
    # simple_erasures()
    # complex_erasures()
    probability_erasures()
    probability_group_erasures()
