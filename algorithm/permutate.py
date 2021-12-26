def permutate(vals):
    if len(vals) == 0:
        return ['']
    return insert(vals[0], permutate(vals[1:]))

def insert(val, vals):
    new_vals = []
    for v in vals:
        for i in range(len(v)+1):
            new_vals.append(v[:i] + val + v[i:])

    return new_vals

def compose(m, vals):
    if len(vals) == 0:
        return []
    if m == 1:
        return list(vals)
    return [vals[0] + v  for v in compose(m-1, vals[1:])] + compose(m,
            vals[1:])


a = 'abcdefgh'
p = permutate(a)
# print(p, len(p))
comp = compose(2, a)
print(comp, len(comp))
