#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

# Función que inyectaremos para medir textos (Pillow 10+)
GET_SIZE_DEF = """
def get_size(font, text):
    if font is None:
        return (0, 0)
    b = font.getbbox(str(text))
    return (b[2] - b[0], b[3] - b[1])
"""

def patch_files():
    # Regex para fuentes, sizers y toolbars
    regex_draw_ts = r'(\s*)([\w\s,]+)\s*=\s*draw\.textsize\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)'
    regex_font_gs = r'(\s*)([\w\s,]+)\s*=\s*([\w\.]+)\.getsize\s*\(\s*([^)]+)\s*\)'
    regex_fgsizer = r'(\s*)([\w\s,]+)\s*=\s*wx\.FlexGridSizer\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)'

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
                    indent = re.match(r'\s*', line).group(0)
                    stripped = line.strip()

                    if stripped.startswith("#"):
                        new_lines.append(line)
                        continue

                    # 1. Pillow: textsize / getsize
                    m1 = re.search(regex_draw_ts, line)
                    m2 = re.search(regex_font_gs, line)
                    m3 = re.search(regex_fgsizer, line)

                    if m1:
                        ind, vars, txt, fnt = m1.groups()
                        new_lines.append(f"{ind}# {stripped}\n")
                        new_lines.append(f"{ind}{vars.strip()} = get_size({fnt.strip()}, {txt.strip()})\n")
                        modified = True
                    elif m2:
                        ind, vars, fnt, txt = m2.groups()
                        new_lines.append(f"{ind}# {stripped}\n")
                        new_lines.append(f"{ind}{vars.strip()} = get_size({fnt.strip()}, {txt.strip()})\n")
                        modified = True
                    
                    # 2. wxPython: FlexGridSizer
                    elif m3:
                        ind, var_name, r, c = m3.groups()
                        new_lines.append(f"{ind}# {stripped}\n")
                        new_lines.append(f"{ind}{var_name.strip()} = wx.FlexGridSizer({r}, {c}, 0, 0)\n")
                        modified = True

                    # 3. wxPython: Sizer Flags (GROW/EXPAND vs ALIGN)
                    elif ("wx.GROW" in stripped or "wx.EXPAND" in stripped) and \
                         ("wx.ALIGN_CENTER_HORIZONTAL" in stripped or "wx.ALIGN_CENTRE_HORIZONTAL" in stripped):
                        new_lines.append(f"{indent}# {stripped}\n")
                        cleaned = line.replace("|wx.ALIGN_CENTER_HORIZONTAL", "").replace("|wx.ALIGN_CENTRE_HORIZONTAL", "")
                        new_lines.append(cleaned)
                        modified = True

                    # 4. wxPython: AddLabelTool -> AddTool (Soporte mejorado para argumentos)
                    elif ".AddLabelTool(" in stripped:
                        new_lines.append(f"{indent}# {stripped}\n")
                        # Quitamos los nombres de los argumentos para usar el orden posicional
                        new_line = line.replace(".AddLabelTool", ".AddTool")
                        new_line = new_line.replace("shortHelp=", "")
                        new_line = new_line.replace("longHelp=", "")
                        new_lines.append(new_line)
                        modified = True

                    # 5. wxPython: PreDialog System
                    elif "pre = wx.PreDialog()" in stripped:
                        new_lines.append(f"{indent}# {stripped}\n")
                        modified = True
                    elif "pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)" in stripped:
                        new_lines.append(f"{indent}# {stripped}\n")
                        new_lines.append(f"{indent}self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)\n")
                        modified = True
                    elif "pre.Create(" in stripped:
                        args_match = re.search(r'pre\.Create\((.*)\)', stripped)
                        if args_match:
                            args = args_match.group(1)
                            new_lines.append(f"{indent}# {stripped}\n")
                            new_lines.append(f"{indent}wx.Dialog.__init__(self, {args})\n")
                            modified = True
                    elif "self.PostCreate(pre)" in stripped:
                        new_lines.append(f"{indent}# {stripped}\n")
                        modified = True

                    # 6. Imágenes y compatibilidad general
                    elif "wx.EmptyImage(" in stripped:
                        new_lines.append(f"{indent}# {stripped}\n")
                        new_lines.append(line.replace("wx.EmptyImage", "wx.Image"))
                        modified = True
                    elif ".tostring()" in stripped:
                        new_lines.append(f"{indent}# {stripped}\n")
                        new_lines.append(line.replace(".tostring()", ".tobytes()"))
                        modified = True
                    elif "wx.BitmapFromImage(" in stripped:
                        new_lines.append(f"{indent}# {stripped}\n")
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
                    print(f"✔️ Corregido: {path}")

if __name__ == "__main__":
    patch_files()
    print("\n✅ ¡Parche integral corregido aplicado!")
