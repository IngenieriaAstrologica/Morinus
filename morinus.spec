# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['morinus.py'],
    pathex=[],
    binaries=[],
    # Runtime data: the app chdir()s to the exe dir and uses relative
    # paths (Res/, SWEP/Ephem/). Hors/ (user charts) and Opts/ (user
    # config) are intentionally NOT bundled: Opts/ falls back to
    # defaults and Hors/ contains personal data.
    datas=[('Res', 'Res'), ('SWEP/Ephem', 'SWEP/Ephem')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='morinus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='morinus',
)
