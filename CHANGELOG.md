# CHANGELOG — Morinus SE

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
