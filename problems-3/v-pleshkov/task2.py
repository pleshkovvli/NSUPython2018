from itertools import islice
from sys import argv


def main():
    percentages = 90

    filename = argv[1]

    with open(filename, "r") as file:
        count = sum(1 for line in file if line.startswith("open"))
        file.seek(0)
        times = (float(line.split(' ', 3)[2]) for line in file if line.startswith("open"))

        top_count = int(count * (100 - percentages) / 100 + 1)

        top_times = dict()
        for time in islice(times, 0, top_count):
            _inc_value(top_times, time)

        min_time = min(top_times.keys())
        for time in times:
            if time > min_time:
                _dec_value(top_times, min_time)
                _inc_value(top_times, time)
                min_time = min(top_times.keys())

        decile = min(top_times.keys())
        print(f"{percentages}% of time values less or equal to {decile}")


def _dec_value(counter, value):
    counter[value] -= 1
    if counter[value] == 0:
        counter.pop(value)


def _inc_value(counter, value):
    if value in counter.keys():
        counter[value] += 1
    else:
        counter[value] = 1

if __name__ == "__main__":
    if len(argv) >= 2:
        main()
    else:
         print("Usage: python3 task1.py FILENAME")
