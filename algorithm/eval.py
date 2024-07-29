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

def postfix_to_normal(expr):
    elm_st = []
    try:
        for elm in get_elms(expr):
            if not is_operator(elm):
                elm_st.append(elm)
            else:
                right = elm_st.pop()
                left = elm_st.pop()
                expr = f'({left} {elm} {right})'

                elm_st.append(expr)

        if len(elm_st) == 1:
            return elm_st[0]
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


def all_exps_old(nums):
    exp_len = len(nums)*2 - 1
    return all_exps_imp(nums, exp_len)

def all_exps(nums):
    import itertools
    ops = ['+', '-', '*', '/']
    length = len(nums)
    index_comp = list(itertools.combinations(range(len(nums)), 2))
    ops_comp = list(itertools.combinations_with_replacement(ops,
        len(nums)-1))

    exprs = []
    for comp in ops_comp:
        for i_comp in index_comp:
            headpart = list(itertools.permutations([nums[i] for i in i_comp]) )
            temp = [nums[i] for i in range(length) if i not in i_comp] + list(comp)
            tailpart = set(itertools.permutations(temp))

            exprs += [head + tail for head in headpart for tail in tailpart]

    return set(exprs)

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

def exprs_with_value(nums, value):
    for expr in all_equal(all_exps(nums), value):
        print(' -----------------')
        print(' '.join(expr))
        print(postfix_to_normal(' '.join(expr)))


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
    exprs_with_value(nums, 24)
    nums = ['7','3','7','3']
    exprs_with_value(nums, 24)

    end = datetime.now()
    print(end - begin)

# test_get_elms()
# test_eval()
# test_all_exps()
test_all_equal()
