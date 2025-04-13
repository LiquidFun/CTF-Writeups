# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "opencv-python",
#     "pyzbar",
#     "qreader",
#     "tqdm",
# ]
# ///

from tqdm import tqdm
from pathlib import Path
import cv2
from qreader import QReader
from multiprocessing import Pool

# Global variable to be instantiated in each worker process
qreader = None

def worker_init():
    """Initialize QReader in each worker process."""
    global qreader
    qreader = QReader()

def read_qr_letter(img_path):
    """Read an image from img_path, decode its QR code, and return the decoded text."""
    # Ensure we convert the Path to a string for cv2.imread
    image = cv2.cvtColor(cv2.imread(str(img_path)), cv2.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)
    return decoded_text

def process_image(img_path):
    """
    Process a single image:
      - Decode the QR code using read_qr_letter.
      - If a QR code is found, filter out any falsey characters.
      - If exactly one character is decoded, return it.
      - If multiple characters are found, wrap them in parentheses.
      - If no QR is found, return None.
    Returns a tuple of (image file name, processed letter or None).
    """
    letter = read_qr_letter(img_path)
    if letter is not None:
        # Filter out any empty values
        letter = [l for l in letter if l]
        if len(letter) == 1:
            result = letter[0]
        elif len(letter) >= 2:
            result = "(" + ''.join(letter) + ")"
        else:
            result = None
    else:
        result = None
    return (img_path.name, result)

def main():
    input_dir = Path("diff_avg11")  # adjust if needed
    image_files = sorted(input_dir.glob("*.png"))
    
    # Use multiprocessing Pool with worker initializer
    with Pool(initializer=worker_init) as pool:
        # pool.map preserves the order of the input list
        # results = pool.map(process_image, image_files)
        results = list(tqdm(pool.imap(process_image, image_files), total=len(image_files), desc="Processing images"))
    
    letters = []
    # Process results in order and print individual outputs
    for img_name, letter in results:
        if letter is not None:
            print(f"{img_name}: {letter}")
            letter = [l for l in letter if l]
            if len(letter) == 1:
                letters.append(letter[0])
            elif len(letter) >= 2:
                letters.append("(" + ''.join(letter) + ")")
        else:
            print(f"{img_name}: No QR found")
    
    print("\nDecoded Letters:")
    print("".join(letters))

if __name__ == "__main__":
    main()
