"""
Script to get images from google images using URL's
Code borrowed mostly from PyImageSearch
"""

import requests
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument('-u', '--urls', required=True, help='path to file containing urls')
ap.add_argument('-o', '--output', required=True, help='path to output images')
args = ap.parse_args()

if __name__ == '__main__':

    rows = open(args.urls).read().strip().split("\n")
    total = 0

    for url in rows:
        try:
            r = requests.get(url, timeout=60)
            p = os.path.join(args.output, '{}.jpg'.format(str(total).zfill(8)))
            f = open(p, 'wb')
            f.write(r.content)
            f.close()
            print("[INFO] downloaded: {}".format(p))

        except:
            print("[INFO] error downloading {} ... skipping".format(p))

        total += 1

    # Removing corrupted images
    for imagePath in os.listdir(args.output):
        imagePath = os.path.join(args.output, imagePath)

        try:
            image = cv2.imread(imagePath)

            if image is None:
                print("[INFO] deleting {}".format(imagePath))
                os.remove(imagePath)

        except:
            print("[INFO] deleting {}".format(imagePath))
            os.remove(imagePath)