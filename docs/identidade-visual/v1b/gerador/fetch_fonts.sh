#!/bin/sh
# Fetches the OFL font (TTF) the generator outlines into the SVGs (decision 255).
# Run from this folder: sh fetch_fonts.sh && python3 -B build.py  (needs fonttools)
set -eu
mkdir -p fonts
get() { url=$(curl -sS -A "curl/8" "https://fonts.googleapis.com/css2?family=$1:wght@$2" | grep -o 'https://fonts.gstatic.com[^)]*' | head -1); curl -sS -o "fonts/$3.ttf" "$url"; }
get Atkinson+Hyperlegible+Next 800 atkinson-800
get Atkinson+Hyperlegible+Next 400 atkinson-400
