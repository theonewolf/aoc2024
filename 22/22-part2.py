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
def sliding_subsequences(sequence, total, subsequences=dict()):
    for i in range(len(sequence)):
        if(len(sequence[i:i+4]) != 4): continue
        if tuple(sequence[i:i+4]) not in subsequences:
            subsequences[tuple(sequence[i:i+4])] = [[] for _ in range(total)]
    return subsequences

def best_price(seqid, subsequences, sequence, subsequence, prices):
    max_price = 0

    for location in subsequences[subsequence][seqid]:
        if prices[location+4] > max_price:
            max_price = prices[location+4]

    return max_price

def index(sequences, subsequences):
    for subseq in subsequences:
        for seqid, seq in enumerate(sequences):
            for i in range(len(seq)):
                if(len(seq[i:i+4]) != 4): continue
                subsequences[tuple(seq[i:i+4])][seqid].append(i)

def search(prices, diffs):
    max_price = float('-inf')
    best_subsequence = []

    subsequences = dict()

    for seq in diffs:
        sliding_subsequences(seq, len(diffs), subsequences)

    index(diffs, subsequences)

    for subseq in subsequences:
        max_prices = []
        for seqid, (seq, pricelist) in enumerate(zip(diffs, prices)):
            max_prices.append(best_price(seqid, subsequences, seq, subseq, pricelist))
        if sum(max_prices) > max_price:
            best_subsequence = subseq
            max_price = sum(max_prices)

    return max_price, best_subsequence

if __name__ == '__main__':
    with open('input') as fd:
        secret_numbers = [int(line) for line in fd]
        prices = []
        diffs = []
        print(secret_numbers)

        for secret in secret_numbers:
            secret_log = [secret]

            for _ in range(1999):
                secret_log.append(compute_secret_hash(secret, 1))
                secret = secret_log[-1]

            prices.append([get_price(secret) for secret in secret_log])
            diffs.append([b - a for a,b in zip(prices[-1], prices[-1][1:])])

        max_price, best_subsequence = search(prices, diffs)

        print(f'max_price = {max_price} and best_subsequence = {best_subsequence}')
