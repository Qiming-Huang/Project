from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.layers import Conv2D, Flatten
from tensorflow.keras.layers import Reshape, Conv2DTranspose
from tensorflow.keras.models import Model
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend as K

import numpy as np

train = np.load('../sudoku.npz')['train'][:100000] / 9
train = train.reshape((100000, 9, 9, 1))
test = np.load('../sudoku.npz')['train'][100000:110000] / 9
test = test.reshape((10000, 9, 9, 1))

input_shape = (9, 9, 1)
batch_size = 32
kernel_size = 3
latent_dim = 3

layer_filters = [32, 64]
inputs = Input(shape=input_shape, name='encoder_input')
x = inputs

for filters in layer_filters:
    x = Conv2D(filters=filters,
               kernel_size=kernel_size,
               activation='relu',
               strides=2,
               padding='same')(x)
shape = K.int_shape(x)
x = Flatten()(x)
latent = Dense(latent_dim, name='latent_vector')(x)
encoder = Model(inputs,
                latent,
                name='encoder')
encoder.summary()
plot_model(encoder,
           to_file='encoder.png',
           show_shapes=True)

latent_inputs = Input(shape=(latent_dim,), name='decoder_input')
# use the shape (7, 7, 64) that was earlier saved
x = Dense(shape[1] * shape[2] * shape[3])(latent_inputs)
# from vector to suitable shape for transposed conv
x = Reshape((shape[1], shape[2], shape[3]))(x)
# for filters in layer_filters[::-1]:
#     x = Conv2DTranspose(filters=filters,
#                         kernel_size=kernel_size,
#                         activation='relu',
#                         strides=,
#                         padding='same')(x)
x = Conv2DTranspose(filters=64,
                    kernel_size=(3,3),
                    activation='relu',
                    strides=1,
                    padding='same')(x)
x = Conv2DTranspose(filters=32,
                    kernel_size=(3,3),
                    activation='relu',
                    strides=3,
                    padding='same')(x)

outputs = Conv2DTranspose(filters=1,
                          kernel_size=kernel_size,
                          activation='sigmoid',
                          padding='same',
                          name='decoder_output')(x)
decoder = Model(latent_inputs, outputs, name='decoder')
decoder.summary()
autoencoder = Model(inputs,
                    decoder(encoder(inputs)),
                    name='autoencoder')
autoencoder.summary()

autoencoder.compile(loss='mse', optimizer='adam')
autoencoder.fit(train,
                train,
                validation_data=(test, test),
                epochs=20,
                batch_size=batch_size)

encoder.save('encoder.h5')
