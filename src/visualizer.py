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
        # fig, ax = plt.subplots(1, 1, figsize=[7, 6])
        data = self._read_json(Path('data/random_results_10_5.json'))
        df = self._preprocess_data(data)
        data = self._read_json(Path('data/random_results_10_5_identity.json'))
        df_identity = self._preprocess_data(data)
        df_identity.columns = [name + '_identity' for name in df_identity.columns]
        common_df = pd.concat([df, df_identity], axis=1)

        fig, ax = plt.subplots(1, 1, figsize=[12, 10])
        self._draw_image(common_df, ax=ax, title='Независимые стирания',
                         labels=['метод равновесных столбцов', 'модификация метода равновесных столбцов'])
        self._increase_font_size(ax)
        plt.savefig(self.path_to_save.with_name(f'{self.path_to_save.stem}a.png'))

        fig, ax = plt.subplots(1, 1, figsize=[12, 10])
        self._draw_image2(common_df, ax=ax, title='Группирующиеся стирания')
        # plt.savefig(self.path_to_save)
        self._increase_font_size(ax)
        plt.savefig(self.path_to_save.with_name(f'{self.path_to_save.stem}b.png'))

    def pair_plot(self, info):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 2, figsize=[15, 6])
        data = self._read_json(Path(info['file1']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax[0], title=info['title1'], labels=info['labels1'])
        data = self._read_json(Path(info['file2']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax[1], title=info['title2'], labels=info['labels2'])
        self._increase_font_size(ax)
        plt.savefig(self.path_to_save)

    def pair_plot_by_letters(self, info):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 1, figsize=[12, 10])
        data = self._read_json(Path(info['file1']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax, title=info['title1'], labels=info['labels1'])
        self._increase_font_size(ax)
        plt.savefig(self.path_to_save.with_name(f'{self.path_to_save.stem}a.png'))

        fig, ax = plt.subplots(1, 1, figsize=[12, 10])
        data = self._read_json(Path(info['file2']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax, title=info['title2'], labels=info['labels2'])
        self._increase_font_size(ax)
        plt.savefig(self.path_to_save.with_name(f'{self.path_to_save.stem}b.png'))

    def theory_plot(self, info):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 1, figsize=[12, 10])

        data = self._read_json(Path(info['file1']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax, labels=info['labels1'], just_simple=True)
        data = self._read_json(Path(info['file2']))
        df = self._preprocess_data(data, just_simple=True)
        self._draw_image(df, ax=ax, labels=info['labels2'], title=info['title2'], just_simple=True, style='--')
        self._increase_font_size(ax)
        plt.savefig(self.path_to_save)

    def common_plot(self, info):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 1, figsize=[12, 10])
        data = self._read_json(Path(info['file']))
        df = self._preprocess_data(data)
        self._draw_image(df, ax=ax, labels=info['labels'], title=info['title'], just_simple=False)
        self._increase_font_size(ax)
        plt.savefig(self.path_to_save)

    @staticmethod
    def _read_json(path_to_file):
        with open(path_to_file, 'r') as file:
            info = json.load(file)
        return info

    @staticmethod
    def _preprocess_data(data, kernel_size=20, just_simple=False):
        data = sorted(data, key=lambda x: 1 - x['probability'])
        df = pd.DataFrame(data)
        if not just_simple:
            df['group'] = 1 - df['group']
            df['simple'] = 1 - df['simple']
        # усреднение
        kernel = np.ones(kernel_size) / kernel_size
        if not just_simple:
            group_array = np.pad(df['group'], (kernel_size // 2, kernel_size // 2 - 1), mode='edge')
        simple_array = np.pad(df['simple'], (kernel_size // 2, kernel_size // 2 - 1), mode='edge')
        if not just_simple:
            df['group erasures'] = np.convolve(group_array, kernel, mode='valid')
        df['simple erasures'] = np.convolve(simple_array, kernel, mode='valid')
        # df['group erasures'] = df['group']
        # df['simple erasures'] = df['simple']
        return df

    def _draw_image(self, df, ax=None, title=None, labels=None, just_simple=False, style='solid'):
        sns.set_theme(style="darkgrid")
        fig = sns.lineplot(data=df, x='probability', y='simple erasures', label=labels[0], color='black', linestyle=style, ax=ax, linewidth=2)
        if not just_simple:
            fig = sns.lineplot(data=df, x='probability', y='group erasures', label=labels[1], color='black', linestyle='--', ax=ax, linewidth=2)
        if len(labels) > 2:
            fig = sns.lineplot(np.linspace(0.0, 0.5), np.linspace(0.0, 0.5), label=labels[2], color='black', linestyle='-.', ax=ax, linewidth=2)
        fig.set(title=title + '\n' if title is not None else title,
                xlabel='Вероятность стирания в канале',
                ylabel='Вероятность ошибки декодирования',
                xlim=[-0.01, 0.61],
                ylim=[-0.01, 0.61])
        plt.setp(ax.get_legend().get_texts(), fontsize='24')

    @staticmethod
    def _draw_image2(df, ax=None, title=None):
        sns.set_theme(style="darkgrid")
        fig = sns.lineplot(data=df, x='probability', y='group erasures', label='метод равновесных столбцов', color='black', linestyle='solid', ax=ax,  linewidth=2)
        fig = sns.lineplot(data=df, x='probability', y='group erasures_identity', label='модификация метода равновесных столбцов', color='black', linestyle='--', ax=ax, linewidth=2)
        fig.set(title=title + '\n' if title is not None else title,
                xlabel='Вероятность стирания в канале',
                ylabel='Вероятность ошибки декодирования',
                xlim=[-0.01, 0.51],
                ylim=[-0.01, 0.51])
        plt.setp(ax.get_legend().get_texts(), fontsize='24')  # for legend text

    @staticmethod
    def _increase_font_size(ax):
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(26)


if __name__ == '__main__':
    Visualizer(Path('data/figure_2.png')).combine()

    cfg1 = {
        'file1': 'data/random_results_10_5.json',
        'title1': 'Метод равновесных столбцов',
        'labels1': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],

        'file2': 'data/random_results_10_5_identity.json',
        'title2': 'Модифицированный метод равновесных столбцов',
        'labels2': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],
    }

    cfg2 = {
        'file1': 'data/random_results_12_6.json',
        'title1': 'Метод равновесных столбцов с параметрами (12, 6)',
        'labels1': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],

        'file2': 'data/random_results_14_7.json',
        'title2': 'Метод равновесных столбцов с параметрами (14, 7)',
        'labels2': ['равномерные стирания', 'группирующиеся стирания', 'передача данных без кодирования'],
    }

    cfg3 = {
        'file1': 'data/random_results_10_5.json',
        'title1': 'Метод равновесных столбцов',
        'labels1': ['практическая оценка', 'группирующиеся стирания'],

        'file2': 'data/theory_evaluation.json',
        'title2': 'Сравнение теоретического и практического расчетов',
        'labels2': ['теоретическая оценка', 'передача данных без кодирования'],
    }

    cfg4 = {
        'file': 'data/random_results_10_5_9.json',
        'title': 'Увеличение избыточности для группирующихся стираний',
        'labels': ['равномерные стирания для параметров (9, 5)', 'группирующиеся стирания для параметров (10, 5)']
    }

    # первый и второй рисунок
    for path_to_figure, cfg in zip(['data/figure_1.png', 'data/figure_3.png'], [cfg1, cfg2]):
        Visualizer(Path(path_to_figure)).pair_plot_by_letters(cfg)

    Visualizer(Path('data/figure_4.png')).theory_plot(cfg3)
    Visualizer(Path('data/figure_5.png')).common_plot(cfg4)
