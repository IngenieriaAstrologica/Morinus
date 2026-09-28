# Morinus SE — Software libre de astrología tradicional | Free Traditional Astrology Software

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.txt)
[![Python 3](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://www.python.org/)
[![wxPython](https://img.shields.io/badge/GUI-wxPython%204.x-orange.svg)](https://wxpython.org/)

**Morinus SE** es un programa libre de **astrología tradicional** basado en [Morinus](http://www.morinus.hu/) de Robert Nagy, con efemérides suizas de alta precisión (Swiss Ephemeris). Calcula cartas natales, **direcciones primarias** (Placidus, Regiomontanus, Campanus), **profecciones / atacires**, **firdaria**, revoluciones solares y lunares, tránsitos, direcciones secundarias, sinastría, estrellas fijas, partes arábigas, antiscia y dodecatemoria. Disponible en **6 idiomas** (español, inglés, húngaro, italiano, francés y ruso).

**Morinus SE** is a free **traditional astrology** program based on Robert Nagy's [Morinus](http://www.morinus.hu/), powered by high-precision Swiss Ephemeris. It computes natal charts, **primary directions** (Placidus, Regiomontanus, Campanus), **profections**, **firdaria**, solar and lunar returns, transits, secondary directions, synastry, fixed stars, arabic parts, antiscia and dodecatemoria. Available in **6 languages** (English, Spanish, Hungarian, Italian, French, Russian).

> Palabras clave / Keywords: astrología tradicional, traditional astrology, direcciones primarias, primary directions, profecciones, profections, atacires, firdaria, revolución solar, solar return, tránsitos, transits, sinastría, synastry, Swiss Ephemeris, software astrología libre, free astrology software, Morinus.

## Capturas / Screenshots

![Carta astral calculada con Morinus SE](Res/charts.png)
![Tablas de posiciones planetarias y direcciones primarias](Res/tables.png)

## Características / Features

- Carta natal, horaria, electiva y mundana (Natal, horary, electional and mundane charts).
- **Direcciones primarias** con métodos Placidus (semiarco y bajo el polo), Regiomontanus y Campanus, con claves Naibod, Cardan y Ptolomeo.
- **Atacires / profecciones** anuales y mensuales del C-12, **firdaria** (Bonatti y Al-Biruni).
- Revoluciones solares/lunares/planetarias, tránsitos exactos, direcciones secundarias directas y conversas.
- Estrellas fijas, partes arábigas, antiscia y contraantiscia, paralelos zodiacales, puntos medios, horas planetarias.
- Speculum tradicional, dignidades esenciales y accidentales, almutens de la carta y tópicos, sizigia y parte de la fortuna.
- Búsqueda de lugares online (GeoNames) y base de datos de lugares integrada.
- **6 idiomas conmutables**: English, Magyar, Italiano, Français, Русский, Español (edición SE en español por defecto).

## Instalación / Installation

### Dependencias / Requirements

- Python 3.11+
- wxPython 4.x (`pip install wxPython`)
- Pillow (`pip install Pillow`)
- NumPy (`pip install numpy`)
- Módulo C `sweastrology` incluido (ver `SWEP/src/`)

### Ejecutar / Run

```bash
cd "Morinus SE"
python morinus.py
```

### Compilar `sweastrology` (módulo C) / Build the C extension

Binarios precompilados incluidos: Linux 64-bit (`.so`) y Windows 32/64-bit (`.pyd`). Para recompilar en Linux:

```bash
cd SWEP/src
python setup.py build
cp build/lib.*/sweastrology*.so ../../
```

### Generar ejecutable / Build executable (PyInstaller)

```bash
pip install pyinstaller
pyinstaller morinus.spec
```

El ejecutable queda en `dist/morinus/`. Si se agregan dependencias nuevas y el `.exe` falla al arrancar, añadirlas a `hiddenimports` en `morinus.spec`.

## Idioma / Language

**ES:** Opciones → Lenguajes (`Shift+J`), elige idioma, guarda y **reinicia Morinus** para que los menús se reconstruyan.

**EN:** Options → Languages, pick a language, save and **restart Morinus** so menus are rebuilt.

| id | Idioma / Language | Ayuda / Help file |
|----|-------------------|-------------------|
| 0 | English (default upstream) | `Res/helpEng.html` |
| 1 | Magyar (Hungarian) | `helpEng.html` (fallback) |
| 2 | Italiano (Italian) | `helpEng.html` (fallback) |
| 3 | Français (French) | `helpEng.html` (fallback) |
| 4 | Русский (Russian) | `helpEng.html` (fallback) |
| 5 | Español — Spanish, **por defecto en SE** | `Res/helpEsp.html` |

> Nota de migración: las opciones guardadas con la versión solo-español (`Opts/languages.opt = 0`) ahora se interpretan como inglés. Selecciona Español una vez y reinicia.

## Estructura / Project layout

```
Morinus SE/
  morinus.py          # Punto de entrada / entry point
  morin.py            # Ventana principal (MFrame) / main window
  mtexts.py           # Textos en 6 idiomas / i18n strings (ES por defecto)
  mtexts.py-funciona  # Referencia original multi-idioma / upstream reference
  options.py          # Opciones y persistencia en Opts/*.opt
  langsdlg.py         # Diálogo de selección de idioma / language dialog
  astrology.py        # Envoltorio de Swiss Ephemeris / ephemeris wrapper
  SWEP/src/           # Fuente del módulo C sweastrology / C source
  SWEP/Ephem/         # Datos de efemérides / ephemeris data
  Res/                # Recursos, ayudas HTML e imágenes / resources
  Opts/               # Opciones guardadas / saved options
```

## Licencia / License

GNU General Public License v3 (GPLv3) — ver `LICENSE.txt`.

## Créditos / Credits

- Robert Nagy — Morinus original.
- Roberto Luporini (v7), Elías D. Molins (v8) — ediciones previas.
- Campus Astrología — Edición Especial SE.
- Javier JIPE — port a Python 3 / wxPython 4 y restauración multi-idioma.
