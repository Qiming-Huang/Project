"""
To train a cnn model to solve sudoku puzzle for the later applying taylor decompostion using keras
training data set comes from https://www.kaggle.com/bryanpark/sudoku
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Reshape, Activation, BatchNormalization
from tensorflow.keras.utils import to_categorical, plot_model

# data preprocess
data = np.load('sudoku.npz')
train = data['train'] / 9
train = train.reshape((train.shape[0], 9, 9, 1))
target = data['target']


# build model
model = keras.models.Sequential()

model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same', input_shape=(9,9,1)))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))

model.add(Flatten())
model.add(Dense(81*10))
model.add(Reshape((81, 10)))
model.add(Activation('softmax'))

# train model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
model.fit(train, target, epochs=30000, batch_size=32)
model.save('my_model.h5')
model.summary()

