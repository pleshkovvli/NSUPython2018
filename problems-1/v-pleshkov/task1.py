import unittest

from primes import max_possible_divider, prime_numbers_fast
from sys import argv


def prime_multipliers(number, primes=None):
    if number < 0:
        number = abs(number)
        yield [-1, 1]

    if primes is None:
        primes = prime_numbers_fast()

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
    if numerator == 0:
        return 0

    count = 0
    while numerator % divisor == 0:
        numerator //= divisor
        count += 1
    return count


class TestPrimes(unittest.TestCase):
    def testSimpleCases(self):
        self.assertEqual(list(prime_multipliers(0)), [])
        self.assertEqual(list(prime_multipliers(1)), [])
        self.assertEqual(list(prime_multipliers(2)), [[2, 1]])
        self.assertEqual(list(prime_multipliers(3)), [[3, 1]])

    def testPrimes(self):
        self.assertEqual(list(prime_multipliers(7)), [[7, 1]])
        self.assertEqual(list(prime_multipliers(37)), [[37, 1]])
        self.assertEqual(list(prime_multipliers(101)), [[101, 1]])
        self.assertEqual(list(prime_multipliers(231109)), [[231109, 1]])

    def testCompositeNumbers(self):
        self.assertEqual(list(prime_multipliers(2323)), [[23, 1], [101, 1]])
        self.assertEqual(list(prime_multipliers(27)), [[3, 3]])
        self.assertEqual(list(prime_multipliers(66)), [[2, 1], [3, 1], [11, 1]])
        self.assertEqual(list(prime_multipliers(32334)), [[2, 1], [3, 1], [17, 1], [317, 1]])

    def testNegative(self):
        self.assertEqual(list(prime_multipliers(-2323)), [[-1, 1], [23, 1], [101, 1]])
        self.assertEqual(list(prime_multipliers(-1)), [[-1, 1]])
        self.assertEqual(list(prime_multipliers(-2)), [[-1, 1], [2, 1]])
        self.assertEqual(list(prime_multipliers(-37)), [[-1, 1], [37, 1]])


def main():
    if len(argv) < 2:
        unittest.main()
        return

    try:
        number = int(argv[1])
        print([n for n in prime_multipliers(number)])
    except ValueError:
        print("Integer number expected as argument")


if __name__ == "__main__":
    main()
