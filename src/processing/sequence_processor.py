import numpy as np
import cv2
import os
from io_utils.visualization_writer import save_visualization
from io_utils.csv_writer import save_to_csv

MAX_FRONT_JUMP_RATIO = 0.18

def draw_front(img: np.ndarray, front: np.ndarray):
    out = img.copy()
    for x, y in enumerate(front):
        if not np.isnan(y):
            cv2.circle(out, (x, int(y)), 1, (0, 0, 255), -1)
    return out

def create_result_handler_callback(output_dir: str):
    def callback(img_path: str, img: np.ndarray, front: np.ndarray):
        image_name = os.path.splitext(os.path.basename(img_path))[0]
        per_image_output_dir = os.path.join(output_dir, f"{image_name}_results")
        os.makedirs(per_image_output_dir, exist_ok=True)

        vis_img = draw_front(img, front)
        save_visualization(vis_img, per_image_output_dir)
        save_to_csv(front, per_image_output_dir)
    return callback

class SequenceProcessor:
    
    def __init__(self, output_dir: str) -> None:
        self.last_front = None
        self.last_mean = 0
        self.output_dir = output_dir
        self.result_handler = create_result_handler_callback(output_dir)

    def detect_fire_regions(self, img: np.ndarray):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        max_val = gray.max()
        threshold = int(max_val * 0.9)
        mask = gray >= threshold

        mask = mask.astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        out = img.copy()
        final_mask = np.zeros_like(mask)

        for c in contours:
            cv2.drawContours(out, [c], -1, (0, 255, 0), 1)
            cv2.drawContours(final_mask, [c], -1, 255, -1)

        return out, final_mask
    
    def find_fire_front(self, mask: np.ndarray) -> np.ndarray:
        h, w = mask.shape
        front = np.full(w, np.nan, dtype=float)

        max_dist = int(MAX_FRONT_JUMP_RATIO * h)
        min_y_global = max(0, int(self.last_mean - max_dist))
        max_y_global = min(h - 1, int(self.last_mean + max_dist))

        for x in range(w):
            ys = np.where(mask[:, x] > 0)[0]
            if len(ys) == 0:
                continue

            min_y = max(min_y_global, self.last_front[x])

            valid_ys = ys[(ys >= min_y) & (ys <= max_y_global)]

            if len(valid_ys) > 0:
                front[x] = valid_ys.max()

        return front
    
    def constrain_front_with_previous(self, front: np.ndarray) -> np.ndarray:
        notnan = ~np.isnan(front)
        front[notnan] = np.maximum(front[notnan], self.last_front[notnan])
        return front


    def update_last_front(self, front: np.ndarray) -> None:
        to_update = np.greater(front, self.last_front)
        self.last_front[to_update] = front[to_update]

    def process_images(self, image_paths: list[str]) -> None:
        for file in image_paths:
            img = cv2.imread(file)
            if img is None:
                print(f"Skipping file '{file}'\nCause: file not readable as an image")
                continue

            if self.last_front is None:
                self.last_front = np.zeros(img.shape[1])

            out_img, mask = self.detect_fire_regions(img)
            front = self.find_fire_front(mask)
            front_limited = self.constrain_front_with_previous(front)
            self.update_last_front(front_limited)
            
            mean = int(np.nanmean(front_limited)) if np.any(~np.isnan(front_limited)) else img.shape[0] - 1
            self.last_mean = mean
            self.result_handler(file, out_img, front_limited)
