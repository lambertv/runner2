//PE7.cpp
//Program by Valerie Lambert

/*  Project Euler Problem 7- - - -
 *  By listing the first six prime numbers: 2, 3, 5, 7, 11, 13, we can
 *  see that the 6th prime is 13.
 *  What is the 10,001st prime number?
 *  - - - - - - - - - - - - - - - -
 *
 *  I spent forever trying to figure out why my program was printing
 *  the prime prior to the correct answer, then I re-read the question
 *  and realize it was asking for the 10,001st prime, not the 10,000st.
 */

#include<iostream>

bool isPrime(int n)
{
    for (int i = 2; i < n; i++)
    {
        if (n%i == 0) {
            return false;
        }
    }
    return true;
}

int main()
{
    int num = 3;
    int primes_count = 2;
    while (primes_count < 10001)
    {
        num += 2;
        if (isPrime(num))
        {
            primes_count++;
        }
    }
    std::cout << num << std::endl;
    return 0;
}
