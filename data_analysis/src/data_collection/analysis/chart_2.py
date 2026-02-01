import os
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# =====================
# Configuration & Path Fix
# =====================

def find_data_dir():
    """
    Trova la cartella 'data' in modo robusto, evitando duplicazioni nel percorso.
    Cerca risalendo le cartelle finché non trova la struttura corretta.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current = script_dir
    
    # 1. Risaliamo finché non troviamo "Resource_Allocator"
    while current != "/" and os.path.basename(current) != "Resource_Allocator":
        current = os.path.dirname(current)
    
    project_root = current
    
    # Se non trova Resource_Allocator (es. nome cartella diverso), fallback relativo
    if project_root == "/":
        # Tentativo relativo diretto: se siamo in charts/simulation/plots, risaliamo a data
        # Prova path comuni rispetto allo script
        candidates = [
            os.path.join(script_dir, "../data"),                      # Se script in plots/
            os.path.join(script_dir, "data"),                         # Se script in simulation/
            os.path.join(script_dir, "simulation", "data"),           # Se script in charts/
            os.path.abspath(os.path.join(script_dir, "../../../data_analysis/charts/simulation/data"))
        ]
        for path in candidates:
            if os.path.exists(path):
                return os.path.abspath(path), os.path.abspath(os.path.join(path, "../plots"))
        
        print("[CRITICAL ERROR] Impossibile trovare la root 'Resource_Allocator'.")
        return None, None
    
    # 2. Costruiamo il percorso pulito dalla root trovata
    data_dir = os.path.join(project_root, "data_analysis", "charts", "simulation", "data")
    output_dir = os.path.join(project_root, "data_analysis", "charts", "simulation", "plots")
    
    return data_dir, output_dir

# Setup Percorsi
DATA_DIR, OUTPUT_DIR = find_data_dir()

if DATA_DIR is None:
    exit(1)

# Creazione cartella output se non esiste
if not os.path.exists(OUTPUT_DIR):
    try:
        os.makedirs(OUTPUT_DIR)
    except OSError:
        pass # Ignora se esiste già

print(f"--- PATH CHECK ---")
print(f"DATA_DIR:   {DATA_DIR}")
print(f"OUTPUT_DIR: {OUTPUT_DIR}")
print(f"------------------")

Z_ALPHA = 1.645  # 90% confidence interval

VALID_N = [8, 16, 24, 32, 40]
VALID_K = [2, 3, 5, 10, 20, 50, 1000]

# Mappa metriche
METRICS_MAP = {
    "A": "AVG Queue Length",
    "T": "Throughput",
    "B": "avgBGrant",
    "Q": "avgAccumulatedQueueLength",
    "W": "avgWaitingTimeFrame"
}

# Regex
FILENAME_RE = re.compile(r'^(A|T|B|Q|W)_(\d+)_(\d+)\.csv$')

# =====================
# Helpers
# =====================

def read_values(filepath: str) -> np.ndarray:
    values = []
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        # Salta header
        for line in lines[1:]:
            line = line.strip().replace(',', '.')
            if line:
                try: values.append(float(line))
                except ValueError: pass
    except Exception as e:
        print(f"[WARN] Errore file {os.path.basename(filepath)}: {e}")
        return np.array([])
    return np.array(values)

def mean_and_ci(values: np.ndarray):
    if len(values) == 0: return 0.0, 0.0
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    ci = Z_ALPHA * std / np.sqrt(len(values))
    return mean, ci

def generate_plot(metric_code, metric_name, data_subset):
    if not data_subset: return

    # Filtra K presenti e validi
    present_ks = sorted([k for k in VALID_K if k in data_subset])
    if not present_ks: return

    plt.figure(figsize=(12, 7))
    x_values = sorted(VALID_N)
    x_indices = np.arange(len(x_values))
    
    total_width = 0.8                   
    bar_width = total_width / len(present_ks)
    cmap = plt.get_cmap('tab10')
    colors = {val: cmap(i % cmap.N) for i, val in enumerate(present_ks)}

    for i, K in enumerate(present_ks):
        means = []
        cis = []
        for N in x_values:
            val = data_subset.get(K, {}).get(N, (0, 0))
            means.append(val[0])
            cis.append(val[1])
        
        offset = (i * bar_width) + (bar_width / 2) - (total_width / 2)
        plt.bar(x_indices + offset, means, yerr=cis, width=bar_width, 
                label=f'K={K}', color=colors[K], capsize=4, alpha=0.9, edgecolor='black', linewidth=0.5)

    plt.xlabel('N (Number of nodes)', labelpad=10)
    plt.ylabel(metric_name, labelpad=20)
    plt.title(f'{metric_name} Analysis')
    plt.xticks(x_indices, x_values)
    plt.legend(title="K Parameter")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    filename = f"{metric_name.replace(' ', '_')}.png"
    save_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[PLOT] Creato: {filename}")

# =====================
# Main
# =====================

def main():
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Cartella dati NON trovata: {DATA_DIR}")
        return

    global_data = defaultdict(lambda: defaultdict(dict))
    files_found = 0

    # Lettura file
    for fname in os.listdir(DATA_DIR):
        match = FILENAME_RE.match(fname)
        if match:
            ftype, n_str, k_str = match.groups()
            N, K = int(n_str), int(k_str)

            if N in VALID_N and K in VALID_K:
                path = os.path.join(DATA_DIR, fname)
                values = read_values(path)
                if len(values) > 0:
                    mean, ci = mean_and_ci(values)
                    global_data[ftype][K][N] = (mean, ci)
                    files_found += 1

    print(f"Files CSV caricati: {files_found}")

    # Generazione
    for code, name in METRICS_MAP.items():
        if code in global_data:
            generate_plot(code, name, global_data[code])
        else:
            print(f"[INFO] Nessun dato per {name} ({code})")

    print(f"--- COMPLETATO ---")
    print(f"Grafici salvati in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()