rules, pages = open('inputs/day5_sample.txt').read().split('\n\n')

def key_func(x):
    l=[x+'|'+y in rules for y in p]
    val=-sum(l)
    print(f'x={x}, val={val}, p={p}, l={l}')
    return val

a = [0, 0]
for p in pages.split():
    p = p.split(',')
    s = sorted(p, key=key_func)
    a[p!=s] += int(s[len(s)//2])

print(*a)