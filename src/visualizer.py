import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class Visualizer:
    def __init__(self, path_to_save):
        self.path_to_save = Path(path_to_save)

    def combine(self):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 2, figsize=[15, 6])
        data = self._read_json(Path('data/random_results_500.json'))
        df = self._preprocess_data(data)
        data = self._read_json(Path('data/random_results_identity_500.json'))
        df_identity = self._preprocess_data(data)
        df_identity.columns = [name + '_identity' for name in df_identity.columns]
        common_df = pd.concat([df, df_identity], axis=1)

        self._draw_image(common_df, ax=ax[0], title='Равномерные стирания',
                         labels=['Равномерные стирания', 'Группирующиеся стирания'])
        self._draw_image2(common_df, ax=ax[1], title='Группирующиеся стирания')

    def pair_plot(self, info):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 2, figsize=[15, 6])
        data = self._read_json(Path(info['file1']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax[0], title=info['title1'], labels=info['labels1'])
        data = self._read_json(Path(info['file2']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax[1], title=info['title2'], labels=info['labels2'])

        plt.savefig(self.path_to_save)

    @staticmethod
    def _read_json(path_to_file):
        with open(path_to_file, 'r') as file:
            info = json.load(file)
        return info

    @staticmethod
    def _preprocess_data(data, kernel_size=20):
        data = sorted(data, key=lambda x: 1 - x['probability'])
        df = pd.DataFrame(data)
        df['group'] = 1 - df['group']
        df['simple'] = 1 - df['simple']
        # усреднение
        # kernel = np.ones(kernel_size) / kernel_size
        # group_array = np.pad(df['group'], (kernel_size // 2, kernel_size // 2 - 1), mode='edge')
        # simple_array = np.pad(df['simple'], (kernel_size // 2, kernel_size // 2 - 1), mode='edge')
        # df['group erasures'] = np.convolve(group_array, kernel, mode='valid')
        # df['simple erasures'] = np.convolve(simple_array, kernel, mode='valid')
        df['group erasures'] = df['group']
        df['simple erasures'] = df['simple']
        return df

    def _draw_image(self, df, ax=None, need_new_plot=False, title=None, labels=None):
        sns.set_theme(style="darkgrid")
        fig = sns.lineplot(data=df, x='probability', y='simple erasures', label=labels[0], color='black', linestyle='--', ax=ax)
        fig = sns.lineplot(data=df, x='probability', y='group erasures', label=labels[1], color='black', linestyle='solid', ax=ax)
        # fig = sns.lineplot(np.linspace(0.0, 0.5), np.linspace(0.0, 0.5), label=labels[2], color='black', linestyle='-.', ax=ax)
        fig.set(title=title,
                xlabel='Вероятность получения стирания',
                ylabel='Вероятность ошибки декодирования',
                xlim=[-0.01, 0.61],
                ylim=[-0.01, 0.61])
        # plt.savefig(f'{self.path_to_file.with_suffix(".png")}')

    @staticmethod
    def _draw_image2(df, ax=None, title=None):
        sns.set_theme(style="darkgrid")
        fig = sns.lineplot(data=df, x='probability', y='group erasures', label='метод равновесных столбцов', color='black', linestyle='--', ax=ax)
        fig = sns.lineplot(data=df, x='probability', y='group erasures_identity', label='модификация метода равновесных столбцов', color='black', linestyle='solid', ax=ax)
        fig.set(title=title,
                xlabel='Вероятность получения стирания',
                ylabel='Вероятность ошибки декодирования',
                xlim=[-0.01, 0.51],
                ylim=[-0.01, 0.51])
        plt.savefig('data/figure_2.png')


if __name__ == '__main__':
    # Visualizer(Path('data/random_results_2.png')).combine()

    cfg1 = {
        'file1': 'data/random_results_500.json',
        'title1': 'Метод равновесных столбцов',
        'labels1': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],

        'file2': 'data/random_results_identity_500.json',
        'title2': 'Модицицированный метод равновесных столбцов',
        'labels2': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],
    }

    cfg2 = {
        'file1': 'data/random_results_12_6_old.json',
        'title1': 'Метод равновесных столбцов с параметрами (6, 12)',
        'labels1': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],

        'file2': 'data/random_results_14_7.json',
        'title2': 'Метод равновесных столбцов с параметрами (7, 14)',
        'labels2': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],
    }

    Visualizer(Path('data/figure_3.png')).pair_plot(cfg1)