#!/usr/bin/python3

from random import SystemRandom
from argparse import ArgumentParser
from time import time


def main():
    args = create_parser().parse_args()
    bits = args.bits[0]

    public_key, private_key = generate_keypair(bits)
    print(public_key, private_key)


def create_parser():
    parser = ArgumentParser(description="Generate an RSA keypair of a defined size")
    parser.add_argument("bits", type=int, nargs=1, help="key bit length")
    return parser


def generate_keypair(bits):
    e = 65537

    while True:
        print("Generating p...", end="", flush=True)
        start_t = time()
        p = generate_random_prime(bits)
        elapsed = time() - start_t
        print(" -> {} generated in {}ms".format(p, elapsed * 1000))

        print("Generating q...", end="", flush=True)
        start_t = time()
        q = generate_random_prime(bits)
        elapsed = time() - start_t
        print(" -> {} generated in {}ms".format(q, elapsed * 1000))

        l = lcm(p - 1, q - 1)

        if gcd(e, l) == 1 and abs(p - q) >> (bits // 2) != 0:
            break

    N = p * q
    d = mod_inv(e, l)
    return {'N': N, 'e': e}, {'N': N, 'd': d}


def generate_random_prime(bits):
    min = 1 << (bits - 1)
    max = (1 << bits) - 1
    rng = SystemRandom()
    checked = []

    while True:
        while True:
            p = rng.randint(min, max)

            if p not in checked:
                break

        if test_primality(p):
            return p


def test_primality(num, iterations=5):
    rng = SystemRandom()
    max = num - 2
    for i in range(iterations):
        a = rng.randint(2, max)
        if mod_pow(num, a - 1, a) != 1:
            return False

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


def mod_pow(num, exp, mod):
    base = num
    result = 1

    while exp > 0:
        if exp & 1:
            quot, rem = divmod(result * base, mod)
            result = rem
        exp >>= 1
        quot, rem = divmod(pow(base, 2), mod)
        base = rem

    return result


def mod_inv(num, mod):
    t = 0
    new_t = 1
    r = mod
    new_r = num

    while new_r != 0:
        q = r // new_r

        last_t = t
        last_r = r
        t = new_t
        r = new_r

        new_t = last_t - (q * new_t)
        new_r = last_r - (q * new_r)

    if r != 1:
        raise ValueError()

    if t < 0:
        t += mod

    if num < 0:
        return -t

    return t


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return (a // gcd(a, b)) * b


if __name__ == "__main__":
    main()
