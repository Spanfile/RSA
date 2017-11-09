#!/usr/bin/python3

from random import SystemRandom
from argparse import ArgumentParser


def main():
    args = create_parser().parse_args()
    bits = args.bits[0]
    print("Using {}-bit keys".format(bits))

    print("Generating two primes: p and q")
    p = generate_random_prime(bits)
    q = generate_random_prime(bits)
    N = p * q
    p1q1 = (p - 1) * (q - 1)
    print("p: {}, q: {}, N: {}, (p-1)(q-1): {}".format(p, q, N, p1q1))

    print("Generating public-key exponent e")
    e = generate_public_key_exponent(N, p1q1)
    print("e: {}".format(e))

    print("Generating private-key exponent d")
    d = generate_private_key_exponent(bits, e, p1q1)
    print("d: {}".format(d))

    print("Public key: \{N: {}, e: {}\}".format(N, e))
    print("Private key: \{N: {}, d: {}\}".format(N, d))


def create_parser():
    parser = ArgumentParser(description="Generate an RSA keypair of a defined size")
    parser.add_argument("bits", type=int, nargs=1, help="key bit length")
    return parser


def shuffle_range(rng, min, max):
    l = list(range(min, max))
    rng.shuffle(l)
    return l


def generate_random_prime(bits):
    min = 4
    max = (1 << bits) - 1
    rng = SystemRandom()

    for p in shuffle_range(rng, min, max):
        if test_primality(p):
            return p


def test_primality(num, iterations=5):
    rng = SystemRandom()
    checked = []
    # print("Testing if {} is prime with {} iterations".format(num, iterations))
    for i in range(0, iterations):
        while True:
            a = rng.randint(2, num - 2)
            if a not in checked:
                break

        a_pow = pow(a, num - 2)
        quot, rem = divmod(a_pow, num)
        # print("-> a: {}, a**n-1 mod n: {}".format(a, a_modpow))
        if not rem == 1:
            return False

        print("+", end="", flush=True)

    print("*")
    return True


def pow(num, exp):
    base = num
    result = 1

    while exp > 0:
        if exp & 1:
            result *= base
        exp >>= 1
        base *= base
        # print("result: {}, exp: {}, base: {}".format(result, exp, base))

    return result


def generate_public_key_exponent(N, p1q1):
    rng = SystemRandom()

    for e in shuffle_range(rng, 1, N):
        if gcd(e, p1q1) == 1:
            return e


def generate_private_key_exponent(bits, e, p1q1):
    max = (1 << bits) - 1
    checked = []
    rng = SystemRandom()

    while True:
        while True:
            d = rng.randint(1, max)

            if d not in checked:
                break

        checked.append(d)
        quot, rem = divmod((d * e) - 1, p1q1)
        if rem == 0:
            return d


def gcd(a, b):
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a

    return a


if __name__ == "__main__":
    main()
