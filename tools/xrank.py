# xrank.py: for xmatch groups that hold 2+ functions of one program, give twin lines the name of the
# same-rank (by address) member of the reference program instead of the first name.
# usage: py -3.13 -I xrank.py <ghidra dir> <xmatch.txt> <ref prog> PROG...
import sys, re, collections
gd, xm, ref, progs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def load(p):
    d = {}
    for l in open(f'{gd}/hand_{p}.txt', encoding='utf-8'):
        f = l.rstrip('\n').split(' ', 3)
        if f[0].startswith('0x'): d[int(f[0], 16)] = f
    return d
hand = {p: load(p) for p in progs}
fix = collections.defaultdict(dict)
for l in open(xm):
    if l.startswith('#'): continue
    by = collections.defaultdict(list)
    for t in l.split()[3:]:
        p, a = t.split(':'); by[p].append(int(a, 16))
    if ref not in by or len(by[ref]) < 2: continue
    rn = [hand[ref][a][2] for a in sorted(by[ref]) if a in hand[ref]]
    if len(rn) != len(by[ref]): continue
    for p, al in by.items():
        if p == ref or p not in hand or len(al) != len(rn): continue
        for a, nm in zip(sorted(al), rn):
            f = hand[p].get(a)
            if f and len(f) > 3 and '(twin' in f[3] and f[2] != nm: fix[p][a] = nm
for p, m in fix.items():
    used = {f[2] for a, f in hand[p].items() if a not in m}
    out = []
    for l in open(f'{gd}/hand_{p}.txt', encoding='utf-8').read().splitlines():
        f = l.split(' ', 3)
        if f[0].startswith('0x') and int(f[0], 16) in m:
            nm = base = m[int(f[0], 16)]; k = 2
            while nm in used: nm = f'{base}_{k}'; k += 1
            used.add(nm); f[2] = nm; l = ' '.join(f)
        out.append(l)
    open(f'{gd}/hand_{p}.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(p, 'fixed', len(m))
