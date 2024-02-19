"""
KERNELS VARIABLES FILE, HOLDS MOST OF THE KERNELS FOR THE IMG FILTERING

FILE IS COMPLETE AS OF 21/8/23 DO NOT MODIFY FURTHER
"""



import numpy as np


#direction KERNELS

S2N_kernel = np.array([
    [-1, -1, -1, -1, -1],
    [-1, -2, -4, -2, -1],
    [0, 0, 0, 0, 0],
    [1, 2, 4, 2, 1],
    [1, 1, 1, 1, 1]
])

N2S_kernel = np.array([
    [1, 1, 1, 1, 1],
    [1, 2, 4, 2, 1],
    [0, 0, 0, 0, 0],
    [-1, -2, -4, -2, -1],
    [-1, -1, -1, -1, -1]
])

W2E_kernel = np.array([
    [1, 1, 0, -1, -1],
    [1, 2, 0, -2, -1],
    [1, 4, 0, -4, -1],
    [1, 2, 0, -2, -1],
    [1, 1, 0, -1, -1]
])

E2W_kernel = np.array([
    [-1, -1, 0, 1, 1],
    [-1, -2, 0, 2, 1],
    [-1, -4, 0, 4, 1],
    [-1, -2, 0, 2, 1],
    [-1, -1, 0, 1, 1]
])

blurred_kernel = (1 / 256) * np.array([[1, 4, 6, 4, 1],
                                    [4, 16, 24, 16, 4],
                                    [6, 24, 36, 24, 6],
                                    [4, 16, 24, 16, 4],
                                    [1, 4, 6, 6, 1]])

normalisation_kernel = (1/20) * np.array([
                                          
                                          [1,1,1,1],
                                          [1,2,2,1],
                                          [1,2,2,1],
                                          [1,1,1,1]])
""" ridge_kernel = np.array([
    [-1, -1, 0, 1, 1],
    [-1, -2, 0, 2, 1],
    [-1, -4, 0, 4, 1],
    [-1, -2, 0, 2, 1],
    [-1, -1, 0, 1, 1]
]) """

""" 
ridge_kernel = np.array([
    [-1, -1, -1, -1, -1],
    [-1, -2, -4, -2, -1],
    [0, 0, 0, 0, 0],
    [1, 2, 4, 2, 1],
    [1, 1, 1, 1, 1]
])
"""