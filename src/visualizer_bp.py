import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class VisualizerBP:
    def __init__(self, path_to_data):
        self.path_to_data = Path(path_to_data)

    def exploration(self):
        with open(self.path_to_data, 'r') as file:
            data = json.load(file)

        for k in range(5, 11):
            filt_data = [el for el in data if el['k'] == k]
            filt_data = sorted(filt_data, key=lambda x: x['probability'])
            df = pd.DataFrame(filt_data)
            path_to_save = Path(f'data/bp/k_{k}.png')
            path_to_save.parent.mkdir(parents=True, exist_ok=True)
            self.pair_plot(df, path_to_save)

    def pair_plot(self, df, path_to_save):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(1, 2, figsize=[15, 6])

        title = 'Время работы алгоритмов при различных вероятностях стираний'
        labels = ['Распространение доверия', 'Гибридный по ИС']
        columns = {
            'x': 'probability',
            'y1': 'total_time_bp',
            'y2': 'total_time_hybrid',
        }
        xlabel = 'Вероятность стирания в канале'
        ylabel = 'Общее время работы алгоритма'
        self._draw_image(df, ax=ax[0], title=title, labels=labels, columns=columns, xlabel=xlabel, ylabel=ylabel)

        title = 'Количество исправляемых пакетов при различных вероятностях стираний'
        labels = ['Распространение доверия', 'Гибридный по ИС']
        columns = {
            'x': 'probability',
            'y1': 'successful_count_bp',
            'y2': 'successful_count_hybrid',
        }
        xlabel = 'Вероятность стирания в канале'
        ylabel = 'Кол-во исправленных пакетов'
        self._draw_image(df, ax=ax[1], title=title, labels=labels, columns=columns, xlabel=xlabel, ylabel=ylabel)

        # self._increase_font_size(ax)
        plt.savefig(path_to_save)


    @staticmethod
    def _read_json(path_to_file):
        with open(path_to_file, 'r') as file:
            info = json.load(file)
        return info

    def _draw_image(self, df, ax=None, title=None, labels=None, columns=None, xlabel=None, ylabel=None):
        sns.set_theme(style="darkgrid")
        fig = sns.lineplot(data=df, x=columns['x'], y=columns['y1'], label=labels[0], color='black', linestyle='-',
                           ax=ax, linewidth=2)
        fig = sns.lineplot(data=df, x=columns['x'], y=columns['y2'], label=labels[1], color='black', linestyle='--',
                           ax=ax, linewidth=2)
        fig.set(
            title=title + '\n' if title is not None else title,
            xlabel=xlabel,
            ylabel=ylabel,
            # xlim=[-0.01, 0.61],
            # ylim=[-0.01, 0.61]
        )
        # plt.setp(ax.get_legend().get_texts(), fontsize='24')

    @ staticmethod
    def _increase_font_size(ax):
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(26)


if __name__ == '__main__':
    VisualizerBP('data/bp_results.json').exploration()
