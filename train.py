import matplotlib
matplotlib.use("Agg")

from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.optimizers import Adam
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from model import small_vgg
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os
import pathlib


app = argparse.ArgumentParser()
app.add_argument('-d', '--dataset', required=True, help='path to input dataset')
app.add_argument('-m', '--model', required=True, help='path to model')
app.add_argument('-l', '--labelbin', required=True, help='path to output label binarizer')
app.add_argument('-p', '--plot', type=str, required=True, default='plot.png',
                 help='path to output accuracy/loss plot')
args = app.parse_args()

# Initialize the hyperparameters
EPOCHS = 100
INIT_LR = 1e-3
BS = 32
IMAGE_DIMS = (96, 96, 3)

# Initialize the data and labels
data = []
labels = []
label_to_index = {}

# grab the image paths and randomly shuffle them
print("[INFO] loading images ...")
data_path = pathlib.Path(args.dataset)
file_paths = [filepath for filepath in data_path.glob('*/*')]
label_names = sorted([cat for cat in os.listdir(args.dataset)])
for i, label_name in enumerate(label_names):
    label_to_index[label_name] = i

for file_path in file_paths:
    image = cv2.imread(file_path)
    image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    image = img_to_array(image)
    data.append(image)

    label = file_path.parent.name
    label = label_to_index[label]
    labels.append(label)

data = np.array(data, dtype='float') / 255.0
labels = np.array(labels)

(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2, random_state=42)

aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1, height_shift_range=0.1,
                         shear_range=0.2, zoom_range=0.2, horizontal_flip=True,
                         fill_mode='nearest')

print("[INFO] compiling model ...")
model = small_vgg.SmallerVGG.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0],
                                   depth=IMAGE_DIMS[2], classes=len(label_names))

optimizer = Adam(learning_rate=INIT_LR, decay=INIT_LR/EPOCHS)
model.compile(optimizer=optimizer,
              loss='categorical_crossentropy',
              metrics=['loss', 'accuracy'])
print("[INFO] training network ...")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
                        epochs=EPOCHS, validation_data=(testX, testY), steps_per_epoch=len(trainX)//BS)

plt.style.use("ggplot")
plt.figure()
N = EPOCHS
plt.plot(np.arange(0, N), H.history["loss"], label='train_loss')
plt.plot(np.arange(0, N), H.history["val_loss"], label='val_loss')
plt.plot(np.arange(0, N), H.history["acc"], label='train_acc')
plt.plot(np.arange(0, N), H.history["val_acc"], label='val_acc')
plt.title("Training Loss and Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper left")
plt.savefig(args.plot)
