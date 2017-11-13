#!/usr/bin/python3

import json
from argparse import ArgumentParser


def main():
    args = create_parser().parse_args()
    m = args.message[0]

    with open("rsa_public_key", "r") as f:
        public_key = json.load(f)

    print(mod_pow(m, public_key['e'], public_key['N']))


def create_parser():
    parser = ArgumentParser(description="Encrypt an RSA message")
    parser.add_argument("message", type=int, nargs=1, help="the message to encrypt")
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
