import re
import os

# --- TU LISTA DE FIRMAS (La pegas tal cual la tienes) ---
signatures = [
    r'\bjgs\b', r'\bmga\b', r'\bvk\b', r'\bgl\b', r'\bunknown\b',
    r'\bak\b', r'\bap\b', r'\bab\b', r'\bad\b', r'\bag\b', r'\bah\b', r'\bahk\b',
    r'\bakn\b', r'\bamer\b', r'\baos\b', r'\bapc\b', r'\bapx\b', r'\barm\b', r'\barv\b',
    r'\bas\b', r'\bash\b', r'\bast\b', r'\batc\b', r'\baw\b', r'\bazc\b', r'\bctr\b',
    r'\bdrs\b', r'\bdrS\b', r'\bheia\b', r'\bhm\b', r'\bilmk\b', r'\bmuserna\b',
    r'\bseal\b', r'\bbf\b', r'\bR\b', r'\bbthomas\b', r'\bberna\b', r'\bbg\b', r'\bbkn\b',
    r'\bblgm\b', r'\bbmw\b', r'\bbni\b', r'\bboba\b', r'\bbodom\b', r'\bbp\b', r'\bbug\b',
    r'\bgrh\b', r'\blbm\b', r'\bmbfh\b', r'\bbn\b', r'\bwfct\b', r'\bcat\b', r'\bceejay\b',
    r'\bcf\b', r'\bcfbd\b', r'\bcgmm\b', r'\bchev\b', r'\bcjr\b', r'\bcml\b', r'\bcvn\b',
    r'\bcww\b', r'\bktj\b', r'\bdg\b', r'\bdan hunt\b', r'\bdb\b', r'\bdcau\b', r'\bdd\b',
    r'\bdew\b', r'\bdm\b', r'\bdmr\b', r'\bdp\b', r'\bdrs\b', r'\bdrx\b', r'\bds\b',
    r'\bdsi\b', r'\bdski\b', r'\bdwb\b', r'\bjek\b', r'\bnick\b', r'\bnm\b', r'\bxemu\b',
    r'\bzi\b', r'\bemj\b', r'\berik\b', r'\betf\b', r'\btargon\b', r'\bfp\b', r'\bcatalyst\b',
    r'\bfk\b', r'\bfl\b', r'\bfrm\b', r'\bmik\b', r'\balf\b', r'\bgan\b', r'\bgc\b',
    r'\bgfj\b', r'\bggn\b', r'\bgnv\b', r'\bgpyy\b', r'\bgrp\b', r'\bha\b', r'\bhebu\b',
    r'\bhf\b', r'\bhh\b', r'\bhjm\b', r'\bhjw\b', r'\bhrr\b', r'\bhs\b', r'\bmrf\b',
    r'\bosfa\b', r'\bie\b', r'\bijd\b', r'\bitz\b', r'\bjav\b', r'\bjf\b', r'\bbger\b',
    r'\bbrainchild\b', r'\bfloyd\b', r'\bgoodwin\b', r'\bind\b', r'\biwo\b', r'\bjaa\b',
    r'\bjah\b', r'\bjal\b', r'\bjb\b', r'\bjf\b', r'\bjg\b', r'\bjgs\b', r'\bjim\b',
    r'\bjiri\b', r'\bjjs\b', r'\bjnh\b', r'\bjo\b', r'\bjoey\b', r'\bjon\b', r'\bjorn\b',
    r'\bjrd\b', r'\bjrei\b', r'\bjro\b', r'\bjrs\b', r'\bjs\b', r'\bjsdk\b', r'\bjurcy\b',
    r'\bjv\b', r'\bjw\b', r'\bjww\b', r'\bwny\b', r'\bcyberfox\b', r'\bdlk\b', r'\bkck\b',
    r'\bkg\b', r'\bkrg\b', r'\bklr\b', r'\bkm\b', r'\bko1\b', r'\bkostja\b', r'\bkrogg\b',
    r'\bkrr\b', r'\bkth\b', r'\bdc\b', r'\bejm\b', r'\bhawkeye\b', r'\bjulus\b', r'\blc\b',
    r'\blc\b', r'\bldb\b', r'\blds\b', r'\blgb\b', r'\blka\b', r'\blm\b', r'\blr\b',
    r'\bls\b', r'\bls\b', r'\blt\b', r'\blucc\b', r'\bluk\b', r'\bna\b', r'\bmjr\b',
    r'\b^^s\b', r'\bmk\b', r'\bdem\b', r'\bfsc\b', r'\bjittlov\b', r'\bkos\b', r'\bmk\b',
    r'\bm-k\b', r'\bm1a\b', r'\bmax\b', r'\bmb\b', r'\bmb\b', r'\bmc\b', r'\bmcr\b',
    r'\bmeph\b', r'\bmfj\b', r'\bmga\b', r'\bmgk\b', r'\bmh\b', r'\bmic\b', r'\bmjp\b',
    r'\bmmjb\b', r'\bmn\b', r'\bmrc\b', r'\bmrz\b', r'\bms\b', r'\bmt\b', r'\bmv\b',
    r'\bmx\b', r'\bsm\b', r'\bvalkyrie\b', r'\bhd\b', r'\bksr\b', r'\bnad\b', r'\bnc\b',
    r'\bncf\b', r'\bndt\b', r'\bpils\b', r'\bts\b', r'\bo!o\b', r'\bojo\b', r'\bo.s\b',
    r'\blf\b', r'\bbit\b', r'\bbrojek\b', r'\bbr\b', r'\bdew\b', r'\bpb\b', r'\bpch\b',
    r'\bpf\b', r'\bpgmg\b', r'\bphh\b', r'\bphs\b', r'\bpjb\b', r'\bpjl\b', r'\bpjp\b',
    r'\bpjy\b', r'\bpkw\b', r'\bpn\b', r'\bpr59\b', r'\bpru\b', r'\bps\b', r'\bpw\b',
    r'\btori\b', r'\bphoenix\b', r'\broy\b', r'\brb\b', r'\brg\b', r'\brjm\b', r'\brob\b',
    r'\brow\b', r'\brr\b', r'\brs\b', r'\bll\b', r'\bmelody\b', r'\bs@yan\b', r'\bsc\b',
    r'\bscesw\b', r'\bscs\b', r'\bsher^\b', r'\bsdm\b', r'\bsjm\b', r'\bsjw\b', r'\bsk\b',
    r'\bsl\b', r'\bsmd\b', r'\bsnd\b', r'\bspb\b', r'\bsps\b', r'\bsst\b', r'\bstef\b',
    r'\bsue\b', r'\bsusie\b', r'\bws\b', r'\bamc\b', r'\blester\b', r'\bdd\b', r'\bds\b',
    r'\bgr\b', r'\bpcs\b', r'\btal\b', r'\btantris\b', r'\btantris\b', r'\btbk\b', r'\bteb\b',
    r'\btis\b', r'\btk\b', r'\btt\b', r'\btl\b', r'\btm\b', r'\btr\b', r'\btvg\b', r'\bvg\b',
    r'\bvl\b', r'\bvj\b', r'\bvr\b', r'\bvw\b', r'\bwt\b', r'\bwb\b', r'\bwc\b', r'\bwj\b',
    r'\bwl\b', r'\bwm\b', r'\bwp\b', r'\bwt\b', r'\bwy\b', r'\bxl\b', r'\bxx\b', r'\byh\b',
    r'\bym\b', r'\byp\b', r'\bzs\b',
    # --- AGREGADOS MANUALES COMUNES EN TU DATASET ---
    r'by\s.*',       # Líneas que empiezan con "by ..."
    r'http\S+',      # URLs
    r'www\.\S+'      # Webs
]

