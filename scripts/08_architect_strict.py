import os
import re

def count_leading_spaces(line):
    count = 0
    for char in line:
        if char == ' ':
            count += 1
        else:
            break
    return count

def get_vertical_tag(current_line, total_lines):
    if total_lines < 3: return "[MID]"
    ratio = current_line / total_lines
    if ratio <= 0.25: return "[TOP]"
    elif ratio >= 0.85: return "[BOT]"
    else: return "[MID]"

def process_gentle_architect(input_path, output_path):
    print(f"📐 Iniciando Arquitecto Suave (Preservando Geometría) en: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if "<|endoftext|>" in content:
        raw_blocks = content.split("<|endoftext|>")
    else:
        raw_blocks = content.split("\n\n")

    processed_data = []
    
    for block in raw_blocks:
        lines = block.strip().split('\n')
        if not lines: continue
        
        prompt_line = ""
        art_lines = []
        
        # --- 1. EXTRACCIÓN Y LIMPIEZA DE BUGS ---
        for line in lines:
            # Bug Fix: Ignorar etiquetas de sistema que se hayan colado en el texto
            if "<|startoftext|>" in line or "<|endoftext|>" in line:
                continue
                
            if "User:" in line:
                prompt_line = line
            elif "AI:" in line:
                continue 
            elif line.startswith("<L"):
                # Aquí está el truco: Limpiamos la etiqueta <Lxx> pero 
                # MANTENEMOS LOS ESPACIOS originales para contarlos
                # Regex: Quita <Lxx> del inicio
                clean_raw = re.sub(r'^<L\d+>', '', line)
                
                # Si la línea no está vacía, la guardamos
                if clean_raw.strip(): 
                    art_lines.append(clean_raw) # Guardamos con espacios
            elif line.strip():
                art_lines.append(line)

        if len(art_lines) < 2: continue

        # --- 2. CONSTRUCCIÓN DEL VECTOR ---
        new_block = []
        new_block.append("<|startoftext|>")
        new_block.append(prompt_line)
        new_block.append("AI:")
        
        total_lines = len(art_lines)
        
        for i, raw_content in enumerate(art_lines):
            line_num = i + 1
            if line_num > 60: break

            # A. ID de Línea
            token_line = f"<L{line_num:02d}>"
            
            # B. Zona Vertical
            token_zone = get_vertical_tag(line_num, total_lines)
            
            # C. Espaciado (Indentación)
            spaces = count_leading_spaces(raw_content)
            token_space = f"[S:{spaces:02d}]" # Siempre 2 dígitos
            
            # D. Contenido (Sin espacios al inicio, porque ya están en el token)
            final_content = raw_content.lstrip()
            
            # --- ENSAMBLAJE ---
            # Formato: <Lxx> [ZONA] [S:xx] Contenido
            vector_line = f"{token_line} {token_zone} {token_space} {final_content}"
            
            new_block.append(vector_line)

        new_block.append("<|endoftext|>")
        processed_data.append("\n".join(new_block))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed_data))

    print(f"✅ Dataset Vectorizado (Suave) listo.")
    print(f"   Archivo: {output_path}")

if __name__ == "__main__":
    # Asegúrate de apuntar al V7 MATRIX CLEANEST (el que salió de la guillotina)
    # y ajusta la ruta si es necesario (../dataset/...)
    INPUT = "../dataset/dataset_v8_MATRIX_CLEANEST.txt" 
    OUTPUT = "../dataset/dataset_v11_VECTOR_GENTLE.txt"
    
    if os.path.exists(INPUT):
        process_gentle_architect(INPUT, OUTPUT)
    else:
        # Fallback local
        process_gentle_architect("dataset_v8_MATRIX_CLEANEST.txt", "dataset_v11_VECTOR_GENTLE.txt")