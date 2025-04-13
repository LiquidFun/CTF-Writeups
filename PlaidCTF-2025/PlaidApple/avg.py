# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "opencv-python",
# ]
# ///
from pathlib import Path
import numpy as np
import cv2
from multiprocessing import Pool

input_dir = Path("diff")
output_dir = None
diff_files = []

def load_image(path):
    img = cv2.imread(str(path))
    if img is None:
        raise ValueError(f"Could not load image {path}")
    return img.astype(np.float32)

def save_image(path, img):
    img_uint8 = np.clip(img, 0, 255).astype(np.uint8)
    cv2.imwrite(str(path), img_uint8)

def process_window(images, method="avg"):
    stack = np.stack(images, axis=0)
    if method == "avg":
        # diff = np.diff(bw, axis=0)
        #change_map = np.clip((np.sum(np.abs(diff), axis=0) - 130) * 3, 0, 255)
        bw = stack
        # print(bw.shape)
        # [11, 1000, 1000, 3]
        bw = np.mean(bw, axis=0)
        bw = np.mean(bw, axis=-1)

        # bw[bw > 200] = 255
        # bw[bw < 50] = 0
        # ab = bw / 255 - 0.5
        # bw = np.clip((ab / np.abs(ab)) + 0.5, 0, 1) * 255
        bw *= 3

        bw = np.clip(bw, 0, 255)
        return bw
    elif method == "min":
        return np.min(np.max(stack, axis=-1), axis=0)
    else:
        raise ValueError(f"Unknown method '{method}'")

def process_and_save(args):
    i, n, method = args
    window = diff_files[i:i + n]
    imgs = [load_image(f) for f in window]
    result = process_window(imgs, method=method)
    out_name = window[-1].name
    save_image(output_dir / out_name, result)
    return out_name

def main(n=3, method="avg"):
    global diff_files, output_dir
    output_dir = Path(f"diff_{method}{n}")
    output_dir.mkdir(exist_ok=True)

    diff_files = sorted([f for f in input_dir.glob("*.png")])
    indices = list(range(6400, 7500, 3))

    with Pool() as pool:
        for out_name in pool.imap_unordered(process_and_save, [(i, n, method) for i in indices]):
            print(out_name)

if __name__ == "__main__":
    main(n=11, method="avg")  # Change to method="min" if needed
