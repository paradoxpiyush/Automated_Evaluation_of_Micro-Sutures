import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import functions as fn

def evaluate(img):
    ret,thresh = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    # cv.imshow('otsu orig', thresh)
    blur = cv.GaussianBlur(thresh,(15,15),0)
    inv_blur = 255 - blur
    # cv.imshow('blur_inv', inv_blur)
    # edges = cv.Canny(thresh,100,200)
    blur_edges = cv.GaussianBlur(thresh,(15,15),0)
    # cv.imshow('canny otsu', edges)
    # cv.imshow('tozero', thresh_tozero[1])
    kernel = np.array([[3,5,3],[0,0,0],[-3,-5,-3]])
    # kernel2 = np.ones((1, 9), np.float32)
    sob_y = cv.filter2D(blur_edges, -1, kernel)
    # cv.imshow('sobel y', sob_y)

    grad_x = cv.Sobel(blur_edges, cv.CV_64F, 1, 0, ksize=5)
    grad_y = cv.Sobel(blur_edges, cv.CV_64F, 0, 1, ksize=5)

    grad_dir = np.arctan2(grad_y, grad_x)*180/np.pi
    grad_dir = (grad_dir + 180) % 180

    angle_thresh = 25
    filtered_edges = np.where((grad_dir > 90 - angle_thresh) & (grad_dir < 90 + angle_thresh), sob_y, 0).astype(np.uint8)
    new_grad_dir = np.where((grad_dir > 90 - angle_thresh) & (grad_dir < 90 + angle_thresh), grad_dir, 0).astype(np.uint8)
    angle_dev = np.std(new_grad_dir)
    suture_angle = np.mean(new_grad_dir)
    # cv.imshow('filtered edges', filtered_edges)
    kernel_morph0 = np.ones((5,5), np.uint8)
    kernel_morph1 = np.ones((3,3), np.uint8)
    kernel_morph2 = np.ones((2,2), np.uint8)
    eroded = cv.erode(filtered_edges, kernel_morph2, iterations=1)
    eroded = cv.erode(eroded, kernel_morph1, iterations=1)
    blur_eroded = cv.GaussianBlur(eroded, (15, 15), 0)
    eroded = cv.erode(blur_eroded, kernel_morph2, iterations=1)
    dilated = cv.dilate(eroded, kernel_morph1, iterations=1)
    # cv.imshow('eroded', eroded)
    # cv.imshow('dilated', dilated)
    horizontal_sum = np.sum(dilated, axis=1)
    new_horizontal_sum = np.where(horizontal_sum < 1200, 0, horizontal_sum)
    reverse_sum = new_horizontal_sum[::-1]
    # Create y-axis values (row indices)

    gaps = fn.zero_interval(reverse_sum)
    if len(gaps) != 0:
        gaps.pop(0)

    # print(gaps)
    interval_lengths = [end - start + 1 for start, end in gaps]
    # print(interval_lengths)
    # Calculate mean and variance
    mean_gap = np.mean(interval_lengths)
    std_dev = np.std(interval_lengths)
    # print("mean = {mean_gap}, std_dev = {std_dev}".format(mean_gap=mean_gap, std_dev=std_dev))
    new_interval = []
    new_gaps = []
    for i in range(len(interval_lengths)):
        if interval_lengths[i] > mean_gap - 1.5*std_dev:
            new_interval.append(interval_lengths[i])
            new_gaps.append(gaps[i])
    # print(new_interval)
    # print(new_gaps)
    complementary_gaps = []
    for i in range(len(new_gaps)-1):
        complementary_gaps.append((new_gaps[i][1], new_gaps[i+1][0]))
    mean_peaks = np.mean([end - start + 1 for start, end in complementary_gaps])
        
    suture_count = len(new_interval) +1
    suture_distance = mean_gap + mean_peaks
    dist_dev = std_dev
    cv.waitKey(0)

    y_values = np.arange(dilated.shape[0])
    plt.plot(reverse_sum, y_values)
    plt.title('Intensity vs Y Plot')
    plt.xlabel('Intensity')
    plt.ylabel('Y')
    # plt.show()

    return suture_count, suture_distance, suture_angle, dist_dev, angle_dev

# img = cv.imread('test/img2.png', cv.IMREAD_GRAYSCALE)
# count, distance, angle, dist_dev, angle_dev = evaluate(img)
# print("count: ", count)