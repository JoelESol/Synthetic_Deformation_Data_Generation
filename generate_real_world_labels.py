import os

def create_text_file(folder1, folder2, output_file):
    # Get the list of image files from each folder
    images_folder1 = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))]
    images_folder2 = [f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))]

    with open(output_file, 'a+') as text_file:
        for image in images_folder1:
            image_path = os.path.join(folder1, image)
            text_file.write(f'{image_path} 0\n')  # Classification 0 for folder1
        for image in images_folder2:
            image_path = os.path.join(folder2, image)
            text_file.write(f'{image_path} 1\n')  # Classification 1 for folder2