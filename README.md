# Slice Viewer with SimpleITK

This project provides a Python-based utility for visualizing and analyzing 3D medical images using the SimpleITK library. It includes functionalities for reading, normalizing, labeling, and visualizing image slices, along with animations for dynamic visualization.

<img src="https://github.com/rightpunchChen/slice_viewer/blob/main/demo.png" width="50%">

## Requirements

- Python 3.7
- SimpleITK
- NumPy
- Matplotlib

## Usage
### 1. Slice Viewer Parameters
The `slice_viewer` function takes the following parameters:

- `data` (list): A list of 3D image arrays to visualize.
- `n` (int): Number of columns in the grid layout for displaying slices.
- `pad` (bool): If `True`, pads images to the same shape before displaying.
- `ani_path` (str, optional): File path to save the animation as a video. If not provided, the viewer displays the slices interactively.

### 2. Example Code
Here's how to use the `SliceViewer` class:

```python
from slice_viewer import SliceViewer

# Initialize SliceViewer
sv = SliceViewer()

# File paths
t2f_file = "BraTS-MET-00001-000-t2f.nii.gz"
t2w_file = "BraTS-MET-00001-000-t2w.nii.gz"
t1c_file = "BraTS-MET-00001-000-t1c.nii.gz"
t1n_file = "BraTS-MET-00001-000-t1n.nii.gz"
gt_file = "BraTS-MET-00001-000-seg.nii.gz"

# Read images
t2f = sv.read_img(t2f_file)
t2w = sv.read_img(t2w_file)
t1c = sv.read_img(t1c_file)
t1n = sv.read_img(t1n_file)
gt = sv.read_img(gt_file)

# Visualize slices
sv.slice_viewer(
    [t2f, t2w, t1c, t1n, gt, sv.labeled_img(t2f, gt, modality='ALL')],
    n=4
)
```
### 3. Label Mapping
Customize the label colors for different modalities using the `COLOR_MAPPING` dictionary. The current mapping is as follows:

```python
COLOR_MAPPING = {
    'ALL': {3: [1, 1, 0], 2: [1, 0, 0], 1: [0, 1, 0]},
    'WT': {3: [1, 1, 0], 2: [1, 1, 0], 1: [1, 1, 0]},
    'TC': {3: [1, 1, 0], 1: [1, 1, 0]},
    'ET': {3: [1, 1, 0]},
}
```

- `modality`: Specifies the mapping type (e.g., `ALL`, `WT`, `TC`, or `ET`).
- `alpha`: Controls the transparency of the overlay.

### 4. Saving Animations
To save the slice navigation as an animation, provide a file path for `ani_path` in the `slice_viewer` method:

```python
sv.slice_viewer(
    [t2f, t2w, t1c, t1n, gt, sv.labeled_img(t2f, gt, modality='ALL')],
    n=4,
    ani_path='output_animation.mp4'
)
```
