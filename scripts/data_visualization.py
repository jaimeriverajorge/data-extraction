import imageio
import imageio_ffmpeg


from pathlib import Path

# path to images that we want to animate
image_path = Path('plotted_oaks')
images = list(image_path.glob('*.jpg'))
image_list = []
for file_name in images:
    image_list.append(imageio.imread(file_name))

# create animated image using mimwrite()
imageio.mimwrite('animated_from_images.gif', image_list)
