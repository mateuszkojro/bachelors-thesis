import os
import json
import sys


def main():
    folder = sys.argv[1]

    all_meta = {}
    for measurement in os.listdir(folder):
        measurement_folder = folder + "/" + measurement
        for file in os.listdir(measurement_folder):
            path = measurement_folder + "/" + file
            if path.endswith("metadata.json"):
                with open(path) as f:
                    meta = json.load(f)
                    all_meta[measurement] = meta
    
    with open("metadata.json", "w") as f:
        json.dump(all_meta, f)

if __name__ == "__main__":
    main()