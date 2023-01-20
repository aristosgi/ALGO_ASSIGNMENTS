import sys

if("-f" in sys.argv):
    f1 = (sys.argv[len(sys.argv)-2])
    f2 = (sys.argv[len(sys.argv)-1])
    with(open(f1, 'r') as f1):
        a = f1.readlines()
    with(open(f2, 'r')as f2):
        b = f2.readlines()
else:
    a = (sys.argv[len(sys.argv)-2])
    b = (sys.argv[len(sys.argv)-1])

A = "".join(a)

 
g = int(sys.argv[len(sys.argv)-5])
m = int(sys.argv[len(sys.argv)-4])
d = int(sys.argv[len(sys.argv)-3])


def create_F(seq1, seq2):
    F = (len(seq1)+1)*[[]]
    for num in range(len(F)):
        F[num] = (len(seq2)+1) * [0]
    for i in range(len(F)):
        for j in range(len(F[i])):
            if(i == j == 0):
                F[i][j] = 0
            elif(i == 0):
                F[i][j] = j * g
            elif(j == 0):
                F[i][j] = i * g
            else:
                possible = []
                possible.append(F[i-1][j] + g)
                possible.append(F[i][j-1] + g)
                if(seq1[i-1] == seq2[j-1]):
                    possible.append(F[i-1][j-1] + m)
                else:
                    possible.append(F[i-1][j-1] + d)
                F[i][j] = max(possible)
    return F


def maximum(list):
    a = max(list)
    ret = []
    for i in range(len(list)):
        if (list[i] == a):
            ret.append(i)
    return ret


def NeedlemanWunsch(A, B):
    WW = []
    ZZ = []
    F = create_F
    EnumerateAlignments(A, B, create_F(A, B), "", "", WW, ZZ)
    return WW, ZZ


def sum_(list1, list2):
    result = []
    for i in range(len(list1)):
        result.append(list1[i] + list2[i])
    return result


def ComputeAlignmentScore(A, B):
    L = []
    for j in range(len(B)+1):
        L.append(j*g)
    for i in range(1, len(A)+1):
        K = L.copy()
        L[0] = i*g
        for j in range(1, len(B)+1):
            if(A[i-1] == B[j-1]):
                last = K[j-1]+m
            else:
                last = K[j-1]+d
            L[j] = max([L[j-1]+g, K[j]+g, last])
    return L


def remove_extra(list1, list2):
    ii = []
    for i in range(1, len(list1)):
        if(list1[i] == list1[i-1] and list2[i] == list2[i-1]):
            ii.append(i)
    c = 0
    for i in ii:
        list1.pop(i - c)
        list2.pop(i - c)
        c = c + 1

    return list1, list2


def UpdateAlignments(WW, ZZ, WWl, WWr, ZZl, ZZr):
    if(len(WWl) == 1 and len(WWr) == 1):
        WW_ = WWl+WWr
        ZZ_ = ZZl+ZZr
        WW.append(''.join(WW_[0:]))
        ZZ.append(''.join(ZZ_[0:]))
    else:
        for l in range(len(WWl)):
            for r in range(len(WWr)):
                templ = []
                tempr = []
                templ.append(WWl[l])
                tempr.append(WWr[r])
                temp = (templ + tempr)
                WW.append(''.join(temp[0:]))
                templ = []
                tempr = []
                templ.append(ZZl[l])
                tempr.append(ZZr[r])
                temp = (templ + tempr)
                temp = (templ + tempr)
                ZZ.append(''.join(temp[0:]))
    WW, ZZ = remove_extra(WW, ZZ)

    return WW, ZZ, [], [], [], []


def print_res(WW, ZZ):
    for i in range(len(WW)):
        print(WW[i])
        print(ZZ[i])
        print(" ")


def EnumerateAlignments(A, B, F, W, Z, WW, ZZ):
    i = len(A)
    j = len(B)
    if(i == 0 and j == 0):
        WW.append(W)
        ZZ.append(Z)
        return
    if(i > 0 and j > 0):
        if(A[i-1] == B[j-1]):
            help = int(F[i-1][j-1] + m)
        else:
            help = int(F[i-1][j-1] + d)
        if(F[i][j] == help):
            EnumerateAlignments(A[0:i-1], B[0:j-1],
                                create_F(A, B), A[i-1]+W, B[j-1]+Z, WW, ZZ)
    if(i > 0 and F[i][j] == F[i-1][j]+g):
        EnumerateAlignments(A[0:i-1], B, create_F(A, B),
                            A[i-1] + W, "-"+Z, WW, ZZ)
    if(j > 0 and F[i][j] == F[i][j-1]+g):
        EnumerateAlignments(A, B[0:j-1], create_F(A, B),
                            "-" + W, B[j-1]+Z, WW, ZZ)


def Hirschberg(A, B):

    if(len(A) == 0):
        WW = list("-"*len(B))
        ZZ = list(B)
    elif(len(B) == 0):
        WW = list(A)
        ZZ = list("-"*len(A))
    elif(len(A) == 1 or len(B) == 1):
        WW, ZZ = NeedlemanWunsch(A, B)
    else:
        i = int(len(A)/2)
        Sl = ComputeAlignmentScore(A[0:i], B)
        Sr = ComputeAlignmentScore(A[i:len(A)][::-1], B[::-1])
        S = sum_(Sl, Sr[::-1])
        J = maximum(S)
        WW = []
        ZZ = []
        for j in J:
            if("-t" in sys.argv):
                print(f"{i}, {j}")
            
            WWl, ZZl = Hirschberg(A[0:i], B[0:j])
            WWr, ZZr = Hirschberg(A[i:len(A)], B[j:len(B)])
            WW, ZZ, WWl, WWr, ZZl, ZZr = UpdateAlignments(
                WW, ZZ, WWl, WWr, ZZl, ZZr)
    return (WW), (ZZ)

WW,ZZ = Hirschberg(a,b)
print_res(WW,ZZ)


