# xunify.py: give every member of an xprop conflict group the first member's name.
# usage: py -3.13 -I xunify.py <ghidra dir> <conflict lines file>
import sys, re
gd, cf = sys.argv[1], sys.argv[2]
ren = {}
for l in open(cf):
    mem = [t.split('=') for t in l.split()[1:]]
    nm = mem[0][1]
    for pa, n in mem[1:]:
        p, a = pa.split(':'); ren.setdefault(p, {})[int(a, 16)] = nm
for p, m in ren.items():
    fn = f'{gd}/hand_{p}.txt'; out = []; used = set()
    lines = open(fn, encoding='utf-8').read().splitlines()
    for l in lines:
        f = l.split(' ', 3)
        if f[0].startswith('0x') and int(f[0], 16) not in m: used.add(f[2])
    for l in lines:
        f = l.split(' ', 3)
        if f[0].startswith('0x') and int(f[0], 16) in m:
            nm = m[int(f[0], 16)]; k = 2; base = nm
            while nm in used: nm = f'{base}_{k}'; k += 1
            used.add(nm); f[2] = nm; l = ' '.join(f)
        out.append(l)
    open(fn, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(p, 'renamed', len(m))
