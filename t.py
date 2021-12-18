import json
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    with open('data/times.json', 'r') as file:
        times = json.load(file)

    sns.lineplot(data=times[:100000])
    plt.show()
