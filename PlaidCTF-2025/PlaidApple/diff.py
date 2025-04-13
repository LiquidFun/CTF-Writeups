# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "opencv-python",
# ]
# ///
from pathlib import Path
import cv2
import numpy as np
from multiprocessing import Pool

# Directories
frames_dir = Path("frames")
diff_dir = Path("diff")
diff_dir.mkdir(exist_ok=True)

# List and sort frame files
frame_files = sorted([f for f in frames_dir.glob("*.png")])

# Build list of adjacent frame pairs
frame_pairs = [(frame_files[i], frame_files[i + 1]) for i in range(len(frame_files) - 1)]

def process_pair(pair):
    file1, file2 = pair
    img1 = cv2.imread(str(file1))
    img2 = cv2.imread(str(file2))

    if img1 is None or img2 is None:
        return

    # Compute absolute difference
    diff = cv2.absdiff(img1, img2)

    # Output filename based on second frame (to match order)
    output_name = file2.name
    output_path = diff_dir / output_name

    cv2.imwrite(str(output_path), diff)
    print(output_path)

if __name__ == "__main__":
    with Pool() as pool:
        pool.map(process_pair, frame_pairs)
