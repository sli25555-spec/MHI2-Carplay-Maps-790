# MHI2-Carplay-Maps 790 v2 — changes vs omonob/MHI2-Carplay-Maps v2.0.1

Modified version of [omonob/MHI2-Carplay-Maps](https://github.com/omonob/MHI2-Carplay-Maps) v2.0.1, released under GPL-3.0.
Modification date: 2026-11-11. Not affiliated with or endorsed by omonob.

Base: the full MQB package `VW_SKODA_ALL_CarPlay_Maps_VC_FULL_MQB_Toolbox_V4.2A_v2.0.1.zip` (sha256 `86aada968b035710…`).
Only the files listed below differ from it. Everything else in the release ZIP is byte-identical
(including `dio_manager.wrapper.sh` and `carplay-cluster-supervisor`: logging is exactly as in omonob 2.0.1).

## Changed files (`Custom/carplay_maps_vc/…`)

| File | Change | Source / how to reproduce |
|---|---|---|
| `payload/profiles/MU1440/790/core.so` | default variant YANDEX-2026 (see below) | `tools/gen_core201.py` from the original `core.so` (sha256 `97ccb829f996b743…`) |
| `payload/profiles/MU1440/790/VARIANT` | **added**: variant label shown in the status | text |
| `payload/common/install-carplay-maps.sh` | adds the variant name to `VERSION`, installs the variant menu, removes menu scripts of older builds, refreshes an old (1.2.x) Toolbox restore script | `patches/install-carplay-maps.sh.diff` |
| `menu790/*` | **added**: MQB Toolbox screen `cpmap-790-variants` and switch scripts | shell / ESD |
| `variants790/*` | **added**: one folder per variant (`core.so`, `VARIANT`) | `tools/gen_core201.py` |
| `VARIANTS.txt`, `README_790_v2.md`, `CHANGES.md`, `LICENSE-GPL-3.0.txt`, `tools/*`, `patches/*` | **added**: documentation and build scripts | — |

No code from other projects is added. Profiles other than MU1440/790 are unchanged.

## `core.so` patch (MU1440/790 profile of omonob 2.0.1)

Data only; the code is not changed. The script finds each place by pattern and refuses if it is not found exactly once.

| Offset (2.0.1) | Meaning | omonob 2.0.1 | YANDEX-2026 |
|---|---|---|---|
| `0x6f28` view 0 | safe area x, y, w, h — no route (Left / Right / Off) | 202, 16, 606, 344 | 214, 55, 606, 284 |
| `0x6f38` view 1 | route, card Left | 18, 75, 606, 284 | 0, 55, 692, 284 |
| `0x6f48` view 2 | route, card Right | 386, 75, 606, 284 | 346, 55, 653, 284 |
| `0x6f58` view 3 | card Center (with and without route) | 325, 75, 360, 284 | 325, 30, 360, 319 |
| `0x6f68` view 4 | route, card Off | 42, 16, 606, 344 | 42, 16, 606, 344 |
| `0x66a8` | `maxFPS` (`mov r2,#imm`) | 60 | 30 |
| `0x769c` / `0x7740` | Left / Right card URL | `showETA=no&…&showSpeedLimit=no` | `showETA=yes&maneuverLayout=…` |

The Center (`topAligned`) and Off (`…/map?…`) URLs and the physical screen size (202 × 75 mm) are unchanged. The new URLs are shorter than the originals; they are written in place and padded with NUL bytes.

Variant OMONOB201 is byte-identical to the original `core.so`.
