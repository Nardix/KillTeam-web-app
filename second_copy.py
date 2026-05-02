import json
import shutil
import os

# --- IMPOSTAZIONI PERCORSI ---
# Inserisci il percorso della cartella principale dove si trovano le cartelle dei team
# Se esegui lo script dalla stessa cartella in cui sono salvate, puoi lasciare "."
base_folder = "."
output_folder = os.path.join(base_folder, "img")

with open("order.json", encoding="utf-8") as f:
    data = json.load(f)

order_names = list(data.keys())


def unisci_e_rinomina_immagini():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Creata cartella di destinazione: {output_folder}")

    existing_folders = [name for name in order_names if os.path.isdir(os.path.join(base_folder, name))]

    if not existing_folders:
        print("Nessuna cartella corrispondente ai nomi in order.json trovata.")
        return

    for cartella in existing_folders:
        cartella_path = os.path.join(base_folder, cartella)
        print(f"Elaborazione cartella: {cartella}...")

        range_info = data[cartella].get("range", {})
        start = range_info.get("start")
        end = range_info.get("end")
        
        contatore = start
        print(f"  Usando range: start={start}, end={end}")

        immagini = [f for f in os.listdir(cartella_path) if f.lower().endswith(".webp")]
        immagini.sort()

        for immagine in immagini:
            if end is not None and contatore > end:
                print(f"  Attenzione: troppi file in {cartella}. Ignoro {immagine} perché supera end={end}.")
                break
            
            src_path = os.path.join(cartella_path, immagine)
            nuovo_nome = f"{contatore}.webp"
            dest_path = os.path.join(output_folder, nuovo_nome)
            shutil.copy2(src_path, dest_path)
            contatore += 1

    print(f"\nOperazione completata! Immagini copiate nella cartella '{output_folder}'.")


if __name__ == "__main__":
    unisci_e_rinomina_immagini()
 