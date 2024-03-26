import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def display_images(img_path):
    image_np = np.array(Image.open(img_path))
    plt.imshow(image_np)
    plt.axis('off')
    plt.show()

def census_transform(image):
    height, width = image.shape
    census = np.zeros_like(image)
    
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            center = image[y, x]
            census_code = 0
            idx = 0
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if image[y + j, x + i] >= center:
                        census_code |= 1 << idx
                    idx += 1
            census[y, x] = census_code
    
    return census

def hamming_distance(census1, census2):
    return np.count_nonzero(census1 != census2)

def calculate_disparity_map_census(left_img, right_img, window_size=5, max_disparity=50):
    left_arr = np.array(left_img)
    right_arr = np.array(right_img)
    height, width = left_arr.shape
    
    disparity_map = np.zeros((height, width))
    
    half_window = window_size // 2
    
    for y in range(half_window, height - half_window):
        for x in range(half_window, width - half_window):
            min_hamming = float('inf')
            best_disparity = 0
            for d in range(max_disparity):
                if x - d - half_window < 0:
                    break
                left_window = left_arr[y - half_window:y + half_window + 1, x - half_window:x + half_window + 1]
                right_window = right_arr[y - half_window:y + half_window + 1, x - d - half_window:x - d + half_window + 1]
                if left_window.shape != right_window.shape:
                    break
                census_left = census_transform(left_window)
                census_right = census_transform(right_window)
                hamming_dist = hamming_distance(census_left, census_right)
                if hamming_dist < min_hamming:
                    min_hamming = hamming_dist
                    best_disparity = d
            disparity_map[y, x] = best_disparity
    return disparity_map

def driver_function(left_address, right_address, size_pixel):
    display_images(left_address)
    display_images(right_address)
    left_image = Image.open(left_address).convert('L')
    right_image = Image.open(right_address).convert('L')
    disparity_map = calculate_disparity_map_census(left_image, right_image, window_size=size_pixel)
    plt.imshow(disparity_map, cmap='gray')
    plt.axis('off')
    plt.savefig(fname=left_address + " + " + right_address + " " + str(size_pixel) + ".jpg", format='jpg')
    plt.show()

