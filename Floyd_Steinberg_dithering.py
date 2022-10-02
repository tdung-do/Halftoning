import numpy as np
from PIL import Image

#Set GREYSCALE to True if expect the output to be greyscale image
GREYSCALE = True
# img_name = '1665_Girl_with_a_Pearl_Earring.jpeg'
img_name = 'Ddo_Ava.png'
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

FS_rev_mat = np.array([[1,      5,      3], 
                       [7,      0,      0], 
                       [0,      0,      0]], dtype = float) /16
    
FS_mod_mat = np.array([[0,      0,      0], 
                       [0,      0,      1], 
                       [13,     1,      1]], dtype = float) /16


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


#Distribute error when recurse from top left to bottom right
def dist_error(row, col, diff, arr, dist_mat):
    #Coefficients
    # right = 7 / 16
    # bot_l = 3 / 16
    # bot = 5 / 16
    # bot_r = 1 / 16
    
    # if col + 1 < new_w:
    #     arr[row, col + 1] += diff * right
    # if row + 1 < new_h:
    #     if col - 1 >= 0:
    #         arr[row + 1, col - 1] += diff * bot_l
            
    #     arr[row + 1, col] += diff * bot
        
    #     if col + 1 < new_w:
    #         arr[row + 1, col + 1] += diff * bot_r
    
    
    n = len(dist_mat)
    mid = n // 2
    for i in range(mid, n):
        tmp1 = i - mid
        if row + tmp1 < new_h:
            for j in range(n):
                tmp2 = j - mid
                if 0 <= col + tmp2 < new_w:
                    arr[row + tmp1, col + tmp2] += diff * dist_mat[i, j]
        
    
def dist_error_rev(row, col, diff, arr, dist_mat):
    #Coefficients
    # left = 7 / 16
    # top_r = 2 / 16
    # top = 5 / 16
    # top_l = 2 / 16
    
    # if col - 1 >= 0:
    #     arr[row, col - 1] += diff * left
    # if row - 1 >= 0:
    #     if col + 1 < new_w:
    #         arr[row - 1, col + 1] += diff * top_r
            
    #     arr[row - 1, col] += diff * top
        
    #     if col - 1 >= 0:
    #         arr[row - 1, col - 1] += diff * top_l
    
    n = len(dist_mat)
    mid = n // 2
    for i in range(mid + 1):
        tmp1 = i - mid
        if row + tmp1 >= 0:
            for j in range(n):
                tmp2 = j - mid
                if 0 <= col + tmp2 < new_w:
                    arr[row + tmp1, col + tmp2] += diff * dist_mat[i, j]
    

def Floyd_Steinberg_dither(img, nc):
    arr = np.array(img, dtype= float) / 255
    
    for row in range(new_h):
        for col in range(new_w):
            #Update new color value for each pixel
            old_val = arr[row, col].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, col] = new_val
            
            #Distribute "error"
            diff = old_val - new_val
            dist_error(row, col, diff, arr, FS_mat)
            
    arr = np.array(arr * 255 , dtype = np.uint8)
    return Image.fromarray(arr)


def Floyd_Steinberg_dither_reverse(img, nc):
    arr = np.array(img, dtype= float) / 255
    
    for row in range(new_h - 1, -1, -1):
        for col in range(new_w -1, -1, -1):
            #Update new color value for each pixel
            old_val = arr[row, col].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, col] = new_val
            
            #Distribute "error"
            diff = old_val - new_val
            dist_error_rev(row, col, diff, arr, FS_rev_mat)
            
    arr = np.array(arr * 255 , dtype = np.uint8)
    return Image.fromarray(arr)

    
def modified_dither(img, nc):
    arr = np.array(img, dtype= float) / 255
    
    for row in range(new_h):
        for col in range(new_w):
            #Update new color value for each pixel
            old_val = arr[row, col].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, col] = new_val
            
            #Distribute "error"
            diff = old_val - new_val
            dist_error(row, col, diff, arr, FS_mod_mat)
            
    arr = np.array(arr * 255 , dtype = np.uint8)
    return Image.fromarray(arr)

def Jarvis_Judice_Ninke_dither(img, nc):
    arr = np.array(img, dtype= float) / 255
    
    for row in range(new_h):
        for col in range(new_w):
            #Update new color value for each pixel
            old_val = arr[row, col].copy()
            new_val = new_pixel_val(old_val, nc)
            arr[row, col] = new_val
            
            #Distribute "error"
            diff = old_val - new_val
            dist_error(row, col, diff, arr, JJN_mat)
            
    arr = np.array(arr * 255 , dtype = np.uint8)
    return Image.fromarray(arr)

def palette_reduce(img, nc):
    """Simple palette reduction without dithering."""
    arr = np.array(img, dtype=float) / 255
    arr = new_pixel_val(arr, nc)

    arr = np.array(arr * 255 , dtype = np.uint8)
    return Image.fromarray(arr)


w, h = img.size
for i in [50]:
    # Resize the original image or, in other word, reduce number of pixels
    new_w = i
    new_h = int(h * new_w / w)
    img = img.resize(size = (new_w, new_h))


    img1 = Floyd_Steinberg_dither(img, 2)
    # img1.show()
    tmp  =img_name.split('.')[0] + '_FS_GS_width=' + str(i) +'.png'
    img1.save(tmp)
    
    # img2 = palette_reduce(img, 2)
    # # img2.show()
    # img2.save('Palette-{}.jpg'.format(i))
    
    # img3 = Floyd_Steinberg_dither_reverse(img, 2)
    # img3.show()
    # img3.save('ReversedFS-width={}.jpg'.format(i))
    
    # img4 = modified_dither(img, 2)
    # img4.show()
    # img4.save('ModFS-width={}.jpg'.format(i))
    
    img5 = Jarvis_Judice_Ninke_dither(img, 2)
    # img5.show()
    
    tmp  =img_name.split('.')[0] + '_JJN_GS_width=' + str(i) + '.png'
    img5.save(tmp)
    
    
    
    

            
            
            
            
            
            