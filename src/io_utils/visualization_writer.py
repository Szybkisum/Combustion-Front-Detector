import numpy as np
import os
import cv2

def save_visualization(img: np.ndarray, output_dir: str):
    output_file = os.path.join(output_dir, 'visualization.png')
    cv2.imwrite(output_file, img)