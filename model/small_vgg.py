from keras.models import Sequential
from keras.layers import BatchNormalization, Dense, Conv2D, ReLU
from keras.layers import Dropout, MaxPooling2D, Activation, Flatten
from keras import backend as K

class SmallerVGG:

    @staticmethod
    def build(width, height, depth, classes):
        model = Sequential()
        inputShape = (height, width, depth)
        channelDim = -1

        if K.image_data_format() == 'channels_first':
            inputShape = (depth, height, width)
            channelDim = 1

        model.add(Conv2D(32, (3,3), padding='same', input_shape=inputShape))
        model.add(BatchNormalization(axis=channelDim))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(3,3)))
        model.add(Dropout(0.25))

        model.add(Conv2D(64, (3,3), padding='same'))
        model.add(BatchNormalization(axis=channelDim))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3,3), padding='same'))
        model.add(BatchNormalization(axis=channelDim))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, (3,3), padding='same'))
        model.add(BatchNormalization(axis=channelDim))
        model.add(Activation('relu'))
        model.add(Conv2D(128, (3,3), padding='same'))
        model.add(BatchNormalization(axis=channelDim))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(classes))
        model.add(Activation('softmax'))

        return model