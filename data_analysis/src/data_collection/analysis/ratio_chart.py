import os
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# =====================
# Configuration
# =====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../"))
INPUT_DATA_DIR = os.path.join(PROJECT_ROOT, "data_analysis", "charts", "simulation", "data")
BASE_PLOTS_DIR = os.path.join(PROJECT_ROOT, "data_analysis", "charts", "simulation", "plots")

VALID_N = [8, 16, 24, 32, 40]
VALID_K = [2, 3, 5, 10, 20, 50, 1000]

# Filename pattern: A_N_K.csv or T_N_K.csv
FILENAME_RE = re.compile(r'^(A|T)_(\d+)_(\d+)\.csv$')

# =====================
# Helpers
# =====================

def read_mean(filepath: str) -> float:
    values = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Salta la prima riga (header)
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        line = line.replace(',', '.')
        try:
            values.append(float(line))
        except ValueError:
            pass
    
    if not values:
        return None
    return np.mean(values)

# =====================
# Data Loading
# =====================

# Data structure: data[K][N] = {'T': valore_medio, 'A': valore_medio}
data = defaultdict(lambda: defaultdict(dict))

print("Loading data...")

for fname in os.listdir(INPUT_DATA_DIR):
    match = FILENAME_RE.match(fname)
    if not match:
        continue

    ftype, N_str, K_str = match.groups()
    N = int(N_str)
    K = int(K_str)

    if N not in VALID_N or K not in VALID_K:
        continue

    val_mean = read_mean(os.path.join(INPUT_DATA_DIR, fname))
    
    if val_mean is not None:
        data[K][N][ftype] = val_mean

# =====================
# Plotting (Ratio vs N)
# =====================

plt.figure(figsize=(10, 6))

# Ordiniamo i K per avere una legenda coerente e colori stabili
sorted_Ks = sorted(data.keys())

# Creiamo una mappa di colori
cmap = plt.get_cmap('tab10')
colors = {val: cmap(i % cmap.N) for i, val in enumerate(sorted_Ks)}

for K in sorted_Ks:
    xs = []
    ys = []

    sorted_Ns = sorted(data[K].keys())
    
    for N in sorted_Ns:
        metrics = data[K][N]
        
       
        if 'T' in metrics and 'A' in metrics:
            val_T = metrics['T']
            val_A = metrics['A']
            
            ratio = val_T / val_A
            
            xs.append(N)
            ys.append(ratio)
    
    if not xs:
        continue

    
    plt.plot(
        xs,
        ys,
        marker='o',
        linestyle='-',
        linewidth=2,
        markersize=6,
        color=colors[K],
        label=f'K={K}'
    )

plt.xlabel('N', labelpad=10)
plt.ylabel('Ratio (Avg Throughput / Avg Queue Length)', labelpad=20)
plt.title('Performance Ratio')
plt.legend()
plt.grid(axis='both', linestyle='--', alpha=0.5)
filename = f"ratio.png"
save_path = os.path.join(BASE_PLOTS_DIR, filename)
plt.savefig(save_path, dpi=300)