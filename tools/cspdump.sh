#!/bin/bash
# decompile dumps of the six Cyber Speedway programs
S=C:/Users/john/AppData/Local/Temp/claude/C--/d4e4ed81-a8a4-4c6e-ad3f-fc40eb86e6a6/scratchpad
G=C:/Users/john/Documents/CyberSpeedway/ghidra
for f in "$@"; do
  SP=C:/Users/john/Documents/Amok/ghidra/scripts bash $G/csprun.sh $S/dd_$f.log -process $f.BIN -readOnly -noanalysis -postScript CsDumpAll.java $G/decomp_$f.c > /dev/null 2>&1
  echo "$f $(grep -c '^// ==== ' $G/decomp_$f.c 2>/dev/null) $(wc -l < $G/decomp_$f.c)"
done
