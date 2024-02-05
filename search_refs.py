from pprint import pprint

import numpy as np



if __name__ == '__main__':
    with open('text_dis.txt', 'r') as file:
        text = file.read()

    lines = list()
    start_index = 0
    end_index = 0
    while True:
        start_pos = text.find('[', start_index)
        end_pos = text.find(']', end_index)
        if start_pos != -1 and end_pos != -1:
            lines.append(text[start_pos:end_pos + 1])
            start_index = start_pos + 1
            end_index = end_pos + 1
        else:
            break

    print('length:', len(lines))
    # for line in lines:
    #     print(line)

    filtered_lines = [line for line in lines if 'п' in line]
    print(f'filtered lines: {len(filtered_lines)}')

    prepared_numbers = list()
    for line in filtered_lines:
        if ',' in line:
            line = line[1:-1]
            references = line.split(',')
            references = [ref.replace(' ', '') for ref in references]
            numbers = [int(ref[1:]) for ref in references]
            prepared_numbers.extend(numbers)
        else:
            number = int(line[2:-1])
            prepared_numbers.append(number)

    print(prepared_numbers)
    print(len(prepared_numbers))

    total_refs = 133
    missed = list()
    for i in range(1, total_refs + 1):
        if i not in prepared_numbers:
            missed.append(i)

    print(f'missed: {missed}')

    is_used = set()
    assign_dict = dict()
    counter = 1
    for number in prepared_numbers:
        if number not in is_used:
            assign_dict[number] = counter
            counter += 1
            is_used.add(number)

    print(counter)
    for key, value in sorted(assign_dict.items(), key=lambda x: x[1]):
        print(f'п{key} : {value}')


    # with open('list_of_literature.txt', 'r') as file:
    #     literature_list = file.readlines()
    #
    # print(len(literature_list))
    #
    # for k, v in assign_dict.items():
    #     print(literature_list[k - 1], end='')


    # unique_numbers = np.unique(prepared_numbers)
    # print(unique_numbers.shape)
    # print(unique_numbers)


