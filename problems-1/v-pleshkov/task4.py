from os import listdir, stat
from os.path import join, isfile
from sys import argv


def main():
    if len(argv) < 2:
        print(f"Usage: python3 {argv[0]} DIRECTORY")
        return

    current_path = argv[1]
    files_names = listdir(current_path)

    files = []
    for name in files_names:
        path = join(current_path, name)
        if isfile(path):
            size = stat(path).st_size
            files.append((name, size))

    files.sort(key = lambda filesize: filesize[0])
    files.sort(key = lambda filesize: filesize[1], reverse=True)

    for file in files:
        print(f"{file[0]}: {file[1]} bytes")


if __name__ == "__main__":
    main()
