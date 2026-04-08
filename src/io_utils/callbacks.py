import os
import numpy as np
from io_utils.visualization import save_visualization, draw_front
from io_utils.csv_writer import save_to_csv

def create_result_handler_callback(output_dir: str):
    def callback(img_path: str, img: np.ndarray, front: np.ndarray):
        image_name = os.path.splitext(os.path.basename(img_path))[0]
        per_image_output_dir = os.path.join(output_dir, f"{image_name}_results")
        os.makedirs(per_image_output_dir, exist_ok=True)

        vis_img = draw_front(img, front)
        save_visualization(vis_img, per_image_output_dir)
        save_to_csv(front, per_image_output_dir)
    return callback