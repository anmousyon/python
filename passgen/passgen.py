import hashlib


def main():
    key = input('Please enter the site you are generating the password for on the next line:\n')
    process(key)

def process(key):
    s = ''
    password = ''
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '1234567890'
    special = '!@#$%^&*()'
    for x in key[:]:
        s += str(ord(x))
    #hash_res = hashlib.sha256(key).digest()
    print('s:', s)
    s = ''.join(sorted(set(s), key=s.index))
    print('s:', s)
    q = len(s)
    for x in range(4):
        print('x:', x)
        password = password + alphabet[int(s[(3*x)%q])] + numbers[int(s[(3*x + 1)%q])] + special[int(s[(3*x + 2)%q])]
        password = password + key[x].capitalize()
        print(password)
    print(password)
main()