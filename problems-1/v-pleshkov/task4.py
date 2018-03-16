from os import listdir, stat
from os.path import join, isfile
from sys import argv


def main():
    if len(argv) < 2:
        print(f"Usage: python3 {argv[0]} DIRECTORY")
        return

    current_path = argv[1]

    try:
        files_names = listdir(current_path)
    except OSError as e:
        print(f"Failed to read directory: {e.strerror}")
        return

    files = []
    for name in files_names:
        path = join(current_path, name)
        if isfile(path):
            size = stat(path).st_size
            files.append((size, name))

    files.sort(key = lambda size_with_name: (-size_with_name[0], size_with_name[1]))

    for file in files:
        print(f"{file[1]}: {file[0]} bytes")


if __name__ == "__main__":
    main()
