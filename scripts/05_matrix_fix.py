import os

def split_side_by_side_art(lines, min_gap=3): # <--- CAMBIO: Bajamos a 3 espacios de tolerancia
    if not lines:
        return [lines]

    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    
    empty_cols = []
    for col_idx in range(max_len):
        is_empty = True
        for line in padded_lines:
            if line[col_idx] != ' ':
                is_empty = False
                break
        empty_cols.append(is_empty)

    gaps = []
    current_gap_start = -1
    
    for i, is_empty in enumerate(empty_cols):
        if is_empty:
            if current_gap_start == -1:
                current_gap_start = i
        else:
            if current_gap_start != -1:
                gaps.append((current_gap_start, i))
                current_gap_start = -1
    if current_gap_start != -1:
        gaps.append((current_gap_start, len(empty_cols)))

    # Filtro: gaps válidos que no sean márgenes
    valid_split_gaps = [
        (start, end) for start, end in gaps 
        if (end - start) >= min_gap and start > 2 and end < (max_len - 2)
    ]

    if not valid_split_gaps:
        return [lines]

    split_gap = max(valid_split_gaps, key=lambda x: x[1]-x[0])
    cut_point = (split_gap[0] + split_gap[1]) // 2

    left_block = [line[:cut_point].rstrip() for line in padded_lines]
    right_block = [line[cut_point:].rstrip() for line in padded_lines]

    left_block = [l for l in left_block if l.strip()]
    right_block = [l for l in right_block if l.strip()]

    # Recursividad para separar múltiples dibujos (ej. los 3 gatos)
    return split_side_by_side_art(left_block, min_gap) + split_side_by_side_art(right_block, min_gap)


def process_final_fix(input_path, output_path):
    print(f"🚑 Aplicando Cirugía Final en: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    content = content.replace('\t', '    ')
    
    if "<|endoftext|>" in content:
        raw_blocks = content.split("<|endoftext|>")
    else:
        raw_blocks = content.split("\n\n\n")

    processed_data = []
    count = 0

    for block in raw_blocks:
        if not block.strip():
            continue

        lines = block.strip().split('\n')
        
        # --- EXTRACCIÓN INTELIGENTE ---
        prompt_line = ""
        art_lines = []
        
        # Buscamos la línea que empieza por User:
        user_lines = [l for l in lines if l.startswith("User:")]
        if user_lines:
            prompt_line = user_lines[0]
        else:
            # Si no hay User:, la primera línea es el prompt raw
            prompt_line = f"User: Dibuja un ASCII art de {lines[0]}"
        
        # Todo lo que NO sea User: ni AI: es dibujo
        for line in lines:
            if line.startswith("User:") or line.strip() == "AI:" or line.strip() == "AI":
                continue # Saltamos las etiquetas, solo queremos el dibujo
            art_lines.append(line)

        # Limpieza de líneas vacías al inicio
        while art_lines and not art_lines[0].strip():
            art_lines.pop(0)
            
        if not art_lines: continue

        # --- GUILLOTINA ---
        separated_arts = split_side_by_side_art(art_lines, min_gap=3)
        
        for art in separated_arts:
            if len(art) < 3: continue 
            
            # --- CONSTRUCCIÓN MATRIX ---
            entry = []
            entry.append("<|startoftext|>")
            entry.append(prompt_line)
            entry.append("AI:") # Aquí ponemos el AI: limpio
            
            # Ahora sí, el dibujo empieza con L01
            for i, line in enumerate(art):
                if i >= 60: break
                token = f"<L{i+1:02d}>"
                entry.append(f"{token}{line}") # <L01>   / \
            
            entry.append("<|endoftext|>")
            processed_data.append("\n".join(entry))
            count += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed_data))

    print(f"✅ Dataset V7 Ready.")
    print(f"   Total dibujos limpios: {count}")
    print(f"   Archivo: {output_path}")

if __name__ == "__main__":
    # Ajusta tu ruta de entrada al RAW original
    INPUT = "../dataset/dataset_v3_combined_raw.txt" 
    OUTPUT = "../dataset/dataset_v7_MATRIX_FINAL.txt"
    
    if not os.path.exists(INPUT):
        INPUT = "dataset_v3_combined_raw.txt"
        OUTPUT = "dataset_v7_MATRIX_FINAL.txt"
        
    process_final_fix(INPUT, OUTPUT)