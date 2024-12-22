#!/usr/bin/env python3

from math import floor

def compute_secret_hash(secret, iterations):
    for _ in range(iterations):
        result = secret * 64
        secret ^= result
        secret %= 16777216

        result = secret / 32
        result = floor(result)
        secret ^= result
        secret %= 16777216

        result = secret * 2048
        secret ^= result
        secret %= 16777216

    return secret

def get_price(secret):
    return secret % 10

if __name__ == '__main__':
    with open('test_input') as fd:
        secret_numbers = [int(line) for line in fd]
        print(secret_numbers)

        secret_numbers = [compute_secret_hash(secret, 2000) for secret in secret_numbers]
        prices = [get_price(secret) for secret in secret_numbers]

        print(prices)
        print(prices[1:])
        print([a - b for a,b in zip(prices, prices[1:])])
        print(sum(secret_numbers))
