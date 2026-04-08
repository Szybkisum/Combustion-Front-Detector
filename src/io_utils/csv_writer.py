import os
import pandas as pd
import numpy as np

def save_to_csv(front_data: np.ndarray, output_dir: str):
    output_file = os.path.join(output_dir, 'front.csv')
    df = pd.DataFrame(front_data)
    df.to_csv(output_file, index=False)