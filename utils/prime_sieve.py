"""Prime generation and primality helpers based on a sieve."""
import logging

LOG = logging.getLogger(__name__)


def sieve(limit):
    """Return every prime not exceeding limit using the sieve of Eratosthenes."""
    if limit < 2:
        return []
    flags = [True] * (limit + 1)
    flags[0] = flags[1] = False
    for prime in range(2, int(limit ** 0.5) + 1):
        if flags[prime]:
            for multiple in range(prime * prime, limit + 1, prime):
                flags[multiple] = False
    return [index for index, flag in enumerate(flags) if flag]


def is_prime(value):
    """Return whether value is prime using trial division."""
    number = int(value)
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def primes_below(limit):
    """Return the prime count and the largest prime strictly below limit."""
    found = sieve(limit - 1)
    return len(found), (found[-1] if found else 0)


__all__ = ['sieve', 'is_prime', 'primes_below']
