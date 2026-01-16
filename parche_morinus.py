#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# Definición de la función que se insertará al principio de los archivos
GET_SIZE_DEF = """
def get_size(font, text):
    b = font.getbbox(str(text))
    return (b[2] - b[0], b[3] - b[1])
"""

def patch_files():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file != "parche_morinus.py":
                path = os.path.join(root, file)
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                modified = False
                new_lines = []
                # Verificamos si ya tiene la función para no duplicarla
                has_get_size = any("def get_size(font, text):" in line for line in lines)

                for line in lines:
                    indent = re.match(r'\s*', line).group(0)
                    stripped = line.strip()
                    
                    # 1. Caso: draw.textsize(txt, font)
                    if "draw.textsize(" in stripped and not stripped.startswith("#"):
                        match = re.search(r'draw\.textsize\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)', stripped)
                        if match:
                            texto, fuente = match.group(1).strip(), match.group(2).strip()
                            new_lines.append(f"{indent}# {stripped}\n")
                            new_lines.append(f"{indent}w, h = get_size({fuente}, {texto})\n")
                            modified = True
                            continue

                    # 2. Caso: wx.EmptyImage
                    if "wx.EmptyImage(" in stripped and not stripped.startswith("#"):
                        new_lines.append(f"{indent}# {stripped}\n")
                        new_lines.append(line.replace("wx.EmptyImage", "wx.Image"))
                        modified = True
                        continue

                    # 3. Caso: tostring()
                    if ".tostring()" in stripped and not stripped.startswith("#"):
                        new_lines.append(f"{indent}# {stripped}\n")
                        new_lines.append(line.replace(".tostring()", ".tobytes()"))
                        modified = True
                        continue

                    # 4. Caso: wx.BitmapFromImage
                    if "wx.BitmapFromImage(" in stripped and not stripped.startswith("#"):
                        new_lines.append(f"{indent}# {stripped}\n")
                        new_lines.append(line.replace("wx.BitmapFromImage", "wx.Bitmap"))
                        modified = True
                        continue

                    # Si no coincide con nada, mantenemos la línea igual
                    new_lines.append(line)

                # Si el archivo fue modificado y no tenía get_size, lo insertamos arriba
                if modified:
                    if not has_get_size and any("get_size" in l for l in new_lines):
                        insert_idx = 0
                        for i, l in enumerate(new_lines):
                            if l.startswith("import ") or l.startswith("from "):
                                insert_idx = i + 1
                        new_lines.insert(insert_idx, GET_SIZE_DEF + "\n")

                    with open(path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Procesado: {path}")

if __name__ == "__main__":
    patch_files()
    print("\n¡Todo listo! Se han comentado las líneas antiguas y añadido las nuevas.")
