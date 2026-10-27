#!/usr/bin/env python3
"""Make carplay-cluster-supervisor.nolog from the omonob 1.2.2 carplay-cluster-supervisor.
The only change: the MOST bridge log path at file offset 0x47c0
("/ramdisk/altscreen-most-bridge.log", 35 bytes with NUL) becomes "/dev/null"
padded with NUL bytes, so the bridge log no longer fills the 20 MB RAM disk.
Same patch as mathsls/MHI2-Carplay-Maps (src/fork/README.md, section 1).
Usage: python3 patch_supervisor.py <carplay-cluster-supervisor> <output>
"""
import hashlib, sys
ORIG_SHA = 'cdc2f9c64eae'  # prefix of the omonob 1.2.2 file
OLD = b'/ramdisk/altscreen-most-bridge.log\0'
d = open(sys.argv[1], 'rb').read()
assert hashlib.sha256(d).hexdigest().startswith(ORIG_SHA), 'unexpected input file'
assert d.count(OLD) == 1 and d.index(OLD) == 0x47c0
out = d.replace(OLD, b'/dev/null'.ljust(len(OLD), b'\0'))
assert len(out) == len(d)
open(sys.argv[2], 'wb').write(out)
print('ok', hashlib.sha256(out).hexdigest())
