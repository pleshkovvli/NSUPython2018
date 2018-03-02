import unittest

from primes import is_prime, prime_numbers_fast
from sys import argv


def prime_numbers(limit):
    return [2] + [n for n in range(3, limit, 2) if is_prime(n)]


def main():
    if len(argv) < 2:
        print(f"Usage: python3 {__file__} LIMIT")
        return
    if argv[1] == "test":
        unittest.main()
    else:
        print(prime_numbers(int(argv[1])))


if __name__ == "__main__":
    main()
