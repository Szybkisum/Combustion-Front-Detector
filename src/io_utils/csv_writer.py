import os
import pandas as pd
import numpy as np

def save_to_csv(front_data: np.ndarray, output_dir: str, image_height: int) -> None:
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "front.csv")
    column_idx = np.arange(front_data.shape[0], dtype=int)

    inverted_height = (image_height - 1) - front_data.astype(float)

    df = pd.DataFrame(
        {
            "column": column_idx,
            "height": inverted_height,
        }
    )
    df.to_csv(output_file, index=False)