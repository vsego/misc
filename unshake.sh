#!/usr/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 file_path"
    exit 1
fi

odir="/tmp/unshake/"
mkdir -p "$odir"

iname="$(realpath "$1")"
oname="$(basename "$1")"

cd "$odir" &&
ffmpeg -i "$iname" -vf vidstabdetect=shakiness=10:accuracy=15 -f null - &&
ffmpeg -i "$iname" -vf vidstabtransform=smoothing=30:input="transforms.trf" "$oname" &&
rm -f transforms.trf
