# MHI2-Carplay-Maps 790 v1 — changes vs omonob/MHI2-Carplay-Maps v1.2.2

Modified version of [omonob/MHI2-Carplay-Maps](https://github.com/omonob/MHI2-Carplay-Maps) v1.2.2, released under GPL-3.0.
Modification date: 2026-10-27. Not affiliated with or endorsed by omonob.

Base: the full MQB package `VW_SKODA_ALL_CarPlay_Maps_VC_FULL_MQB_Toolbox_V4.2A_v1.2.2.zip` (sha256 `06955ade05e461b2…`).
Only the files listed below differ from it. Everything else in the release ZIP is byte-identical.

## Changed files (`Custom/carplay_maps_vc/…`)

| File | Change | Source / how to reproduce |
|---|---|---|
| `payload/profiles/MU1440/790/core.so` | default variant YANDEX11 (see below) | `tools/build_790_variants.py` from the original `core.so` (sha256 `a4bb6ce6e9e63a05…`) |
| `payload/profiles/MU1440/790/libcardshim.so` | **added**: announces the cluster display as "Instrument Cluster", card style via `CLUSTER_ZOOM` | mathsls, GPL-3.0, `third_party/mathsls-cardshim/` |
| `payload/profiles/MU1440/790/CLUSTER_ZOOM`, `VARIANT` | **added**: card style 1.5, variant label | text |
| `payload/common/carplay-cluster-supervisor.nolog` | **added**: MOST-bridge log path `/ramdisk/altscreen-most-bridge.log` (offset `0x47c0`) → `/dev/null` | `tools/patch_supervisor.py` (patch by mathsls) |
| `payload/common/install-carplay-maps.sh` | installs the default variant, `libcardshim.so`, `CLUSTER_ZOOM`, RAM logs OFF and the variant menu; removes menu scripts of older builds | `patches/install-carplay-maps.sh.diff` |
| `payload/common/dio_manager.wrapper.sh` | preloads `libcardshim.so` before `core.so`; video/session logs → `/dev/null` when `NO_RAM_LOGS` exists | `patches/dio_manager.wrapper.sh.diff` |
| `menu790/*` | **added**: MQB Toolbox screen `cpmap-790-variants` and switch scripts | shell / ESD |
| `variants790/*` | **added**: one folder per variant (`core.so`, optional `libcardshim.so`, `CLUSTER_ZOOM`, `VARIANT`) | `tools/build_790_variants.py` |
| `VARIANTS.txt`, `README_790_v1.md`, `tools/*` | **added**: documentation and build scripts | — |

## `core.so` patch (MU1440/790 profile of omonob 1.2.2)

All values are ARM `mov`/`movw` immediates in `AirPlayCopyServerInfo` and its callers:

| Offset | Meaning | omonob 1.2.2 |
|---|---|---|
| `0x26b0` / `0x26a0` / `0x26a4` / `0x26a8` | safe area x / y / width / height | 202 / 16 / 606 / 344 |
| `0x257c` | `maxFPS` | 40 |
| `0x78c0` | cluster URL string (32 bytes) | `maps:/car/instrumentcluster/map` |

URLs longer than 31 characters (`…?showETA=yes`, `…?maneuverLayout=topAligned`) are written at `0x7a48`, over the two log-only event names `alt-force-after-showui-scheduled` and `alt-force-after-showui-schedule-failed`. Both URL references are redirected there: the GOT-relative literals at `0x28d4` (initialURL) and `0x46ec` (`showUI` in `delayed_alt_activation_thread`). The map-app table used for long-press switching is not touched.

Variant OMONOB is byte-identical to the original `core.so`.
