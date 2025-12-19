from sympy import isprime, binomial, product
import numpy as np
import math

def task1():
    num = 871000
    tg = 1
    sum_odd_squres = 0

    while tg <= 871000: #1000:
        if (tg*tg) % 2 != 0:
                sum_odd_squres += tg*tg
            # print(sum_odd_squres)
        tg += 1
    
    print(sum_odd_squres)


def problem1(): 
    multiple = 0
    m_list = []
    the_num = 1000
    for i in range(1,1 + the_num//3):        
        if i*3 < the_num:                
                multiple += i*3
                m_list.append(i*3)
             #   print(i*3)
    for j in range(1,1 + the_num//5):
        if j*5 < the_num:
                multiple += j*5
                m_list.append(j*5)
              #  print(j*5)
                
    unique_list = list(dict.fromkeys(m_list))

    print(sum(m_list), sum(unique_list))

   # print(multiple)


def problem2():

    f = []
    f.append(1)
    f.append(2)
    
    for n in range(2, 100):
        f.append(f[n-1] + f[n-2])
        if f[n] > 4000000:
            break
     
    sum = 0
    for num in f:
        if num % 2 == 0:
            sum += num

    print(sum)

def B_func(n : int):    
    #arr = np.asarray(values)
    result = 1

    for k in range(0, n+1):
        binom = binomial(n, k)        
        result *= binom
    return result

def prime_factorization(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def sigma(n):
    factors = prime_factorization(n)
    result = 1
    for p, a in factors.items():
        result *= (p**(a + 1) - 1) // (p - 1)
    return result

def sum_of_squares(n):
    total = 0
    for i in range(1, n+1):
        total += i*i
    return total

def square_of_sum(n):
    total = 0
    for i in range(1, n+1):
        total += i
    return total * total

def problem650():
    # binominal(n,k)
    # B(n) = product()
    print(B_func(5))
    tot = 0
    for i in range(1,101):

        #
        tot += sigma(B_func(i)) % 1_000_000_007
    
    print(tot)

def problem6():
    
    print(square_of_sum(100)-sum_of_squares(100))
    return 0

def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)

    # 0 and 1 are not prime
    if limit >= 0:
        is_prime[0] = False
    if limit >= 1:
        is_prime[1] = False

    for number in range(2, int(limit ** 0.5) + 1):
        if is_prime[number]:
            for multiple in range(number * number, limit + 1, number):
                is_prime[multiple] = False

    return [num for num, prime in enumerate(is_prime) if prime]


def nth_prime(n):
    if n < 1:
        return None

    if n == 1:
        return 2

    # Better upper bound for nth prime
    limit = int(n * (math.log(n) + math.log(math.log(n)))) + 3

    primes = sieve_of_eratosthenes(limit)
    return primes[n - 1]


#print(nth_prime(10)) 


def problem7():
    print(nth_prime(10001))




def problem8():
    raw = """73167176531330624919225119674426574742355349194934
        96983520312774506326239578318016984801869478851843
        85861560789112949495459501737958331952853208805511
        12540698747158523863050715693290963295227443043557
        66896648950445244523161731856403098711121722383113
        62229893423380308135336276614282806444486645238749
        30358907296290491560440772390713810515859307960866
        70172427121883998797908792274921901699720888093776
        65727333001053367881220235421809751254540594752243
        52584907711670556013604839586446706324415722155397
        53697817977846174064955149290862569321978468622482
        83972241375657056057490261407972968652414535100474
        82166370484403199890008895243450658541227588666881
        16427171479924442928230863465674813919123162824586
        17866458359124566529476545682848912883142607690042
        24219022671055626321111109370544217506941658960408
        07198403850962455444362981230987879927244284909188
        84580156166097919133875499200524063689912560717606
        05886116467109405077541002256983155200055935729725
        71636269561882670428252483600823257530420752963450"""

    digits = [int(c) for c in raw if c.isdigit()]

    maxval = 0

    for i in range(len(digits) - 13):
        tmpsum = 1
        for j in range(13):
            tmpsum*= digits[i+j]
        if tmpsum > maxval:
            maxval = tmpsum

    print(maxval)


problem8()

