#!/bin/ksh
# MHI2-Carplay-Maps 790 v1 - switch MU1440/790 variants from the SD card.
# Usage: cpmap_variant.sh OMONOB|YANDEX11|YANDEX22|YANDEX33|YANDEX44|YANDEX55|GOOGLE11|GOOGLE22|show
# Changes only core.so, libcardshim.so, CLUSTER_ZOOM and VERSION inside
# /mnt/app/carplaymaps. "Restore factory files" still removes everything.
export PATH=/proc/boot:/bin:/usr/bin:/usr/sbin:/sbin:/mnt/app/armle/bin:/mnt/app/armle/sbin:/mnt/app/armle/usr/bin:/mnt/app/armle/usr/sbin:$PATH

WANT="$1"
fail() { echo "CPMAP_VARIANT_FAIL=$1"; exit 1; }

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

show() {
    echo "Installed: `cat "$ROOT/VERSION"`"
    if [ -s "$ROOT/libcardshim.so" ]; then echo "Instrument Cluster shim: on"; else echo "Instrument Cluster shim: off"; fi
    if [ -s "$ROOT/CLUSTER_ZOOM" ]; then echo "Card style (zoomFactor): `cat "$ROOT/CLUSTER_ZOOM"`"; else echo "Card style: default"; fi
    if [ -e "$ROOT/NO_RAM_LOGS" ]; then echo "RAM logs: OFF"; else echo "RAM logs: ON (original)"; fi
    ram_usage
}

# RAM disk fill level. df where available, otherwise the sum of file sizes
# against the 20 MB RAM disk (size reported by mathsls for these units).
ram_usage() {
    RD="$MMX/ramdisk"
    [ -d "$RD" ] || { echo "RAM disk: not found"; return 0; }
    DFPCT=""
    if df -k "$RD" >/dev/null 2>&1; then
        for tok in `df -k "$RD" 2>/dev/null`; do
            case "$tok" in *%) DFPCT="$tok" ;; esac
        done
    fi
    SUM=0
    for f in "$RD"/* "$RD"/*/*; do
        [ -f "$f" ] || continue
        line=`ls -ln "$f" 2>/dev/null` || continue
        set -- $line
        case "$5" in ''|*[!0-9]*) continue ;; esac
        SUM=$((SUM + $5 / 1024))
    done
    PCT=$((SUM * 100 / 20480))
    if [ -n "$DFPCT" ]; then
        echo "RAM disk used: $DFPCT (df); files $SUM KB of ~20480 KB = ~$PCT%"
    else
        echo "RAM disk used: ~$PCT% (files $SUM KB of ~20480 KB)"
    fi
}

if [ "$WANT" = show ]; then
    show
    exit 0
fi
case "$WANT" in OMONOB|YANDEX11|YANDEX22|YANDEX33|YANDEX44|YANDEX55|GOOGLE11|GOOGLE22) ;; *) fail "UNKNOWN_VARIANT_$WANT" ;; esac

grep -q libcardshim "$DIO" 2>/dev/null || fail "INSTALL_790_FROM_THIS_PACKAGE_FIRST"

SRC=""
if [ -n "${CPMAP_TEST_SD:-}" ]; then
    SRC="$CPMAP_TEST_SD/Custom/carplay_maps_vc/variants790/$WANT"
else
    for medium in /fs/sda0 /fs/sdb0 /net/mmx/fs/sda0 /net/mmx/fs/sdb0 /media/mp000 /media/mp001 /media/mp002; do
        if [ -s "$medium/Custom/carplay_maps_vc/variants790/$WANT/core.so" ]; then
            SRC="$medium/Custom/carplay_maps_vc/variants790/$WANT"
            break
        fi
    done
fi
[ -n "$SRC" ] && [ -s "$SRC/core.so" ] || fail "VARIANT_FILES_NOT_FOUND_ON_SD"
line=`ls -ln "$SRC/core.so" 2>/dev/null`; set -- $line
[ "$5" = 72794 ] || fail "CORE_SIZE_UNEXPECTED_$5"
[ -s "$SRC/VARIANT" ] || fail "VARIANT_LABEL_MISSING"
read LABEL < "$SRC/VARIANT"

if [ -n "${CPMAP_TEST_ROOT:-}" ]; then
    :
elif [ -n "$MMX" ]; then
    on -f mmx mount -uw /mnt/app >/dev/null 2>&1 || fail "APP_REMOUNT_FAILED"
else
    mount -uw /mnt/app >/dev/null 2>&1 || fail "APP_REMOUNT_FAILED"
fi

# core.so is mapped by the running dio_manager: write a new file and rename it over.
cp "$SRC/core.so" "$ROOT/core.so.new" || fail "CORE_COPY_FAILED"
line=`ls -ln "$ROOT/core.so.new" 2>/dev/null`; set -- $line
[ "$5" = 72794 ] || { rm -f "$ROOT/core.so.new"; fail "CORE_COPY_INCOMPLETE"; }
chmod 644 "$ROOT/core.so.new"

SHIM_NEW=no
if [ -s "$SRC/libcardshim.so" ]; then
    cp "$SRC/libcardshim.so" "$ROOT/libcardshim.so.new" || { rm -f "$ROOT/core.so.new"; fail "SHIM_COPY_FAILED"; }
    chmod 644 "$ROOT/libcardshim.so.new"
    SHIM_NEW=yes
fi

mv "$ROOT/core.so.new" "$ROOT/core.so" || fail "CORE_ACTIVATION_FAILED"
if [ "$SHIM_NEW" = yes ]; then
    mv "$ROOT/libcardshim.so.new" "$ROOT/libcardshim.so" || fail "SHIM_ACTIVATION_FAILED"
else
    rm -f "$ROOT/libcardshim.so"
fi
if [ -s "$SRC/CLUSTER_ZOOM" ]; then
    cp "$SRC/CLUSTER_ZOOM" "$ROOT/CLUSTER_ZOOM" && chmod 644 "$ROOT/CLUSTER_ZOOM"
else
    rm -f "$ROOT/CLUSTER_ZOOM"
fi
echo "V70-PLAINTEXT-TOOLBOX-1.2.2+$LABEL" > "$ROOT/VERSION"
sync 2>/dev/null || true

echo "CPMAP_VARIANT_OK=$LABEL"
show
echo "A full unit reboot is required (hold the power button ~10 s)."
exit 0
