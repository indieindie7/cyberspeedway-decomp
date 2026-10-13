#!/bin/bash
# slicecheck.sh <slices dir>: per slice, functions in the .c without a line in hand_<slice>.txt
cd "$1" || exit 1
for c in *_s[0-9]*.c; do
  b=${c%.c}; h=hand_$b.txt
  [ -f "$h" ] || { echo "$b: no output yet"; continue; }
  miss=$(grep -o '^// ==== FUN_[0-9a-f]*' $c | sed 's/.*FUN_/0x/' | sort > /tmp/a_$$; awk '{print $1}' $h | sort > /tmp/b_$$; comm -23 /tmp/a_$$ /tmp/b_$$ | tr '\n' ' ')
  echo "$b: $(grep -c '^// ==== ' $c) funcs, $(grep -c '^0x' $h) lines, missing: $miss"
done
rm -f /tmp/a_$$ /tmp/b_$$
