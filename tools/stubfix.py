# usage: py -3.13 -I stubfix.py <ghidra dir> PROG...  : stub_<addr>[_n] names carried from another program get the line's own address
import sys, os, re
gd, progs = sys.argv[1], sys.argv[2:]
for p in progs:
    fn = os.path.join(gd, 'hand_%s.txt' % p)
    out, ch = [], 0
    for l in open(fn):
        t = l.rstrip('\n').split(None, 3)
        if len(t) > 2:
            m = re.match(r'stub_([0-9a-fA-F]{8})(_\d+)?$', t[2])
            own = '%08x' % int(t[0], 16)
            if m and (m.group(1).lower() != own or m.group(2)):
                t[2] = 'stub_' + own; ch += 1
        out.append(' '.join(t) + '\n')
    open(fn, 'w').write(''.join(out))
    if ch: print(p, 'stubs renamed', ch)
