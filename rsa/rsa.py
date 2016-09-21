import math
import random
import sympy

def mod_mul_inv(a, n):
    t = 0
    nt = 1
    r = n
    nr = a % n

    #if n is negative, get flip its sign
    if n<0:
        n = -n
    if a<0:
        a = n - (-a % n)
    while nr != 0:
        quot = r // nr
        print('quot', quot)
        tmp = nt
        nt = t - quot*nt
        t = tmp
        tmp = nr
        nr = r - quot*nr
        r = tmp
    if r > 1:
        return -1
    if t < 0:
        t += n
    return t

def rand_prime(min_, max_):
    '''get a random prime between two numbers'''
    p = math.floor(random.random() * ((max_ - 1) - min_ + 1)) + min_
    if sympy.isprime(p):
        print(p, 'is prime')
        return p
    else:
        print(p, 'is not prime')
        return rand_prime(min_, max_)

def gen():
    '''generate public and private key values'''
    #get two 8 bit prime numbers
    p = rand_prime(1, 255)
    q = rand_prime(1, 255)

    #multiply the primes together
    n = p * q

    #get totient
    t = (p-1) * (q-1)

    #get a random prime less than totient
    e = rand_prime(1,t)

    #???
    d = mod_mul_inv(e, t)
    #n = public key (part 1)
    #e = public key (part 2)
    #d = private key
    return {'n': n, 'e': e, 'd': d}

def encrypt(m, n, e):
    '''encrypt an integer'''
    print('e:', e)
    print('n:', n)
    rt = pow(m, e) % n
    return rt

def decrypt(mEnc, d, n):
    '''decrypt an integer'''
    print('d:', d)
    print('n:', n)
    rt = pow(mEnc, d) % n
    return rt

def main():
    message = int(input('Enter number to encrypt: '))
    keys = gen()
    encrypted = encrypt(message, keys['n'], keys['e'])
    print('encrypted:', encrypted)
    decrypted = decrypt(encrypted, keys['d'], keys['n'])
    print('decrypted:', decrypted)

main()