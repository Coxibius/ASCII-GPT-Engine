import os

def split_side_by_side_art(lines, min_gap=4):
    """
    Detecta si hay dos dibujos pegados horizontalmente buscando 
    una columna vertical de espacios vacíos que atraviese todo el bloque.
    """
    if not lines:
        return [lines]

    # 1. Normalizar longitud de líneas (padding con espacios)
    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    
    # 2. Buscar columnas vacías (Ríos verticales)
    # Creamos una lista de booleanos: True si la columna 'i' es todo espacios en todas las filas
    empty_cols = []
    for col_idx in range(max_len):
        is_empty = True
        for line in padded_lines:
            if line[col_idx] != ' ':
                is_empty = False
                break
        empty_cols.append(is_empty)

    # 3. Encontrar el hueco más grande
    # Buscamos secuencias de True consecutivas
    gaps = []
    current_gap_start = -1
    
    for i, is_empty in enumerate(empty_cols):
        if is_empty:
            if current_gap_start == -1:
                current_gap_start = i
        else:
            if current_gap_start != -1:
                gaps.append((current_gap_start, i)) # (inicio, fin)
                current_gap_start = -1
    # Check final gap
    if current_gap_start != -1:
        gaps.append((current_gap_start, len(empty_cols)))

    # 4. Decidir si cortar
    # Filtramos gaps que sean lo suficientemente anchos (min_gap) 
    # y que no estén en los bordes extremos (ignoramos margen izq/der)
    valid_split_gaps = [
        (start, end) for start, end in gaps 
        if (end - start) >= min_gap and start > 2 and end < (max_len - 2)
    ]

    if not valid_split_gaps:
        return [lines] # No hay separación clara

    # Cortamos en el medio del gap más grande encontrado
    # (Solo hacemos un corte por pasada para simplificar, recursividad opcional)
    split_gap = max(valid_split_gaps, key=lambda x: x[1]-x[0])
    cut_point = (split_gap[0] + split_gap[1]) // 2

    left_block = [line[:cut_point].rstrip() for line in padded_lines]
    right_block = [line[cut_point:].rstrip() for line in padded_lines]

    # Limpieza: quitamos líneas vacías que hayan podido quedar
    left_block = [l for l in left_block if l.strip()]
    right_block = [l for l in right_block if l.strip()]

    # Recursividad: intentar separar más por si hay 3 dibujos
    return split_side_by_side_art(left_block) + split_side_by_side_art(right_block)


def process_and_cut(input_path, output_path):
    print(f"🪓 Iniciando Protocolo Guillotina en: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Estandarizar
    content = content.replace('\t', '    ')
    
    if "<|endoftext|>" in content:
        raw_blocks = content.split("<|endoftext|>")
    else:
        raw_blocks = content.split("\n\n\n")

    processed_data = []
    total_drawings = 0
    split_count = 0

    for block in raw_blocks:
        if not block.strip():
            continue

        lines = block.strip().split('\n')
        if len(lines) < 2: continue

        # Identificar Prompt y Dibujo
        prompt_line = lines[0]
        # Si la primera línea no es User/Prompt, asumimos que es el prompt del scrape
        if "User:" not in prompt_line:
            prompt_text = prompt_line
        else:
            prompt_text = prompt_line # Ya viene formateada

        # El resto es el dibujo
        art_lines = lines[1:]
        
        # Eliminar líneas vacías al inicio del dibujo
        while art_lines and not art_lines[0].strip():
            art_lines.pop(0)
            
        if not art_lines: continue

        # --- APLICAR GUILLOTINA ---
        # Detectar si hay dibujos lado a lado y separarlos
        separated_arts = split_side_by_side_art(art_lines)
        
        if len(separated_arts) > 1:
            split_count += 1

        # Procesar cada dibujo resultante (sea 1 o sean 2 cortados)
        for art in separated_arts:
            if len(art) < 3: continue # Dibujos muy pequeños (basura del corte)
            
            # Construir bloque Matrix
            entry = []
            entry.append("<|startoftext|>")
            # Aseguramos formato User: ...
            if "User:" not in prompt_text:
                entry.append(f"User: Dibuja un ASCII art de {prompt_text}")
            else:
                entry.append(prompt_text)
                
            entry.append("AI:") # El AI va solo en su línea
            
            # Inyectar Tokens
            for i, line in enumerate(art):
                if i >= 60: break # Limite vertical
                token = f"<L{i+1:02d}>"
                entry.append(f"{token}{line}")
            
            entry.append("<|endoftext|>")
            processed_data.append("\n".join(entry))
            total_drawings += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed_data))

    print(f"✅ Proceso completado.")
    print(f"   Dibujos encontrados (originales): {len(raw_blocks)}")
    print(f"   Casos de 'siameses' separados: {split_count}")
    print(f"   Total final de dibujos para training: {total_drawings}")
    print(f"   Archivo guardado: {output_path}")

if __name__ == "__main__":
    # Ajusta tu ruta aquí
    INPUT = "../dataset/dataset_v3_combined_raw.txt"
    OUTPUT = "../dataset/dataset_v7_MATRIX_SPLIT.txt"
    
    if not os.path.exists(INPUT):
        INPUT = "dataset_v3_combined_raw.txt" # Fallback local
        OUTPUT = "dataset_v7_MATRIX_SPLIT.txt"
        
    process_and_cut(INPUT, OUTPUT)