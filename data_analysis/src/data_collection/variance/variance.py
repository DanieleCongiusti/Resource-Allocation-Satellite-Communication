import csv
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))

INPUT_DATA_DIR = os.path.join(PROJECT_ROOT, "charts", "variance", "data")

BASE_PLOTS_DIR = os.path.join(PROJECT_ROOT, "charts", "variance", "plots")


OUTPUT_DIRS_MAP = {
    "A": os.path.join(BASE_PLOTS_DIR, "queue_length_variance"),
    "T": os.path.join(BASE_PLOTS_DIR, "throughput_variance")
}


N_VALUES = [8, 16, 24, 32, 40]
K_VALUES = [2, 3, 5, 10, 20, 50, 1000]


def read_csv_values(filepath):
    values = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)

        for row in reader:
            if not row:
                continue
            val_str = row[0].replace(',', '.')
            values.append(float(val_str))

    return np.array(values)


def variance_vs_sample_size(data):
    sample_sizes = []
    variances = []

    for n in range(2, len(data) + 1):
        sample = data[:n]
        variances.append(np.var(sample, ddof=1))
        sample_sizes.append(n)

    return sample_sizes, variances


def save_plot(sample_sizes, variances, title, output_path):
    plt.figure(figsize=(8, 5))
    plt.plot(sample_sizes, variances)
    plt.xlabel("Sample size")
    plt.ylabel("Sample variance")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def ensure_directories():
    if not os.path.exists(INPUT_DATA_DIR):
        print(f"[ERROR] Data folder does not exist: {INPUT_DATA_DIR}")
        exit(1)

    for path in OUTPUT_DIRS_MAP.values():
        os.makedirs(path, exist_ok=True)
        print(f"[INFO] Output folder verified: {path}")


def process_file(prefix, N, K):
    filename = f"{prefix}_{N}_{K}.csv"
    full_input_path = os.path.join(INPUT_DATA_DIR, filename)

    if not os.path.exists(full_input_path):
        print(f"[SKIP] File not found: {filename}")
        return

    try:
        data = read_csv_values(full_input_path)
        sample_sizes, variances = variance_vs_sample_size(data)

        title = f"{prefix} – N={N}, K={K}"
        
        target_dir = OUTPUT_DIRS_MAP.get(prefix)
        if not target_dir:
            print(f"[ERROR] Unknown prefix: {prefix}")
            return

        output_path = os.path.join(target_dir, f"{prefix}_{N}_{K}.png")

        save_plot(sample_sizes, variances, title, output_path)
        print(f"[OK] Generated: {output_path}")
        
    except Exception as e:
        print(f"[ERROR] Problem with file {filename}: {e}")

def main():
    print("--- Starting Variance Analysis ---")
    print(f"Directory Script: {SCRIPT_DIR}")
    print(f"Directory Input:  {INPUT_DATA_DIR}")
    
    ensure_directories()

    # Ciclo su Prefissi, N e K
    for prefix in ["A", "T"]:
        for N in N_VALUES:
            for K in K_VALUES:
                process_file(prefix, N, K)
    
    print("--- Variance Analysis Completed ---")


if __name__ == "__main__":
    main()