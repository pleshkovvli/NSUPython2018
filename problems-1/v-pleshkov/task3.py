from primes import max_possible_divider
from bitarray import bitarray
from enum import Enum
from time import time
from sys import argv


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


def execution_time(fun):
    start = time()
    value = fun()
    return value, time() - start


def main():
    if len(argv) < 2:
        print(f"Usage: python3 {__file__} LIMIT [TYPE=0,1,2]")
        return

    if len(argv) >=3:
        sieve_type = Sieve(int(argv[2]))
    else:
        sieve_type = Sieve.LIST

    primes, exec_time = execution_time(lambda : prime_numbers(int(argv[1]), sieve_type))
    print(primes)
    print(exec_time)


if __name__ == "__main__":
    main()
