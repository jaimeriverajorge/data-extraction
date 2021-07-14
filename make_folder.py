# Script to make the folder of training data,
# containing only the oak images that have
# already been landmarked

import oaks
import cv2
import os

num_images = 33
oak_dict = {}
for i in range(num_images):
    currentOak = oaks.makeOaks(i)
    id = currentOak.id
    oak_dict[i] = currentOak


def copy_image(oak):
    img_name = oak.file_name
    img = cv2.imread(f'oak_images_small/{img_name}')
    path = 'training_folder'
    cv2.imwrite(os.path.join(path, img_name), img)


for i in oak_dict:
    copy_image(oak_dict[i])
