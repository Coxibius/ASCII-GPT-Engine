import requests
import json
import os
import time
from tqdm import tqdm

# --- CONFIGURACIÓN V2.0 ---
UMBRAL_DENSIDAD = 0.20   
MIN_LINEAS = 6           
URL_FUENTE = "https://raw.githubusercontent.com/asweigart/asciiartjsondb/master/asciiartdb-asciiarteu.json"
ARCHIVO_SALIDA = "dataset_TRAVIAN_CLEAN_V2.txt" # <--- Archivo nuevo

def calcular_densidad(arte):
    total_chars = len(arte)
    if total_chars == 0: return 0
    tinta = len(arte.replace(' ', '').replace('\n', '').replace('\r', ''))
    return tinta / total_chars

def limpiar_texto(texto):
    # Quita barras de categorias tipo "animals/cats" -> "animals cats"
    return texto.replace('/', ' ').replace('_', ' ').strip()

def limpiar_y_guardar():
    print(f"⛏️  MINERO V2.0: Protocolo de Recuperación de Nombres...")
    
    print("⬇️  Descargando...")
    try:
        response = requests.get(URL_FUENTE)
        datos = response.json()
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    buffer_salida = []
    
    # Lista de textos prohibidos que indican que no hay descripción
    descripciones_inutiles = ["no description", "unknown", "untitled", "", "none"]

    for item in tqdm(datos, desc="Procesando"):
        arte = item.get('art', '')
        desc = item.get('desc', '').lower().strip()
        cat = item.get('category', '').lower().strip()
        
        # --- FILTROS DE CALIDAD ---
        if len(arte.split('\n')) < MIN_LINEAS: continue
        if calcular_densidad(arte) < UMBRAL_DENSIDAD: continue
        
        # --- LÓGICA DE NOMBRES INTELIGENTE ---
        # 1. ¿La descripción es útil?
        es_inutil = any(x in desc for x in descripciones_inutiles) or len(desc) < 3
        
        nombre_final = ""
        
        if not es_inutil:
            nombre_final = desc # Usamos la descripción original
        else:
            # Plan B: Usar la categoría
            # Si la categoría es "animals/dogs", el nombre será "animals dogs"
            if len(cat) > 2:
                nombre_final = limpiar_texto(cat)
            else:
                # Plan C: Si no hay nada de nada, inventamos un genérico
                nombre_final = "ascii art object"

        # Limpieza final del texto
        arte_limpio = arte.replace('\\n', '\n').replace('\\r', '').rstrip()
        
        bloque = (
            f"<|startoftext|>\n"
            f"User: Dibuja un ASCII art de {nombre_final}\n"
            f"AI:\n"
            f"{arte_limpio}\n"
            f"<|endoftext|>\n"
        )
        buffer_salida.append(bloque)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.writelines(buffer_salida)

    print(f"✅ ¡LISTO! Nuevo dataset generado: {ARCHIVO_SALIDA}")
    print(f"   Revisa si ahora tienen nombres como 'animals dragons' en lugar de 'No description'.")

if __name__ == "__main__":
    limpiar_y_guardar()