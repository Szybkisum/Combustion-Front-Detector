import argparse
import os
import sys
from sequence_processor import SequenceProcessor

def main():
    parser = argparse.ArgumentParser(description="Detect combustion fronts in a sequence of images.")
    parser.add_argument('input_dir', type=str, help='Path to the directory containing the image sequence.')
    parser.add_argument(
        'output_dir',
        nargs='?',
        default=None,
        help='Path to the directory where results will be saved (default: input_dir).'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)

    if args.output_dir is None:
        args.output_dir = args.input_dir
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    sequence_processor = SequenceProcessor()
    # logic

if __name__ == "__main__":
    main()