


def problem3():
    print("Problem 3")
    num = 600851475143 // 71
    num = num // 839
    num = num // 1471
    num = num // 6857
    print("num =", num)
    for i in range(2, 10000):
        if num % i == 0:
            print(f"Found a prime factor of {i}")

def is_symmetric_6_digit(n):
    s = str(n)
    if len(s) != 6 or not s.isdigit():
        return False
    return s[0] == s[5] and s[1] == s[4] and s[2] == s[3]


def problem4():
    print("Problem 4")
    maxval = 0
    for i in range(999,99,-1):
        for j in range(999,99,-1):
            if is_symmetric_6_digit(i * j):
              #  print(f"Found palindrome product {i} * {j} = {i * j}")
                if i * j > maxval:
                    maxval = i * j
    print(maxval)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def gcd_of_list(numbers):
    g = numbers[0]
    for n in numbers[1:]:
        g = gcd(g, n)
    return g

def comp_div(num : int) -> int:
    num_dif = 0
    #divisible = []
    for i in range(2,21):
        if num % i == 0:
            num_dif += 1
     #       divisible.append(i)

    if num_dif >19:
        print(f"{num_dif} of 20 divisors for {num}")
    return num_dif

def comp_div2(num: int) -> int:
    count = 0
    for i in range(2, 21):
        if num % i != 0:
            return count   # early exit
        count += 1
    return count

CHECK = (11, 12, 13, 14, 15, 16, 17, 18, 19, 20)

def comp_div3(num: int) -> int:
    for d in CHECK:
        if num % d != 0:
            return False
    return True


def problem5():
    #print(f"GCD = ", gcd_of_list([4,6,8,9,10,12,14,15,16,18]))
   # 1,2,3,5,7,11,13,17,19
    #print(comp_div([4,6,8,9,10,12,14,15,16,18]))
    startpt = 232396278
    endpt = startpt + 100_000_000
    total = endpt - startpt

    print_step = 1_000_000  # print every 1M iterations

    for idx, i in enumerate(range(startpt, endpt), start=1):
        if idx % print_step == 0:
            percent = 100 * idx / total
            print(f"\rProgress: {percent:6.2f}%, i = {i}", end='', flush=True)

        if comp_div3(i):
            print("")
            print("")

            print(f"{i} = True")
            break


def prime_factorization(n):
    factors = {}

    # factor out 2
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2

    # factor odd numbers
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 2

    # leftover prime
    if n > 1:
        factors[n] = factors.get(n, 0) + 1

    return factors


def problem9():
    for a in range(1000):
        for b in range(1000):
            c = 1000 - a - b
            if a*a + b*b == c*c and a != 0 and b != 0:
                print(f"a+b+c = {a+b+c} (a={a}, b={b}, c={c})")
                print(a*b*c)


def triangle_number(n):
    return n * (n + 1) // 2


def factorsfunc(n):
    factors = prime_factorization(n)
    dn = 1
    for a, b in factors.items():
  #      print(f"a={a}, b={b}")
        dn *= (1 + b)
  #  print(f"dn = {dn}")
    return dn

def problem12():
    maxfac = 0
    index = 1
    while maxfac < 500:
        i = triangle_number(index)
        dn = factorsfunc(i)
        if dn > maxfac:
            maxfac = dn
            print(f"maxfac = {maxfac}, num = {i}")
        index += 1

def itseq(num):
    if num % 2 == 0:
        return num // 2
    else:
        return num * 3 + 1

def pb14helper(num):
    tmpnum = num
    chainsize = 1
    while tmpnum != 1:
        tmpnum = itseq(tmpnum)
        chainsize += 1
    return chainsize

def problem14():
    maxlen = 0
    for i in range(1,1_000_000):
        a = pb14helper(i)
       # print(a)
        if a > maxlen:
            maxlen = a
            print(f"maxlen = {maxlen} at {i}")


problem14()


