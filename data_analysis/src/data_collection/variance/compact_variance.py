import csv
import os
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))

INPUT_DATA_DIR = os.path.join(PROJECT_ROOT, "charts", "variance", "data")

BASE_PLOTS_DIR = os.path.join(PROJECT_ROOT, "charts", "variance", "plots")

OUTPUT_DIRS_MAP = {
    "A": os.path.join(BASE_PLOTS_DIR, "compact_queue_length_variance"),
    "T": os.path.join(BASE_PLOTS_DIR, "compact_throughput_variance")
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


def plot_for_fixed_N(prefix, N):
    plt.figure(figsize=(9, 6))
    found_any = False

    for K in K_VALUES:
        filename = f"{prefix}_{N}_{K}.csv"
        full_input_path = os.path.join(INPUT_DATA_DIR, filename)

        if not os.path.exists(full_input_path):
            print(f"[SKIP] File not found: {filename}")
            continue

        try:
            data = read_csv_values(full_input_path)
            sample_sizes, variances = variance_vs_sample_size(data)
            
            plt.plot(sample_sizes, variances, label=f"K={K}")
            found_any = True
        except Exception as e:
            print(f"[ERROR] Problem in {filename}: {e}")

    if not found_any:
        plt.close()
        return

    
    plt.xlabel("Dimensione del sample")
    plt.ylabel("Varianza campionaria")
    plt.title(f"{prefix} – Varianza vs sample size (N={N})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    target_dir = OUTPUT_DIRS_MAP[prefix]
    output_filename = f"{prefix}_N{N}_compact.png"
    output_path = os.path.join(target_dir, output_filename)

    plt.savefig(output_path)
    plt.close()

    print(f"[OK] Saved chart: {output_path}")


def ensure_directories():
    if not os.path.exists(INPUT_DATA_DIR):
        print(f"[ERROR] Data folder not found: {INPUT_DATA_DIR}")
        exit(1)

    for path in OUTPUT_DIRS_MAP.values():
        os.makedirs(path, exist_ok=True)


def main():
    print("--- Starting charts generation ---")
    print(f"Input: {INPUT_DATA_DIR}")
    
    ensure_directories()

    for prefix in ["A", "T"]:
        for N in N_VALUES:
            plot_for_fixed_N(prefix, N)
            
    print("--- Completed ---")


if __name__ == "__main__":
    main()