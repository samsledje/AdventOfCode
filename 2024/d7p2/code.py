import sys
import re
import numpy as np

# def safe_eval_l2r(expr, soln):
#     # evaluate left to right
#     first_val = int(re.match(r"\d+", expr)[0])
#     expr = re.findall(r"([+*\|])(\d+)", expr)
#     for (op, val) in expr:
#         if op == "+":
#             first_val = first_val + int(val)
#         elif op == "*":
#             first_val = first_val * int(val)
#         elif op == "|":
#             first_val = int(str(first_val) + val)
#     if first_val > soln:
#         return np.infty
#     return first_val

def safe_eval_l2r(expr, soln):
    expr_iter = iter(expr)
    base = next(expr_iter)
    for operator in expr_iter:
        base = operator(base, next(expr_iter))
        if base > soln:
            return np.infty
    return base

# def recurse_build(vals):
#     if len(vals) == 1:
#         return [f"{vals[0]}"]
#     else:
#         curr_value = vals[0]
#         running_vals = recurse_build(vals[1:])

#         new_vals = []
#         for v in running_vals:
#             new_vals.append(f"{curr_value}+"+v)
#             new_vals.append(f"{curr_value}*"+v)
#             new_vals.append(f"{curr_value}|"+v)
#         return new_vals   
# 

def np_cat(a,b):
    return int(str(a)+str(b))

def recurse_build(vals):
    if len(vals) == 1:
        return [[vals[0]]]
    else:
        curr_value = vals[0]
        running_vals = recurse_build(list(vals[1:]))
        new_vals = []
        for v in running_vals:
            try:
                new_vals.append([curr_value, np.add]+v)
                new_vals.append([curr_value, np.multiply]+v)
                new_vals.append([curr_value, np_cat]+v)
            except TypeError:
                raise TypeError
        return new_vals      


def test_equation(soln, vals):
    soln_space = [safe_eval_l2r(v, soln) for v in recurse_build(vals)]
    # print(soln, soln_space)
    return (soln in soln_space)

if __name__ == "__main__":
    
    equations = {}
    with open(sys.argv[1], "r") as file:
        for line in file:
            k = int(line.split(":")[0])
            v = [int(i) for i in line.split(":")[1].strip().split(" ")]
            equations[k] = v
    
    print(sum([k for k, v in equations.items() if test_equation(k, v)]))