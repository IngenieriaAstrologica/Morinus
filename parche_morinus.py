#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

GET_SIZE_DEF = """
def get_size(font, text):
    b = font.getbbox(str(text))
    return (b[2] - b[0], b[3] - b[1])
"""

def patch_files():
    # Expresión regular mejorada:
    # Captura CUALQUIER variable (wpl, hpl, etc.) antes del '='
    # Captura el texto (arg1) y la fuente (arg2) dentro de textsize
    regex_textsize = r'(\s*)([\w\s,]+)\s*=\s*draw\.textsize\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)'

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file != "parche_morinus.py":
                path = os.path.join(root, file)
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                modified = False
                new_lines = []
                has_get_size = any("def get_size(font, text):" in line for line in lines)

                for line in lines:
                    stripped = line.strip()
                    # Buscamos la coincidencia con la regex
                    match = re.search(regex_textsize, line)
                    
                    if match and not stripped.startswith("#"):
                        indent = match.group(1)      # Sangría
                        variables = match.group(2).strip() # Ej: "wpl, hpl"
                        texto = match.group(3).strip()     # Ej: "txt"
                        fuente = match.group(4).strip()    # Ej: "self.fntText"
                        
                        # Comentamos la línea original tal cual estaba
                        new_lines.append(f"{indent}# {stripped}\n")
                        # Creamos la nueva línea respetando las variables originales
                        new_lines.append(f"{indent}{variables} = get_size({fuente}, {texto})\n")
                        modified = True
                    
                    # --- Aquí mantenemos los otros parches de wx que ya funcionaban ---
                    elif "wx.EmptyImage(" in stripped and not stripped.startswith("#"):
                        new_lines.append(f"{re.match(r'\s*', line).group(0)}# {stripped}\n")
                        new_lines.append(line.replace("wx.EmptyImage", "wx.Image"))
                        modified = True
                    elif ".tostring()" in stripped and not stripped.startswith("#"):
                        new_lines.append(f"{re.match(r'\s*', line).group(0)}# {stripped}\n")
                        new_lines.append(line.replace(".tostring()", ".tobytes()"))
                        modified = True
                    elif "wx.BitmapFromImage(" in stripped and not stripped.startswith("#"):
                        new_lines.append(f"{re.match(r'\s*', line).group(0)}# {stripped}\n")
                        new_lines.append(line.replace("wx.BitmapFromImage", "wx.Bitmap"))
                        modified = True
                    else:
                        new_lines.append(line)

                if modified:
                    if not has_get_size and any("get_size" in l for l in new_lines):
                        insert_idx = 0
                        for i, l in enumerate(new_lines):
                            if l.startswith("import ") or l.startswith("from "):
                                insert_idx = i + 1
                        new_lines.insert(insert_idx, GET_SIZE_DEF + "\n")

                    with open(path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Corregido con variables dinámicas: {path}")

if __name__ == "__main__":
    patch_files()
    print("\n¡Hecho! Ahora se respetan los nombres de las variables (wpl, wsp, etc.).")
