from PIL import Image
import numpy as np

CAM_RESOLUTION = (1080, 720)
SERV_PORT = 8000


def normalize_rgb(rgb_image: Image):
    gray = rgb_image.convert('L')
    bw = gray.point(lambda x: -1 if x < 128 else 1, '1')
    return np.array(bw)
