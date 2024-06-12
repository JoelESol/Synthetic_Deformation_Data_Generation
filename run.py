from Blender_scripts import blender
import generate_real_world_labels as gen_labels
import greenscreen_image_augmentation


def main():
    #Base Image Generation
    blender.generate_nondeformed()
    blender.generate_deformed()

    #BG_20K data augmentation
    input_folder = 'data/train'
    background_folder = 'Backgrounds/train'
    output_folder = 'data/random_background'
    greenscreen_image_augmentation.replace_background(input_folder, background_folder, output_folder)

    #Generate Labels for real world dataset
    folder1_path = "physical_can/truth_images"
    folder2_path = "physical_can/deform_images"
    output_text_file = "physical_can/image_data.txt"

    gen_labels.create_text_file(folder1_path, folder2_path, output_text_file)


if __name__ == "__main__":
    main()