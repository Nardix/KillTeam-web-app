"""
testing: script che random un'immagine e le parole associate 
"""

"""
if 1 parola dentro l'altra and stessa immagine coinvolta
    elimino una
"""

"""
if end-start == len(list)
    procedi
"""

"""
per ogni oggetto in ita2
    if gia elaborata
        skip
    end-start
    if end-start == list.length
        per ogni oggetto in list
            per ogni parola chiave
                quella parola conterra' start+indice_oggetto(o cnt)
"""

import json
import os
from collections import defaultdict
import re

with open('new_archivio.json', 'r') as f2:
    archivio_2 = json.load(f2)

# Utilizziamo defaultdict per creare automaticamente liste per le nuove chiavi
kt_map = defaultdict(list)

# Iteriamo correttamente spacchettando chiave (nome_oggetto) e valore (dati_oggetto)
for nome_oggetto, dati_oggetto in archivio_2.items():
    
    start = dati_oggetto.get("start")
    end = dati_oggetto.get("end")
    lista_agenti = dati_oggetto.get("list", [])
    
    diff = end - start + 1
    
    if diff == len(lista_agenti):
        print("elaborando " + str(nome_oggetto))
        cnt = 0
        for agent in lista_agenti:
            
            # Calcoliamo il numero dell'immagine una sola volta
            numero_img = start + cnt 
            # NOTA: se le immagini partono dal numero di 'start', cambia la riga sopra in: numero_img = start + cnt
            
            # Controlliamo l'estensione del file
            if os.path.isfile(f"img/{numero_img}.jpg"):
                nome_file = f"{numero_img}.jpg"
            else:
                nome_file = f"{numero_img}.png"
                
            # 2. Aggiungiamo l'immagine alla lista della parola chiave senza sovrascrivere
            for parola in agent.get("parole_chiavi", []):
                lower_parola = parola.lower()
                # Aggiungiamo l'immagine solo se non è già presente per quella parola chiave (evita duplicati)
                if nome_file not in kt_map[lower_parola]:
                    kt_map[lower_parola].append(nome_file)
            
            cnt += 1
    else:
        print("lunghezze differenti per l'oggetto " + str(nome_oggetto))
    
# Convertiamo di nuovo in un dizionario standard prima di esportarlo in JSON (opzionale ma consigliato)
kt_map_finale = dict(kt_map)

chiavi_da_rimuovere = set()
tutte_le_chiavi = list(kt_map_finale.keys())

for i in range(len(tutte_le_chiavi)):
    for j in range(len(tutte_le_chiavi)):
        
        if i == j:
            continue
            
        chiave1 = tutte_le_chiavi[i]  # La potenziale chiave più corta (es. "ciao")
        chiave2 = tutte_le_chiavi[j]  # La potenziale chiave più lunga (es. "ciao gelato")
        
        # 1. Creiamo il pattern per cercare 'chiave1' come parola intera.
        # re.escape() protegge eventuali caratteri speciali presenti nella parola chiave.
        pattern = r'\b' + re.escape(chiave1) + r'\b'
        
        # 2. Usiamo re.search() invece di 'in'
        if re.search(pattern, chiave2):
            
            # 3. Se la parola intera è presente, controlliamo se le liste di immagini coincidono
            if set(kt_map_finale[chiave1]).issubset(kt_map_finale[chiave2]):
                
                # Segniamo la chiave più corta per la rimozione
                chiavi_da_rimuovere.add(chiave1)

# Creiamo il dizionario pulito
kt_map_pulito = {k: v for k, v in kt_map_finale.items() if k not in chiavi_da_rimuovere}

print(f"Rimosse {len(chiavi_da_rimuovere)} chiavi ridondanti: {chiavi_da_rimuovere}")

# Carichiamo il file esistente archivio_ITA.js se esiste, altrimenti inizializziamo un dizionario vuoto
try:
    with open('archivio_ITA.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = {}

# Uniamo kt_map_pulito con existing_data
for key, value in kt_map_pulito.items():
    if key in existing_data:
        # Combiniamo le liste senza duplicati
        existing_data[key] = list(set(existing_data[key] + value))
    else:
        existing_data[key] = value

# Scriviamo il dizionario unito in archivio_ITA.js
with open('archivio_ITA.json', 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, indent=4, ensure_ascii=False)