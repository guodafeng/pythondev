import re
import math

def get_elms(expr):
    #operand number|operator are split by space
    pattern = re.compile(r'\-?\d+|[\+\-\/\*]') 
    match = pattern.search(expr)

    start = 0
    while match:
        yield match.group()
        start += match.end()
        match = pattern.search(expr[start:])

def is_operator(elm):
    return elm in ['+', '-', '*', '/']

def eval_postfix(expr):
    value_st = []
    try:
        for elm in get_elms(expr):
            #print(value_st)
            if not is_operator(elm):
                value_st.append(eval(elm))
            else:
                right = value_st.pop()
                left = value_st.pop()
                value_st.append(calc(left, right, elm))

        if len(value_st) == 1:
            return value_st[0]
    except IndexError as e:
        #print("The expression is likely invalid" + str(e))
        return None
    except ZeroDivisionError as e:
        return None
    
    return None

def is_valid(expr):
    return eval_postfix(' '.join(expr)) is not None


def all_valid(exprs):
    return [exp for exp in exprs if is_valid(exp)]

def is_equal(expr, val):
    expr_val = eval_postfix(' '.join(expr))
    if expr_val is not None:
        return math.isclose(float(expr_val), float(val))
    else:
        return False

def all_equal(exprs, val):
    return [exp for exp in exprs if is_equal(exp, val)]


def all_exps(nums):
    exp_len = len(nums)*2 - 1
    return all_exps_imp(nums, exp_len)

def all_exps_imp(nums, exp_len):
    ops = ['+', '-', '*', '/']
    if len(nums) >= (exp_len + 1)//2: #can only be num otherwise invalid
        ops = []

    if exp_len <= 1:
        return [[num] for num in nums] + [[op] for op in ops]

    exps = []
    tmp = all_exps_imp(nums, exp_len-1)
    for op in ops:
        exps += map(lambda a,b:a+b, [[op]]*len(tmp), tmp)

    for i, num in enumerate(nums):
        tmp = all_exps_imp(nums[:i]+nums[i+1:], exp_len-1) 
        exps += map(lambda a,b:a+b, [[num]]*len(tmp), tmp)
       
    return exps


def calc(left, right, operator):
    return eval('%s %s %s' % (str(left), operator, str(right)))

def test_get_elms():
    expr = '-27 -16 + -2 *'
    print(list(get_elms(expr)))

def test_eval():
    # print(eval_postfix(expr))
    
    expr = '-27 -16 / -2 + 7 /'
    print(eval_postfix(expr))

def test_all_exps():
    nums = [3,5,6,7]
    nums = [str(num) for num in nums]
    print(len(all_exps(nums))) 
    print(len(all_valid(all_exps(nums))))
def test_all_equal():
    from datetime import datetime 
    begin = datetime.now()

    nums = ['3','4','8','6']
    print(list(map(lambda x:' '.join(x), all_equal(all_exps(nums),24))))
    nums = ['7','3','7','3']
    print(list(map(lambda x:' '.join(x), all_equal(all_exps(nums),24))))

    end = datetime.now()
    print(end - begin)

#test_get_elms()
#test_eval()
test_all_exps()
#test_all_equal()
