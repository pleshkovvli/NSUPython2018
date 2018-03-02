import unittest
from math import sqrt, floor


def max_possible_divider(number):
    return int(floor(sqrt(abs(number))))


def is_prime(number):
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    for i in range(3, max_possible_divider(number) + 1, 2):
        if number % i == 0:
            return False
    return True


def prime_numbers_pure():
    yield 2
    current = 3
    while True:
        if is_prime(current):
            yield current
        current += 2


def prime_numbers_fast():
    yield 2
    yield 3
    primes = [2, 3]
    while True:
        yield _next_prime(primes)


def _next_prime(primes):
    current = primes[-1] + 2
    max_divider = max_possible_divider(current)
    while True:
        for prime in primes:
            if prime > max_divider:
                max_divider = max_possible_divider(current)
                if prime > max_divider:
                    primes.append(current)
                    return current
            if current % prime == 0:
                current += 2
                break
        else:
            primes.append(current)
            return current


class TestPrimes(unittest.TestCase):
    def testPrimes(self):
        test_limit = 200000

        for n in prime_numbers_pure():
            self.assertTrue(is_prime(n))
            if n > test_limit:
                break

        for n in prime_numbers_fast():
            self.assertTrue(is_prime(n))
            if n > test_limit:
                break

        for p, f in zip(prime_numbers_pure(), prime_numbers_fast()):
            self.assertEqual(p, f)
            if p > test_limit:
                break


if __name__ == "__main__":
    unittest.main()
