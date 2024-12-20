#!/usr/bin/env python3

def stripe_search(stripes, towel, depth):
    if len(towel) == 0: return True
    if depth < 0:
        return False

    for stripe in stripes:
        if towel.startswith(stripe):
            if stripe_search(stripes, towel[len(stripe):], depth - 1): return True
        else:
            pass

    return False

# Exploring the problem with ChatGPT
#   - This is referred to as the word break problem
#   - Should use a DP solution as SO said
#   - Reviewing DP with ChatGPT is fun!
def stripe_search2(stripes, towel):
      # Convert stripes to a set for O(1) lookup
      stripes_set = set(stripes)
      
      # Create a DP array initialized to False
      dp = [0] * (len(towel) + 1)
      dp[0] = 1 # Base case: empty string can be formed
      
      # Iterate through the string towel
      for i in range(1, len(towel) + 1):
          for j in range(i):
              # Check if the substring towel[j:i] is in stripes_set and dp[j] is True
              if dp[j] and towel[j:i] in stripes:
                  dp[i] += dp[j]
      
      return dp[len(towel)]

if __name__ == '__main__':
    with open('input') as fd:
        towels = []
        stripes = []

        for line in fd:
            line = line.strip()
            if ',' in line:
                stripes = [l.strip() for l in line.split(',')]
            elif line:
                towels += [line]

        count = 0
        total = 0
        for towel in towels:
            count += stripe_search2(stripes, towel)
            total += 1
            print(f'Checked {total} / {len(towels)}')
        print(count)
