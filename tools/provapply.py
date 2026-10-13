# provapply.py: apply provisional-name review results to every hand_<P>.txt.
# usage: py -3.13 -I provapply.py <ghidra dir> <res file>...
# Result lines: PROG 0xaddr oldname CONFIRM|RENAME|UNSURE newname reason
# CONFIRM drops the provisional marker on every line whose name is oldname or oldname_N;
# RENAME also renames them (newname, keeping the _N suffix). UNSURE changes nothing.
import sys, os, re
g = sys.argv[1]
act = {}
for rf in sys.argv[2:]:
    for l in open(rf, encoding='utf-8', errors='replace'):
        f = l.split(None, 5)
        if len(f) < 5 or f[3] not in ('CONFIRM', 'RENAME', 'UNSURE'): continue
        old = re.sub(r'_[0-9]+$', '', f[2]); new = re.sub(r'_[0-9]+$', '', f[4])
        if f[3] == 'RENAME' and not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', new): continue
        act[old] = (f[3], new if f[3] == 'RENAME' else old)
progs = open(os.path.join(g, 'progs_all.txt')).read().split()
cnt = {'CONFIRM': 0, 'RENAME': 0}
for p in progs:
    fn = os.path.join(g, 'hand_%s.txt' % p)
    lines = open(fn, encoding='utf-8', errors='replace').read().splitlines()
    names = set(l.split()[2] for l in lines if len(l.split()) > 2)
    out = []
    for l in lines:
        f = l.split(' ', 4)
        if len(f) < 4 or 'provisional' not in l.lower(): out.append(l); continue
        m = re.fullmatch(r'(.*?)(_[0-9]+)?', f[2]); base, suf = m.group(1), m.group(2) or ''
        a = act.get(base) or act.get(f[2])
        if not a or a[0] == 'UNSURE': out.append(l); continue
        if a[1] != base and base not in act: suf = ''
        nn = (a[1] + suf) if a[0] == 'RENAME' and base in act else (a[1] if a[0] == 'RENAME' else f[2])
        rest = f[4] if len(f) > 4 else ''
        rest = re.sub(r'^provisional:?\s*', '', rest)
        rest = re.sub(r'\bprovisional\b:?\s*', '', rest)
        if a[0] == 'RENAME' and nn != f[2]: rest = (rest + ' (was %s)' % f[2]).strip()
        out.append(' '.join([f[0], f[1], nn, f[3]] + ([rest] if rest else [])))
        cnt[a[0]] += 1
    open(fn, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('lines confirmed', cnt['CONFIRM'], 'renamed', cnt['RENAME'])
