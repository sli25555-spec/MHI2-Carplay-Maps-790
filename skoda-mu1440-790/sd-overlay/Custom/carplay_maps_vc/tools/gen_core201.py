#!/usr/bin/env python3
"""MHI2-Carplay-Maps 790 v2 - make variant core.so files from omonob 2.0.x.

Input: the original MU1440/790 core.so of omonob/MHI2-Carplay-Maps 2.0.1
(sha256 97ccb829f996b743...). Patches are found by pattern, not by fixed
offsets, so the script refuses (assert) instead of guessing if a later 2.0.x
build looks different.

What is changed (data only, no code is moved):
  1. the five navigation-card view areas (safe areas) used by updateViewArea:
       0 idle (no route)   1 card Left + route   2 card Right + route
       3 card Center + route   4 card Off + route
     table of 5 x (x, y, width, height) int32 in .rodata;
  2. the Left and Right card URLs: showETA=no -> showETA=yes; the shorter
     string is written in place and padded with NUL bytes (the Center URL
     topAligned and the 'Off' URL .../map?... are left unchanged since v3);
  3. maxFPS: the immediate of 'mov r2,#60' right after the "maxFPS" key load;
  4. optional, not used by the shipped variants: physical screen size
     widthPhysical/heightPhysical (spec key 'phys', two 'mov r2,#imm' immediates).

Usage:
  gen_core201.py <core.so original> <out dir>     -> <out dir>/<VARIANT>/core.so
  gen_core201.py --check <core.so>                -> print what was found
"""
import hashlib, os, struct, sys

ORIG_SHA = '97ccb829f996b74305099ca54e6f4a693a17381b391d170c1227f44e49ff0769'

ORIG_RECTS = [(202, 16, 606, 344),   # 0 idle
              (18, 75, 606, 284),    # 1 Left + route
              (386, 75, 606, 284),   # 2 Right + route
              (325, 75, 360, 284),   # 3 Center + route
              (42, 16, 606, 344)]    # 4 Off + route

URL_BASE = b'maps:/car/instrumentcluster?'
ORIG_URLS = {
    'top':   URL_BASE + b'showETA=no&maneuverLayout=topAligned&showSpeedLimit=no',
    'left':  URL_BASE + b'showETA=no&maneuverLayout=leftAligned&showSpeedLimit=no',
    'right': URL_BASE + b'showETA=no&maneuverLayout=rightAligned&showSpeedLimit=no',
}
ETA_URLS = {
    'top':   URL_BASE + b'showETA=yes&maneuverLayout=topAligned',
    'left':  URL_BASE + b'showETA=yes&maneuverLayout=leftAligned',
    'right': URL_BASE + b'showETA=yes&maneuverLayout=rightAligned',
}


def xr(x0, x1, y0, y1):
    """Zone from pixel ranges (as written in the docs) to (x, y, w, h)."""
    return (x0, y0, x1 - x0, y1 - y0)


# Zone sets. Index order = view area index (see table above).
VARIANTS = {
    'OMONOB201': None,  # byte-identical original omonob 2.0.1 core.so
    # YANDEX-2026: zones by D., car-tested with Yandex Maps (default variant).
    'YANDEX-2026': dict(fps=30, eta=True, rects=[
        xr(214, 820, 55, 339),   # 0 idle (no route; shared by Left/Right/Off)
        xr(0, 692, 55, 339),     # 1 Left + route
        xr(346, 999, 55, 339),   # 2 Right + route
        xr(325, 685, 30, 349),   # 3 Center (with and without route)
        xr(42, 648, 16, 360),    # 4 Off + route (omonob value)
    ]),
}


def arm_imm(v):
    """ARM data-processing immediate (imm8 ror 2*rot) -> 12-bit field."""
    for rot in range(16):
        r = (2 * rot) % 32
        val = ((v << r) | (v >> (32 - r))) & 0xFFFFFFFF if r else v
        if val < 256:
            return (rot << 8) | val
    raise ValueError(v)


