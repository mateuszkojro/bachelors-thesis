import os
import shutil
import argparse

QUESTIONARES_DIR = "./results/"
RECORDINGS_DIR = "./recordings/"
OUTPUT_DIR = "./combined/"

def parse_args():
    pass
    # parser = argparse.ArgumentParser("Combine questionare and recordings into one folder structure")
    # parser.add_argument("questionares-dir")
    # parser.add_argument("recordings-dir")
    # parser.add_argument("--output-dir", default="./combined/")
    # parser.parse_args()
    
    # global QUESTIONARES_DIR
    # global RECORDINGS_DIR
    # global OUTPUT_DIR

    # QUESTIONARES_DIR = parser.questionares_dir
    # RECORDINGS_DIR = parser.recordings_dir
    # OUTPUT_DIR = parser.output_dir

def copy(src, dst):
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        print(f"Fail: {e}")

def mkdir(path):
    os.makedirs(path, exist_ok=True)


def main():
    parse_args()
    mkdir(OUTPUT_DIR)
    
    measurements = os.listdir(QUESTIONARES_DIR)
    for measurement in measurements:
        src_prefix = QUESTIONARES_DIR + "/" + measurement

        if not os.path.isdir(src_prefix):
            print(f"Not a dir (skiping): {src_prefix}")
            continue

        dst_dir = OUTPUT_DIR + "/" + measurement
        print(f"Making dir: {dst_dir}")
        mkdir(dst_dir)
        
        for file in os.listdir(src_prefix):
            src = src_prefix + "/" + file
            print(f"Copying: {src} -> {dst_dir}")
            copy(src, dst_dir)

        for file in os.listdir(RECORDINGS_DIR):
            src = RECORDINGS_DIR + "/" + file
            if measurement in file:
                print(f"Copying: {src} -> {dst_dir}")
                copy(src, dst_dir)


if __name__ == '__main__':
    main()