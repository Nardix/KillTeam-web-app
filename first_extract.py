import fitz  # PyMuPDF
from PIL import Image
import os
import json

with open('order.json', 'r') as f:
    order = json.load(f)

def mm_to_px(mm, dpi=300):
    return (mm / 25.4) * dpi

def estrai_schede_miste(pdf_path, output_folder, page_config):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # --- IMPOSTAZIONI GENERALI ---
    DPI = 300
    PAGE_W_MM = 210.02
    PAGE_H_MM = 297.01
    
    # --- TIPI DI LAYOUT ---
    layout_types = {
        # TIPO A: 4 schede orizzontali in colonna (120x70 mm)
        "120x70": {
            "card_w": 120,
            "card_h": 70,
            "rows": 4,
            "cols": 1,
            # Calcolo margini automatico
            "margin_x": (PAGE_W_MM - 120) / 2,      # 45.01 mm
            "margin_y": (PAGE_H_MM - (70 * 4)) / 2  # 8.505 mm
        },
        # TIPO B: 4 schede verticali in griglia 2x2 (70x120 mm)
        "70x120": {
            "card_w": 70,
            "card_h": 120,
            "rows": 2,
            "cols": 2,
            # Calcolo margini automatico
            "margin_x": (PAGE_W_MM - (70 * 2)) / 2,  # 35.01 mm
            "margin_y": (PAGE_H_MM - (120 * 2)) / 2  # 28.505 mm
        }
    }

    try:
        doc = fitz.open(pdf_path)
        print(f"\nPDF aperto: {os.path.basename(pdf_path)} ({len(doc)} pagine).")
    except Exception as e:
        print(f"Errore apertura PDF: {e}")
        return

    scheda_globale_count = 0

    for i, page in enumerate(doc):
        page_num = i + 1  
        
        # Determina il layout usando il dizionario creato dinamicamente per questo PDF
        layout_name = page_config.get(page_num)
        
        if not layout_name:
            # Se ci sono più pagine nel PDF rispetto a quelle dichiarate nel JSON le salta
            print(f"Pagina {page_num} ignorata (non dichiarata in order.json).")
            continue

        layout = layout_types[layout_name]
        
        print(f"Elaborazione Pagina {page_num} con layout {layout_name}...")

        # Renderizza pagina
        zoom = DPI / 72
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Converti i margini e dimensioni in pixel
        margin_left_px = mm_to_px(layout["margin_x"], DPI)
        margin_top_px = mm_to_px(layout["margin_y"], DPI)
        card_w_px = mm_to_px(layout["card_w"], DPI)
        card_h_px = mm_to_px(layout["card_h"], DPI)

        # Ciclo sulle righe e colonne
        for r in range(layout["rows"]):
            for c in range(layout["cols"]):
                
                # Calcolo coordinate ritaglio
                x = margin_left_px + (c * card_w_px)
                y = margin_top_px + (r * card_h_px)
                
                # Esegui crop
                crop_area = (x, y, x + card_w_px, y + card_h_px)
                card_img = img.crop(crop_area)
                
                scheda_globale_count += 1
                filename = f"{output_folder}/scheda_{scheda_globale_count:03d}_p{page_num}_{layout_name}.jpg"
                card_img.save(filename, quality=95)
                # print(f" -> Salvata: {filename}")

    print(f"\nFinito! Salvate {scheda_globale_count} schede in '{output_folder}'.")

input_folder = r"C:\Users\Antonio\Desktop\KillTeam_webapp\all_pdf"

# 1. Recupero la lista di tutti i file PDF presenti nella cartella
pdf_disponibili = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]

# Ordina gli elementi del json in base al valore "id"
# order.items() crea liste del tipo: ('nome_file', {'id': 1, 'layout': {'orizzontal': 3, 'vertical': 4}})
ordinati_per_id = sorted(order.items(), key=lambda item: item[1]['id'])

cnt = 0
# 3. Scorro i nomi estratti dal JSON in ordine
for nome_chiave, file_data in ordinati_per_id:
    
    file_trovato = None
    
    # 4. Cerco se 'nome_chiave' (es. murderwing) è contenuto in uno dei file PDF
    for pdf_corrente in pdf_disponibili:
        if nome_chiave.lower() in pdf_corrente.lower():
            file_trovato = pdf_corrente
            break  # Interrompe la ricerca appena trova il primo match
            
    if file_trovato:
        file_path = os.path.join(input_folder, file_trovato)
        cnt += 1
        
        # Estrai i conteggi per orizzontale e verticale
        layout_data = file_data.get("layout", {})
        num_orizzontali = layout_data.get("orizzontal", 0)
        num_verticali = layout_data.get("vertical", 0)
        
        # Crea il page_config dinamico per il file corrente
        dynamic_page_config = {}
        current_page = 1
        
        # Assegna le orizzontali
        for _ in range(num_orizzontali):
            dynamic_page_config[current_page] = "120x70"
            current_page += 1
            
        # Assegna le verticali
        for _ in range(num_verticali):
            dynamic_page_config[current_page] = "70x120"
            current_page += 1
        
        # Cartella di output univoca per mantenere ordine
        out_folder = "schede_finali_" + str(cnt)
        
        # Lancia l'estrazione
        estrai_schede_miste(file_path, output_folder=out_folder, page_config=dynamic_page_config)
    else:
        print(f"\n[ATTENZIONE] Nessun file PDF contiene la parola '{nome_chiave}'. Elemento saltato.")