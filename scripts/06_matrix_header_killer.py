import os
import re

def is_pure_text_line(line):
    """
    Detecta si una línea es puramente texto (letras y espacios) 
    sin caracteres de dibujo ASCII (/ \ | _).
    Esto sirve para matar títulos repetidos al inicio.
    """
    # Si la línea tiene caracteres típicos de ASCII art, NO es texto puro
    if re.search(r'[\\/\|_\-\(\)\[\]]', line):
        return False
    # Si solo tiene letras, números y espacios, ES texto puro (basura para el dibujo)
    if re.match(r'^[a-zA-Z0-9\s]+$', line):
        return True
    return False

def split_side_by_side_art(lines, min_gap=3):
    # (Misma función de guillotina de antes, la mantenemos porque funciona bien)
    if not lines: return [lines]
    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    empty_cols = []
    for col_idx in range(max_len):
        is_empty = True
        for line in padded_lines:
            if line[col_idx] != ' ':
                is_empty = False; break
        empty_cols.append(is_empty)
    gaps = []
    current_gap_start = -1
    for i, is_empty in enumerate(empty_cols):
        if is_empty:
            if current_gap_start == -1: current_gap_start = i
        else:
            if current_gap_start != -1:
                gaps.append((current_gap_start, i)); current_gap_start = -1
    if current_gap_start != -1: gaps.append((current_gap_start, len(empty_cols)))
    valid_split_gaps = [(s, e) for s, e in gaps if (e-s)>=min_gap and s>2 and e<(max_len-2)]
    if not valid_split_gaps: return [lines]
    split_gap = max(valid_split_gaps, key=lambda x: x[1]-x[0])
    cut_point = (split_gap[0] + split_gap[1]) // 2
    left = [l[:cut_point].rstrip() for l in padded_lines]
    right = [l[cut_point:].rstrip() for l in padded_lines]
    left = [l for l in left if l.strip()]
    right = [l for l in right if l.strip()]
    return split_side_by_side_art(left, min_gap) + split_side_by_side_art(right, min_gap)

def process_header_killer(input_path, output_path):
    print(f"🔪 Ejecutando Header Killer en: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    content = content.replace('\t', '    ') # Tab to spaces
    
    if "<|endoftext|>" in content:
        raw_blocks = content.split("<|endoftext|>")
    else:
        raw_blocks = content.split("\n\n\n")

    processed_data = []
    
    for block in raw_blocks:
        if not block.strip(): continue
        lines = block.strip().split('\n')
        
        # --- 1. EXTRACCIÓN DEL PROMPT ---
        # Asumimos que la PRIMERA línea del bloque SIEMPRE es el título/prompt
        raw_title = lines[0].strip()
        
        # Formateamos el prompt
        if "User:" in raw_title:
            final_prompt = raw_title
        else:
            final_prompt = f"User: Dibuja un ASCII art de {raw_title}"

        # --- 2. FILTRADO AGRESIVO ---
        art_lines = []
        
        # Empezamos a mirar desde la línea 1 (saltamos la 0 que es el título)
        potential_art = lines[1:]
        
        start_collecting = False
        
        for line in potential_art:
            clean_line = line.strip()
            
            # Saltamos etiquetas explícitas
            if clean_line == "AI:" or clean_line == "AI":
                continue
            if clean_line.startswith("User:"):
                continue
                
            # AGRESIVO: Si la línea es IGUAL al título original, es basura.
            # Ejemplo: <L01>Animals Birds Water
            if clean_line == raw_title:
                continue
            
            art_lines.append(line)

        # --- 3. LIMPIEZA INICIAL DEL DIBUJO ---
        # Eliminamos líneas vacías al inicio
        while art_lines and not art_lines[0].strip():
            art_lines.pop(0)

        # CHECK FINAL DE TEXTO:
        # Si la primera línea que sobrevivió es puro texto (sin símbolos de arte), bórrala.
        # Esto mata el caso de tu screenshot si se coló por alguna razón.
        if art_lines and is_pure_text_line(art_lines[0]):
            # print(f"DEBUG: Eliminando línea de texto basura: {art_lines[0]}")
            art_lines.pop(0)

        # Volver a limpiar vacíos por si acaso
        while art_lines and not art_lines[0].strip():
            art_lines.pop(0)

        if not art_lines: continue

        # --- 4. GUILLOTINA (Separar siameses) ---
        separated_arts = split_side_by_side_art(art_lines, min_gap=3)
        
        for art in separated_arts:
            if len(art) < 3: continue 
            
            # --- 5. MATRIX INJECTION ---
            entry = []
            entry.append("<|startoftext|>")
            entry.append(final_prompt)
            entry.append("AI:") 
            
            for i, line in enumerate(art):
                if i >= 60: break
                token = f"<L{i+1:02d}>"
                entry.append(f"{token}{line}")
            
            entry.append("<|endoftext|>")
            processed_data.append("\n".join(entry))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed_data))

    print(f"✅ Proceso Finalizado. Archivo limpio: {output_path}")

if __name__ == "__main__":
    # Ajusta rutas
    INPUT = "../dataset/dataset_v3_combined_raw.txt" 
    OUTPUT = "../dataset/dataset_v7_MATRIX_CLEANEST.txt"
    
    if not os.path.exists(INPUT):
        INPUT = "dataset_v3_combined_raw.txt"
        OUTPUT = "dataset_v7_MATRIX_CLEANEST.txt"
        
    process_header_killer(INPUT, OUTPUT)