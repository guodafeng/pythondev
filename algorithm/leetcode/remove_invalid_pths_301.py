def removeInvalidParentheses2(s):
    def isValid(s):
        count = 0
        for ch in s:
            if ch == '(':
                count += 1
            elif ch == ')':
                count -= 1
            if count < 0:
                return False
        return count == 0

    level = {s}
    while True:
        valid = filter(isValid, level)
        if valid:
            return valid
        level = {s[:i] + s[i+1:] for s in level for i in range(len(s))}

def removeInvalidParentheses(s):
    def isvalid(s):
        ctr = 0
        for c in s:
            if c == '(':
                ctr += 1
            elif c == ')':
                ctr -= 1
                if ctr < 0:
                    return False
        return ctr == 0
    level = {s}
    while True:
        valid = set(filter(isvalid, level)) 
        # important set call here in python 3
        if valid:
            return valid
        level = {s[:i] + s[i+1:] for s in level for i in range(len(s))}
if __name__ == "__main__":
    # print(list(removeInvalidParentheses('()')))
    # print(list(removeInvalidParentheses(')(')))
    # print(list(removeInvalidParentheses(')()(')))
    print(list(removeInvalidParentheses('()((()()')))

