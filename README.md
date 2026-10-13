# Cyber Speedway (Sega Saturn, 1995) reverse-engineering notes and symbols

Hand-named function maps, review records, tools and working notes for the Sega Saturn game
**Cyber Speedway** (Sega / Nextech 1995, MK-81205; *Gran Chaser* in Japan). The game is split into
38 SH-2 program overlays (AUTOEXEC, MENU, one per course MAP*/MAPW*, ROOM1-6, STATION, END, PROLOGUE,
TITLE_OP, SMPCPK4, and the AAAAA000/AAAAA001 boot stubs). Same method as
[scorcher-decomp](https://github.com/indieindie7/scorcher-decomp),
[amok-decomp](https://github.com/indieindie7/amok-decomp) and
[cybersled-decomp](https://github.com/indieindie7/cybersled-decomp). Non-commercial, done for study and preservation.

**No game data is included**: no disc image, no program files, no decompiled C, no Ghidra database.
You need your own copy of the game to use any of this.

## What is here

| Path | Content |
|---|---|
| `NOTES.md` | the working log: disc layout, overlay load addresses, the naming pipeline, every review pass |
| `ghidra/hand_<PROG>.txt` | hand-named functions (`0x<addr> func <name> hand <comment>`); 18495 functions over the 38 programs, no `FUN_` and no provisional names left |
| `ghidra/funcinfo_<PROG>.tsv` | per-function export: `F` address name source size, `C` callees, `S` string references |
| `ghidra/progs_all.txt` | the 38 program names |
| `ghidra/review/` | provisional-name review prompts and verdicts (`<PROG> 0x<addr> <old> CONFIRM/RENAME/UNSURE <new> <reason>`), passes 1-3 |
| `ghidra/scripts/` | `FindSh2FunctionsMem.java` (SH-2 function discovery), `DumpLong.java` (decompile with a long timeout) |
| `ghidra/csprun.sh` | headless Ghidra wrapper |
| `tools/` | cross-overlay name matching (`xmatch`, `xprop`, `xunify`, `xrank`, `xpos`), `dedupe`, `stubfix`, provisional review (`provreview`, `provctx`, `provapply`), `storeseq.py` (decodes unrolled SH-2 store initialisers from raw bytes), apply/dump scripts |

Paths inside the scripts point at the author's machine; edit them for yours. `ApplyNames.java` and
`ExportFuncInfo.java` come from the Scorcher / AMOK repos.

## Memory layout in short

Overlays load at 0x06012000 (AAAAA000 at 0x06020000, AAAAA001 at 0x06004000). All overlays share a
library prefix (Sega SBL-era GFS, CDC, SND, SCL/VDP2, VDP1, SMPC, CPK) and then diverge; twins across
overlays carry the same name, with `(twin PROG:addr)` in the comment.

## Licence

Notes, names and tools: MIT (see `LICENSE`). Cyber Speedway itself belongs to its rights holders;
nothing from the game is distributed here. Takedown requests will be honoured.