print("🛠️  Compilando patrones de búsqueda...")
signature_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in signatures]

def is_signature_line(line):
    # Si la línea es muy larga (>25 chars), probablemente NO es una firma, es parte del dibujo
    if len(line.strip()) > 25: 
        return False
    # Si la línea está casi vacía, la ignoramos
    if len(line.strip()) < 2:
        return False
        
    for pattern in signature_patterns:
        if pattern.search(line):
            return True
    return False

# Nombres de archivo
input_file = 'dataset_FINAL_V3_READY.txt'
output_file = 'dataset_FINAL_V3_CLEANED.txt'

if not os.path.exists(input_file):
    print(f"❌ ERROR: No encuentro '{input_file}' en esta carpeta.")
    print("Asegúrate de poner el script en la misma carpeta que el .txt")
    exit()

print(f"📂 Leyendo {input_file}...")

# Leemos con 'utf-8' y 'replace' para evitar errores de caracteres raros
with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

blocks = re.split(r'<\|endoftext\|>', content)
cleaned_blocks = []
total_deleted_lines = 0
processed_blocks = 0

print(f"🧹 Iniciando limpieza de {len(blocks)} bloques de arte...")

for block in blocks:
    if not block.strip():
        continue
    
    # Procesar solo si tiene estructura de dibujo
    if 'AI:\n' in block:
        parts = block.split('AI:\n', 1)
        instruct = parts[0] + 'AI:\n'
        art = parts[1].rstrip() # Quitamos espacios finales
        
        art_lines = art.split('\n')
        cleaned_art_lines = []
        
        # Analizamos línea por línea
        for i, line in enumerate(art_lines):
            # Solo chequeamos las últimas 3 líneas
            if i >= len(art_lines) - 3: 
                if is_signature_line(line):
                    total_deleted_lines += 1
                    # print(f"   [Borrado]: {line.strip()}") # Descomenta para ver qué borra
                    continue 
            
            cleaned_art_lines.append(line)
            
        cleaned_art = '\n'.join(cleaned_art_lines)
        # Reconstruimos el bloque asegurando el token final
        cleaned_block = instruct + cleaned_art + '\n<|endoftext|>\n'
        cleaned_blocks.append(cleaned_block)
        processed_blocks += 1
    else:
        # Si no tiene AI:, lo guardamos tal cual (por si acaso)
        cleaned_blocks.append(block + '<|endoftext|>\n')

print("💾 Guardando archivo limpio...")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(''.join(cleaned_blocks))

print("="*40)
print(f"✅ ¡LIMPIEZA COMPLETADA!")
print(f"📊 Bloques procesados: {processed_blocks}")
print(f"🗑️ Firmas eliminadas: {total_deleted_lines}")
print(f"📁 Archivo listo para subir: {output_file}")
print("="*40)
print("¡A esto le llamo yo Higiene de Datos! 🧼")