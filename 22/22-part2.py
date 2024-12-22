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

# You're going to need as many bananas as possible, so you'll need to determine
# which sequence of four price changes will cause the monkey to get you the
# most bananas overall. Each buyer is going to generate 2000 secret numbers
# after their initial secret number, so, for each buyer, you'll have 2000 price
# changes in which your sequence can occur.

# If we have a dict, we can compute price as we go through all sequences...
# We don't need a multipass algorithm; track all prices, then pick the max
def sliding_subsequences(sequence, prices, subsequences=dict()):
    seen = set()
    for i in range(len(sequence)):
        subseq = None
        try:
            subseq = tuple(sequence[i:i+4])
        except:
            continue

        price = None
        try:
            price = prices[i+3]
        except:
            continue

        if subseq in seen: continue

        if subseq not in subsequences:
            subsequences[subseq] = price
            seen.add(subseq)
        else:
            subsequences[subseq] += price
            seen.add(subseq)

def search(prices, diffs):
    subsequences = dict()

    for price, seq in zip(prices, diffs):
        sliding_subsequences(seq, price, subsequences)

    max_price = max(subsequences.values())
    best_subsequences = [key for key, value in subsequences.items() if value == max_price]

    return max_price, best_subsequences

if __name__ == '__main__':
    with open('input') as fd:
        secret_numbers = [int(line) for line in fd]
        prices = []
        diffs = []

        for secret in secret_numbers:
            secret_log = [secret]

            for _ in range(2000):
                secret_log.append(compute_secret_hash(secret, 1))
                secret = secret_log[-1]

            prices.append([get_price(secret) for secret in secret_log])
            diffs.append([None] + [b - a for a,b in zip(prices[-1], prices[-1][1:])])

        max_price, best_subsequence = search(prices, diffs)

        print(f'max_price = {max_price} and best_subsequence = {best_subsequence}')
