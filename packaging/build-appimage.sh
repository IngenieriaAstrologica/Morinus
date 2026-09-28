#!/bin/bash
# Build the Morinus SE AppImage (x86_64) from this repo checkout.
# Usage: ./packaging/build-appimage.sh [output-dir]
# Requirements: python3, pip packages (wxPython, Pillow, numpy, pyinstaller),
#   FUSE (or it falls back to APPIMAGE_EXTRACT_AND_RUN for appimagetool).
set -e
cd "$(dirname "$0")/.."

OUTDIR="${1:-/tmp/opencode/appimage-build}"
VERSION="8.0.0"
ARCH="x86_64"
APPDIR="$OUTDIR/AppDir"
APPIMAGE="$OUTDIR/Morinus_SE-${VERSION}-${ARCH}.AppImage"

echo "==> [1/5] PyInstaller build"
pyinstaller --noconfirm morinus.spec

echo "==> [2/5] Assemble AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
cp -r dist/morinus/* "$APPDIR/usr/bin/"
# PyInstaller 6 places datas under _internal/, but the app chdir()s to the
# exe dir and uses relative paths (Res/, SWEP/). Bridge with symlinks.
ln -sfn _internal/Res "$APPDIR/usr/bin/Res"
ln -sfn _internal/SWEP "$APPDIR/usr/bin/SWEP"
cp packaging/AppRun "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"
cp packaging/morinus.desktop "$APPDIR/morinus.desktop"
python3 -c "
from PIL import Image
im = Image.open('Res/MorinusSE.ico').convert('RGB').resize((128, 128))
im.save('$APPDIR/morinus.png')
im.save('$APPDIR/.DirIcon', format='PNG')
print('icon ok')
"

echo "==> [3/5] appimagetool"
TOOL="$OUTDIR/appimagetool-${ARCH}.AppImage"
if [ ! -x "$TOOL" ]; then
  curl -sL -o "$TOOL" "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-${ARCH}.AppImage"
  chmod +x "$TOOL"
fi

echo "==> [4/5] Generate AppImage"
cd "$OUTDIR"
ARCH="$ARCH" "$TOOL" AppDir "$APPIMAGE"

echo "==> [5/5] Done: $APPIMAGE"
ls -la "$APPIMAGE"
