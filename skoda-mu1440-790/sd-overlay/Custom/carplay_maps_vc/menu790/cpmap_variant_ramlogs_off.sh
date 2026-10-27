#!/bin/ksh
S=/mnt/app/eso/hmi/engdefs/scripts/mqb
[ -s "$S/cpmap_variant_ramlogs.sh" ] || S=/net/mmx/mnt/app/eso/hmi/engdefs/scripts/mqb
/bin/ksh "$S/cpmap_variant_ramlogs.sh" off
exit $?
