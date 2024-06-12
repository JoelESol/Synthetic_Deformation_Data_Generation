import cv2
import numpy as np
import os
import random

def replace_background(input_folder, background_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all image files in the input folder
    input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Get a list of all background image files
    background_files = [f for f in os.listdir(background_folder) if os.path.isfile(os.path.join(background_folder, f))]

    for input_file in input_files:
        output_file = os.path.join(output_folder, input_file)
        # Skip if the file already exists in the output folder
        if os.path.exists(output_file):
            print(f"Skipping '{input_file}' as a file with the same name already exists in the output folder.")
            continue
        # Load the image with the green background
        green_background_image = cv2.imread(os.path.join(input_folder, input_file))
        print(input_file)
        # Select a random background image
        background_image_file = random.choice(background_files)
        replacement_image = cv2.imread(os.path.join(background_folder, background_image_file))

        # Resize the replacement image to fit the green background without distorting its aspect ratio
        green_aspect_ratio = green_background_image.shape[1] / green_background_image.shape[0]
        replacement_aspect_ratio = replacement_image.shape[1] / replacement_image.shape[0]

        if green_aspect_ratio > replacement_aspect_ratio:
            new_width = green_background_image.shape[1]
            new_height = int(new_width / replacement_aspect_ratio)
        else:
            new_height = green_background_image.shape[0]
            new_width = int(new_height * replacement_aspect_ratio)

        replacement_image_resized = cv2.resize(replacement_image, (new_width, new_height))
        crop_x = max(new_width - green_background_image.shape[1], 0) // 2
        crop_y = max(new_height - green_background_image.shape[0], 0) // 2

        if crop_x > 0 or crop_y > 0:
            replacement_image_resized = replacement_image_resized[crop_y:crop_y + green_background_image.shape[0],
                                        crop_x:crop_x + green_background_image.shape[1]]

        # Define range of green color in RGB (adjust these values to tighten or loosen the green screen)
        lower_green = np.array([0, 225, 0])  # Adjust these values
        upper_green = np.array([25, 255, 25])  # Adjust these values

        # Threshold the green background image to get only green colors
        mask = cv2.inRange(green_background_image, lower_green, upper_green)

        # Perform morphological operations
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Closing to fill small holes
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Opening to remove small noise

        # Invert the mask
        mask_inv = cv2.bitwise_not(mask)

        # Apply erosion to further refine the mask
        erosion_kernel = np.ones((3, 3), np.uint8)
        mask_inv = cv2.erode(mask_inv, erosion_kernel, iterations=1)

        mask = cv2.bitwise_not(mask_inv)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(green_background_image, green_background_image, mask=mask_inv)

        # Bitwise-AND mask and resized replacement image
        replacement_no_bg = cv2.bitwise_and(replacement_image_resized, replacement_image_resized, mask=mask)

        # Combine the two images using bitwise_or
        result = cv2.bitwise_or(res, replacement_no_bg)

        # Save the result
        output_file = os.path.join(output_folder, input_file)
        cv2.imwrite(output_file, result)

# Example usage
#input_folder = 'data/can/Synthetic_Can_Data/train'
#background_folder = 'Backgrounds/train'
#output_folder = 'data/can/Synthetic_Can_Data/random_background'

#replace_background(input_folder, background_folder, output_folder)