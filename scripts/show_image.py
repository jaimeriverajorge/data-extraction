# script to show an image from a specific folder

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def show_image(image_name):
    myImage = mpimg.imread(f"../oak_images_small/{image_name}")
    plt.imshow(myImage)
    plt.show()


def main():
    show_image('MB-MG518-W-A.jpg')


if __name__ == "__main__":
    main()
