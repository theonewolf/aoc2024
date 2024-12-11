#!/usr/bin/env python3
import time
import math

# Define a large integer for testing
large_int = 1234567890123456789012345678901234567890

# Function to check even digits using logarithm
def has_even_digits_log(n):
    num_digits = math.floor(math.log10(n)) + 1
    return num_digits % 2 == 0

# Function to check even digits using string conversion
def has_even_digits_str(n):
    return len(str(n)) % 2 == 0

# Adjust the number of iterations for benchmarking
iterations = 1000000

# Benchmark: has_even_digits_log
start_time = time.time()
for _ in range(iterations):
    result_log = has_even_digits_log(large_int)
log_time = time.time() - start_time

# Benchmark: has_even_digits_str
start_time = time.time()
for _ in range(iterations):
    result_str = has_even_digits_str(large_int)
str_time = time.time() - start_time

# Print results
print(f"Time for has_even_digits_log: {log_time:.6f} seconds")
print(f"Time for has_even_digits_str: {str_time:.6f} seconds")
