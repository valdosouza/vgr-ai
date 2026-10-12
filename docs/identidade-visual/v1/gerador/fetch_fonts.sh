#!/bin/sh
# Fetches the three OFL fonts (TTF) the generator outlines into the SVGs.
# Run from this folder: sh fetch_fonts.sh && python3 build.py  (needs fonttools)
set -eu
mkdir -p fonts
get() { url=$(curl -sS -A "curl/8" "https://fonts.googleapis.com/css2?family=$1:wght@$2" | grep -o 'https://fonts.gstatic.com[^)]*' | head -1); curl -sS -o "fonts/$3.ttf" "$url"; }
get Atkinson+Hyperlegible+Next 700 atkinson-700; get Atkinson+Hyperlegible+Next 400 atkinson-400
get Figtree 800 figtree-800; get Figtree 400 figtree-400
get Lexend 600 lexend-600; get Lexend 400 lexend-400
