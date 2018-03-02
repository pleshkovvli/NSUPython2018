import itertools
import unittest

from enum import Enum
from sys import argv
from bitarray import bitarray
from primes import max_possible_divider, prime_numbers_fast


class Sieve(Enum):
    LIST = 0
    SET = 1
    BITARRAY = 2


def prime_numbers(limit, sieve_type):
    if limit < 2:
        return []
    if limit == 2:
        return [2]
    if limit == 3:
        return [2, 3]

    if sieve_type == Sieve.LIST:
        return _prime_numbers_list([True] * (limit + 1), limit)
    elif sieve_type == Sieve.SET:
        sieve_set = set(range(3, limit, 2))
        sieve_set.add(2)
        return _prime_numbers_set(sieve_set, limit)
    elif sieve_type == Sieve.BITARRAY:
        array = bitarray(limit + 1)
        array.setall(True)
        return _prime_numbers_list(array, limit)


def _prime_numbers_list(sieve, limit):
    max_prime = max_possible_divider(limit)

    current_prime = 2
    while current_prime <= max_prime:
        for i in range(current_prime * current_prime, limit + 1, current_prime):
            sieve[i] = False
        for i in range(current_prime + 1, max_prime + 1):
            if sieve[i]:
                current_prime = i
                break
        else:
            break

    primes = []
    for i in range(2, limit + 1):
        if sieve[i]:
            primes.append(i)
    return primes


def _prime_numbers_set(sieve, limit):
    max_prime = max_possible_divider(limit)

    prime = 2
    while prime <= max_prime:
        for i in range(prime * prime, limit + 1, prime):
            if i in sieve:
                sieve.remove(i)
        for i in range(prime + 1, max_prime + 1):
            if i in sieve:
                prime = i
                break
        else:
            break
    primes = []
    for i in range(2, limit + 1):
        if i in sieve:
            primes.append(i)
    return primes


class WrongSieveTypeException(Exception):
    pass


def get_sieve_type(index):
    sieve_values = [e.value for e in Sieve]
    try:
        type_index = int(index)
        if type_index not in sieve_values:
            raise WrongSieveTypeException(f"Allowed sieve type indices are: {sieve_values}")
        return Sieve(type_index)
    except ValueError:
        raise WrongSieveTypeException(f"Sieve type should be a number in {sieve_values}")


class TestEratosthenesPrimes(unittest.TestCase):
    def testEdgeCases(self):
        for sieve_type in Sieve:
            self.assertEqual(prime_numbers(0, sieve_type), [])
            self.assertEqual(prime_numbers(1, sieve_type), [])
            self.assertEqual(prime_numbers(-1, sieve_type), [])
            self.assertEqual(prime_numbers(-2, sieve_type), [])
            self.assertEqual(prime_numbers(-231, sieve_type), [])

    def testPrimes(self):
        for sieve_type in Sieve:
            self._testPrimes(3342, sieve_type)
            self._testPrimes(5232, sieve_type)
            self._testPrimes(92313, sieve_type)
            self._testPrimes(2213, sieve_type)
            self._testPrimes(4121, sieve_type)

    def _testPrimes(self, limit, sieve_type):
        primes = prime_numbers(limit, sieve_type)
        self.assertEqual(primes, [n for n in itertools.islice(prime_numbers_fast(), len(primes))])


def main():
    if len(argv) < 2:
        unittest.main()
        return

    if len(argv) >= 3:
        try:
            sieve_type = get_sieve_type(argv[2])
        except WrongSieveTypeException as e:
            print(str(e))
            return
    else:
        sieve_type = Sieve.LIST

    try:
        limit = int(argv[1])
        print(prime_numbers(limit, sieve_type))
    except ValueError:
        print("Integer number expected as limit")


if __name__ == "__main__":
    main()
