import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def show_image(image_name):
    myImage = mpimg.imread(f"../oak_images/{image_name}")
    plt.imshow(myImage)
    plt.show()


show_image('IN-MG638-N-B.jpg')
