import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import functions as fn
import evaluate as ev

import os
import cv2
import csv
import sys

def process_images(img_dir, output_csv):
    if not os.path.exists(img_dir):
        print(f"Error: The specified directory '{img_dir}' does not exist.")
        return
    with open(output_csv, 'w', newline='') as csv_file:
        fieldnames = ['image name', 'number of sutures', 'distance', 'angle']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for filename in os.listdir(img_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add more image extensions if needed
                image_path = os.path.join(img_dir, filename)
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                count, distance, angle, dist_dev, angle_dev = ev.evaluate(img)
                writer.writerow({'image name': filename, 'number of sutures': count, 'distance': round(distance,2), 'angle': round(angle,2)})
                # print("count: ", count)

    print(f"CSV file '{output_csv}' generated successfully for part {part_id}.")

def compare_images(input_csv, output_csv):
    with open(input_csv, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header row
        rows = list(reader)

    with open(output_csv, 'w', newline='') as output_csv_file:
        fieldnames = ['img1 path', 'img2 path', 'output distance', 'output angle']
        writer = csv.DictWriter(output_csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            img1_path, img2_path = row[0], row[1]

            img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

            count1, distance1, angle1, dist_dev1, angle_dev1 = ev.evaluate(img1)
            count2, distance2, angle2, dist_dev2, angle_dev2 = ev.evaluate(img2)

            # Compare based on inter-suture distance
            if dist_dev1 < dist_dev2:
                output_distance = 1
            else:
                output_distance = 2

            # Compare based on angulation of sutures
            if angle_dev1 < angle_dev2:
                output_angle = 1
            else:
                output_angle = 2

            writer.writerow({
                'img1 path': img1_path,
                'img2 path': img2_path,
                'output distance': output_distance,
                'output angle': output_angle
            })

    print(f"Comparison results saved to '{output_csv}'.")

if __name__ == "__main__":
   
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <part id> <img dir> <output csv>")
        sys.exit(1)

    part_id = sys.argv[1]
    img_dir = sys.argv[2]
    output_csv = sys.argv[3]
    if(int(part_id) == 1):
        process_images(img_dir, output_csv)
    elif(int(part_id) == 2):
        compare_images(img_dir, output_csv)
