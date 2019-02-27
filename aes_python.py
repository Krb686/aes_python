#def SubBytes():

#def ShiftRows():

#def MixColumns():

#def AddRoundKey():

import gfmath

def int2list(a):
    return [int(x) for x in reversed(bin(a)[2:])]

def list2int(a):
    sum = 0
    for i in range(len(a)):
        sum = sum + a[i]*2**i
    return sum

# the core sbox/isbox transformation that is common to
# both forward and inverse computation
def aes_sbox_core_transform(a, const_matrix, const_col):
    if isinstance(a, int):
        a = int2list(a)
    if len(a) > 8:
        return -1
    if len(a) < 8:
        for i in range(8-len(a)):
            a.append(0)

    b = gfmath.gf_matrix_mult(const_matrix, a)
    c = gfmath.gf_col_add(b, const_col)
    return list2int(c)

# the forward sbox transformation
def aes_sbox_transform(a):
    const_matrix = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1]
    ]

    const_col = [1, 1, 0, 0, 0, 1, 1, 0]

    return aes_sbox_core_transform(a, const_matrix, const_col)

# the inverse sbox transformation
def aes_isbox_transform(a):
    const_matrix = [
        [0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0]
    ]

    const_col = [1, 0, 1, 0, 0, 0, 0, 0]

    return aes_sbox_core_transform(a, const_matrix, const_col)

def aes_sbox(a):
    return aes_sbox_transform(gfmath.gfinverse(a))

def aes_isbox(a):
    return gfinverse(aes_isbox_transform(a))


def aes_key_expansion(key):
    # ensure the input is a string
    if not isinstance(key, str):
        return -1
    # ensure the input is 32 characters long
    if len(key) != 32:
        return -1
    # ensure all characters are hexadecimal
    try:
        i = int(key, 16)
    except ValueError:
        return -1

    # convert input string to 4x4 byte array
    key_array = [
        # rows here are columns in AES diagrams
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    expanded_key = [[[0 for k in range(4)] for j in range(4)] for i in range(11)]

    # convert input key string to key array
    for i in range(4):
        for j in range(4):
            c1 = 2*(4*i+j)
            byte_str = key[c1:c1+2]
            key_array[i][j] = int(byte_str, 16)

    expanded_key[0] = key_array

    rconj = 0
    for i in range(len(expanded_key)):
        word_plane = expanded_key[i]
        for j in range(len(word_plane)):
            # the 1st 4 words are direct copy from the input key, so skip them
            if i > 0:
                if j == 0:
                    prev_word1 = expanded_key[i-1][3]
                    g_out, rconj = g_function(prev_word1, rconj)
                    prev_word4 = expanded_key[i-1][j]
                    expanded_key[i][j][0] = g_out[0] ^ prev_word4[0]
                    expanded_key[i][j][1] = g_out[1] ^ prev_word4[1]
                    expanded_key[i][j][2] = g_out[2] ^ prev_word4[2]
                    expanded_key[i][j][3] = g_out[3] ^ prev_word4[3]
                else:
                    # simple
                    prev_word4 = expanded_key[i - 1][j]
                    prev_word1 = expanded_key[i][j - 1]
                    expanded_key[i][j][0] = prev_word4[0] ^ prev_word1[0]
                    expanded_key[i][j][1] = prev_word4[1] ^ prev_word1[1]
                    expanded_key[i][j][2] = prev_word4[2] ^ prev_word1[2]
                    expanded_key[i][j][3] = prev_word4[3] ^ prev_word1[3]

    for i in range(len(expanded_key)):
        word_plane = expanded_key[i]
        for j in range(len(word_plane)):
            word = word_plane[j]
            print(word)


def g_function(a, rconj):


    # 1) RotWord
    b = [a[1], a[2], a[3], a[0]]

    # 2) SubWord
    b[0] = aes_sbox(b[0])

    b[1] = aes_sbox(b[1])
    b[2] = aes_sbox(b[2])
    b[3] = aes_sbox(b[3])


    # 3) xor with rconj
    if rconj == 0:
        rconj = 1
    else:
        rconj = gfmult(rconj, 2)
    b[0] = b[0] ^ rconj

    return b, rconj

#print(aes_key_expansion("00000000000000000000000000000000"))
#print(aes_sbox(0x31))
#print(aes_isbox(0x31))

def generate_t_tables():

    t0a = []
    t1a = []
    t2a = []
    t3a = []

    for i in range(1, 3):
        sbox_val1 = aes_sbox(i)
        sbox_val2 = gfmath.gfmult(2, sbox_val1)
        sbox_val3 = gfmath.gfmult(3, sbox_val1)
        t0 = [sbox_val2, sbox_val1, sbox_val1, sbox_val3]
        t1 = [sbox_val3, sbox_val2, sbox_val1, sbox_val1]
        t2 = [sbox_val1, sbox_val3, sbox_val2, sbox_val1]
        t3 = [sbox_val1, sbox_val1, sbox_val3, sbox_val2]

        t0a.append(t0)
        t1a.append(t1)
        t2a.append(t2)
        t3a.append(t3)
    return t0a, t1a, t2a, t3a


t0a, t1a, t2a, t3a = generate_t_tables()
#print(t0a)
#print(t1a)
#print(t2a)
#print(t3a)

# 3x = 2x+x
# a = value to multiply
# b7
#   - a7a6 = 01 (64 to 127)
#   - a7a6 = 10 (128 to 191)
# b6
#   - a6a5 = 01 (32 to 63)
#   - a6a5 = 10 (64 to 95

# for b4, it gets more complicated because of XOR with 1b
# bits that affect b4
#   - b7
#   - b4
#   - b3
# when b7 = 0, same as b7, b6, or b5
#   - b4b3 = 01
#   - b4b3 = 10
# when b7 = 1
#   - b4b3 = 00
#   - b4b3 = 11
# in summary
#   - b7b4b3 = 001
#   -        = 010
#   -        = 100
#   -        = 111

y = 96
print(format(y, '08b'))
z = gfmath.gfmult(y, 3)
print(format(z, '08b'))


