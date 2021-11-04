import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class Visualizer:
    def __init__(self, path_to_file):
        self.path_to_file = Path(path_to_file)

    def run(self):
        data = self._read_json(self.path_to_file)
        df = self._preprocess_data(data)
        self._draw_image(df)

    def combine(self):
        data = self._read_json(Path('data/random_results_500.json'))
        df = self._preprocess_data(data)
        self._draw_image(df)
        data = self._read_json(Path('data/random_results_identity_500.json'))
        df = self._preprocess_data(data)
        self._draw_image2(df)

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
        kernel = np.ones(kernel_size) / kernel_size
        df['group erasures'] = np.convolve(df['group'], kernel, mode='same')
        df['simple erasures'] = np.convolve(df['simple'], kernel, mode='same')
        return df

    def _draw_image(self, df, need_new_plot=True):
        if need_new_plot:
            plt.figure(figsize=[12, 6])
        sns.set_theme(style="darkgrid")
        fig = sns.lineplot(data=df, x='probability', y='simple erasures', label='простой тип стираний', color='black', linestyle='--')
        fig = sns.lineplot(data=df, x='probability', y='group erasures', label='групповой тип стираний', color='black', linestyle='solid')
        fig = sns.lineplot(np.linspace(0.0, 0.5), np.linspace(0.0, 0.5), label='передача чистой информации', color='black', linestyle='-.')
        fig.set(xlabel='Вероятность получения стирания',
                ylabel='Вероятность ошибки декодирования',
                xlim=[-0.01, 0.51],
                ylim=[-0.01, 0.51])
        plt.savefig(f'{self.path_to_file.with_suffix(".png")}')

    @staticmethod
    def _draw_image2(df):
        fig = sns.lineplot(data=df, x='probability', y='simple erasures', label='простой тип стираний, модификация', color='black', linestyle='solid')
        fig = sns.lineplot(data=df, x='probability', y='group erasures', label='групповой тип стираний, модификация', color='black', linestyle='solid')
        plt.savefig('data/combined_group.png')


if __name__ == '__main__':
    json_files = Path('data').glob('*.json')
    for json_file in json_files:
        vis = Visualizer(json_file)
        vis.run()

    # Visualizer(Path('data/random_results_500.json')).combine()
