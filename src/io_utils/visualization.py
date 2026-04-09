import numpy as np
import os
import cv2

def save_visualization(img: np.ndarray, output_dir: str):
    output_file = os.path.join(output_dir, 'visualization.png')
    cv2.imwrite(output_file, img)

def draw_fire_regions(img: np.ndarray, mask: np.ndarray):
    out = img.copy()
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, contours, -1, (0, 255, 0), 1)

    return out

def draw_front(img: np.ndarray, front: np.ndarray):
    out = img.copy()
    for x, y in enumerate(front):
        if not np.isnan(y):
            cv2.circle(out, (x, int(y)), 1, (0, 0, 255), -1)
    return out