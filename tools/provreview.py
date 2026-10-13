# provreview.py: collect origin (non-twin, non-pos) provisional hand lines, one per distinct name,
# with the function body from decomp_<P>.c, into N review files.
# usage: py -3.13 -I provreview.py <ghidra dir> <N> <out prefix>
import sys, os, re
g, n, pre = sys.argv[1], int(sys.argv[2]), sys.argv[3]
progs = open(os.path.join(g, 'progs_all.txt')).read().split()
bodies = {}
def load(p):
    if p in bodies: return bodies[p]
    d = {}; cur = None; buf = []
    fn = os.path.join(g, 'decomp_%s.c' % p)
    if os.path.exists(fn):
        for l in open(fn, encoding='utf-8', errors='replace'):
            m = re.match(r'// ==== (\S+) @ ([0-9a-fA-F]+)', l)
            if m:
                if cur: d[cur] = ''.join(buf)
                cur = m.group(2).lower(); buf = []
            buf.append(l)
        if cur: d[cur] = ''.join(buf)
    bodies[p] = d; return d
seen = set(); items = []
for p in progs:
    for l in open(os.path.join(g, 'hand_%s.txt' % p), encoding='utf-8', errors='replace'):
        if 'provisional' not in l.lower() or '(twin ' in l or '(pos ' in l: continue
        f = l.split(None, 4)
        base = re.sub(r'_[0-9]+$', '', f[2])
        if base in seen: continue
        b = load(p).get(f[0][2:].lower().zfill(8))
        if not b: continue
        seen.add(base); items.append((p, l.rstrip(), b))
print('items', len(items))
tot = sum(len(i[2]) for i in items); per = tot / n; k = 0; acc = 0; out = None
for p, l, b in items:
    if out is None or (acc > per * (k) and k < n):
        k += 1; out = open('%s%d.txt' % (pre, k), 'w', encoding='utf-8')
    out.write('#### %s | %s\n%s\n' % (p, l, b)); acc += len(b)
print('files', k)
