#!/usr/bin/python3

import json
from argparse import ArgumentParser


def main():
    args = create_parser().parse_args()
    m = args.message[0]

    with open("rsa_private_key", "r") as f:
        private_key = json.load(f)

    print(mod_pow(m, private_key['d'], private_key['N']))


def create_parser():
    parser = ArgumentParser(description="Decrypt an RSA message")
    parser.add_argument("message", type=int, nargs=1, help="the encrypted message to decrypt")
    return parser


def mod_pow(num, exp, mod):
    result = 1

    while exp:
        if exp & 1:
            result = result * num % mod
        exp >>= 1
        num = num * num % mod

    return result


if __name__ == "__main__":
    main()
