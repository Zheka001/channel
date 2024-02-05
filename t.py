from itertools import combinations

if __name__ == '__main__':
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    counter = 0
    for comb in combinations(a, 5):
        print(comb)
        counter += 1

    print(f'total: {counter}')