# xpos.py: name leftovers by position between anchors (functions with the same hand name in both programs).
# usage: py -3.13 -I xpos.py <ghidra dir> <ref prog> <target prog> [...]
# Between two consecutive anchors, if the unnamed target functions and the ref functions have the same count
# and the same sizes in order, each target function gets the ref name (comment "(pos REF:addr)"). Appends to hand_<target>.txt.
import sys, re
gd, ref, tgts = sys.argv[1], sys.argv[2], sys.argv[3:]
def fi(p):
    out = []
    for l in open(f'{gd}/funcinfo_{p}.tsv', encoding='utf-8', errors='replace'):
        f = l.split()
        if len(f) >= 5 and f[0] == 'F': out.append((int(f[1], 16), int(f[4])))
    return sorted(out)
def hand(p):
    d = {}
    for l in open(f'{gd}/hand_{p}.txt', encoding='utf-8'):
        f = l.rstrip('\n').split(' ', 4)
        if f[0].startswith('0x'): d[int(f[0], 16)] = (f[2], f[4] if len(f) > 4 else '')
    return d
rf, rh = fi(ref), hand(ref)
rname = {}
for a, (n, c) in rh.items(): rname.setdefault(n, []).append(a)
for t in tgts:
    tf, th = fi(t), hand(t)
    used = {n for n, c in th.values()}
    anchors = [(-1, -1)]
    last = -1
    for a, s in tf:
        if a in th:
            ra = rname.get(th[a][0])
            if ra and len(ra) == 1 and ra[0] > last: anchors.append((ra[0], a)); last = ra[0]
    anchors.append((1 << 40, 1 << 40))
    add = []
    for (r0, t0), (r1, t1) in zip(anchors, anchors[1:]):
        rg = [(a, s) for a, s in rf if r0 < a < r1]
        tg = [(a, s) for a, s in tf if t0 < a < t1]
        if not any(a not in th for a, s in tg): continue
        if len(rg) != len(tg) or any(rs != ts for (ra, rs), (ta, ts) in zip(rg, tg)): continue
        for (ra, rs), (ta, ts) in zip(rg, tg):
            if ta in th or ra not in rh: continue
            nm = base = rh[ra][0]; k = 2
            while nm in used: nm = f'{base}_{k}'; k += 1
            used.add(nm); th[ta] = (nm, '')
            add.append(f'0x{ta:08x} func {nm} hand {rh[ra][1]} (pos {ref}:{ra:08x})')
    if add:
        with open(f'{gd}/hand_{t}.txt', 'a', encoding='utf-8') as f: f.write('\n'.join(add) + '\n')
    print(t, 'pos added', len(add))
