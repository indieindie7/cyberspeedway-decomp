# usage: py -3.13 -I dedupe.py <ghidra dir> PROG...  : per hand file, keep one line per address and suffix repeated names _2, _3...
import sys, os
gd, progs = sys.argv[1], sys.argv[2:]
for p in progs:
    fn = os.path.join(gd, 'hand_%s.txt' % p)
    lines = [l.rstrip('\n') for l in open(fn) if l.strip()]
    seen_a, out, used, ch = set(), [], set(), 0
    for l in lines:
        a = int(l.split()[0], 16)
        if a in seen_a: ch += 1; continue
        seen_a.add(a); out.append(l.split(None, 3))
    for t in out: used.add(t[2])
    names = set()
    for t in out:
        n = t[2]
        if n in names:
            k = 2
            while '%s_%d' % (n, k) in used: k += 1
            t[2] = '%s_%d' % (n, k); used.add(t[2]); ch += 1
        names.add(t[2])
    open(fn, 'w').write(''.join(' '.join(t) + '\n' for t in out))
    if ch: print(p, 'changed', ch)
