import json

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from pathlib import Path


class Visualizer:
    def __init__(self, path_to_file):
        self.path_to_file = Path(path_to_file)
        self.info = None

    def _read_json(self):
        with open(self.path_to_file, 'r') as file:
            self.info = json.load(file)

    def run(self):
        self._read_json()
        self.info = sorted(self.info, key=lambda x: 1 - x['probability'])
        df = pd.DataFrame(self.info)
        df['group'] = 1 - df['group']
        df['simple'] = 1 - df['simple']
        df.plot(x='probability')
        plt.plot(np.linspace(0.0, 0.5), np.linspace(0.0, 0.5))
        plt.show()


if __name__ == '__main__':
    vis = Visualizer('../data/random_results.json')
    vis.run()
