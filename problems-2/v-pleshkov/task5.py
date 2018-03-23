import codecs

from sys import argv
from math import sqrt
from task4 import get_counts, get_frequencies


def main():
    filename = argv[1]
    counts = get_counts(filename)
    frequencies = get_frequencies(counts)

    encoding_frequencies = encodings_frequencies(_default_encodings(), _default_frequencies())

    differences = [(encoding[0], distance(frequencies, encoding[1])) for encoding in encoding_frequencies]
    encoding_name = min(differences, key= lambda x: x[1])[0]

    print(f"I guess, encoding is {encoding_name}")
    answer = input("Print file? y/n ")
    if answer == "y":
        print_encoded_file(encoding_name, filename)


def print_encoded_file(encoding_name, filename):
    with codecs.open(filename, "r", encoding_name) as file:
        buf_size = 1024 * 1024
        while True:
            read_bytes = file.read(buf_size)
            if len(read_bytes) == 0:
                break
            print(read_bytes)


def distance(frequencies, encoding):
    current_distance = 0
    for byte, frequency in frequencies:
        if byte in encoding.keys():
            encoding_byte = encoding[byte]
        else:
            continue
        code_distance = abs(encoding_byte - frequency)
        current_distance += code_distance * code_distance
    return sqrt(current_distance)


def encodings_frequencies(encodings, frequencies):
    return [(encoding, dict((list(letter.encode(encoding))[0], frequency)
                            for low_letter, frequency in frequencies.items()
                            for letter in (low_letter))) for encoding in encodings]


def _default_encodings():
    return ['koi8-r', 'cp866', 'cp1251', 'iso_8859-5']


def _default_frequencies():
    return {
        'о': 10.98,
        'е': 8.48,
        'а': 8,
        'и': 7.36,
        'н': 6.7,
        'т': 6.318,
        'с': 5.47,
        'р': 4.75,
        'в': 4.53,
        'л': 4.34,
        'к': 3.87,
        'м': 3.2,
        'д': 2.98,
        'п': 2.8,
        'у': 2.615,
        'я': 2,
        'ы': 1.9,
        'ь': 1.73,
        'г': 1.69,
        'з': 1.64,
        'б': 1.59,
        'ч': 1.45,
        'й': 1.2,
        'х': 0.96,
        'ж': 0.94,
        'ш': 0.72,
        'ю': 0.63,
        'ц': 0.48,
        'щ': 0.36,
        'э': 0.33,
        'ф': 0.26,
        'ъ': 0.037,
        'ё': 0.013
    }


if __name__ == "__main__":
    if len(argv) < 2:
        print("USAGE: python3.6 task4.py FILENAME")
    else:
        main()
