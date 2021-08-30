def qsort(s,left,right):
    if left >= right:
        return s
    l = left
    r = right
    k = s[l]

    flag = True # True means minus r 
    while l < r:
        if flag:
            if s[r] < k:
                s[l] = s[r]
                flag = False
            else:
                r -= 1
        else:
            if s[l] > k:
                s[r] = s[l]
                flag = True
            else:
                l += 1
    m = r            
    if flag:
        m = l
    s[m] = k
    qsort(s, left, m-1)
    qsort(s, m+1, right)
    return s





    return
if __name__ == '__main__':
    s = list('abezjklabkadkbeoaopywq')

    print(s)
    print(qsort(s,0,len(s)-1))
    print(s)

