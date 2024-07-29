def all_combine(str):
    res = []
    for i in range(len(str)):
        res = res + combine(str,i+1)
    return res
        

def combine(s, n):
    if n < 1:
        return []
    if n == 1:
        return [c for c in s]
    if len(s) < 1:
        return []

    return [s[0] + p for p in combine(s[1:], n-1)] + combine(s[1:], n)

if __name__ == '__main__':
    s = 'abcde'
    print(combine(s, 2))
    print(all_combine(s))
