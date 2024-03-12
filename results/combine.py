import os
import shutil
import argparse

QUESTIONARES_DIR = "./questionares/"
RECORDINGS_DIR = "./recordings/"
OUTPUT_DIR = "./combined/"

def parse_args():
    parser = argparse.ArgumentParser("Combine questionare and recordings into one folder structure")
    parser.add_argument("questionares-dir")
    parser.add_argument("recordings-dir")
    parser.add_argument("--output-dir", default="./combined/")
    parser.parse_args()
    
    global QUESTIONARES_DIR
    global RECORDINGS_DIR
    global OUTPUT_DIR
    
    QUESTIONARES_DIR = parser.questionares_dir
    RECORDINGS_DIR = parser.recordings_dir
    OUTPUT_DIR = parser.output_dir

def main():
    parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    measurements = os.listdir(QUESTIONARES_DIR)
    for measurement in measurements:
        src_prefix = QUESTIONARES_DIR + "/" + measurement

        if not os.path.isdir(src_prefix):
            print(f"Not a dir (skiping): {src_prefix}")
            continue

        dst_dir = OUTPUT_DIR + "/" + measurement
        print(f"Making dir: {dst_dir}")
        os.makedirs(dst_dir)
        
        for file in os.listdir(src_prefix):
            src = src_prefix + "/" + file
            print(f"Copying: {src} -> {dst_dir}")
            shutil.copy2(src, dst_dir)

        for file in os.listdir(RECORDINGS_DIR):
            src = RECORDINGS_DIR + "/" + file
            if measurement in file:
                print(f"Copying: {src} -> {dst_dir}")
                shutil.copy2(src, dst_dir)


if __name__ == '__main__':
    main()