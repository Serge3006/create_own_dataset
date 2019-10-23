import os
import cv2
import pathlib
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--dataset', required=True,
                help='directory to dataset')

args = ap.parse_args()

if __name__ == '__main__':

    data_dir = args.dataset
    new_height = 480
    for filepath in pathlib.Path(data_dir).glob('*/'):

        img = cv2.imread(str(filepath))
        print(img.shape)
        new_width = int(img.shape[1] * (new_height / img.shape[0]))
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        print(img.shape)
        cv2.putText(img, "n: next image", (10, 50), 2, 0.5, (0, 255, 255), 2)
        cv2.putText(img, "d: delete image", (10, 80), 2, 0.5, (0, 255, 255), 2)
        cv2.imshow("img", img)

        while True:
            key = cv2.waitKey(0)
            if key == ord("n") or key == ord("d") or key == ord("s"):
                break

        if key == ord('n'):
            continue

        elif key == ord('d'):
            print("[INFO] deleting not relevant image {}".format(filepath))
            os.remove(str(filepath))

        elif key == ord('s'):
            break