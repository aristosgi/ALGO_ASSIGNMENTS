import re
import sys
import math



len = len(sys.argv)
flag = False

if ("-t" in sys.argv):
    flag = True

file_name = sys.argv[len-1]
table_size = sys.argv[len-2]
global g,b
g = sys.argv[len-3]
b = sys.argv[len-4]


with(open(file_name, 'r') as f1):
        a = f1.readlines()

seq = []
table = {}
f = {}


for i in a:
    seq.append(int(i))
    

k = 0
for i in seq:
    k = k + 1

for i in range(k-1):
    f[seq[i]] = seq[i+1]


def SearchTableΥ(table ,y):

    res = []
    for i in table:
        if(table[i] == y):
            res.append(i)


    if(res != []):
        return min(res)
    else:
        return -1

def SearchTableJ(table ,j):
    
    res = []
    for i in table:
        if(i == j):
            res.append(table[i])
    if(res != []):
        return min(res)
    else:
        return -1
        
def InsertInTable(y,i):   
    table[i] = y

def DetectCycle(x , b = int(b) , g = int(g), f=f):

    y = x
    i = 0
    m = 0

    while True:

        if((i%b==0) and (m == int(table_size))):

            b = 2*b
            Purge(table , b)
            m = math.ceil(m/2)

        if(i%b==0):
            
            InsertInTable(y,i)

            m = m + 1

        y = f[y]

        i = i + 1

        if((i%(g*b))<b):

            j = SearchTableΥ(table , y)
            
            if(j!=-1):
                
                return y,i,j,b

def Calculator(k ,c, b=int(b) ):

    value = b*math.floor(k/b)

    k_ = SearchTableJ(table , value)

    res = k_

    rep = k%b

    if(res == -1):
        res = seq[0]
        rep = k

    for fe in range(rep):
        res = f[res]

    flc = res
    
    for i in range(c):
        flc = f[flc]

    return res , flc


def Purge(table , b):
    
    for p in table:
        if (p % b != 0):
            table.pop(p)
            Purge(table , b)           
            break

(y,i,j,b) = (DetectCycle(seq[0]))


def RecoverCyclePrelim(y,i,j , g=int(g) , b=int(b)):
    
    c = 1
    found_c = False
    y_ = y
    while((c <= (g+1)*b) and found_c==False):
        y_ = f[y_]
        if(y == y_):
            found_c = True
        else:
            c=c+1
    
    if(found_c==False):
        c = i - j

    block_length = b*g

    final_block = block_length * math.floor(i/block_length)

    previous_block = final_block - block_length
    
    i_ = max(c,previous_block)
    
    j_ = i_ - c
    l = j_ + 1
    
    fl , flc= Calculator(l , c)
    
    while((fl != flc)):
        l = l + 1

        fl = f[fl]
        flc = f[flc]
    return l , c

l,c = RecoverCyclePrelim(y,i,j)

print("cycle" , c , "leader" , l)

if(flag):
    printer = (sorted(table.items(), key=lambda item: item[1]))

    for i in printer:
        print(i[1] , i[0])


