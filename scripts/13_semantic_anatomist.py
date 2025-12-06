import os
import re

# --- DICCIONARIO DE ANATOMÍA ASCII V13 (MASTER EDITION) ---
# Cubre: Animales, Humanos, Armas, Edificios, Espacio, Naturaleza, Vehículos y Fantasía.

ANATOMY_PATTERNS = {
    # =========================================================
    # SECCIÓN 1-5: LO BÁSICO (Animales, Caras, Armas)
    # =========================================================
    "[EYES_COMPLEX]": [
        r"\(\s*['\"`^oO0e@*xX\-><]\s*[\._,;]*\s*['\"`^oO0e@*xX\-><]\s*\)", # (o.o)
        r"\[\s*['\"`^oO0e@*xX\-><]\s*[\._,;]*\s*['\"`^oO0e@*xX\-><]\s*\]", # [o.o]
        r"\(@+\)", r"\(O+\)", r"\(\s*oo\s*\)"
    ],
    "[EYES_SIMPLE]": [
        r"o\s+o", r"O\s+O", r"0\s+0", r"@\s+@", r"\*\s+\*", r"\^\s+\^",
        r"e\s+e", r"\.\s+\.", r"-\s+-", r"'\s+'", r"`\s+`"
    ],
    "[EARS]": [
        r"/\\_*/\\", r"\|\^\|", r"d\s*b", r"\(\s*\\/\s*\)", 
        r"\\\s*/", r"/\s+\\", r"/\)\s*\(\\"
    ],
    "[MOUTH/NOSE]": [
        r">\s*[\^.]\s*<", r"=\s*[\^.]\s*=", r"w", r"vv", r"\\_/", 
        r"_\s*_\s*_", r"\.\.\.", r"UU", r"\(\s*_\s*\)"
    ],
    "[ARMS/LEGS]": [
        r"/ \s+ \\", r"\|\s+\|", r"\\ \s+ /", r"_\)\s+\(_", r"/\s+/", r"\\\s+\\"
    ],
    "[PAWS/FEET]": [
        r"\(\"\)", r"\('\)", r"mm", r"MM", r"db", r"qp", r"L\s*L", r"_/\s*\\_"
    ],
    "[SWORD_BLADE]": [
        r"\|\|", r"\[\]", r"\{\}", r"\|:", r":\|", r"!!"
    ],
    "[SWORD_GUARD]": [
        r"_\+_", r"=\+=", r"\\\|\|/", r"//\|\|\\\\", r"\[\s*\]", r"~\+~"
    ],
    "[SWORD_HANDLE]": [
        r"\(\)", r"\[\]", r"0", r"O", r"T", r"X"
    ],

    # =========================================================
    # SECCIÓN 6: NATURALEZA (Árboles, Flores, Hongos)
    # =========================================================
    "[FLOWER_HEAD]": [
        r"\(@\)", r"\{@\}", r"\(\*\)", r"888", r"%%%"  # Flores
    ],
    "[LEAVES/BUSH]": [
        r"\{\{\{", r"\}\}\}", r"\*\*\*", r"###", r"%%% ", # Arbustos
        r"&", r"@@" 
    ],
    "[TRUNK/STEM]": [
        r"\|\|", r"\\|/", r"\|", r"\}|\{"             # Troncos y tallos
    ],
    "[MUSHROOM_CAP]": [
        r"/\s*-\s*\\", r"/\s*_\s*\\", r"\(\s*_\s*\)"  # Sombrero hongo
    ],

    # =========================================================
    # SECCIÓN 7: ESPACIO Y CIENCIA FICCIÓN (Aliens, Naves)
    # =========================================================
    "[STARS/SPACE]": [
        r"\s\.\s", r"\s\+\s", r"\s\*\s", r"\s`\s"      # Fondo estrellado
    ],
    "[ROCKET_BODY]": [
        r"/\s*\\", r"\|\s*\|", r"A", r"I\s*I"          # Fuselaje cohete
    ],
    "[FLAMES/EXHAUST]": [
        r"MMMMM", r"WWWWW", r"vvvv", r"^^^^", r"///"   # Fuego propulsor
    ],
    "[PLANET]": [
        r"\(\s*   \s*\)", r"O", r"o", r"@"             # Planetas redondos
    ],
    "[UFO_DOME]": [
        r"_\s*\.", r"\.-\.", r"\(.*\)", r"/ \s* \\"    # Cúpulas
    ],

    # =========================================================
    # SECCIÓN 8: ARQUITECTURA (Castillos, Casas)
    # =========================================================
    "[ROOF]": [
        r"/\s*\\", r"A", r"_\^___", r"______", r"~~~~" # Techos
    ],
    "[WALL/BRICK]": [
        r"\|__|\|", r"\[__\]", r"I\s*I", r"H", r"|_|"  # Ladrillos
    ],
    "[WINDOW]": [
        r"\[\s*\]", r"\[\+\]", r"\[-\]", r"\(\+\)"     # Ventanas
    ],
    "[TOWER_TOP]": [
        r"/\^\ \s", r"|A|", r"/\-\\"                   # Torres
    ],
    "[DOOR/GATE]": [
        r"/\|\|\\", r"|  |", r"|nn|", r"|OO|"           # Puertas (CORREGIDO EL BUG AQUÍ)
    ],

    # =========================================================
    # SECCIÓN 9: FANTASÍA (Dragones, Magia)
    # =========================================================
    "[DRAGON_WINGS]": [
        r"//\s*\\\\", r"/\.\.\.", r"_\)\s*\(_", 
        r"-\.--\.-", r"'\-\.", r"`._______"            # Alas membranosas
    ],
    "[SCALES/SKIN]": [
        r"vvv", r"^^^", r"uuu", r"ccc", r"nnn"         # Escamas
    ],
    "[CLAWS]": [
        r"VV", r"MM", r"W", r"M"                       # Garras afiladas
    ],
    "[SMOKE/MAGIC]": [
        r"\)\)\)", r"\(\(\(", r"sss", r"~~~"           # Humo
    ],

    # =========================================================
    # SECCIÓN 10: VEHÍCULOS Y VARIOS (Coches, Trenes)
    # =========================================================
    "[WHEEL]": [
        r"\(@\)", r"\(O\)", r"\(\*\)", r"O", r"o"      # Ruedas
    ],
    "[WINDSHIELD]": [
        r"/____\\", r"/    \\", r"|    |"              # Parabrisas
    ],
    "[BUMPER]": [
        r"______", r"======", r"------"                # Parachoques
    ],
    
    # ---------------------------------------------------------
    # FALLBACKS (Texturas generales)
    # ---------------------------------------------------------
    "[TEXTURE_SOLID]": [
        r"###", r"%%%", r"\$\$\$", r"@@@"
    ],
    "[TEXTURE_LIGHT]": [
        r":::", r"...", r",,,"
    ],
    "[BORDER]": [
        r"----", r"____", r"~~~~", r"====="
    ]
}

