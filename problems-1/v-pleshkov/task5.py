import unittest

import itertools

from primes import is_prime, prime_numbers_fast
from sys import argv


def prime_numbers(limit):
    return [n for n in range(2,3) if limit >= 2] + [n for n in range(3, limit + 1, 2) if is_prime(n)]


class TestEratosthenesPrimes(unittest.TestCase):
    def testEdgeCases(self):
        self.assertEqual(prime_numbers(0), [])
        self.assertEqual(prime_numbers(1), [])
        self.assertEqual(prime_numbers(-1), [])
        self.assertEqual(prime_numbers(-2), [])
        self.assertEqual(prime_numbers(-231), [])

    def testPrimes(self):
        self._testPrimes(3342)
        self._testPrimes(5232)
        self._testPrimes(92313)
        self._testPrimes(2213)
        self._testPrimes(4121)

    def _testPrimes(self, limit):
        primes = prime_numbers(limit)
        self.assertEqual(primes, [n for n in itertools.islice(prime_numbers_fast(), len(primes))])


def main():
    if len(argv) < 2:
        unittest.main()
        return

    try:
        limit = int(argv[1])
        print([n for n in prime_numbers(limit)])
    except ValueError:
        print("Integer number expected as argument")


if __name__ == "__main__":
    main()
