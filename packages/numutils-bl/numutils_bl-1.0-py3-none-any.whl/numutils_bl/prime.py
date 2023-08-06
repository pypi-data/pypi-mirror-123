"""
calculates prime number in range
"""


def prime(n):
    for i in range(2, n):
        is_prime = True
        for j in range(2, i):
            if i % j == 0:
                is_prime = False
        if is_prime:
            print(f"{i} es primo")
