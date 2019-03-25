import numpy as np

SERV_PORT = 61612
IMG_DIM = (540, 360)


def normalize_img(rgb_image):
    img = rgb_image.scale(IMG_DIM[0], IMG_DIM[1])
    gray = img.getGrayNumpy()
    bw = gray.point(lambda x: -1 if x < 128 else 1, '1')
    return np.array(bw)
