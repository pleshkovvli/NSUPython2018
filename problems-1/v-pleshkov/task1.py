import unittest

from primes import max_possible_divider, prime_numbers_fast
from sys import argv


def prime_multipliers(number, primes = prime_numbers_fast()):
    if number < 0:
        number = abs(number)
        yield [-1, 1]

    max_div = max_possible_divider(number)

    for prime in primes:
        count = divide_count(number, prime)
        if count > 0:
            number //= prime ** count
            max_div = max_possible_divider(number)
            yield [prime, count]
        if prime > max_div:
            break

    if number > 1:
        yield [number, 1]


def divide_count(numerator, divisor):
    count = 0
    while numerator % divisor == 0:
        numerator //= divisor
        count += 1
    return count


def main():
    if len(argv) < 2:
        print(f"Usage: python3 {__file__} NUMBER")
        return
    if argv[1] == "test":
        unittest.main()
    else:
        print([n for n in prime_multipliers(int(argv[1]))])


if __name__ == "__main__":
    main()
