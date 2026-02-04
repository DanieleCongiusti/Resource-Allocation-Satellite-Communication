import os
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../"))
INPUT_DATA_DIR = os.path.join(PROJECT_ROOT, "data_analysis", "charts", "simulation", "data")
BASE_PLOTS_DIR = os.path.join(PROJECT_ROOT, "data_analysis", "charts", "simulation", "plots")

if not os.path.exists(BASE_PLOTS_DIR):
    try:
        os.makedirs(BASE_PLOTS_DIR)
    except OSError:
        pass

print(f"--- PATH CHECK ---")
print(f"INPUT_DATA_DIR:   {INPUT_DATA_DIR}")
print(f"BASE_PLOTS_DIR:   {BASE_PLOTS_DIR}")
print(f"------------------")

Z_ALPHA = 1.645  # 90% confidence interval

VALID_N = [8, 16, 24, 32, 40]
VALID_K = [2, 3, 5, 10, 20, 50, 1000]

METRICS_MAP = {
    "A": "Avg Queue Length",
    "T": "Avg Throughput",
    "B2": "Avg B=2 Grant",
    "B4": "Avg B=4 Grant",
    "B8": "Avg B=8 Grant",
    "B16": "Avg B=16 Grant",
    "BMinus1": "Avg B=-1 Grant",
    "W": "Avg Waiting Time",
    "M": "Avg exceedM Count"
}

# Regex
FILENAME_RE = re.compile(r'^(A|T|M|W|BMinus1|B\d+)_(\d+)_(\d+)\.csv$')

