__author__ = 'Ravi Budhu'
__license__ = 'Apache License, Version 2.0'

from os import path
import argparse
from math import floor
from sklearn.cluster import KMeans
import cv2
import numpy as np

def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)
    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
    # return the histogram
    return hist

parser = argparse.ArgumentParser(description='Turn image into blockheads')
parser.add_argument('input_file', help='Input image file')
parser.add_argument('--block_height', dest='block_height', type=int, default=15)
parser.add_argument('--clusters', dest='clusters', type=int, default=7)
parser.add_argument('--max_height', dest='max_height', type=int, default=300)
parser.add_argument('--tolerance', dest='tolerance', type=float, default=0.85)
parser.add_argument('--log', action='store_true')
args = parser.parse_args()

image = cv2.imread(args.input_file)
height, width = image.shape[0:2]

# Resize the image if it is too tall
if height > args.max_height:
    scale_percent = args.max_height / height
    width = int(width * scale_percent)
    image = cv2.resize(image, (width, args.max_height),
                       interpolation=cv2.INTER_AREA)
height, width = image.shape[0:2]
rec_height = floor(height/args.block_height)

# Add a border for edge detection
top = int(image.shape[0] * 0.02)
bottom = top
left = int(image.shape[1] * 0.02)
right = left
border_image = cv2.copyMakeBorder(image, top, bottom, left, right,
                                  cv2.BORDER_CONSTANT, None,
                                  image[0, 0].tolist())
# Find edges
edges = cv2.Canny(border_image, 100, 200)
if args.log:
    cv2.imwrite('edges.jpg', edges)
# Find contours
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros((border_image.shape[0], border_image.shape[1]), np.uint8)
cv2.drawContours(mask, contours,
                 -1, (255, 255, 255), 3)
# Do it again with the drawn contours to create a mask
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros((border_image.shape[0], border_image.shape[1]), np.uint8)
cv2.drawContours(mask, [max(contours, key=cv2.contourArea)],
                 -1, 255, thickness=-1)
# Convert image to HSV
x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
src = cv2.cvtColor(border_image, cv2.COLOR_BGR2RGB)
# Crop the image
src = src[y:y+h, x:x+w]
mask = mask[y:y+h, x:x+w]
if args.log:
    cv2.imwrite('src.jpg', src)
    cv2.imwrite('mask.jpg', mask)

# Convert mask to boolean
mask = np.array(mask, dtype=bool)

# Output file
out = np.zeros((height, int(width / 2), 3), dtype='uint8')
steps = int(height / rec_height)

for i in range(0, steps):
    cropped_image = src[i*rec_height:(i+1)*rec_height, 0:width]
    cropped_mask = mask[i*rec_height:(i+1)*rec_height, 0:width]
    valid_pixels = []
    # Create an array with the pixels to consider in the cropped_image
    c = cropped_image[cropped_mask]
    # Must be a faster way to do this
    for d in c:
        valid_pixels.append(d)
    if not valid_pixels:
        continue
    # Cluster with KMeans to find dominant colors
    clt = KMeans(args.clusters)
    clt.fit(valid_pixels)
    hist = centroid_histogram(clt)
    centroids = clt.cluster_centers_
    zipped = zip(hist, centroids)
    zipped = list(zipped)
    # Sort by most dominant percent
    res = sorted(zipped, key = lambda x: x[0], reverse=True)
    # Get the most dominant color
    dominant_color = res[0][1]
    if args.log:
        print('dominant color = {}'.format(
            dominant_color.astype('uint8').tolist()))
    cv2.rectangle(out, (0, i*rec_height), (int(width/2), (i+1)*rec_height),
                  dominant_color.astype('uint8').tolist(), -1)
# Write the output
out = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)
fname, ext = path.splitext(args.input_file)
cv2.imwrite('{}-block{}'.format(fname, ext), out)
