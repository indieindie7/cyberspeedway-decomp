# xmatch.py: find the same function in several Cyber Speedway overlays.
# usage: py -3.13 -I xmatch.py <ghidra dir> <cd dir> PROG [PROG...]
# Each PROG is loaded at 0x06012000 from <cd>/<PROG>.BIN; functions come from funcinfo_<PROG>.tsv.
# Body hash masks bra/bsr displacements and mov.l/mov.w @(disp,PC) displacements, so code that moved
# keeps its hash. Literal pool words inside the body are kept (they hold constants and addresses).
# --loose: also masks 0x060xxxxx words, size >= 24 only (second pass for builds whose addresses shifted).
# Prints groups: "<hash> <n progs> PROG:addr ..." for bodies present in 2+ overlays; summary at the end.
import sys, hashlib, collections
BASE = 0x06012000
BASES = {'AAAAA000': 0x06020000, 'AAAAA001': 0x06004000}
LOOSE = '--loose' in sys.argv
if LOOSE: sys.argv.remove('--loose')
def funcs(path):
    out = []
    for line in open(path, encoding='utf-8', errors='replace'):
        p = line.rstrip('\n').split()
        if len(p) >= 5 and p[0] == 'F':
            out.append((int(p[1], 16), p[2], int(p[4])))
    return out
def mask(b):
    w = bytearray(b)
    for i in range(0, len(w) - 1, 2):
        op = (w[i] << 8) | w[i + 1]
        hi = op >> 12
        if hi in (0xA, 0xB):            # bra / bsr disp12
            w[i] &= 0xF0; w[i + 1] = 0
        elif hi in (0xD, 0x9):          # mov.l / mov.w @(disp,PC),Rn
            w[i + 1] = 0
        elif (op & 0xFF00) in (0x8900, 0x8B00, 0x8D00, 0x8F00):  # bt bf bt/s bf/s
            w[i + 1] = 0
    if LOOSE:                          # also mask 0x060xxxxx words (addresses that moved between builds)
        for i in range(0, len(w) - 3, 2):
            if w[i] == 0x06 and w[i + 1] < 0x10:
                w[i:i + 4] = bytes(4)
    return bytes(w)
def main():
    gd, cd, progs = sys.argv[1], sys.argv[2], sys.argv[3:]
    groups = collections.defaultdict(list)
    total = {}
    for p in progs:
        data = open(f'{cd}/{p}.BIN', 'rb').read()
        fl = funcs(f'{gd}/funcinfo_{p}.tsv')
        total[p] = len(fl)
        for a, n, s in fl:
            if s < (24 if LOOSE else 8): continue
            b = data[a - BASES.get(p, BASE):a - BASES.get(p, BASE) + s]
            h = hashlib.sha1(mask(b)).hexdigest()[:12]
            groups[h].append((p, a, n, s))
    shared = {p: 0 for p in progs}
    ncommon = 0
    for h, lst in sorted(groups.items(), key=lambda kv: kv[1][0][1]):
        ps = {x[0] for x in lst}
        if len(ps) < 2: continue
        for p in ps: shared[p] += 1
        if len(ps) == len(progs): ncommon += 1
        print(h, len(ps), lst[0][3], ' '.join(f'{x[0]}:{x[1]:08x}' for x in lst))
    print('# per prog shared/total:', ' '.join(f'{p} {shared[p]}/{total[p]}' for p in progs))
    print('# in all progs:', ncommon)
main()
