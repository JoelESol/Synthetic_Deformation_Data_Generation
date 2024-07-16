# [CASE 2024] Visual Deformation Detection Using Soft Material Simulation for Pre-training of Condition Assessment Models
### Used in the following paper:
### [Joel Sol, Amir M. Soufi Enayati, Homayoun Najjaran, "Visual Deformation Detection Using Soft Material Simulation for Pre-training of Condition Assessment Models"](https://arxiv.org/abs/2405.14877)

## Citation
If you use associated code for your work please cite the following paper:

```
@misc{sol2024visual,
      title={Visual Deformation Detection Using Soft Material Simulation for Pre-training of Condition Assessment Models}, 
      author={Joel Sol and Amir M. Soufi Enayati and Homayoun Najjaran},
      year={2024},
      eprint={2405.14877},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## Requirements
```
BlendTorch v0.4
opencv-python 4.10.0.82
numpy 1.26.3
torch 2.3.1
pillow 10.2.0
tqdm 4.66.4
torchvision 0.18.1
```
## Needed Software
Download [Blender 3.1](https://download.blender.org/release/Blender3.1/), [BlendTorch](https://github.com/cheind/pytorch-blender)

Please follow the installation instructions listed on the BlendTorch link

Please make the following change to pytorch-blender-develop/pkg_pytorch/blendtorch/btt/constants.py
```
DEFAULT_TIMEOUTMS = 600000
```
Please make the following change to pytorch-blender-develop/pkg_pytorch/setup.py

```
version="0.4.0",
```
## Additional Datasets Needed:
Download [Pop Can Dataset](https://drive.google.com/drive/folders/19KR56Hvpdkcomvz7Y-ff3Mr0PLp9So1P?usp=sharing), [BG-20k](https://drive.google.com/drive/folders/1ZBaMJxZtUNHIuGj8D8v3B9Adn8dbHwSS)

## Folder Structure of Datasets
```
├── data
      ├── train
            ├──Truth_*.png
            ├──Deform_*.png
      ├── random_background
            ├──Truth_*.png
            ├──Deform_*.png
      ├── train.txt
      
├──physical_can
      ├── deform_images
            ├── *.png
      ├──truth_images
            ├── *.png
      ├──image_data.txt
      
```
## Run.py
When ran will generate deformed and non-deformed data then augment it with backgrounds from BG-20k, finally a txt file is created to store the labels of the real world data for the can dataset

Please feel free to comment out any operations not needed.
