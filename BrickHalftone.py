import numpy as np
from Dithering import *


left_brick_dist_mat = np.array([[0,     0,      0,      0,      0],
                                [0,     0,      0,      0,      0],
                                [0,     0,      0,      0,      9],
                                [3,     6,      8,      6,      3],
                                [1,     3,      5,      3,      1]], dtype= float) / 48

right_brick_dist_mat = np.array([[0,     0,      0,      0,      0],
                                [0,     0,      0,      0,      0],
                                [0,     0,      0,      7,      5],
                                [3,     5,      7,      5,      3],
                                [1,     3,      5,      3,      1]], dtype= float) / 48




left_brick_dist_mat_2 = np.array([[0,     0,      0,      0,      0],
                                [0,     0,      0,      0,      0],
                                [0,     0,      0,      0,      4],
                                [1,     3,      4,      3,      1],
                                [0,     0,      0,      0,      0]], dtype= float) / 16

right_brick_dist_mat_2 = np.array([[0,      0,      0], 
                                [0,      0,      7], 
                                [3,      5,      1]], dtype = float) /16




def brick_dither(img, nc, mat_1, mat_2):
    arr = np.array(img, dtype= float) / 255
    tmp_h, tmp_w = len(arr), len(arr[0])
    for row in range(tmp_h):
        if tmp_w % 2 == 1 and row % 2 == 1:
            old_val = arr[row, 0].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, 0] = new_val
            for col in range(1, tmp_w):
                #Update new color value for each pixel
                if col % 2 == 1:
                    old_val_1 = arr[row, col].copy()
                    old_val_2 = arr[row, col+1].copy()
                    old_val = (old_val_1 + old_val_2) / 2
                    new_val = new_pixel_val(old_val, nc)
                    arr[row, col] = new_val
                    arr[row, col+1] = new_val
                    #Distribute "error"
                    diff = old_val - new_val
                    dist_error(row, col, diff, arr, mat_1)
                    dist_error(row, col+1, diff, arr, mat_2)
        elif tmp_w % 2 == 1 and row % 2 == 0:
            for col in range(tmp_w - 1):
                #Update new color value for each pixel
                if col % 2 == 0:
                    old_val_1 = arr[row, col].copy()
                    old_val_2 = arr[row, col+1].copy()
                    old_val = (old_val_1 + old_val_2) / 2
                    new_val = new_pixel_val(old_val, nc)
                    arr[row, col] = new_val
                    arr[row, col+1] = new_val
                    #Distribute "error"
                    diff = old_val - new_val
                    dist_error(row, col, diff, arr, mat_1)
                    dist_error(row, col+1, diff, arr, mat_2)
            old_val = arr[row, tmp_w - 1].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, tmp_w - 1] = new_val
        
        elif tmp_w % 2 == 0 and row % 2 == 1:
            old_val = arr[row, 0].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, 0] = new_val
            for col in range(1, tmp_w-1):
                #Update new color value for each pixel
                if col % 2 == 1:
                    old_val_1 = arr[row, col].copy()
                    old_val_2 = arr[row, col+1].copy()
                    old_val = (old_val_1 + old_val_2) / 2
                    new_val = new_pixel_val(old_val, nc)
                    arr[row, col] = new_val
                    arr[row, col+1] = new_val
                    #Distribute "error"
                    diff = old_val - new_val
                    dist_error(row, col, diff, arr, mat_1)
                    dist_error(row, col+1, diff, arr, mat_2)
            old_val = arr[row, tmp_w - 1].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, tmp_w - 1] = new_val
        else:
            for col in range(tmp_w ):
                #Update new color value for each pixel
                if col % 2 == 0:
                    old_val_1 = arr[row, col].copy()
                    old_val_2 = arr[row, col+1].copy()
                    old_val = (old_val_1 + old_val_2) / 2
                    new_val = new_pixel_val(old_val, nc)
                    arr[row, col] = new_val
                    arr[row, col+1] = new_val
                    #Distribute "error"
                    diff = old_val - new_val
                    dist_error(row, col, diff, arr, mat_1)
                    dist_error(row, col+1, diff, arr, mat_2)
    
            
    return np.array(arr * 255, dtype=np.uint8)

