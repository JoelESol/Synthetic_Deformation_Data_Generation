from torch.utils.data import DataLoader
from contextlib import ExitStack
from pathlib import Path
import blendtorch.btt as btt
from PIL import Image
from tqdm import tqdm
import os
import cv2
import numpy as np

BATCH = 4
BLENDER_INSTANCES = 1
WORKER_INSTANCES = 4
truth_views_per_shape = 3000
deform_views_per_shape = 3000
Rebuild_Data = True


def save_to_text_file(image_path, classification, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Construct the full path for the text file
    text_file_path = os.path.join(output_directory, 'train.txt')

    # Open the file in append mode ('a') or create it if it doesn't exist
    with open(text_file_path, 'a+') as text_file:
        # Write image paths and classifications to the text file
        text_file.write(f'{image_path} {classification}\n')

def generate_nondeformed():
    with ExitStack() as es:
        # Launch Blender instance. Upon exit of this script all Blender instances will be closed.
        bl = es.enter_context(
            btt.BlenderLauncher(
                scene=Path(__file__).parents[1] / "Blender Simulations/Blender Models/popcan_lattice_deform.blend",
                script=Path(__file__).parent / "truth.blend.py",
                num_instances=BLENDER_INSTANCES,
                named_sockets=["DATA"],
            )
        )

        addr = bl.launch_info.addresses["DATA"]
        ds = btt.RemoteIterableDataset(addr, max_items=truth_views_per_shape)
        dl = DataLoader(ds, batch_size=1, num_workers=1)
        count = 0

        directory_path = "data/train/"
        # Create the directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        for item in dl:
            count = count + 1
            img = item["image"].numpy()
            img = img[0, :, :, :]
            # convert using gamma = 1/2.2
            gamma = 1 / 2.2
            image_gamma_corrected = np.power(img / 255.0, gamma)
            # Convert 64-bit floating-point image to 8-bit
            image_gamma_corrected = (image_gamma_corrected * 255).astype(np.uint8)

            # Perform RGB to BGR color space conversion
            image_gamma_corrected = cv2.cvtColor(image_gamma_corrected, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f"data/train/truth_{str(count)}.png", image_gamma_corrected)
            save_to_text_file(f"train/truth_{str(count)}.png", 0, "data")

def generate_deformed():
    with ExitStack() as es:
        # Launch Blender instance. Upon exit of this script all Blender instances will be closed.
        bl = es.enter_context(
            btt.BlenderLauncher(
                scene=Path(__file__).parents[1] / "Blender Simulations/Blender Models/popcan_lattice_deform.blend",
                script=Path(__file__).parent / "deformation.blend.py",
                num_instances=BLENDER_INSTANCES,
                named_sockets=["DATA"],
            )
        )

        addr = bl.launch_info.addresses["DATA"]
        ds = btt.RemoteIterableDataset(addr, max_items=deform_views_per_shape)

        dl = DataLoader(ds, batch_size=1, num_workers=1)
        count = 0
        for item in dl:
            count = count + 1
            img = item["image"].numpy()
            img = img[0, :, :, :]
            gamma = 1 / 2.2
            image_gamma_corrected = np.power(img / 255.0, gamma)
            # Convert 64-bit floating-point image to 8-bit
            image_gamma_corrected = (image_gamma_corrected * 255).astype(np.uint8)

            # Perform RGB to BGR color space conversion
            image_gamma_corrected = cv2.cvtColor(image_gamma_corrected, cv2.COLOR_RGB2BGR)
            cv2.imwrite(f"data/train/deform_{str(count)}.png", image_gamma_corrected)
            save_to_text_file(f"train/deform_{str(count)}.png", 1, "data")

