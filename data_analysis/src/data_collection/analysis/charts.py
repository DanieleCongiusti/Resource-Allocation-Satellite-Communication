import os
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# =====================
# Configuration
# =====================
DATA_DIR = '/Users/iacopomassei/Downloads/CSV_NEW'  # directory containing the CSV files
Z_ALPHA = 1.645  # 90% confidence interval

VALID_N = [8, 16, 24, 32, 40]
VALID_K = [2, 3, 5, 10, 20, 50, 1000]

# Filename pattern: A_N_K.csv or T_N_K.csv
FILENAME_RE = re.compile(r'^(A|T)_(\d+)_(\d+)\.csv$')

# =====================
# Helpers
# =====================

def read_values(filepath: str) -> np.ndarray:
    """
    Reads a CSV file with a single header line and numeric values below.
    Values may be integers or floats with comma as decimal separator.
    """
    values = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Skip first line (metric name)
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        line = line.replace(',', '.')
        try:
            values.append(float(line))
        except ValueError:
            pass

    return np.array(values)


def mean_and_ci(values: np.ndarray):
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    ci = Z_ALPHA * std / np.sqrt(len(values))
    return mean, ci

# =====================
# Ask metric
# =====================

print("Select metric to plot:")
print("  A -> AVG Queue Length")
print("  T -> Throughput")
metric = input("Choice (A/T): ").strip().upper()

if metric not in ('A', 'T'):
    raise ValueError("Invalid choice. Use 'A' or 'T'.")

metric_name = 'AVG Queue Length' if metric == 'A' else 'Throughput'

# =====================
# Data loading
# =====================

# data[K][N] = (mean, ci)
data = defaultdict(dict)

for fname in os.listdir(DATA_DIR):
    match = FILENAME_RE.match(fname)
    if not match:
        continue

    ftype, N, K = match.groups()
    if ftype != metric:
        continue

    N = int(N)
    K = int(K)

    if N not in VALID_N or K not in VALID_K:
        continue

    values = read_values(os.path.join(DATA_DIR, fname))
    if len(values) < 2:
        continue

    mean, ci = mean_and_ci(values)
    data[K][N] = (mean, ci)

# =====================
# Plotting (Grouped Bar Chart)
# =====================

plt.figure(figsize=(12, 7))

# Setup assi
x_values = sorted(VALID_N)       # I gruppi sull'asse X (N)
color_values = sorted(data.keys()) # Le serie (K)
x_indices = np.arange(len(x_values))

# Configurazione larghezza barre
total_width = 0.8                   # Larghezza totale del gruppo di barre
num_series = len(color_values)
bar_width = total_width / num_series # Larghezza della singola barra

# Colori
cmap = plt.get_cmap('tab10')
colors = {val: cmap(i % cmap.N) for i, val in enumerate(color_values)}

for i, K in enumerate(color_values):
    means = []
    cis = []
    
    # Estraiamo i dati ordinati per N. Se mancano dati, mettiamo 0.
    for N in x_values:
        val = data.get(K, {}).get(N, (0, 0))
        means.append(val[0])
        cis.append(val[1])
    
    # Calcolo posizione barre per centrarle sul tick
    # Partiamo dal centro del tick (x_indices), ci spostiamo a sinistra di mezzo gruppo,
    # poi aggiungiamo l'offset per la barra corrente.
    offset = (i * bar_width) + (bar_width / 2) - (total_width / 2)
    positions = x_indices + offset

    plt.bar(
        positions, 
        means, 
        yerr=cis,           # Intervallo di confidenza
        width=bar_width, 
        label=f'K={K}',
        color=colors[K],
        capsize=4,          # "Cappello" sulla linea di errore
        alpha=0.9,
        edgecolor='black',  # Bordo nero per definire meglio le barre
        linewidth=0.5
    )

plt.xlabel('N', labelpad=10)
plt.ylabel(metric_name, labelpad=20)
plt.title(f'{metric_name}')
plt.xticks(x_indices, x_values) # Etichette asse X corrette
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()