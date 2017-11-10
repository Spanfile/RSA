#!/usr/bin/python3

from random import SystemRandom
from argparse import ArgumentParser


def main():
    args = create_parser().parse_args()
    bits = args.bits[0]
    print("Using {}-bit keys".format(bits))


def create_parser():
    parser = ArgumentParser(description="Generate an RSA keypair of a defined size")
    parser.add_argument("bits", type=int, nargs=1, help="key bit length")
    return parser


def generate_keypair(bits, output):
    pass


def generate_random_prime(bits):
    pass


def test_primality(num, iterations=5):
    pass


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
    pass


def generate_private_key_exponent(bits, e, p1q1):
    pass


if __name__ == "__main__":
    main()
