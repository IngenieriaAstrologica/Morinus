# CHANGELOG — Morinus SE

## [Sin publicar]

### Rendimiento
- **Direcciones primarias con clave dinámica (arco solar verdadero):** una
  lista completa (1620–1980 direcciones) pasa de ~6 min a ~20 s. El cálculo
  ya no recorre hora a hora, minuto a minuto y segundo a segundo; salta
  directamente cerca del día buscado y afina el segundo exacto. Los
  resultados coinciden con los del método anterior, con una diferencia
  máxima de 1–2 s por redondeo.
- **Carta natal más rápida:** la búsqueda de sizigia pasa de ~315 ms a ~5 ms
  por carta, y las salidas/puestas de astros solo se calculan al abrir su
  ventana, no con cada carta. Se hacen unas 5 veces menos consultas a las
  efemérides (2560 → 532), lo que se nota sobre todo con disco o caché fríos.

### Corregido (cálculo)
- Arco solar verdadero regresivo: en ciertos casos el programa se quedaba
  colgado; ahora termina y devuelve la fecha correcta.
- Clave dinámica con Sol natal por debajo de 120° y un arco que cruza una
  transición: devolvía fechas degeneradas; ahora son correctas.
- Clave ecuatorial (ascensión recta) con un objetivo fuera de 0–360°: daba
  0,0; ahora se normaliza antes de convertir.

### Idioma (i18n)
**Añadido**
- Restaurados los 6 idiomas del Morinus original (English, Magyar, Italiano,
  Français, Русский) en `mtexts.py`, manteniendo el español de la Edición
  Especial como idioma por defecto (`id 5`, `DEF_LANGID = 5`).
- Reabierta la entrada de menú Opciones → Lenguajes (`morin.py`).
- Aviso de reinicio (`NeedRestart`) en los 6 idiomas: el cambio de idioma se
  aplica al reiniciar.
- Entradas SE del menú de ayuda traducidas al inglés (`HEMSpecialEdition`,
  `HEMCampus`, `HEMLibros`, `HEMAprende`); el resto de idiomas reutiliza
  de momento los textos ingleses.
- Ayuda por idioma, con `helpEng.html` si no existe el fichero del idioma.

**Corregido**
- `langsdlg.py`: `langtexts[0]` devolvía la letra `E` (el antiguo
  `langtexts` era un `str`, no una tupla); ahora usa `getLangTxt()`.
- `options.py`: el `langid` leído de `Opts/languages.opt` se valida (rango
  0–5; si no es válido, se usa español).
- `mtexts.setLang()`: ya no fuerza `langid = 0`; acepta cualquier id válido
  y tolera valores corruptos.
- `morin.py`: el idioma elegido se guarda **siempre** al aceptar el diálogo,
  tenga o no activada la opción «guardado automático». Antes solo se guardaba
  con ella activada, así que al cerrar la app el idioma volvía a español.

### Preferencias en carpeta de solo lectura
- `options.py`: si `Opts/` no se puede escribir (por ejemplo, un AppImage
  montado en solo lectura), las preferencias se guardan en una carpeta de
  usuario: `$XDG_CONFIG_HOME/morinus-se/Opts` (normalmente
  `~/.config/morinus-se/Opts`) en Linux, o `%APPDATA%\MorinusSE\Opts` en
  Windows. Esa carpeta se rellena una sola vez con los `.opt` incluidos en
  el programa; los cambios posteriores en esos `.opt` no se aplican.
  Así se conservan el idioma y el resto de preferencias en el AppImage.

### Empaquetado
- `packaging/build-appimage.sh`: permisos correctos del `.desktop` y del
  `AppDir` (el empaquetado fallaba desde sistemas de archivos sin permisos
  POSIX).

### Migración
- Las opciones guardadas con la versión solo-español
  (`Opts/languages.opt = 0`) ahora se interpretan como inglés (`id 0`). Para
  volver a español: Opciones → Lenguajes → Español, aceptar y reiniciar.

### Limpieza del repositorio
- Desindexados 351 artefactos (`__pycache__/`, `*.pyc`, `*~`, `*.bckp`,
  `tags`); `.gitignore` ampliado (`*~`, `*.bckp`, `tags`, `dist/`,
  `build/`).
- `morinus.spec` actualizado al formato PyInstaller moderno.
- `README.md` bilingüe (ES/EN) optimizado para buscadores.
