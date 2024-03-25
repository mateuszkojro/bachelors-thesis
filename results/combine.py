import pandas as pd
import os
import tqdm
import sys

OUT_FILE = "./dataset.csv"
EEG_COLS = [
    "EEG.AF3",
    "EEG.F7",
    "EEG.F3",
    "EEG.FC5",
    "EEG.T7",
    "EEG.P7",
    "EEG.O1",
    "EEG.O2",
    "EEG.P8",
    "EEG.T8",
    "EEG.FC6",
    "EEG.F4",
    "EEG.F8",
    "EEG.AF4",
]
MOT_COLS = [
    "MOT.AccX",
    "MOT.AccY",
    "MOT.AccZ",
]


def parse_meta(path):
    return pd.read_csv(path)


def parse_data(path):
    data = pd.read_csv(path, skiprows=1)
    data[EEG_COLS] *= 1e-6
    return data


def combine(meta: pd.DataFrame, data: pd.DataFrame):
    question_start = None
    answer_time = None
    data["label"] = "calibration"
    data = data.rename(columns={"Timestamp": "timestamp"})
    for idx, row in meta.iterrows():
        if row["type"] == "Trwa_kalibracja_nie_ruszaj_się":
            continue
        elif row["type"] in ["yes", "no"]:
            if question_start is not None:
                answer_time = row["timestamp"]
                data["label"] = data["label"].where(
                    ~(
                        (data["timestamp"] >= question_start)
                        & (data["timestamp"] <= answer_time)
                    ),
                    "thinking",
                )
        else:
            question_start = row["timestamp"]
            data["label"] = data["label"].where(
                ~(
                    (data["timestamp"] <= question_start)
                    & (data["timestamp"] >= answer_time)
                ),
                "waiting",
            )
    return data

def main():
    COMBINED_DIR = sys.argv[1]
    all_measurements = []
    for measurement in tqdm.tqdm(os.listdir(COMBINED_DIR)):
        dir_path = COMBINED_DIR + "/" + measurement
        meta = None
        data = None
        for file in os.listdir(dir_path):
            file_path = dir_path + "/" + file
            if file_path.endswith(".md.pm.bp.csv"):
                data = parse_data(file_path)
            elif file_path.endswith("intervalMarker.csv"):
                meta = parse_meta(file_path)
        data["id"] = measurement
        combined = combine(meta, data)
        combined["label_num"] = pd.Categorical(combined["label"]).codes
        all_measurements.append(combined)
    
    all_data = pd.concat(all_measurements)
    all_data.to_csv(OUT_FILE)


if __name__ == "__main__":
    main()
