import datetime

def generatePerms(elms, m):
    if not elms:
        # return ['']
        yield ''
        return
    for perm in generatePerms(elms[1:]):
        for i in range(len(perm)):
            yield perm[0:i] + elms[0] + perm[i:]
        yield perm + elms[0]


def generatePerms2(elms, m):
    perms = ['']
    for elm in elms:
        perms2 = []
        for perm in perms:
            for i in range(len(perm)):
                perms2.append(perm[0:i] + elm + perm[i:])
            perms2.append(perm + elm)
        perms = perms2

    return perms
        
def generatePermsDFSS(elms, m = 0):
    if m == 0: # full perms by default
        m = len(elms)

    res = []
    elms_set = set(elms)
    elms_map = {}
    for e in elms:
        if elms_map.get(e) is not None:
            elms_map[e] += 1
        else:
            elms_map[e] = 1

    def dfsGen(found):
        for e in elms_set:
            if elms_map[e] > 0:
                found.append(e)
                elms_map[e] -= 1

                if len(found) == m:
                    res.append(found.copy())
                else:
                    dfsGen(found.copy())
                # backtracking
                found = found[0:len(found)-1]
                elms_map[e] += 1
        
    
    dfsGen([])
    return res

def generatePermsDFS(elms, m = 0):
    if m == 0: # full perms by default
        m = len(elms)

    res = []
    elms_set = set(elms)
    elms_map = {}
    for e in elms:
        if elms_map.get(e) is not None:
            elms_map[e] += 1
        else:
            elms_map[e] = 1

    def dfsGen(found):
        for e in elms_set:
            if elms_map[e] > 0:
                found += e
                elms_map[e] -= 1

                if len(found) == m:
                    res.append(found)
                else:
                    dfsGen(found)
                # backtracking
                found = found[0:len(found)-1]
                elms_map[e] += 1
        
    
    dfsGen('')
    return res

def is_operator(elm):
    return elm in ['+', '-', '*', '/']

def eval_postexpr(expr):
    value_st = []
    try:
        for elm in expr:
            if not is_operator(elm):
                value_st.append(elm)
            else:
                right = value_st.pop()
                left = value_st.pop()
                value_st.append(eval('%s %s %s' % (str(left), elm, str(right))))

        if len(value_st) == 1:
            # print(expr)
            return value_st[0]
        else:
            return None
        
    except IndexError as e:
        #print("The expression is likely invalid" + str(e))
        return None
    except ZeroDivisionError as e:
        return None
    
    return None

def trans2NormalExpr(postexpr):
    expr_st = []
    for elm in postexpr:
        if not is_operator(elm):
            expr_st.append((str(elm), 0))
        else:
            right = expr_st.pop()
            left = expr_st.pop()
            
            priority = 0 if elm == '*' or elm == '/' else 1
            left_expr = left[0]
            right_expr = right[0]

            if left[1] > priority:
                left_expr = '(' + left[0] + ')'
            if right[1] > priority:
                right_expr = '(' + right[0] + ')'

            expr_st.append((left_expr + elm + right_expr, priority))
    return expr_st.pop()[0]


# all possible compose choosing m elements in els
def compose(els, m):
    # print(els, m)
    if len(els) == m:
        return [els]
    if m == 1:
        return [e for  e in els]

    return [els[0] + e for e in compose(els[1:], m-1)] + compose(els[1:], m)

def composeR(els, m):
    res_set = set()
    res_set.add('')

    for i in range(m):
        res_list = list(res_set)
        res_set = set()
        for res_e in res_list:
            for e in els:
                new_e = res_e + e
                res_set.add(''.join(sorted(new_e)))

    return list(res_set)


def testcomp():
    a = 'abcd'
    print(len(composeR(a,3)))


def calc24(nums):
    res = []
    for opers in composeR('+-*/', 3):
        elms = nums+list(opers)

        for p in generatePermsDFSS(elms):
            if eval_postexpr(p) == 24:
                res.append(trans2NormalExpr(p))
    return res

def test24_input():
    while True:
        str = input("input 4 number:")
        nums = str.split()

        print(*calc24(nums), sep = '\n')

def test24():
    print(*calc24([2,2,3,3]), sep = '\n')
        
def testeval():
    a = '45+6-8*'
    print(eval_postexpr(a))

def test():
    a = 'abcdefghij'
    count = 0
    t1 = datetime.datetime.now()
    for p in generatePerms(a):
        count += 1

    t2 = datetime.datetime.now()
    print(t2-t1)
    print(count)

def testDfs():
    a = 'aacdd'
    perms = generatePermsDFSS(a)
    print(perms, len(perms))

def testTrans():
    a = '447/-7*'
    print(trans2NormalExpr(a))
    a = '7447/-*'
    print(trans2NormalExpr(a))



# testDfs()
test24_input()
# testTrans()
            
# testeval()
# testcomp()

        
