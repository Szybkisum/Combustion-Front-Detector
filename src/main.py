import argparse
import os
import sys
from processing.sequence_processor import SequenceProcessor
from io_utils.image_sequence import load_image_paths_sequence

def main() -> None:
    parser = argparse.ArgumentParser(description="Detect combustion fronts in a sequence of images.")
    parser.add_argument('input_dir', type=str, help='Path to the directory containing the image sequence.')
    parser.add_argument(
        'output_dir',
        nargs='?',
        default=None,
        help='Path to the directory where results will be saved (default: input_dir).'
    )
    
    args = parser.parse_args()
    input_dir: str = args.input_dir
    output_dir: str = args.output_dir
    
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        sys.exit(1)

    if output_dir is None:
        output_dir = input_dir
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        image_paths = load_image_paths_sequence(input_dir)
    except ValueError as e:
        print(e)
        sys.exit(1)

    sequence_processor = SequenceProcessor(output_dir)
    sequence_processor.process_images(image_paths)

if __name__ == "__main__":
    main()