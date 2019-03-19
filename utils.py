from PIL import Image
import numpy as np


def normalize_rgb(rgb_image: Image):
    gray = rgb_image.convert('L')
    bw = gray.point(lambda x: -1 if x < 128 else 1, '1')
    return np.array(bw)
