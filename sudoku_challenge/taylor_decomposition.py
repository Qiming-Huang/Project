"""
Perform taylor decomposition, plot th result and calculate the dfficulty score
"""
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
from tqdm import tqdm
import matplotlib.pyplot as plt

# calculate difficulty score
def cal_score(grad, x):
    sig_score = (grad * x).numpy()
    sig_score = sig_score.reshape((9,9))
    cot = 0
    for row in range(9):
        for col in range(9):
            if (sig_score[row][col] > 0) & (sig_score[row][col] != 0):
                cot += 1
    return cot / 81

# plot result
def plot_res(df_score):
    plt.hist(df_score, bins=10)
    plt.show()

# loal model and preprocess    
model = load_model('sudoku.h5')
data = np.load('sudoku.npz')
x = data['train'][:20000]
sig_score = []
df_score = []

# calculate significant score which is taylor dicomposition
for i in tqdm(range(100)):
    cal_x = x[i].reshape((1,9,9,1))
    cal_x = tf.constant(cal_x, dtype=tf.float32)
    with tf.GradientTape() as tape:
        tape.watch(cal_x)
        y = model(cal_x)
    grad = tape.gradient(y, cal_x)
    sig_score.append((grad * cal_x).numpy().reshape((9,9)))
    df_score.append(cal_score(grad, cal_x))

plot_res(df_score)
