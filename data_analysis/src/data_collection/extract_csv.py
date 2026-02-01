import os
import csv
import re
import argparse
import sys
from collections import defaultdict

# =====================
# Configuration
# =====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))

ANALYSIS_MAP = {
    "variance": "varianceTest",
    "simulation": "simulationTest"
}

def main():
    parser = argparse.ArgumentParser(description="Data extraction from .sca files to CSV format.")
    parser.add_argument(
        '-n', '--name', 
        type=str, 
        required=True, 
        help=f"Valid options: {list(ANALYSIS_MAP.keys())}"
    )

    args = parser.parse_args()

    if args.name not in ANALYSIS_MAP:
        print(f"\n[ERROR] '{args.name}' analysis is not supported.")
        sys.exit(1) 

    target_folder_name = ANALYSIS_MAP[args.name]
    SOURCE_DIRECTORY = os.path.join(PROJECT_ROOT, "simulations", "results", target_folder_name)
    OUTPUT_DIRECTORY = os.path.join(PROJECT_ROOT, "data_analysis", "charts", args.name, "data")

    if not os.path.exists(SOURCE_DIRECTORY):
        print(f"\n[ERROR] The data folder does not exist: {SOURCE_DIRECTORY}")
        sys.exit(1)

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    print(f"--- CONFIGURATION ---")
    print(f"Input:  {SOURCE_DIRECTORY}")
    print(f"Output: {OUTPUT_DIRECTORY}")
    print(f"---------------------")

    # Dizionario per accumulare i dati
    data_store = defaultdict(lambda: {
        'Throughput': [], 
        'AVGQLen': [], 
        'avgWaitingTimeFrame': [], 
        'accumulatedQueueLength': [], 
        'bGrant': []
    })

    # Regex per N e K: "$N=12, $K=1000"
    filename_pattern = re.compile(r'\$N=(\d+).*?\$K=(\d+)')

    print(f"Starting extraction...")
    count_files = 0
    
    # 1. Scansione file e estrazione
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
                        if line.startswith("scalar"):
                            parts = line.split()
                            if len(parts) >= 3:
                                stat_value = parts[-1]        
                                stat_name_raw = parts[-2]
                                clean_name = stat_name_raw.strip('"')

                                # --- LOGICA DI MATCHING ---
                                
                                # T -> Throughput
                                if "throughputStat:last" in clean_name:
                                    data_store[config_key]['Throughput'].append(stat_value)
                                
                                # A -> AVG Queue Length
                                elif "AvgQLStat:mean" in clean_name:
                                    data_store[config_key]['AVGQLen'].append(stat_value)
                                
                                # W -> Waiting Time
                                elif "avgWaitingTimeFrame:mean" in clean_name:
                                    data_store[config_key]['avgWaitingTimeFrame'].append(stat_value)
                                
                                # Q -> Accumulated Queue Length
                                # Cerca "accumulatedQueueLength" ignorando :min/:max
                                elif "accumulatedQueueLength" in clean_name:
                                    if not any(x in clean_name for x in [':min', ':max', ':stddev']):
                                        data_store[config_key]['accumulatedQueueLength'].append(stat_value)

                                # B -> bGrant
                                # Cerca "bGrant" ignorando :min/:max
                                elif "bGrant" in clean_name:
                                    if not any(x in clean_name for x in [':min', ':max', ':stddev']):
                                        data_store[config_key]['bGrant'].append(stat_value)
                                    
            except Exception as e:
                print(f"Error reading {filename}: {e}")
            
            count_files += 1

    print(f"Analyzed {count_files} .sca files.")

    # 2. Scrittura CSV con intestazioni corrette
    output_count = 0

    for (n, k), stats in data_store.items():
    
        # T_N_K.csv
        if stats['Throughput']:
            path = os.path.join(OUTPUT_DIRECTORY, f"T_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['ThroughputStat:last']) 
                for val in stats['Throughput']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        # A_N_K.csv
        if stats['AVGQLen']:
            path = os.path.join(OUTPUT_DIRECTORY, f"A_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['AVGQLen:mean'])
                for val in stats['AVGQLen']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        # W_N_K.csv -> Intestazione richiesta: avgWaitingTimeFrame:mean
        if stats['avgWaitingTimeFrame']:
            path = os.path.join(OUTPUT_DIRECTORY, f"W_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['avgWaitingTimeFrame:mean'])
                for val in stats['avgWaitingTimeFrame']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        # Q_N_K.csv -> Intestazione richiesta: avgAccumulatedQueueLength:mean
        if stats['accumulatedQueueLength']:
            path = os.path.join(OUTPUT_DIRECTORY, f"Q_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # QUI INSERIAMO L'HEADER ESATTO RICHIESTO
                writer.writerow(['avgAccumulatedQueueLength:mean'])
                for val in stats['accumulatedQueueLength']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        # B_N_K.csv -> Intestazione richiesta: avgBGrant:mean
        if stats['bGrant']:
            path = os.path.join(OUTPUT_DIRECTORY, f"B_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # QUI INSERIAMO L'HEADER ESATTO RICHIESTO
                writer.writerow(['avgBGrant:mean'])
                for val in stats['bGrant']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

    print(f"COMPLETED: Generated {output_count} CSV files in '{OUTPUT_DIRECTORY}'.")

if __name__ == "__main__":
    main()