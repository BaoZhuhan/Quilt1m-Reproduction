import os
import sys

def findmv(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith((".mkv", ".mp4", ".webm")):
                renamemv(os.path.join(root, f))

def renamemv(file_path):
    parent_dir = os.path.basename(os.path.dirname(file_path))
    ext = os.path.splitext(file_path)[1]
    new_name = parent_dir + ext
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)
    if ext.lower() != ".mp4":
        call(new_path)

def call(video_path):
    os.system(f'python /data4/quilt1m/quilt1m/data/wash/trans.py -n "{video_path}"')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        findmv(sys.argv[1])
