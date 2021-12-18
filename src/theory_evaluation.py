import json
from math import comb


if __name__ == '__main__':
    basic_probs = [0.643, 0.929, 1, 1, 1, 1]
    results = list()
    n = 10
    basic_probs = list(reversed(basic_probs))
    for p in range(500):
        prob = p / 1000
        p_e = 1 - sum([basic_probs[i] * comb(n, i) * pow(prob, i) * pow(1-prob, n-i) for i in range(6)])
        # print(prob, p_e)
        results.append({'probability': prob, 'evaluation': p_e})

    with open('data/theory_evaluation.json', 'w') as file:
        json.dump(results, file, indent=4)


