#!/usr/bin/python3

import json
from random import SystemRandom
from argparse import ArgumentParser


def main():
    args = create_parser().parse_args()
    bits = args.bits[0]
    print("Using {}-bit keys".format(bits))

    public_key, private_key = generate_keypair(bits)

    with open("rsa_public_key", "w") as f:
        json.dump(public_key, f)

    with open("rsa_private_key", "w") as f:
        json.dump(private_key, f)

    print("Key files written")


def create_parser():
    parser = ArgumentParser(description="Generate an RSA keypair of a defined size")
    parser.add_argument("bits", type=int, nargs=1, help="key bit length")
    return parser


def generate_keypair(bits):
    e = 65537

    while True:
        print("Generating p...")
        p = generate_random_prime(bits)

        print("Generating q...")
        q = generate_random_prime(bits)

        l = lcm(p - 1, q - 1)

        # if gcd(e, l) == 1 and abs(p - q) >> (bits // 2) != 0:
        if gcd(e, l) == 1:
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


def test_primality(num, iterations=7):
    if num & 1 == 0:
        return False

    rng = SystemRandom()
    max = num - 2
    for i in range(iterations):
        a = rng.randint(2, max)
        if mod_pow(a, num - 1, num) != 1:
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
    result = 1

    while exp:
        if exp & 1:
            result = result * num % mod
        exp >>= 1
        num = num * num % mod

    return result


def mod_inv(num, mod):
    t = 0
    new_t = 1
    r = mod
    new_r = abs(num)

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
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    a = abs(a)
    b = abs(b)
    return (a // gcd(a, b)) * b


if __name__ == "__main__":
    main()
