# list (dst,val) pairs of an unrolled mov.l @(pool),r3 / mov.l @(pool),r2 / mov.l r2,@r3 initialiser
import sys
d=open(sys.argv[1],'rb').read(); base=int(sys.argv[2],16); start=int(sys.argv[3],16); end=int(sys.argv[4],16)
w=lambda a:int.from_bytes(d[a-base:a-base+2],'big')
l=lambda a:int.from_bytes(d[a-base:a-base+4],'big')
pc=start; pairs=[]; regs={}; other=0
while pc<end:
    op=w(pc)
    if op>>12==0xd:
        regs[(op>>8)&15]=l((pc&~3)+4+(op&0xff)*4)
    elif op==0x2322:
        pairs.append((regs.get(3),regs.get(2)))
    elif op>>12==0xa:
        disp=op&0xfff
        if disp&0x800: disp-=0x1000
        pc=pc+4+disp*2; continue
    else:
        other+=1
        if other<12: print('op',hex(pc),hex(op))
    pc+=2
print('pairs',len(pairs),'other',other)
ds=[p[0] for p in pairs if p[0]]; vs=[p[1] for p in pairs if p[1]]
print('dst',hex(min(ds)),hex(max(ds)),'val',hex(min(vs)),hex(max(vs)))
for p in pairs[:6]+pairs[-4:]: print(hex(p[0]),hex(p[1]))
