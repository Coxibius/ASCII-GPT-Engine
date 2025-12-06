import os
import re

def process_raw_to_matrix(input_path, output_path):
    print(f"🧬 Procesando RAW desde: {input_path}")
    
    try:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Error: No encuentro el archivo. Revisa la ruta.")
        return

    # 1. ARREGLAR GEOMETRÍA: Convertir Tabs a 4 Espacios
    # Muchos ASCII arts antiguos usan tabs y al tokenizar se rompen.
    content = content.replace('\t', '    ')

    # 2. SEPARAR BLOQUES
    # Asumimos que el scraper separó los dibujos por doble salto de línea o <|endoftext|>
    # Si tu raw es un chorro de texto, intentamos dividir por dobles espacios vacíos.
    if "<|endoftext|>" in content:
        blocks = content.split("<|endoftext|>")
    else:
        blocks = content.split("\n\n\n") # Ajusta esto si tus dibujos están más pegados (ej: \n\n)

    processed_blocks = []
    count = 0

    for block in blocks:
        if not block.strip():
            continue

        lines = block.strip().split('\n')
        
        # Heurística para Raw Scrape:
        # Asumimos que la Línea 0 es el título/prompt (ej: "Animals Bats")
        # Y el resto es el dibujo.
        
        if len(lines) < 3: # Si tiene menos de 3 líneas, probablemente es basura
            continue

        prompt = lines[0].strip()
        art_lines = lines[1:]

        # Limpieza básica de líneas vacías al inicio del dibujo
        while art_lines and not art_lines[0].strip():
            art_lines.pop(0)

        # CONSTRUCCIÓN DEL BLOQUE MATRIX
        new_block = []
        new_block.append("<|startoftext|>")
        
        # Formateamos el prompt como instrucción
        if "User:" not in prompt:
            new_block.append(f"User: Dibuja un ASCII art de {prompt}")
        else:
            new_block.append(prompt)
            
        new_block.append("AI:")
        
        # Inyectar Tokens de Línea <L01>...
        for i, line in enumerate(art_lines):
            # Límite de seguridad: si un dibujo tiene más de 60 líneas, cortamos 
            # (para evitar que el modelo aprenda ruido infinito)
            if i >= 60: 
                break
                
            token = f"<L{i+1:02d}>" # <L01>, <L02>...
            new_block.append(f"{token}{line}")
            
        new_block.append("<|endoftext|>")
        
        processed_blocks.append("\n".join(new_block))
        count += 1

    # GUARDAR
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(processed_blocks))

    print(f"✅ Inyección completada.")
    print(f"   Dibujos procesados: {count}")
    print(f"   Archivo generado: {output_path}")
    print("   -> Sube este archivo a Kaggle para el entrenamiento.")

if __name__ == "__main__":
    # Ajusta las rutas según tu estructura de carpetas
    INPUT_FILE = "../dataset/dataset_v3_combined_raw.txt" 
    OUTPUT_FILE = "../dataset/dataset_v6_MATRIX_RAW.txt"
    
    # Truco para ejecutarlo desde la carpeta root o scripts
    if not os.path.exists(INPUT_FILE):
        # Intentar ruta local si se ejecuta desde la misma carpeta
        INPUT_FILE = "dataset_v3_combined_raw.txt"
        OUTPUT_FILE = "dataset_v6_MATRIX_RAW.txt"
        
    process_raw_to_matrix(INPUT_FILE, OUTPUT_FILE)