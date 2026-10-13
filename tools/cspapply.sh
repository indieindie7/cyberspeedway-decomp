#!/bin/bash
# apply hand names to each program, then re-export funcinfo
S=C:/Users/john/AppData/Local/Temp/claude/C--/d4e4ed81-a8a4-4c6e-ad3f-fc40eb86e6a6/scratchpad
G=C:/Users/john/Documents/CyberSpeedway/ghidra
for f in "$@"; do
  SP=C:/Users/john/Documents/Amok/ghidra/scripts bash $G/csprun.sh $S/ap_$f.log -process $f.BIN -noanalysis -postScript ApplyNames.java hand_$f.txt hand -postScript ExportFuncInfo.java C:/Users/john/Documents/CyberSpeedway/ghidra/funcinfo_$f.tsv > /dev/null 2>&1
  echo "$f $(grep -c '^F' $G/funcinfo_$f.tsv) FUN_left $(awk '$1=="F" && $3 ~ /^FUN_/' $G/funcinfo_$f.tsv | wc -l) $(grep -o 'ApplyNames.java> [^(]*' $S/ap_$f.log | tail -1)"
done