def pc_refs(d, target):
    """File offsets of 'ldr rX,[pc,#imm]' whose loaded value, added to pc by a
    following 'add rX,pc,rX', points at target (file offset == vaddr here)."""
    out = []
    for i in range(0, len(d) - 4, 4):
        w = struct.unpack_from('<I', d, i)[0]
        if (w & 0xFFFF0000) != 0xE59F0000:
            continue
        rd = (w >> 12) & 0xF
        lit = i + 8 + (w & 0xFFF)
        if lit + 4 > len(d):
            continue
        val = struct.unpack_from('<I', d, lit)[0]
        for j in range(i + 4, min(i + 48, len(d) - 4), 4):
            a = struct.unpack_from('<I', d, j)[0]
            if a == (0xE08F0000 | (rd << 16) | (rd << 12) | rd):
                if (j + 8 + val) & 0xFFFFFFFF == target:
                    out.append((i, j))
                break
    return out


def find(d):
    f = {}
    tbl = b''.join(struct.pack('<4i', *r) for r in ORIG_RECTS)
    assert d.count(tbl) == 1, 'view-area table not found exactly once'
    f['rects'] = d.index(tbl)
    assert pc_refs(d, f['rects']), 'view-area table is not referenced'
    for k, s in ORIG_URLS.items():
        z = s + b'\0'
        assert d.count(z) == 1, 'URL %s not found exactly once' % k
        f['url_' + k] = d.index(z)
        assert len(ETA_URLS[k]) <= len(s)
    key = d.index(b'\0maxFPS\0') + 1
    refs = pc_refs(d, key)
    assert len(refs) == 1, 'maxFPS key reference not unique'
    ldr, add = refs[0]
    movs = [o for o in range(ldr + 4, add, 4)
            if struct.unpack_from('<I', d, o)[0] & 0xFFFFFF00 == 0xE3A02000]
    assert len(movs) == 1, 'mov r2,#fps not found'
    f['fps'] = movs[0]
    f['fps_value'] = d[movs[0]]
    for name, val in (('widthPhysical', 202), ('heightPhysical', 75)):
        key = d.index(b'\0' + name.encode() + b'\0') + 1
        refs = pc_refs(d, key)
        assert len(refs) == 1, name + ' key reference not unique'
        ldr, add = refs[0]
        want = 0xE3A02000 | arm_imm(val)
        movs = [o for o in range(ldr + 4, add, 4) if struct.unpack_from('<I', d, o)[0] == want]
        assert len(movs) == 1, 'mov r2,#%d for %s not found' % (val, name)
        f[name] = movs[0]
    return f


def build(d, spec):
    f = find(d)
    b = bytearray(d)
    tbl = b''.join(struct.pack('<4i', *r) for r in spec['rects'])
    b[f['rects']:f['rects'] + len(tbl)] = tbl
    if spec['eta']:
        for k, s in ORIG_URLS.items():
            if k == 'top' and not spec.get('eta_top'):
                continue  # v3: Center (topAligned) keeps omonob's URL, no ETA
            o = f['url_' + k]
            b[o:o + len(s) + 1] = ETA_URLS[k].ljust(len(s) + 1, b'\0')
    assert 1 <= spec['fps'] <= 255
    b[f['fps']] = spec['fps']
    if spec.get('phys'):
        for name, val in zip(('widthPhysical', 'heightPhysical'), spec['phys']):
            struct.pack_into('<I', b, f[name], 0xE3A02000 | arm_imm(val))
    assert len(b) == len(d)
    return bytes(b)


def main():
    if sys.argv[1] == '--check':
        d = open(sys.argv[2], 'rb').read()
        print('sha256', hashlib.sha256(d).hexdigest())
        for k, v in find(d).items():
            print(k, v if k == 'fps_value' else hex(v))
        return
    src, outdir = sys.argv[1], sys.argv[2]
    d = open(src, 'rb').read()
    sha = hashlib.sha256(d).hexdigest()
    if sha != ORIG_SHA:
        print('warning: input is not omonob 2.0.1 MU1440/790 core.so (%s); patterns are still checked' % sha[:16])
    for name, spec in VARIANTS.items():
        out = d if spec is None else build(d, spec)
        os.makedirs(os.path.join(outdir, name), exist_ok=True)
        open(os.path.join(outdir, name, 'core.so'), 'wb').write(out)
        print('%-12s %s' % (name, hashlib.sha256(out).hexdigest()))


if __name__ == '__main__':
    main()
