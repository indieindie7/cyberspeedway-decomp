# xprop.py: carry hand names across overlays through xmatch groups.
# usage: py -3.13 -I xprop.py <ghidra dir> <xmatch.txt> PROG [PROG...]
# Reads every existing hand_<PROG>.txt; for each xmatch group, the first named member gives its line to
# every member that has no hand line yet (comment gets "(twin PROG:addr)"). Appends to hand_<PROG>.txt.
# Prints per prog: added count. Groups where members already carry different names are listed as "conflict".
import sys, os, re
gd, xm, progs = sys.argv[1], sys.argv[2], sys.argv[3:]
hand = {}
for p in progs:
    hand[p] = {}
    fn = f'{gd}/hand_{p}.txt'
    if os.path.exists(fn):
        for l in open(fn, encoding='utf-8'):
            m = re.match(r'0x([0-9a-fA-F]+) func (\S+) hand ?(.*)', l.strip())
            if m: hand[p][int(m.group(1), 16)] = (m.group(2), m.group(3))
add = {p: [] for p in progs}
conf = 0
for l in open(xm):
    if l.startswith('#'): continue
    mem = []
    for t in l.split()[3:]:
        p, a = t.split(':')
        if p in hand: mem.append((p, int(a, 16)))
    named = [(p, a, hand[p][a]) for p, a in mem if a in hand[p]]
    if not named: continue
    names = {n[2][0] for n in named}
    if len(names) > 1:
        conf += 1; print('conflict', ' '.join(f'{p}:{a:08x}={v[0]}' for p, a, v in named))
    p0, a0, (nm, cm) = named[0]
    for p, a in mem:
        if a not in hand[p]:
            hand[p][a] = (nm, cm)
            add[p].append(f'0x{a:08x} func {nm} hand {cm} (twin {p0}:{a0:08x})')
for p in progs:
    if add[p]:
        with open(f'{gd}/hand_{p}.txt', 'a', encoding='utf-8') as f:
            f.write('\n'.join(add[p]) + '\n')
    print(p, 'added', len(add[p]), 'total', len(hand[p]))
print('conflicts', conf)
