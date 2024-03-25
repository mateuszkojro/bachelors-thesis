import os
import json
import shutil
import pandas as pd
import sys

def remove(path):
    print(f"Removing: {path}")
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(f"Error: {e}")

def main():
    folder = sys.argv[1]
    for measurement in os.listdir(folder):
        measurement_folder = folder + "/" + measurement
        if measurement_folder.endswith("mama-1"):
            remove(measurement_folder)
            continue
        for file in os.listdir(measurement_folder):
            path = measurement_folder + "/" + file
            if path.endswith("metadata.json"):
                with open(path) as f:
                    meta = json.load(f)
                    if meta["question_set"] == "test_questions.json":
                        remove(measurement_folder)
                        break
                    if "mateuszkojro" in meta["email"]:
                        remove(measurement_folder)
                        break
            if path.endswith("bp.csv"):
                df = pd.read_csv(path, skiprows=1)
                time = (df.max() - df.min())["Timestamp"]
                if time < 12 * 60:
                    remove(measurement_folder)
                    break


if __name__ == "__main__":
    main()