def read_values(filepath: str) -> np.ndarray:
    values = []
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        for line in lines[1:]:
            line = line.strip().replace(',', '.')
            if line:
                try: values.append(float(line))
                except ValueError: pass
    except Exception as e:
        print(f"[WARN] FILE ERROR {os.path.basename(filepath)}: {e}")
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

    plt.xlabel('N', labelpad=10)
    plt.ylabel(metric_name, labelpad=20)
    plt.title(f'{metric_name} Analysis')
    plt.xticks(x_indices, x_values)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    filename = f"{metric_name.replace(' ', '_')}.png"
    save_path = os.path.join(BASE_PLOTS_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[PLOT] Created: {filename}")

def generate_exceedM_plot(data_subset):
    fixed_N = 40
    target_Ks = [10, 20]
    
    # Verifica dati
    has_data = any(
        (k in data_subset and fixed_N in data_subset[k]) 
        for k in target_Ks
    )
    
    if not has_data:
        # Se vuoi evitare stampe se mancano i dati, puoi commentare la riga sotto
        # print(f"[INFO] No data for exceedM at N={fixed_N} with K={target_Ks}")
        return

    plt.figure(figsize=(8, 6))
    
    x_indices = np.arange(len(target_Ks))
    means = []
    cis = []
    
    for K in target_Ks:
        val = data_subset.get(K, {}).get(fixed_N, (0.0, 0.0))
        means.append(val[0])
        cis.append(val[1])

    colors = ['#d62728', '#1f77b4'] 

    # Plot delle barre
    plt.bar(x_indices, means, yerr=cis, width=0.5, 
            tick_label=[str(k) for k in target_Ks], 
            color=colors,
            capsize=5, alpha=0.9, edgecolor='black')

    plt.xlabel('K', labelpad=10)
    plt.ylabel('exceedM Count', labelpad=20)
    plt.title(f'exceedM Analysis (N={fixed_N}, Selected K)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # --- FIX POSIZIONAMENTO TESTO ---
    # Troviamo il massimo valore totale (barra + errore) per scalare il margine
    # Se means è vuoto o tutto zero, usiamo un default per evitare crash
    max_height = max([m + c for m, c in zip(means, cis)]) if means else 1.0
    if max_height == 0: max_height = 0.1 # Fallback se tutto è 0

    offset = max_height * 0.05  # Margine del 5% rispetto all'altezza massima

    for i, v in enumerate(means):
        error_val = cis[i]
        # La Y è: Media + Errore + Offset
        text_y = v + error_val + offset
        
        plt.text(i, text_y, f"{v:.2f}", 
                 ha='center', va='bottom', fontweight='bold', color='black')

    # Aumentiamo leggermente il limite Y del grafico per non tagliare il testo
    plt.ylim(top=max_height * 1.2) 

    plt.tight_layout()

    filename = f"exceedM_N{fixed_N}_K10_K20.png"
    save_path = os.path.join(BASE_PLOTS_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[PLOT] Created: {filename}")


import os
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../"))
INPUT_DATA_DIR = os.path.join(PROJECT_ROOT, "data_analysis", "charts", "simulation", "data")
BASE_PLOTS_DIR = os.path.join(PROJECT_ROOT, "data_analysis", "charts", "simulation", "plots")

if not os.path.exists(BASE_PLOTS_DIR):
    try:
        os.makedirs(BASE_PLOTS_DIR)
    except OSError:
        pass

print(f"--- PATH CHECK ---")
print(f"INPUT_DATA_DIR:   {INPUT_DATA_DIR}")
print(f"BASE_PLOTS_DIR:   {BASE_PLOTS_DIR}")
print(f"------------------")

Z_ALPHA = 1.645  # 90% confidence interval

VALID_N = [8, 16, 24, 32, 40]
VALID_K = [2, 3, 5, 10, 20, 50, 1000]

METRICS_MAP = {
    "A": "Avg Queue Length",
    "T": "Avg Throughput",
    "B2": "Avg B=2 Grant",
    "B4": "Avg B=4 Grant",
    "B8": "Avg B=8 Grant",
    "B16": "Avg B=16 Grant",
    "BMinus1": "Avg B=-1 Grant",
    "W": "Avg Waiting Time",
    "M": "Avg exceedM Count"
}

# Regex
FILENAME_RE = re.compile(r'^(A|T|M|W|BMinus1|B\d+)_(\d+)_(\d+)\.csv$')

def read_values(filepath: str) -> np.ndarray:
    values = []
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        for line in lines[1:]:
            line = line.strip().replace(',', '.')
            if line:
                try: values.append(float(line))
                except ValueError: pass
    except Exception as e:
        print(f"[WARN] FILE ERROR {os.path.basename(filepath)}: {e}")
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

    plt.xlabel('N', labelpad=10)
    plt.ylabel(metric_name, labelpad=20)
    plt.title(f'{metric_name} Analysis')
    plt.xticks(x_indices, x_values)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    filename = f"{metric_name.replace(' ', '_')}.png"
    save_path = os.path.join(BASE_PLOTS_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[PLOT] Created: {filename}")

def generate_exceedM_plot(data_subset):
    fixed_N = 40
    target_Ks = [10, 20]
    
    # Verifica dati
    has_data = any(
        (k in data_subset and fixed_N in data_subset[k]) 
        for k in target_Ks
    )
    
    if not has_data:
        # Se vuoi evitare stampe se mancano i dati, puoi commentare la riga sotto
        # print(f"[INFO] No data for exceedM at N={fixed_N} with K={target_Ks}")
        return

    plt.figure(figsize=(8, 6))
    
    x_indices = np.arange(len(target_Ks))
    means = []
    cis = []
    
    for K in target_Ks:
        val = data_subset.get(K, {}).get(fixed_N, (0.0, 0.0))
        means.append(val[0])
        cis.append(val[1])

    colors = ['#d62728', '#1f77b4'] 

    # Plot delle barre
    plt.bar(x_indices, means, yerr=cis, width=0.5, 
            tick_label=[str(k) for k in target_Ks], 
            color=colors,
            capsize=5, alpha=0.9, edgecolor='black')

    plt.xlabel('K', labelpad=10)
    plt.ylabel('exceedM Count', labelpad=20)
    plt.title(f'exceedM Analysis (N={fixed_N}, Selected K)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # --- FIX POSIZIONAMENTO TESTO ---
    # Troviamo il massimo valore totale (barra + errore) per scalare il margine
    # Se means è vuoto o tutto zero, usiamo un default per evitare crash
    max_height = max([m + c for m, c in zip(means, cis)]) if means else 1.0
    if max_height == 0: max_height = 0.1 # Fallback se tutto è 0

    offset = max_height * 0.05  # Margine del 5% rispetto all'altezza massima

    for i, v in enumerate(means):
        error_val = cis[i]
        # La Y è: Media + Errore + Offset
        text_y = v + error_val + offset
        
        plt.text(i, text_y, f"{v:.2f}", 
                 ha='center', va='bottom', fontweight='bold', color='black')

    # Aumentiamo leggermente il limite Y del grafico per non tagliare il testo
    plt.ylim(top=max_height * 1.2) 

    plt.tight_layout()

    filename = f"exceedM_N{fixed_N}_K10_K20.png"
    save_path = os.path.join(BASE_PLOTS_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[PLOT] Created: {filename}")


def generate_bminus1_plot(data_subset):
    fixed_N = 40
    
    present_ks = sorted([k for k in VALID_K if k in data_subset and fixed_N in data_subset[k]])
    
    if not present_ks:
        print(f"[INFO] No data for BMinus1 at N={fixed_N}")
        return

    plt.figure(figsize=(10, 6))
    
    x_indices = np.arange(len(present_ks))
    means = []
    cis = []
    
    for K in present_ks:
        val = data_subset[K][fixed_N]
        means.append(val[0])
        cis.append(val[1])

    
    cmap = plt.get_cmap('tab10')
    colors = [cmap(i % cmap.N) for i in range(len(present_ks))]

    plt.bar(x_indices, means, yerr=cis, width=0.6, 
            tick_label=[str(k) for k in present_ks], 
            color=colors,
            capsize=4, alpha=0.9, edgecolor='black')

    plt.xlabel('K', labelpad=10)
    plt.ylabel('Avg B=-1 Grant', labelpad=20)
    plt.title(f'B=-1 Analysis (Fixed N={fixed_N})')
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    max_height = max([m + c for m, c in zip(means, cis)]) if means else 1.0
    if max_height == 0: max_height = 0.1
    offset = max_height * 0.02

    for i, v in enumerate(means):
        text_y = v + cis[i] + offset
        plt.text(i, text_y, f"{v:.2f}", ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.ylim(top=max_height * 1.15)
    plt.tight_layout()

    filename = f"Avg_B=-1_N=40.png"
    save_path = os.path.join(BASE_PLOTS_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[PLOT] Created: {filename}")
# =====================
# Main
# =====================

def main():
    if not os.path.exists(INPUT_DATA_DIR):
        print(f"[ERROR] Data folder NOT found: {INPUT_DATA_DIR}")
        return

    global_data = defaultdict(lambda: defaultdict(dict))
    files_found = 0

    for fname in os.listdir(INPUT_DATA_DIR):
        match = FILENAME_RE.match(fname)
        if match:
            ftype, n_str, k_str = match.groups()
            N, K = int(n_str), int(k_str)

            if N in VALID_N and K in VALID_K:
                path = os.path.join(INPUT_DATA_DIR, fname)
                values = read_values(path)
                if len(values) > 0:
                    mean, ci = mean_and_ci(values)
                    global_data[ftype][K][N] = (mean, ci)
                    files_found += 1

    print(f"CSV files found: {files_found}")

    for code, name in METRICS_MAP.items():
        if code not in global_data:
            print(f"[INFO] No data for {name} ({code})")
            continue

        if code == "M":
            generate_exceedM_plot(global_data[code])
        
        # 2. CASO SPECIALE: BMinus1 -> N=40, K Variabile
        elif code == "BMinus1":
            generate_bminus1_plot(global_data[code])
            
        # 3. CASO STANDARD (Tutti gli altri) -> N Variabile, K raggruppati
        else:
            generate_plot(code, name, global_data[code])

    print(f"--- COMPLETATO ---")
    print(f"Plots saved: {BASE_PLOTS_DIR}")

if __name__ == "__main__":
    main()