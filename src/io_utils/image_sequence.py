import os

def load_image_paths_sequence(input_directory) -> list[str]:
    images = []
    for filename in sorted(os.listdir(input_directory)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_directory, filename)
            images.append(img_path)
    length = len(images)
    if length == 0:
        raise ValueError(
            f"Sequence cannot be processed: no '.png', '.jpg', '.jpeg' files found in '{input_directory}'."
        )
    print(f"Found {length} images in sequence:")
    for img_path in images:
        print(f" - {img_path}")
    return images