# CHANGELOG — Morinus SE

## [Sin publicar] — Rendimiento del cálculo

### Mejorado
- Direcciones primarias con clave dinámica (arco solar verdadero):
  de ~6 min a ~20 s en una lista completa (1620–1980 direcciones).
  `calcTrueSolarArc`/`calcTrueSolarArcRegressive` (`primdirs.py`) ahora
  saltan por elongación hasta el día objetivo (el Sol no supera
  1,15°/día), reutilizan posiciones solares en caché y localizan el
  segundo exacto por bisección en vez de barrer hora→min→seg con
  `Transits().day`. Resultados verificados contra el algoritmo anterior
  (1620 direcciones: idénticos o ±1–2 s por redondeo de segundo).
- `RiseSet` perezoso (`chart.py`, `risesetframe.py`): las salidas/puestas
  solo se calculan al abrir su ventana, no con cada carta.
- Búsqueda de sizigia (`syzygy.py`): salto grueso día/hora/min/seg más
  `swe_calc` ligero; de ~315 ms a ~5 ms por carta.
- Llamadas a efemérides por carta natal: 2560→532 `swe_calc_ut`,
  75→4 `swe_rise_trans` (decisivo con disco/caché fríos).

### Corregido
- `calcTrueSolarArcRegressive` se colgaba (bucle infinito) con ciertos
  arcos en transición; ahora termina con la fecha correcta.
- Clave dinámica con Sol natal <120° y arco con transición devolvía
  fechas degeneradas; ahora correctas.
- Clave ecuatorial (RA) con objetivo fuera de [0, 360): `ra2ecl`
  devolvía 0.0; ahora se normaliza antes de convertir.

## [Sin publicar] — Selección de idioma (i18n)

### Añadido
- Restaurados los 6 idiomas del Morinus original en `mtexts.py` (English,
  Magyar, Italiano, Français, Русский) manteniendo el español de la
  Edición Especial como idioma por defecto (`id 5`, `DEF_LANGID = 5`).
- Reabierta la entrada de menú Opciones → Lenguajes (`morin.py`).
- Aviso de reinicio (`NeedRestart`) en los 6 idiomas al cambiar de lengua:
  el cambio se aplica al reiniciar.
- Entradas SE del menú de ayuda traducidas al inglés
  (`HEMSpecialEdition`, `HEMCampus`, `HEMLibros`, `HEMAprende`); el resto de
  idiomas reutiliza temporalmente los textos ingleses.
- Ayuda por idioma con fallback a `helpEng.html` si el fichero no existe.

### Corregido
- `langsdlg.py`: `langtexts[0]` devolvía la letra `E` (el antiguo
  `langtexts` era un `str`, no una tupla); ahora usa `getLangTxt()`.
- `options.py`: el `langid` cargado desde `Opts/languages.opt` se valida
  (rango 0–5, con fallback a español).
- `mtexts.setLang()`: ya no fuerza `langid = 0`; acepta cualquier id
  válido y tolera valores corruptos.

### Migración
- Las opciones guardadas con la versión solo-español
  (`Opts/languages.opt = 0`) ahora se interpretan como inglés (`id 0`).
  Seleccionar Español una vez y reiniciar.

### Limpieza del repositorio
- Desindexados 351 artefactos (`__pycache__/`, `*.pyc`, `*~`, `*.bckp`,
  `tags`); `.gitignore` ampliado (`*~`, `*.bckp`, `tags`, `dist/`,
  `build/`).
- `morinus.spec` actualizado al formato PyInstaller moderno.
- `README.md` bilingüe (ES/EN) optimizado para buscadores.
