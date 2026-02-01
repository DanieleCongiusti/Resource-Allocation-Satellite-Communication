import pandas as pd
import matplotlib.pyplot as plt
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))

CHARTS_ROOT = os.path.join(PROJECT_ROOT, "charts")

files_config = {
    'throughput_consistency': {
        'filename': os.path.join(CHARTS_ROOT, 'consistency', 'data', 'consistency_throughput.csv'),
        'param_name': 'N=',
        'title': 'Average Throughput Consistency',
        'ylabel': 'Avg Throughput [bytes/sec]',
        'out': os.path.join(CHARTS_ROOT, 'consistency', 'plots')
    },
    "throughput_continuity": {
        'filename': os.path.join(CHARTS_ROOT, 'continuity', 'data', 'continuity_throughput.csv'),
        'param_name': 'N=',
        'title': 'Average Throughput Continuity',
        'ylabel': 'Avg Throughput [bytes/sec]',
        'out': os.path.join(CHARTS_ROOT, 'continuity', 'plots')
    },
    'queueLength_consistency': {
        'filename': os.path.join(CHARTS_ROOT, 'consistency', 'data', 'consistency_queue_length.csv'),
        'param_name': 'T=',
        'title': 'Average Queue Length Consistency',
        'ylabel': 'Avg Queue length',
        'out': os.path.join(CHARTS_ROOT, 'consistency', 'plots')
    },
    'queueLength_continuity': {
        'filename': os.path.join(CHARTS_ROOT, 'continuity', 'data', 'continuity_queue_length.csv'),
        'param_name': 'T=',
        'title': 'Average Queue Length Continuity',
        'ylabel': 'Avg Queue length',
        'out': os.path.join(CHARTS_ROOT, 'continuity', 'plots')
    }
}

print("Start generating consistency and continuity graphs...")

for plot_name, config in files_config.items():
    print(f"Generating {plot_name}...")
    try:
        plt.figure(figsize=(10, 6))
        df = pd.read_csv(config['filename'])
        mean_df = df.groupby(df.columns[1], as_index=False)['value'].mean()
        positions = range(len(mean_df))

        plt.bar(positions, mean_df['value'], width=0.8)
        plt.xlabel(config['param_name'] + 'value')
        plt.ylabel(config['ylabel'], labelpad=15)
        plt.title(config['title'])
        plt.xticks(positions, mean_df.iloc[:, 0])

        output_folder = config['out']
        os.makedirs(output_folder, exist_ok=True)
        output_filename = f'{output_folder}/{plot_name}_plot.png'
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        plt.close()
    except FileNotFoundError:
        print(f"File not found: {config['filename']}")
        continue