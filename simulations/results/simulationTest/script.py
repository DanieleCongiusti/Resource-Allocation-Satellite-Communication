import os
import csv
import re
from collections import defaultdict

# --- CONFIGURAZIONE ---
SOURCE_DIRECTORY = '.'       
OUTPUT_DIRECTORY = 'CSV'     

# Crea la cartella di destinazione
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

# Struttura dati
data_store = defaultdict(lambda: {'Throughput': [], 'AVGQLen': []})

# Regex per catturare N e K dai file del tipo "$N=12, $K=1000-0.sca"
filename_pattern = re.compile(r'\$N=(\d+).*?\$K=(\d+)')

print(f"--- INIZIO ELABORAZIONE ---")
count_files = 0
found_any_stat = False
debug_first_stats = [] # Per diagnosticare se non trova nulla

# 1. Scansione File
for filename in os.listdir(SOURCE_DIRECTORY):
    if filename.endswith(".sca"):
        match = filename_pattern.search(filename)
        if match:
            n_val = match.group(1)
            k_val = match.group(2)
            config_key = (n_val, k_val)
            
            filepath = os.path.join(SOURCE_DIRECTORY, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        # OMNeT++ scrive: scalar "path" "NomeStatistica" Valore
                        if line.startswith("scalar"):
                            parts = line.split()
                            if len(parts) >= 3:
                                stat_value = parts[-1]        # L'ultimo pezzo è il valore
                                stat_name_raw = parts[-2]     # Il penultimo è il nome (es: "ThrouputStat:last")
                                
                                # Salviamo i primi nomi che incontriamo per debug
                                if len(debug_first_stats) < 5:
                                    debug_first_stats.append(stat_name_raw)

                                # Cerca "ThrouputStat:last" (rimuovendo le virgolette se ci sono)
                                clean_name = stat_name_raw.strip('"')

                                if clean_name == "throughputStat:last":
                                    data_store[config_key]['Throughput'].append(stat_value)
                                    found_any_stat = True
                                
                                elif clean_name == "AvgQLStat:mean":
                                    data_store[config_key]['AVGQLen'].append(stat_value)
                                    found_any_stat = True
                                    
            except Exception as e:
                print(f"Errore leggendo file {filename}: {e}")
            
            count_files += 1

print(f"File analizzati: {count_files}")

if not found_any_stat and count_files > 0:
    print("\n⚠️ ATTENZIONE: Non ho trovato le statistiche richieste.")
    print(f"Ecco alcuni nomi di statistiche che ho trovato nei file: {debug_first_stats}")
    print("Controlla se sono leggermente diversi da 'ThrouputStat:last' e 'AVGQLen:mean'.\n")

# 2. Scrittura CSV
output_count = 0

for (n, k), stats in data_store.items():
    
    # Crea T_N_K.csv (Throughput)
    if stats['Throughput']:
        t_filename = f"T_{n}_{k}.csv"
        path = os.path.join(OUTPUT_DIRECTORY, t_filename)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['ThroughputStat:last']) 
            for val in stats['Throughput']:
                writer.writerow([val.replace('.', ',')])
        output_count += 1

    # Crea A_N_K.csv (AVGQLen)
    if stats['AVGQLen']:
        a_filename = f"A_{n}_{k}.csv"
        path = os.path.join(OUTPUT_DIRECTORY, a_filename)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['AVGQLen:mean'])
            for val in stats['AVGQLen']:
                writer.writerow([val.replace('.', ',')])
        output_count += 1

print(f"COMPLETATO: Generati {output_count} file nella cartella '{OUTPUT_DIRECTORY}'.")