import os
import re
import math

def count_leading_spaces(line):
    """Cuenta cuántos espacios hay al inicio de la línea"""
    count = 0
    for char in line:
        if char == ' ':
            count += 1
        else:
            break
    return count

def get_vertical_tag(current_line, total_lines):
    """Decide si estamos arriba, en medio o abajo"""
    if total_lines < 3:
        return "[MID]" # Dibujos muy pequeños son todo medio
    
    ratio = current_line / total_lines
    
    if ratio <= 0.25:
        return "[TOP]"
    elif ratio >= 0.85:
        return "[BOT]"
    else:
        return "[MID]"

def process_architect_dataset(input_path, output_path):
    print(f"📐 Iniciando Modo Arquitecto en: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Separar por bloques (usamos tu dataset limpio matrix split)
    if "<|endoftext|>" in content:
        raw_blocks = content.split("<|endoftext|>")
    else:
        raw_blocks = content.split("\n\n")

    processed_data = []
    
    for block in raw_blocks:
        if not block.strip(): continue
        
        lines = block.strip().split('\n')
        
        # Extraer Prompt y Dibujo
        prompt_line = ""
        art_lines = []
        
        for line in lines:
            # LIMPIEZA DE ETIQUETAS BASURA
            if "<|startoftext|>" in line or "<|endoftext|>" in line:
                continue # ¡Las ignoramos! No son parte del dibujo
                
            if "User:" in line:
                prompt_line = line
            elif "AI:" in line:
                continue 
            elif line.startswith("<L"):
                # Limpiamos el <Lxx> viejo
                clean = re.sub(r'<L\d+>', '', line).rstrip()
                # También limpiamos si se colaron etiquetas viejas
                clean = clean.replace("<|startoftext|>", "").replace("<|endoftext|>", "")
                if clean.strip():
                    art_lines.append(clean)
            elif line.strip():
                art_lines.append(line.rstrip())

        # Si no hay dibujo válido, saltamos
        if not art_lines or len(art_lines) < 2:
            continue

        # --- CONSTRUCCIÓN ARQUITECTO ---
        new_block = []
        new_block.append("<|startoftext|>")
        new_block.append(prompt_line)
        new_block.append("AI:") # Etiqueta estándar
        
        total_lines = len(art_lines)
        
        for i, line in enumerate(art_lines):
            line_num = i + 1
            if line_num > 60: break # Límite seguridad
            
            # 1. Calcular espacios iniciales (Indentación)
            leading_spaces = count_leading_spaces(line)
            
            # 2. Generar token de espacio [S:XX]
            # Solo ponemos token si hay espacios, si es 0 no ponemos nada
            space_token = f"[S:{leading_spaces:02d}]" if leading_spaces > 0 else ""
            
            # 3. Quitar los espacios reales del inicio (porque ya tenemos el token)
            content_line = line.lstrip()
            
            # 4. Calcular etiqueta vertical [TOP]/[MID]/[BOT]
            vert_tag = get_vertical_tag(line_num, total_lines)
            
            # 5. Armar la línea maestra
            # Formato: <L01> [TOP] [S:05] /\
            final_line = f"<L{line_num:02d}> {vert_tag} {space_token} {content_line}"
            
            # Corrección de espacios dobles si no hubo space_token
            final_line = final_line.replace("  ", " ")
            
            new_block.append(final_line)
            
        new_block.append("<|endoftext|>")
        processed_data.append("\n".join(new_block))

    # Guardar
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed_data))

    print(f"✅ Arquitectura completada.")
    print(f"   Archivo generado: {output_path}")

# Ejecutar sobre tu último dataset limpio (el que salió de la guillotina)
if __name__ == "__main__":
    INPUT = "../dataset/dataset_v8_MATRIX_CLEANEST.txt" # O el nombre que tengas
    OUTPUT = "../dataset/dataset_v9_ARCHITECT.txt"
    
    if os.path.exists(INPUT):
        process_architect_dataset(INPUT, OUTPUT)
    else:
        # Fallback local
        process_architect_dataset("dataset_v8_MATRIX_CLEANEST.txt", "dataset_v9_ARCHITECT.txt")