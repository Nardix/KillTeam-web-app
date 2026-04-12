import shutil
import re
import os

# --- IMPOSTAZIONI PERCORSI ---
# Inserisci il percorso della cartella principale dove si trovano le tue "schede_finali_X"
# Se esegui lo script dalla stessa cartella in cui sono salvate, puoi lasciare "."
base_folder = "."  
output_folder = os.path.join(base_folder, "img")

def unisci_e_rinomina_immagini():
    # Crea la cartella "img" se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Creata cartella di destinazione: {output_folder}")

    # Trova tutte le cartelle che iniziano con "schede_finali_"
    cartelle = [f for f in os.listdir(base_folder) 
                if os.path.isdir(os.path.join(base_folder, f)) and f.startswith("schede_finali_")]

    if not cartelle:
        print("Nessuna cartella 'schede_finali_' trovata.")
        return

    # Funzione per estrarre il numero dal nome della cartella per un ordinamento corretto
    # Così 'schede_finali_2' viene prima di 'schede_finali_10'
    def estrai_numero_cartella(nome_cartella):
        match = re.search(r'\d+', nome_cartella)
        return int(match.group()) if match else 0

    # Ordina le cartelle numericamente
    cartelle_ordinate = sorted(cartelle, key=estrai_numero_cartella)

    contatore_globale = 1

    # Itera attraverso ogni cartella ordinata
    for cartella in cartelle_ordinate:
        cartella_path = os.path.join(base_folder, cartella)
        print(f"Elaborazione cartella: {cartella}...")

        # Trova tutte le immagini JPG nella cartella corrente
        immagini = [f for f in os.listdir(cartella_path) if f.lower().endswith(".jpg")]
        
        # Ordina le immagini alfabeticamente per mantenere l'ordine in cui sono state create
        immagini.sort()

        # Copia e rinomina ogni immagine
        for immagine in immagini:
            src_path = os.path.join(cartella_path, immagine)
            
            # Crea il nuovo nome usando il contatore globale
            nuovo_nome = f"{contatore_globale}.jpg"
            dest_path = os.path.join(output_folder, nuovo_nome)
            
            # Copia il file
            shutil.copy2(src_path, dest_path)
            
            contatore_globale += 1

    print(f"\nOperazione completata! {contatore_globale - 1} immagini copiate nella cartella '{output_folder}'.")

# Esecuzione dello script
unisci_e_rinomina_immagini()