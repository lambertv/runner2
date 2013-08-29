#PE6.py
#Program by Valerie Lambert

"""
Project Euler Problem 6- - - -
The sum of the squares of the first ten natural numbers is,
    
    1**2 + 2**2 + ... + 10**2 = 385

The suare of the sum of the first ten natural numbers is,

    (1 + 2 + ... + 10)**2 = 55**2 = 3025

Hence the difference between the sum of the squares of the first one
ten natural numbers and the square of the sum is 3025 - 385 = 2640.
Find the difference between the sum of the squares of the first one
hundred natural numbers as teh square of the sum.
- - - - - - - - - - - - - - - -

Python version.
"""

NUM_OF_NATURAL = 100

def main():
    sum_of_squares = 0
    square_of_sums = 0
    for i in range(NUM_OF_NATURAL):
        sum_of_squares += (i+1)*(i+1)
        square_of_sums += (i+1)
    square_of_sums *= square_of_sums
    print(square_of_sums - sum_of_squares)

main()
