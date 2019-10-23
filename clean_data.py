import cv2
import os
import numpy as np
import argparse
import pathlib

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--data', required=True,
                help='input directory where the data is')
args = ap.parse_args()

def dhash(image, hashSize=8):
    """
    :param image: image in grayscale
    :param hashSize: integer number
    :return: 64 bit hash number of thr image
    """
    img = cv2.resize(image, (hashSize+1, hashSize))
    diff = img[:, 1:] > img[:, :-1]
    hash_number = sum([2 ** i for i, v in enumerate(diff.flatten()) if v])
    return hash_number

def find_duplicates(subdir, hashing_thr=2**10):

    hash_numbers = []
    filepaths = [filepath for filepath in subdir.glob('*/')]

    for filepath in subdir.glob('*/'):
        img = cv2.imread(str(filepath))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hash_number = dhash(img)
        hash_numbers.append(hash_number)

    hash_numbers = np.array(hash_numbers).reshape(1, -1)
    diffs = np.abs(hash_numbers.T - hash_numbers)
    diffs = diffs > hashing_thr
    lower_idxs = np.tril_indices(diffs.shape[1], k=1)
    diffs[lower_idxs] = True
    final_mask = np.logical_not(np.logical_and.reduce(diffs, axis=0))

    return np.array(filepaths)[final_mask]

if __name__ == '__main__':

    data_dir = args.data
    filepaths = pathlib.Path(data_dir).glob('*/*')
    for filepath in filepaths:
        filepath = str(filepath)

        if not os.path.exists(filepath):
            print("[INFO] filepath {} do not exist".format(filepath))
            continue

        img = cv2.imread(filepath)

        if img is None:
            print("[INFO] deleting corrupted image {}".format(filepath))
            os.remove(filepath)
            continue

        if len(img.shape) != 3:
            print("[INFO] deleting gray image {}".format(filepath))
            os.remove(filepath)

    subdirs = [subdir for subdir in pathlib.Path(data_dir).glob('*/')]
    for subdir in subdirs:
        duplicated_files = find_duplicates(subdir)
        for dup in duplicated_files:
            print("[INFO] deleting duplicated image: {}".format(dup))
            os.remove(str(dup))

