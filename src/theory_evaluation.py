import json
from math import comb


if __name__ == '__main__':
    # basic_probs = [0.643, 0.929, 1, 1, 1, 1]
    # results = list()
    # n = 10
    # basic_probs = list(reversed(basic_probs))
    # for p in range(500):
    #     prob = p / 1000
    #     p_e = 1 - sum([basic_probs[i] * comb(n, i) * pow(prob, i) * pow(1-prob, n-i) for i in range(6)])
    #     # print(prob, p_e)
    #     results.append({'probability': prob, 'evaluation': p_e})
    #
    # with open('data/theory_evaluation.json', 'w') as file:
    #     json.dump(results, file, indent=4)

    with open('data/theory_evaluation.json', 'r') as file:
        theory = json.load(file)

    with open('data/random_results_10_5.json', 'r') as file:
        practic = json.load(file)

    # todo: попробовать посчитать абсолютную и среднеквадратичную ошибки

    print(theory[:10])
    print(practic[:10])

    for element in practic:
        element['probability'] = round(element['probability'], 3)
        element['simple'] = 1 - element['simple']

    mae_list = list()
    mse_list = list()
    for th in theory:
        practics = [pr for pr in practic if pr['probability'] == th['probability']]
        if len(practics) > 0:
            pr = practics[0]

            mae_list.append(abs(pr['simple'] - th['simple']))
            mse_list.append(pow(pr['simple'] - th['simple'], 2))

    print(len(theory), len(mse_list), len(mae_list))

    print('max error =', max(mae_list))
    print('mse = ', sum(mse_list) / len(mse_list))





