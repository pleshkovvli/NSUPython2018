import operator
from functools import reduce
from itertools import islice
from math import sqrt
from sys import argv


def main():
    filename = argv[1]

    with open(filename, "r") as file:
        times = (float(line.split(' ', 3)[2]) for line in file if line.startswith("open"))
        all_sum, sum_squares, count = reduce(lambda acc, triple: tuple(map(operator.add, acc, triple)),
                                             map(lambda time: (time, time * time, 1),
                                                 islice(times, 1, None)))

    mean = all_sum / count
    deviation = standard_deviation(all_sum, sum_squares, count)

    print(f"Mean = {mean:5.2f}, deviation = {deviation:5.4f}, count = {count}")


def standard_deviation(all_sum, sum_squares, count):
    return sqrt((sum_squares - all_sum * all_sum / count) / count)


if __name__ == "__main__":
    if len(argv) >= 2:
        main()
    else:
        print("Usage: python3 task1.py FILENAME")
