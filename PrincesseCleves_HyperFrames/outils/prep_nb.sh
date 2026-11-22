#!/bin/bash
# Pré-calcule le noir et blanc du prompt : grayscale(1) contrast(1.12) brightness(1.04) sepia(.08)
# (matrices CSS Filter Effects appliquées dans l'ordre, en sRGB, avec écrêtage entre chaque étape)
set -e
P="$1"   # dossier projet
GRAY="colorchannelmixer=rr=.2126:rg=.7152:rb=.0722:gr=.2126:gg=.7152:gb=.0722:br=.2126:bg=.7152:bb=.0722"
CB="lutrgb=r='clip(clip((val-127.5)*1.12+127.5,0,255)*1.04,0,255)':g='clip(clip((val-127.5)*1.12+127.5,0,255)*1.04,0,255)':b='clip(clip((val-127.5)*1.12+127.5,0,255)*1.04,0,255)'"
SEP="colorchannelmixer=rr=.95144:rg=.06152:rb=.01512:gr=.02792:gg=.97488:gb=.01344:br=.02176:bg=.04272:bb=.93048"
mkdir -p "$P/assets/nb"
for f in "$P"/assets/images_ia/*.jpg "$P"/assets/archives/*.jpg "$P"/assets/photos/*.jpg; do
  o="$P/assets/nb/$(basename "$f")"; [ -f "$o" ] && continue
  ffmpeg -v error -y -i "$f" -vf "format=rgb24,$GRAY,$CB,$SEP" -q:v 2 "$o"
done
for f in "$P"/assets/images_ia_detourees/*.png; do
  o="$P/assets/nb/$(basename "$f")"; [ -f "$o" ] && continue
  ffmpeg -v error -y -i "$f" -vf "format=rgba,$GRAY,$CB,$SEP" "$o"
done
for f in "$P"/assets/videos/*.mp4; do
  b=$(basename "$f" .mp4); case "$b" in pexels_bougies_extinction) continue;; esac
  o="$P/assets/nb/$b.mp4"; [ -f "$o" ] && continue
  ffmpeg -v error -y -i "$f" -vf "format=rgb24,$GRAY,$CB,$SEP,format=yuv420p" -c:v libx264 -preset slow -crf 15 -r 25 -g 25 -an -movflags +faststart "$o"
done
echo done
