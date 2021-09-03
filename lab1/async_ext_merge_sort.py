import heapq
import os


# Sorts all the input files and stores the sorted data on the disk
def sort_input_files():
    path_to_input = os.getcwd() + "/input/"
    input_files_list = os.listdir(path_to_input)

    for i in range(len(input_files_list)):
        with open(path_to_input + input_files_list[i], 'r') as file:
            numbers = sorted([int(line.strip()) for line in file.readlines()])

        output_file_name = 'sorted_' + str(i) + '.txt'
        with open(output_file_name, 'w') as f:
            for number in numbers:
                f.write("%s\n" % number)


# Merges the sorted data on the disk and writes the merged data into output file
def merge_sorted_files():
    path = os.getcwd()
    output_files = []
    for file in os.listdir(path):
        if file.startswith('sorted'):
            output_files.append(file)
    numbers_list = [[]]

    for i in range(len(output_files)):
        with open(output_files[i], 'r') as file:
            numbers = [int(line.strip()) for line in file.readlines()]
            numbers_list.append(numbers)

    heapq.merge(*numbers_list)
    return heapq.merge(*numbers_list)


def write_result_to_disk(sorted_data):
    with open(os.getcwd() + '/output/async_sorted.txt', 'w') as f:
        for x in sorted_data:
            f.write(str(x)+'\n')


def sort():
    sort_input_files()
    sorted_data = merge_sorted_files()
    write_result_to_disk(sorted_data)


if __name__ == "__main__":
    sort()
