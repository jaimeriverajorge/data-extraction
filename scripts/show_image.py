# script to show an image from a specific folder

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def show_image(image_name):
    myImage = mpimg.imread(f"../../oak_images/{image_name}")
    plt.imshow(myImage)
    plt.show()


def main():
    show_image('MN-MG789E-B.jpg')


if __name__ == "__main__":
    main()
