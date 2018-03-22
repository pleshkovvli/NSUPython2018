from sys import stdin


def main():
    print("Please, enter a number")

    while True:
        try:
            line = stdin.readline()
            if len(line) == 0:
                print("Number hasn't been entered")
                return

            number = float(line)
            print(f"Success! Number = {number}")
            return
        except ValueError:
            print("Not a number! Please, enter a number")


if __name__ == "__main__":
    main()
