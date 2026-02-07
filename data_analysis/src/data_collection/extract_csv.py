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
    "simulation": "simulationTest",
    "variance500": "varianceN16K5"
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
    
    # Data structure: {(N, K): {metric_name: [values]}}
    data_store = defaultdict(lambda: {
        'Throughput': [], 
        'AVGQLen': [], 
        'avgWaitingTimeFrame': [], 
        'exceedM': [], 
        'B_2': [],
        'B_4': [],
        'B_8': [],
        'B_16': [],
        'B_Minus1': [],
    })

    # Regex for N and K: "$N=12, $K=1000"
    filename_pattern = re.compile(r'\$N=(\d+).*?\$K=(\d+)')

    print(f"Starting extraction...")
    count_files = 0
    
    #1. Reading .sca files
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

                                # --- MATCHING ---
                                
                                # T -> Throughput
                                if "throughputStat:last" in clean_name:
                                    data_store[config_key]['Throughput'].append(stat_value)

                                # B_* -> B_*
                                elif "B_2" in clean_name:
                                    data_store[config_key]['B_2'].append(stat_value)
                                elif "B_4" in clean_name:
                                    data_store[config_key]['B_4'].append(stat_value)
                                elif "B_8" in clean_name:
                                    data_store[config_key]['B_8'].append(stat_value)
                                elif "B_16" in clean_name:
                                    data_store[config_key]['B_16'].append(stat_value)
                                elif "B_Minus1" in clean_name:
                                    data_store[config_key]['B_Minus1'].append(stat_value)

                                # A -> AVG Queue Length
                                elif "AvgQLStat:mean" in clean_name:
                                    data_store[config_key]['AVGQLen'].append(stat_value)
                                
                                # W -> Waiting Time
                                elif "avgWaitingTimeFrame:mean" in clean_name:
                                    data_store[config_key]['avgWaitingTimeFrame'].append(stat_value)
                                
                                 # M -> Exceed M
                                elif "exceedM:last" in clean_name:
                                    data_store[config_key]['exceedM'].append(stat_value)
                                
                                    
            except Exception as e:
                print(f"Error reading {filename}: {e}")
            
            count_files += 1

    print(f"Analyzed {count_files} .sca files.")

    # 2. Writing CSV files
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

        # W_N_K.csv -> Header: avgWaitingTimeFrame:mean
        if stats['avgWaitingTimeFrame']:
            path = os.path.join(OUTPUT_DIRECTORY, f"W_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['avgWaitingTimeFrame:mean'])
                for val in stats['avgWaitingTimeFrame']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        # B*_N_K.csv -> Header: B_*
        if stats['B_2']:
            path = os.path.join(OUTPUT_DIRECTORY, f"B2_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # QUI INSERIAMO L'HEADER ESATTO RICHIESTO
                writer.writerow(['B_2'])
                for val in stats['B_2']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1
        
        if stats['B_4']:
            path = os.path.join(OUTPUT_DIRECTORY, f"B4_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # QUI INSERIAMO L'HEADER ESATTO RICHIESTO
                writer.writerow(['B_4'])
                for val in stats['B_4']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1
        
        if stats['B_8']:
            path = os.path.join(OUTPUT_DIRECTORY, f"B8_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # QUI INSERIAMO L'HEADER ESATTO RICHIESTO
                writer.writerow(['B_8'])
                for val in stats['B_8']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        if stats['B_16']:
            path = os.path.join(OUTPUT_DIRECTORY, f"B16_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # QUI INSERIAMO L'HEADER ESATTO RICHIESTO
                writer.writerow(['B_16'])
                for val in stats['B_16']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        if stats['B_Minus1']:
            path = os.path.join(OUTPUT_DIRECTORY, f"BMinus1_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # QUI INSERIAMO L'HEADER ESATTO RICHIESTO
                writer.writerow(['B_Minus1'])
                for val in stats['B_Minus1']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

        # M_N_K.csv -> Header: exceedM:last
        if stats['exceedM']:
            path = os.path.join(OUTPUT_DIRECTORY, f"M_{n}_{k}.csv")
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['exceedM:last'])
                for val in stats['exceedM']:
                    writer.writerow([val.replace('.', ',')])
            output_count += 1

    print(f"COMPLETED: Generated {output_count} CSV files in '{OUTPUT_DIRECTORY}'.")

if __name__ == "__main__":
    main()