#!/usr/bin/env python3
"""Rebuild variants790/*/core.so from the original omonob 1.2.2 MU1440/790 core.so.
Usage: python3 build_790_variants.py <original core.so> <output dir>
The original is payload/profiles/MU1440/790/core.so of omonob 1.2.2 (or variants790/OMONOB/core.so here)
(sha256 a4bb6ce6...); OMONOB is byte-identical to it, all other variants run at 30 fps.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_core as g

P = 'maps:/car/instrumentcluster'
ETA = P + '?showETA=yes'
VARIANTS = [  # name, (x, y, width, height), cluster URL (None = stock .../map), fps
    ('OMONOB',   (202, 16, 606, 344), None, 40),   # identical to the original omonob 1.2.2 core.so
    ('YANDEX11', (30, 41, 778, 292),  ETA, 30),    # default after Install 790
    ('YANDEX22', (65, 41, 743, 292),  ETA, 30),
    ('YANDEX33', (100, 41, 750, 292), ETA, 30),
    ('YANDEX44', (20, 41, 818, 292),  ETA, 30),
    ('YANDEX55', (100, 41, 710, 292), P + '?maneuverLayout=topAligned', 30),
    ('GOOGLE11', (65, 41, 743, 310),  ETA, 30),
    ('GOOGLE22', (45, 41, 750, 310),  ETA, 30),
]

if __name__ == '__main__':
    orig = open(sys.argv[1], 'rb').read()
    for name, zone, url, fps in VARIANTS:
        out = os.path.join(sys.argv[2], name)
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'core.so'), 'wb').write(g.build(orig, zone, fps, url))
        print(name, g.describe(open(os.path.join(out, 'core.so'), 'rb').read()))
