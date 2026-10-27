#!/usr/bin/env python3
"""Generate MU1440/790 core.so variants from the original omonob 1.2.2 core.so.
Usage as module: build(orig_bytes, zone=(x,y,w,h), fps=N, url=str|None, phys=(w,h)|None) -> bytes
"""
import struct
ORIG_SHA = 'a4bb6ce6e9e63a05cc1b6be20c5257983fb4dcbdf89f55528438acbd8edba8ee'
GOT = 0x959c
URL_SLOT, URL_SLOT_LEN = 0x78c0, 32           # stock "maps:/car/instrumentcluster/map\0"
NEW_SLOT, NEW_END = 0x7a48, 0x7a93            # two log-only event names, 75 bytes
URL_REFS = (0x28d4, 0x46ec)                   # initialURL (server info) and showUI (delayed thread)
OFF = dict(x=0x26b0, y=0x26a0, w=0x26a4, h=0x26a8, fps=0x257c, pw=0x25dc, ph=0x25fc)
REG = dict(x=0, y=1, w=2, h=3, fps=2, pw=2, ph=2)
STOCK_URL = 'maps:/car/instrumentcluster/map'

def _rot(v):
    for rot in range(16):
        imm = ((v << (2*rot)) | (v >> (32-2*rot))) & 0xffffffff if rot else v
        if imm < 256:
            return (rot << 8) | imm
    return None

def mov(rd, v):
    assert 0 <= v < 65536
    e = _rot(v)
    if e is not None:
        return struct.pack('<I', 0xE3A00000 | (rd << 12) | e)
    return struct.pack('<I', 0xE3000000 | ((v >> 12) << 16) | (rd << 12) | (v & 0xfff))

def decode(word):
    w = struct.unpack('<I', word)[0]
    if (w & 0x0FF00000) == 0x03A00000:
        rot, imm = (w >> 8) & 15, w & 255
        return ((imm >> (2*rot)) | (imm << (32-2*rot))) & 0xffffffff if rot else imm
    if (w & 0x0FF00000) == 0x03000000:
        return ((w >> 16) & 15) << 12 | (w & 0xfff)
    raise ValueError(hex(w))

def put(d, key, v):
    o = OFF[key]
    d[o:o+4] = mov(REG[key], v)

def build(orig, zone, fps, url=None, phys=None):
    import hashlib
    assert hashlib.sha256(orig).hexdigest() == ORIG_SHA, 'not the original omonob 1.2.2 MU1440/790 core.so'
    d = bytearray(orig)
    x, y, w, h = zone
    assert x + w <= 1010 and y + h <= 376 and w > 0 and h > 0
    put(d, 'x', x); put(d, 'y', y); put(d, 'w', w); put(d, 'h', h); put(d, 'fps', fps)
    if phys:
        put(d, 'pw', phys[0]); put(d, 'ph', phys[1])
    if url and url != STOCK_URL:
        b = url.encode() + b'\0'
        if len(b) <= URL_SLOT_LEN:
            d[URL_SLOT:URL_SLOT+URL_SLOT_LEN] = b.ljust(URL_SLOT_LEN, b'\0')
        else:
            # Same bytes as the car-tested v7 builds: the stock slot also gets the
            # short card URL (it is no longer referenced once relocated).
            base = url.split('?')[0].encode() + b'\0'
            d[URL_SLOT:URL_SLOT+URL_SLOT_LEN] = base.ljust(URL_SLOT_LEN, b'\0')
            assert len(b) <= NEW_END - NEW_SLOT, 'URL too long'
            assert orig[NEW_SLOT:NEW_SLOT+33] == b'alt-force-after-showui-scheduled\0'
            d[NEW_SLOT:NEW_END] = b.ljust(NEW_END - NEW_SLOT, b'\0')
            lit = struct.pack('<I', (NEW_SLOT - GOT) & 0xffffffff)
            for o in URL_REFS:
                assert struct.unpack('<I', orig[o:o+4])[0] == (URL_SLOT - GOT) & 0xffffffff
                d[o:o+4] = lit
    return bytes(d)

def describe(d):
    r = {k: decode(d[o:o+4]) for k, o in OFF.items()}
    u = []
    for o in URL_REFS:
        t = (GOT + struct.unpack('<I', d[o:o+4])[0]) & 0xffffffff
        u.append(d[t:d.index(b'\0', t)].decode())
    r['url'] = u[0] if u[0] == u[1] else u
    return r
