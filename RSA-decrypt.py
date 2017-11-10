#!/usr/bin/python3

from argparse import ArgumentParser


def main():
    args = create_parser().parse_args()
    N = args.N[0]
    d = args.d[0]
    m = args.message[0]

    print(mod_pow(m, d, N))


def create_parser():
    parser = ArgumentParser(description="Decrypt an RSA message with a given private key")
    parser.add_argument("N", type=int, nargs=1, help="N")
    parser.add_argument("d", type=int, nargs=1, help="d")
    parser.add_argument("message", type=int, nargs=1, help="the encrypted message to decrypt")
    return parser


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


if __name__ == "__main__":
    main()
