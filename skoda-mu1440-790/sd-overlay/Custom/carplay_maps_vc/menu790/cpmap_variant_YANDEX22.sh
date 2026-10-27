#!/bin/ksh
S=/mnt/app/eso/hmi/engdefs/scripts/mqb
[ -s "$S/cpmap_variant.sh" ] || S=/net/mmx/mnt/app/eso/hmi/engdefs/scripts/mqb
/bin/ksh "$S/cpmap_variant.sh" YANDEX22
exit $?
