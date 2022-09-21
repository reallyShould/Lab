def maxOfList(x):
    tmp = 0
    for i in x:
        if i > tmp:
            tmp = i
    return tmp

def mediana(l):
    if len(l) % 2 == 0:
        a = int(len(l) / 2)
        b = a - 1
        return (l[a] + l[b]) / 2