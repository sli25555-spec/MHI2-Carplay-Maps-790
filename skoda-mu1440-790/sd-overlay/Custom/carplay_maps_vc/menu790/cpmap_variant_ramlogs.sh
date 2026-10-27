#!/bin/ksh
# CarPlay Maps VC - switch RAM-disk logs off/on (local test build for D.).
# Usage: cpmap_variant_ramlogs.sh off|on
# off: video/session logs go to /dev/null (flag file NO_RAM_LOGS read by the
#      dio_manager wrapper) and the cluster supervisor writes the MOST bridge
#      log to /dev/null (mathsls patch, offset 0x47c0).
# on:  original omonob behaviour.
# Install 790 from this package starts with RAM logs OFF.
# Works with any variant; variant switching does not touch it.
export PATH=/proc/boot:/bin:/usr/bin:/usr/sbin:/sbin:/mnt/app/armle/bin:/mnt/app/armle/sbin:/mnt/app/armle/usr/bin:/mnt/app/armle/usr/sbin:$PATH

WANT="$1"
fail() { echo "CPMAP_RAMLOGS_FAIL=$1"; exit 1; }
case "$WANT" in off|on) ;; *) fail "USAGE_off_or_on" ;; esac

if [ -n "${CPMAP_TEST_ROOT:-}" ]; then
    MMX="$CPMAP_TEST_ROOT"
elif [ -d /mnt/app ] && [ -s /ifs/lsd.jxe ]; then
    MMX=""
elif [ -d /net/mmx/mnt/app ]; then
    MMX="/net/mmx"
else
    fail "MMX_FILESYSTEM_NOT_FOUND"
fi
APP="$MMX/mnt/app"
ROOT="$APP/carplaymaps"
DIO="$APP/eso/bin/apps/dio_manager"

[ -s "$ROOT/VERSION" ] || fail "CARPLAY_MAPS_NOT_INSTALLED"
PROFILE=`cat "$ROOT/PROFILE" 2>/dev/null`
[ "$PROFILE" = "MU1440/790" ] || fail "ONLY_FOR_MU1440_790_PROFILE_($PROFILE)"
grep -q NO_RAM_LOGS "$DIO" 2>/dev/null || fail "INSTALL_790_FROM_THIS_SD_FIRST"
[ -s "$ROOT/carplay-cluster-supervisor" ] || fail "SUPERVISOR_NOT_INSTALLED"

SRC=""
if [ -n "${CPMAP_TEST_SD:-}" ]; then
    SRC="$CPMAP_TEST_SD/Custom/carplay_maps_vc"
else
    for medium in /fs/sda0 /fs/sdb0 /net/mmx/fs/sda0 /net/mmx/fs/sdb0 /media/mp000 /media/mp001 /media/mp002; do
        if [ -s "$medium/Custom/carplay_maps_vc/payload/common/carplay-cluster-supervisor.nolog" ]; then
            SRC="$medium/Custom/carplay_maps_vc"
            break
        fi
    done
fi
if [ "$WANT" = off ]; then SUP="$SRC/payload/common/carplay-cluster-supervisor.nolog"; else SUP="$SRC/payload/common/carplay-cluster-supervisor"; fi
[ -n "$SRC" ] && [ -s "$SUP" ] || fail "SUPERVISOR_FILE_NOT_FOUND_ON_SD"
line=`ls -ln "$SUP" 2>/dev/null`; set -- $line
[ "$5" = 56849 ] || fail "SUPERVISOR_SIZE_UNEXPECTED_$5"

if [ -n "${CPMAP_TEST_ROOT:-}" ]; then
    :
elif [ -n "$MMX" ]; then
    on -f mmx mount -uw /mnt/app >/dev/null 2>&1 || fail "APP_REMOUNT_FAILED"
else
    mount -uw /mnt/app >/dev/null 2>&1 || fail "APP_REMOUNT_FAILED"
fi

# The supervisor is running: write a new file and rename it over.
cp "$SUP" "$ROOT/carplay-cluster-supervisor.new" || fail "SUPERVISOR_COPY_FAILED"
line=`ls -ln "$ROOT/carplay-cluster-supervisor.new" 2>/dev/null`; set -- $line
[ "$5" = 56849 ] || { rm -f "$ROOT/carplay-cluster-supervisor.new"; fail "SUPERVISOR_COPY_INCOMPLETE"; }
chmod 755 "$ROOT/carplay-cluster-supervisor.new"
mv "$ROOT/carplay-cluster-supervisor.new" "$ROOT/carplay-cluster-supervisor" || fail "SUPERVISOR_ACTIVATION_FAILED"

if [ "$WANT" = off ]; then
    echo off > "$ROOT/NO_RAM_LOGS" || fail "FLAG_WRITE_FAILED"
    chmod 644 "$ROOT/NO_RAM_LOGS"
else
    rm -f "$ROOT/NO_RAM_LOGS"
fi
sync 2>/dev/null || true

if [ "$WANT" = off ]; then echo "CPMAP_RAMLOGS_OK=OFF"; else echo "CPMAP_RAMLOGS_OK=ON"; fi
echo "Variant is unchanged. A full unit reboot is required (hold the power button ~10 s)."
[ "$WANT" = off ] && echo "Note: the 'Save logs' menu will find no video/session logs while RAM logs are off."
exit 0
