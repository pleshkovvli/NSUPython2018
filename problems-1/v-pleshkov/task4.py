from os import listdir, stat
from os.path import join, isfile
from sys import argv, stderr


def main():
    if len(argv) < 2:
        print(f"Usage: python3 {argv[0]} DIRECTORY")
        return

    path_name = argv[1]

    try:
        files = get_files_sizes_and_names(path_name)
        files.sort(key = lambda size_with_name: (-size_with_name[0], size_with_name[1]))

        for file in files:
            print(f"{file[1]}: {file[0]} bytes")

    except OSError as e:
        print(f"Failed to read directory: {e.strerror}", file=stderr)
        return


def get_files_sizes_and_names(path_name):
    files_names = listdir(path_name)
    files = []
    for name in files_names:
        current_path = join(path_name, name)
        if isfile(current_path):
            size = stat(current_path).st_size
            files.append((size, name))
    return files


if __name__ == "__main__":
    main()
