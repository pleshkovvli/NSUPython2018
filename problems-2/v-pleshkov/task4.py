from sys import argv


def main():
    encoding = _check_encoding()

    counts = get_counts(argv[1])
    frequencies = get_frequencies(counts)

    char = "unknown"

    byte_count = 0

    for byte, frequency in frequencies:
        if frequency == 0:
            print(f"{byte_count} byte codes found")
            break

        byte_count += 1

        if encoding is not None:
            char = bytes([byte]).decode(encoding)

        print(f"{byte} {frequency:10.6f} {char}")


def get_frequencies(counts):
    non_ascii = counts[128:]
    non_ascii_count = sum(non_ascii)
    frequencies = [(index + 128, count * 100 / non_ascii_count) for index, count in enumerate(non_ascii)]
    frequencies.sort(key=lambda x: x[1], reverse=True)
    return frequencies


def get_counts(filename):
    counts = [0] * 256
    with open(filename, 'rb') as file:
        buf_size = 1024 * 1024
        while True:
            read_bytes = file.read(buf_size)
            if len(read_bytes) == 0:
                break
            for byte in read_bytes:
                counts[byte] += 1
    return counts


def _check_encoding():
    encoding = None
    if len(argv) >= 3:
        encoding = argv[2]
        try:
            bytes([1]).decode(encoding)
        except LookupError:
            print("Invalid encoding! Characters will not be decoded")
            encoding = None
    return encoding


if __name__ == "__main__":
    if len(argv) < 2:
        print("USAGE: python3.6 task4.py FILENAME [ENCODING]")
    else:
        main()
