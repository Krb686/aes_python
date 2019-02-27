# multiply a and b in GF(2^8)
def gfmult(a, b):
    d = 0
    # break b into binary
    # for each digit of 1, get log2 of that digit
    # call xmult that many times and add intermediate products
    bit_array = [(b >> bit) & 1 for bit in range(7, -1, -1)]
    for pos, bit in enumerate(bit_array):
        if bit == 1:
            c = xmult(a, 8-pos-1)
            d = d ^ c
    return d


# find the multiplicative inverse of 'a' in GF(2^8)
def gfinverse(a):
    if a == 0:
        return 0

    i = 0
    b = a
    while True:
        c = gfmult(a, b)
        i = i + 1
        if c == 1:
            break
        b = c
    return b

def gf_col_add(a, b):
    if not isinstance(a, list) or not isinstance(b, list):
        return -1
    if len(a) != len(b):
        return -1

    c = [0] * len(a)
    for i in range(len(a)):
        c[i] = a[i] ^ b[i]
    return c


def gf_matrix_mult(a, b):
    c = [0] * 8
    for i in range(len(a)):
        tmp = 0
        for j in range(len(a[i])):
            tmp = tmp ^ (a[i][j] * b[j])
        c[i] = tmp
    return c

# multiply number 'a' by x 'b' times
def xmult(a, b):
    c = a
    for i in range(b):
        c = c << 1
        if c > 255:
            c = (c ^ 0x1B) & 0xFF
    return c
