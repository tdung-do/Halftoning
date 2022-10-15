import numpy as np
from PIL import Image

#Set GREYSCALE to True if expect the output to be greyscale image
GREYSCALE = True
img_name = '1665_Girl_with_a_Pearl_Earring.jpeg'
# img_name = 'Ddo_Ava.png'
# img_name = 'Di-choi-cover-image.png'

img = Image.open(img_name)


# img.show()



# Change the image into greyscale if wanted
if GREYSCALE:
    img = img.convert(mode="L")
    

    

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
    for i in range(n):
        tmp1 = i - mid
        if 0 <= row + tmp1 < new_h:
            for j in range(n):
                tmp2 = j - mid
                if 0 <= col + tmp2 < new_w:
                    arr[row + tmp1, col + tmp2] += diff * dist_mat[i, j]

        
"""
Dithering
"""
def topl_botr_dither(img, nc, mat):
    arr = np.array(img, dtype= float) / 255
    for row in range(new_h):
        for col in range(new_w):
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
    
    for row in range(new_h - 1, -1, -1):
        for col in range(new_w -1, -1, -1):
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
    
    for row in range(new_h):
        if turn > 0:
            for col in range(new_w):
                #Update new color value for each pixel
                old_val = arr[row, col].copy()
                new_val = new_pixel_val(old_val, nc)
                arr[row, col] = new_val
                
                #Distribute "error"
                diff = old_val - new_val
                dist_error(row, col, diff, arr, l_r_mat)
        else:
            for col in range(new_w -1, -1, -1):
                #Update new color value for each pixel
                old_val = arr[row, col].copy()
                new_val = new_pixel_val(old_val, nc)
                arr[row, col] = new_val
                
                #Distribute "error"
                diff = old_val - new_val
                dist_error(row, col, diff, arr, r_l_mat)
        turn *= -1
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

w, h = img.size
for i in [100]:
    # Resize the original image or, in other word, reduce number of pixels
    new_w = i
    new_h = int(h * new_w / w)
    img = img.resize(size = (new_w, new_h))
    # img.show()
    og_arr = np.array(img, dtype=float)

    tmpArr = topl_botr_dither(img, 2, FS_mat)
    # img1 = Image.fromarray(tmpArr)
    # print("topl_botr_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    print("topl_botr_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img1.show()
    # tmp = './TestingImg/' + img_name.split('.')[0] + '_FS_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img1.save(tmp)
    
    # tmpArr = palette_reduce(img, 2)
    # img2 = Image.fromarray(tmpArr)
    # img2.show()
    # tmp = img_name.split('.')[0] + '_palette_reduce_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img2.save(tmp)
    
    tmpArr = botr_topl_dither(img, 2, FS_botr_topl_mat)
    # img3 = Image.fromarray(tmpArr)
    # print("botr_topl_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    print("botr_topl_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img3.show()
    # tmp = img_name.split('.')[0] + '_FS_reversed_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img3.save(tmp)
    
    tmpArr = topl_botr_dither(img, 2, FS_mod_mat)
    # img4 = Image.fromarray(tmpArr)
    # print("topl_botr_dither FS_mod_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    print("topl_botr_dither FS_mod_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img4.show()
    # tmp = img_name.split('.')[0] + '_FS_modified_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img4.save(tmp)
    
    tmpArr = topl_botr_dither(img, 2, JJN_mat)
    # img5 = Image.fromarray(tmpArr)
    # print("topl_botr_dither JJN_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    print("topl_botr_dither JJN_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img5.show()
    # tmp  =img_name.split('.')[0] + '_JJN_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img5.save(tmp)
    
    tmpArr = topl_serpentine_dither(img, 2, FS_mat, FS_r_l_mat)
    # img6 = Image.fromarray(tmpArr)
    # print("topl_serpentine_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    print("topl_serpentine_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img6.show()
    # tmp = img_name.split('.')[0] + '_FS_topl_serpentine_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img6.save(tmp)

               
