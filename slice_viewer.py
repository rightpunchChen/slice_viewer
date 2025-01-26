import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

COLOR_MAPPING = {
        'ALL': {3: [1, 1, 0], 2: [1, 0, 0], 1: [0, 1, 0]},
        'WT': {3: [1, 1, 0], 2: [1, 1, 0], 1: [1, 1, 0]},
        'TC': {3: [1, 1, 0], 1: [1, 1, 0]},
        'ET': {3: [1, 1, 0]},
        }

class SliceViewer:
    def __init__(self):
        pass

    def read_img(self, path):
        return sitk.GetArrayFromImage(sitk.ReadImage(path))

    def normalize(self, matrix):
        min_val = np.min(matrix)
        max_val = np.max(matrix)
        normalized_matrix = (matrix - min_val) / (max_val - min_val)
        return normalized_matrix

    def pad_and_stack_images(self, data):
        max_shape = np.max(np.array([image.shape for image in data]), axis=0)
        stacked_data = []
        for image in data:
            pad_width = (
                        (0, max_shape[0] - image.shape[0]),
                        ((max_shape[1] - image.shape[1]) // 2, (max_shape[1] - image.shape[1]) // 2), 
                        ((max_shape[2] - image.shape[2]) // 2, (max_shape[2] - image.shape[2]) // 2)
                        )
            padded_image = np.pad(image, pad_width, mode='constant', constant_values=0)
            stacked_data.append(padded_image)
        return stacked_data

    def labeled_img(self, data, label, modality='ALL', alpha=0.35):
        data_norm = self.normalize(data)
        data_rgb = np.stack([data_norm] * 3, axis=-1)

        color_mappings = COLOR_MAPPING
        mapping = color_mappings.get(modality, {})

        for lbl, color in mapping.items():
            mask = (label == lbl)
            color = np.array(color)
            data_rgb[mask] = (1 - alpha) * data_rgb[mask] + alpha * color
        return data_rgb
    
    def slice_viewer(self, data, n=2, pad=False, ani_path=None):
        if pad:
            data = self.pad_and_stack_images(data)
        num_files = len(data)
        num_rows = (num_files + n - 1) // n
        fig, axes = plt.subplots(num_rows, n, figsize=(5 * n, 5 * num_rows))
        if num_rows == 1:
            axes = np.expand_dims(axes, axis=0)
        if n == 1:
            axes = np.expand_dims(axes, axis=1)

        max_shape = np.max([image.shape[0] for image in data], axis=0)

        ims = []

        for i, ax in enumerate(axes.flat):
            if i < num_files:
                vmin, vmax = np.amin(data[i]), np.amax(data[i])
                if len(data[i].shape) == 4:
                    im = ax.imshow(data[i][0, :, :])
                else:
                    im = ax.imshow(data[i][0, :, :], cmap='gray', vmin=vmin, vmax=vmax)
                ax.set_title(f'Slice 1')
                ims.append([im])

        def update(frame):
            artists = []
            for i, ax in enumerate(axes.flat):
                if i < num_files:
                    im = ax.images[0]
                    im.set_data(data[i][frame-1, :, :])
                    ax.set_title(f'Slice {frame}')
                    artists.append(im)
            return artists

        slider_ax = plt.axes([0.2, 0.02, 0.6, 0.03])
        slider = plt.Slider(slider_ax, 'Slice', 1, max_shape, valinit=0, valstep=1)
        
        slider.on_changed(update)

        for i in range(num_files, num_rows * n):
            fig.delaxes(axes.flat[i])

        if ani_path is not None:
            anim = FuncAnimation(fig, update, frames=range(1,max_shape+1), interval=200, blit=True)
            anim.save(ani_path, writer='ffmpeg', fps=15)
        else:
            plt.show()

if __name__ == '__main__':
    sv = SliceViewer()
    t2f_file = f"BraTS-MET-00001-000-t2f.nii.gz"
    t2w_file = f"BraTS-MET-00001-000-t2w.nii.gz"
    t1c_file = f"BraTS-MET-00001-000-t1c.nii.gz"
    t1n_file = f"BraTS-MET-00001-000-t1n.nii.gz"
    gt_file = f"BraTS-MET-00001-000-seg.nii.gz"
    
    t2f = sv.read_img(t2f_file)
    t2w = sv.read_img(t2w_file)
    t1c = sv.read_img(t1c_file)
    t1n = sv.read_img(t1n_file)
    gt = sv.read_img(gt_file)

    sv.slice_viewer([t2f, t2w, t1c, t1n, gt, sv.labeled_img(t2f, gt, modality='ALL')], n=4)