import json
from pathlib import Path

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_comparing_cauchy(path_to_data: Path):
    info_files = [elem for elem in path_to_data.iterdir() if elem.suffix == '.json']

    for filename in info_files:
        path_to_save = filename.with_suffix('.png')
        k, n = str(path_to_save.name).split('_')[2:]
        n = n.split('.')[0]

        with open(filename, 'r') as file:
            data = json.load(file)
        title = f'Сравнение метода равновесных столбцов ({k}, {n}) и метода В. Пана'

        df = pd.DataFrame(data)
        df['ours_perc'] = df['ours'] / df['total'] * 100
        df['cauchy_perc'] = df['cauchy'] / df['total'] * 100

        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 1, figsize=[12, 10])
        fig = sns.lineplot(data=df, x='erasure_count', y='cauchy_perc', label='метод В. Пана', color='black', linestyle='solid',
                           ax=ax, linewidth=2)
        fig = sns.lineplot(data=df, x='erasure_count', y='ours_perc', label='метод равновесных столбцов', color='black',
                           ax=ax, linestyle='--', linewidth=2)

        fig.set(title=title + '\n\n' if title is not None else title,
                xlabel='Количество стираний в кодовом слове, шт.',
                ylabel='Процент успешно декодированных кодовых слов, %',)
                # xlim=[-0.01, 0.61],
                # ylim=[-0.01, 0.61])
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(26)
        plt.setp(ax.get_legend().get_texts(), fontsize='24')
        plt.savefig(path_to_save)


def plot_comparing_cauchy_prob(path_to_data: Path):
    info_files = [elem for elem in path_to_data.iterdir() if elem.suffix == '.json']

    for filename in info_files:
        path_to_save = filename.with_suffix('.png')
        k, n = str(path_to_save.name).split('_')[2:]
        n = n.split('.')[0]

        with open(filename, 'r') as file:
            data = json.load(file)
        title = f'Сравнение метода равновесных столбцов ({k}, {n}) и метода В. Пана'

        data = sorted(data, key=lambda x: 1 - x['erasure_prob'])
        df = pd.DataFrame(data)
        df['ours_perc'] = df['ours'] / df['total'] * 100
        df['cauchy_perc'] = df['cauchy'] / df['total'] * 100

        # усреднение
        kernel_size = 20
        kernel = np.ones(kernel_size) / kernel_size
        simple_array = np.pad(df['ours_perc'], (kernel_size // 2, kernel_size // 2 - 1), mode='edge')
        df['ours_perc'] = np.convolve(simple_array, kernel, mode='valid')
        simple_array = np.pad(df['cauchy_perc'].tolist(), (kernel_size // 2, kernel_size // 2 - 1), mode='edge')
        df['cauchy_perc'] = np.convolve(simple_array, kernel, mode='valid')

        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 1, figsize=[12, 10])
        fig = sns.lineplot(data=df, x='erasure_prob', y='cauchy_perc', label='метод В. Пана', color='black', linestyle='solid',
                           ax=ax, linewidth=2)
        fig = sns.lineplot(data=df, x='erasure_prob', y='ours_perc', label='метод равновесных столбцов', color='black',
                           ax=ax, linestyle='--', linewidth=2)

        fig.set(title=title + '\n\n' if title is not None else title,
                xlabel='Вероятность стирания в канале',
                ylabel='Процент успешно декодированных кодовых слов, %',)
                # xlim=[-0.01, 0.61],
                # ylim=[-0.01, 0.61])
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(26)
        plt.setp(ax.get_legend().get_texts(), fontsize='24')
        plt.savefig(path_to_save)


if __name__ == '__main__':
    # path_to_data = Path('data/cauchy_complex')
    # plot_comparing_cauchy(path_to_data)
    path_to_data = Path('data/cauchy_probability')
    plot_comparing_cauchy_prob(path_to_data)

