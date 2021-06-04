import scipy.io as scio
import matplotlib.pyplot as plt
import numpy as np

data = scio.loadmat('data.mat')
weight = scio.loadmat('weight.mat')

data = data['b'].reshape((1001))
weight = weight['filter_lowpass'].reshape((129))

# class filter:
#     def __init__(self, order, h):
#         self.order = order
#         self.h = h
#         self.output = []
#
#     def FIR_Filter(self, vi):
#         for i in range(len(vi)):
#             sum = 0
#             if i < self.order:
#                 for j in range(i):
#                     sum = sum + self.h[j] * vi[i - j]
#             else:
#                 for j in range(self.order):
#                     sum = sum + self.h[j] * vi[i - j]
#
#             self.output.append(sum)
#         return self.output

h = [-0.0039, 0.0000, 0.0321, 0.1167, 0.2207, 0.2687, 0.2207, 0.1167, 0.0321, 0.0000, -0.0039]

def FIR_Filter(order, h, vi):
    output = []
    for i in range(len(vi)):
        sum = 0
        if i < order:
            for j in range(i):
                sum = sum + h[j] * vi[i - j]
        else:
            for j in range(order):
                sum = sum + h[j] * vi[i - j]

        output.append(sum)
    return output


output_1 = FIR_Filter(10, h, data[200:400])
output_2 = FIR_Filter(10, h, data[400:600])
output_3 = FIR_Filter(10, h, data[600:800])

last = output_1[-1]
delta = (last - output_2[10]) / 10

output_2[0] = last

for i in range(1,10,1):
    noise = np.random.normal(0, 0.5 ** 0.5, 1)
    output_2[i] = (output_2[i-1] - delta) + noise


# output_2 = fill(output_1[-1], output_2, 10)
# output_3 = fill(output_2[-1], output_3, 10)


plt.figure()
plt.plot(range(200+10,400,1), output_1[10:])
plt.plot(range(400,600,1), output_2)
# plt.plot(range(600+10,800,1), output_3[10:])
# plt.plot(range(1,1002,1), data)
plt.show()



