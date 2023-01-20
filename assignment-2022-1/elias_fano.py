import hashlib
import math
import sys


def get_list(file=sys.argv[1]):
    with open(file) as f:
        a = (f.readlines())
        for i in a:
            if(i != " "):
                table.append(int(i))

def find_start(table):
    extra = 0
    m = max(table)
    l = int(math.log(m/len(table), 2))
    u = math.log(max(table), 2) - l
    lengthU = math.ceil((len(table)+math.floor(max(table)/math.pow(2,l)))/8)
    if(u % 1 > 0):
        u = int(u+1)
    lengthL = int(math.log(max(table)/len(table), 2)) * len(table)
    help = lengthL
    if(lengthL % 8 == 0):
        lengthL = int(lengthL/8)
    else:
        lengthL = int(lengthL/8 + 1)
        extra = lengthL*8 - help
    return l, u, lengthL, extra, lengthU


def getlastxbits(num, x):
    number = num << (8-x)
    number = number & 255
    number = number >> (8-x)
    return number


def binary(num):
    return bin(num)[2:].zfill(8)


def print_L():
    for i in L:
        print(binary(i))             

def print_U():
    for i in U:
        print(binary(i))

def create_L():
    position = 0
    counter = 0
    for number in table:
        res = 0
        bits = getlastxbits(number, l)

        counter = counter + l
        if(counter <= 8):
            res = L[position] << l | bits
            L[position] = res
        else:
            l1 = counter - 8 #get number remaining bits for next byte
            l2 = l - l1 #get number of bits to complete this byte
            bits1 = getlastxbits(bits, l1) #get bits for next byte
            bits2 = bits >> l1 #get bits for this bytearray
            res = L[position] << l2 | bits2
            L[position] = res
            position = position + 1
            res = L[position] << l1 | bits1
            L[position] = res
            counter = l1
         
    if(extra > 0):
        L[position] = L[position] << extra


def create_U():
    counter = 0
    position = 0
    previous = 0
    c = 0
    changed = 0
    for i in range(len(table)):
        if(c != 0):
            previous = (table[i-1] >> l)
        number = table[i] >> l
        diff = number - previous
        c = c + 1
        counter = counter + diff + 1

        if(counter <= 8):
            U[position] = U[position] << diff + 1 | 1
            changed = changed + diff + 1

            if(counter == 8):
                position = position + 1
                counter = 0
                changed = 0
        else:
            new = counter - 8
            U[position] = U[position] << 8 - changed
            position = position + 1
            U[position] = U[position] << new | 1
            counter = new
            changed = new

    U[position] = U[position] << 8 - counter

table = []
get_list()
l, u, lengthL, extra, lengthU = find_start(table)
L = bytearray(lengthL)
U = bytearray(lengthU)

create_L()
create_U()

m = hashlib.sha256()
m.update(L)
m.update(U)
digest = m.hexdigest()

print("l" , l)
print("L")
print_L()
print("U")
print_U()
print(digest)
