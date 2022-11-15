import numpy as np


#Floyd-Steinberg Dithering
FS_mat = np.array([[0,      0,      0], 
                   [0,      0,      7], 
                   [3,      5,      1]], dtype = float) /16

FS_botr_topl_mat =    np.array([[1,      5,      3], 
                                [7,      0,      0], 
                                [0,      0,      0]], dtype = float) /16
    
FS_mod_mat = np.array([[0,      0,      0], 
                       [0,      0,      1], 
                       [13,     1,      1]], dtype = float) /16

FS_r_l_mat =  np.array([[0,      0,      0], 
                        [7,      0,      0], 
                        [3,      5,      1]], dtype = float) /16



#Jarvis-Judice-Ninke Dithering
JJN_mat = np.array([[0,     0,      0,      0,      0],
                    [0,     0,      0,      0,      0],
                    [0,     0,      0,      7,      5],
                    [3,     5,      7,      5,      3],
                    [1,     3,      5,      3,      1]], dtype= float) / 48


JJN_mod_mat = np.array([[0,     0,      0,      0,      0],
                        [0,     0,      0,      0,      0],
                        [0,     0,      0,      7,      5],
                        [3,     5,      7,      5,      3],
                        [1,     3,      5,      3,      1]], dtype= float) / 48


"""
Get the "closest" colour to old_val in the 
range [0,1] per channeldivided into nc values.
"""
def new_pixel_val(old_val, nc):
    return np.round(old_val * (nc - 1)) / (nc - 1)


"""
Distribute error 
"""
def dist_error(row, col, diff, arr, dist_mat):    
    n = len(dist_mat)
    mid = n // 2
    tmp_h, tmp_w = len(arr), len(arr[0])
    for i in range(n):
        tmp1 = i - mid
        if 0 <= row + tmp1 < tmp_h:
            for j in range(n):
                tmp2 = j - mid
                if 0 <= col + tmp2 < tmp_w:
                    arr[row + tmp1, col + tmp2] += diff * dist_mat[i, j]

        
"""
Dithering
"""
def topl_botr_dither(img, nc, mat):
    arr = np.array(img, dtype= float) / 255
    tmp_h, tmp_w = len(arr), len(arr[0])
    for row in range(tmp_h):
        for col in range(tmp_w):
            #Update new color value for each pixel
            old_val = arr[row, col].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, col] = new_val
            
            #Distribute "error"
            diff = old_val - new_val
            dist_error(row, col, diff, arr, mat)
            
    return np.array(arr * 255, dtype=np.uint8)


def botr_topl_dither(img, nc, mat):
    arr = np.array(img, dtype= float) / 255
    tmp_h, tmp_w = len(arr), len(arr[0])
    for row in range(tmp_h - 1, -1, -1):
        for col in range(tmp_w -1, -1, -1):
            #Update new color value for each pixel
            old_val = arr[row, col].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, col] = new_val
            
            #Distribute "error"
            diff = old_val - new_val
            dist_error(row, col, diff, arr, mat)
    return np.array(arr * 255, dtype=np.uint8)


def topl_serpentine_dither(img, nc, l_r_mat, r_l_mat):
    arr = np.array(img, dtype= float) / 255
    turn = 1
    tmp_h, tmp_w = len(arr), len(arr[0])
    for row in range(tmp_h):
        if turn > 0:
            for col in range(tmp_w):
                #Update new color value for each pixel
                old_val = arr[row, col].copy()
                new_val = new_pixel_val(old_val, nc)
                arr[row, col] = new_val
                
                #Distribute "error"
                diff = old_val - new_val
                dist_error(row, col, diff, arr, l_r_mat)
        else:
            for col in range(tmp_w -1, -1, -1):
                #Update new color value for each pixel
                old_val = arr[row, col].copy()
                new_val = new_pixel_val(old_val, nc)
                arr[row, col] = new_val
                
                #Distribute "error"
                diff = old_val - new_val
                dist_error(row, col, diff, arr, r_l_mat)
        turn *= -1
    return np.array(arr * 255, dtype=np.uint8)


def topl_botr_dither_half(img, nc, mat):
    arr = np.array(img, dtype= float) / 255
    tmp_h, tmp_w = len(arr), len(arr[0])
    for row in range(tmp_h):
        for col in range(tmp_w):
            #Update new color value for each pixel
            old_val = arr[row, col].copy()
            new_val = new_pixel_val(old_val, nc)
            print(new_val)
            arr[row, col] = new_val
            
            #Distribute "error"
            diff = old_val - new_val
            dist_error(row, col, diff, arr, mat)
            
    return np.array(arr * 255, dtype=np.uint8)


def palette_reduce(img, nc):
    #Simple palette reduction without dithering
    arr = np.array(img, dtype=float) / 255
    arr = new_pixel_val(arr, nc)
    
    return np.array(arr * 255, dtype=np.uint8)


"""
Calculating error
"""
def MSE_1by1(arr, og_arr):
    arr = arr / 255
    og_arr = og_arr / 255
    diff = np.square(arr - og_arr)
    return np.sum(diff) / len(arr) / len(arr[0])


def MSE_2by2(arr, og_arr):
    arr = arr / 255
    og_arr = og_arr / 255
    diff = arr[:-1, :-1]
    r, c = len(diff), len(diff[0])
    for row in range(r):
        for col in range(c):
            diff[row, col] = (arr[row, col] + arr[row+1, col] + arr[row, col+1] + arr[row+1, col+1]
                              - og_arr[row, col] - og_arr[row+1, col] - og_arr[row, col+1] - og_arr[row+1, col+1])
    diff = np.square(diff) / 16
    return np.sum(diff) / r / c
