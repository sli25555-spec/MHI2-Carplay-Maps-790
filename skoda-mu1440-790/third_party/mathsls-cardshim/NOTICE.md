# libcardshim (third-party)

Source: [mathsls/MHI2-Carplay-Maps](https://github.com/mathsls/MHI2-Carplay-Maps), `src/cardshim/` — license GPL-3.0.

`cardshim.c` and `build.sh` are copied unchanged. The binary `libcardshim.so` shipped in this build (sha256 `1cb962c51c5fbb61…`) is the one published by mathsls.

What it does: it runs as an LD_PRELOAD module in front of the CarPlay Maps VC `core.so` and intercepts `AirPlayCopyServerInfo`. It adds `properties = ["Instrument Cluster"]` and `uid` to the cluster display (type 111). It also sets `zoomFactor` from `/mnt/app/carplaymaps/CLUSTER_ZOOM` (the card style). Kill switch: `/mnt/app/carplaymaps/NO_CARD_SHIM`.
