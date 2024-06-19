import os
import pandas as pd
import json
from regipy.registry import RegistryHive
from regipy.plugins.utils import dump_hive_to_json

def parse_hives_to_json_and_csv(hive_paths, output_dir):
    for hive_path in hive_paths:
        # Load the registry hive
        hive = RegistryHive(hive_path)

        # Create JSON output file
        json_file = os.path.join(output_dir, os.path.basename(hive_path) + '.json')
        dump_hive_to_json(hive, json_file, name_key_entry=None)
        print(f"Registry hive dumped to JSON: {json_file}")

        # Create CSV output file
        csv_file = os.path.join(output_dir, os.path.basename(hive_path) + '.csv')
        with open(json_file, 'r') as file:
            data_list = [json.loads(line.strip()) for line in file if line.strip()]

        df = pd.DataFrame(data_list)
        df.to_csv(csv_file, index=False)
        print(f"JSON converted to CSV: {csv_file}")

def main():
    # Get current script directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Specify hive file paths
    hive_paths = [
        os.path.join(current_directory, 'sam'),
        os.path.join(current_directory, 'software'),
        os.path.join(current_directory, 'security'),
        os.path.join(current_directory, 'system'),
        os.path.join(current_directory, 'default')
    ]

    # Output directory for JSON and CSV files
    output_directory = current_directory

    # Parse the hives to JSON and CSV
    parse_hives_to_json_and_csv(hive_paths, output_directory)

if __name__ == "__main__":
    main()