def detect_part(line_content):
    """Escanea la línea buscando órganos conocidos"""
    line_str = line_content.strip()
    
    for tag, patterns in ANATOMY_PATTERNS.items():
        for pattern in patterns:
            # Buscamos si el patrón existe en la línea
            if re.search(pattern, line_str):
                return tag
    
    return "[GENERIC]" # Si no reconocemos nada específico

def count_spaces(line):
    c = 0
    for char in line:
        if char == ' ': c += 1
        else: break
    return c

def get_zone(curr, total):
    if total < 3: return "[MID]"
    ratio = curr / total
    if ratio <= 0.25: return "[TOP]"
    elif ratio >= 0.85: return "[BOT]"
    else: return "[MID]"

def process_anatomy_dataset(input_path, output_path):
    print(f"🩻 Iniciando Escáner Anatómico en: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if "<|endoftext|>" in content:
        blocks = content.split("<|endoftext|>")
    else:
        blocks = content.split("\n\n")

    processed = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if not lines: continue
        
        prompt = ""
        art_lines = []
        
        # Extracción (Compatible con tus versiones anteriores)
        for line in lines:
            if "User:" in line: prompt = line
            elif "AI:" in line: continue
            elif "<|startoftext|>" in line or "<|endoftext|>" in line: continue
            elif line.startswith("<L"):
                # Limpiamos todo lo anterior para quedarnos con el dibujo raw + espacios
                # Quitamos <Lxx>, [TOP], [S:xx]...
                clean = re.sub(r'<L\d+>', '', line)
                clean = re.sub(r'\[.*?\]', '', clean) # Mata cualquier tag [Algo]
                if clean.rstrip(): # Si queda algo que no sea solo espacios
                    art_lines.append(clean) # Mantiene espacios izquierda
            elif line.strip():
                art_lines.append(line)

        if len(art_lines) < 2: continue

        # Construcción V13
        new_block = []
        new_block.append("<|startoftext|>")
        new_block.append(prompt)
        new_block.append("AI:")
        
        total = len(art_lines)
        
        for i, raw_line in enumerate(art_lines):
            line_num = i + 1
            if line_num > 60: break
            
            # 1. Metadatos
            zone_tag = get_zone(line_num, total)
            spaces = count_spaces(raw_line)
            space_tag = f"[S:{spaces:02d}]"
            
            # 2. ANÁLISIS SEMÁNTICO (El cerebro nuevo)
            # Analizamos el contenido sin espacios
            content = raw_line.strip()
            part_tag = detect_part(content)
            
            # 3. Ensamblaje
            # <L01> [TOP] [EYES] [S:05] (o.o)
            final_line = f"<L{line_num:02d}> {zone_tag} {part_tag} {space_tag} {content}"
            new_block.append(final_line)
            
        new_block.append("<|endoftext|>")
        processed.append("\n".join(new_block))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed))

    print(f"✅ Anatomía procesada. Dataset listo: {output_path}")

if __name__ == "__main__":
    # Ajusta la ruta a tu archivo más limpio (V7 o V11 Gentle)
    INPUT = "../dataset/dataset_v8_MATRIX_CLEANEST.txt"
    OUTPUT = "../dataset/dataset_v13_ANATOMY.txt"
    
    if os.path.exists(INPUT):
        process_anatomy_dataset(INPUT, OUTPUT)
    else:
        # Fallback local
        process_anatomy_dataset("dataset_v8_MATRIX_CLEANEST.txt", "dataset_v13_ANATOMY.txt")