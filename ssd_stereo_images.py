import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def display_images(img_path):
    image_np = np.array(Image.open(img_path))
    plt.imshow(image_np)
    plt.axis('off')
    plt.show()

def ssd(window1, window2):
    return np.sum((window1 - window2) ** 2)

def disparity_matrix(left_img, right_img, window_size=5, max_disparity=50):
    left_arr = np.array(left_img)
    right_arr = np.array(right_img)
    height, width, channels = left_arr.shape
    disparity_map = np.zeros((height, width))
    half_window = window_size // 2

    for y in range(half_window, height - half_window):
        for x in range(half_window, width - half_window):
            min_ssd = float('inf')
            best_disparity = 0
            for d in range(max_disparity):
                if x + d + half_window >= width:
                    break
                window1 = left_arr[y - half_window:y + half_window + 1, x - half_window:x + half_window + 1]
                window2 = right_arr[y - half_window:y + half_window + 1, x - half_window + d:x + half_window + 1 + d]
                if window2.shape != window1.shape:  # Check if window size matches
                    break
                ssd_val = ssd(window1, window2)
                if ssd_val < min_ssd:
                    min_ssd = ssd_val
                    best_disparity = d
            disparity_map[y, x] = best_disparity
    return disparity_map


def driver_function(left_address, right_address):
    display_images('ll.png')
    display_images('rr.png')
    left_image = Image.open(left_address)
    right_image = Image.open(right_address)
    plt.imshow(disparity_matrix(left_image, right_image), cmap='gray')
    plt.axis('off')
    plt.show()

driver_function('ll.png', 'rr.png')