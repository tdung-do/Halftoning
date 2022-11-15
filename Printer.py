import numpy as np
from PIL import Image
from Dithering import *
from BrickHalftone import *

#Set GREYSCALE to True if expect the output to be greyscale image
GREYSCALE = True
img_list = [ './OriginalImg/Ddo_Ava.png',
            './OriginalImg/Di-choi-cover-image.png',
            './OriginalImg/Girl_with_a_Pearl_Earring.jpeg',
            './OriginalImg/Starry_Night_Vincent_van_Gogh.webp',
            './OriginalImg/The_Kiss_Gustav_Klimt.jpeg',
            './OriginalImg/The_Lovers_II_Rene_Magritte.jpeg',
            './OriginalImg/Frankenstein_Tom_Carlton.jpeg',
            './OriginalImg/frankenstein300x300.jpg',
            './OriginalImg/Marilyn_Monroe_Laughing.webp',
            './OriginalImg/Albert_Einstein.webp']

img_name = img_list[3]


img = Image.open(img_name)


# img.show()


# Change the image into greyscale if wanted
if GREYSCALE:
    img = img.convert(mode="L")
    


#Testing
w, h = img.size
# print(w,h)
for i in [64]:
    # Resize the original image or, in other word, reduce number of pixels
    new_w = i
    new_h = int(h * new_w / w)
    img = img.resize(size = (new_w, new_h))
    # img.show()
    og_arr = np.array(img, dtype=float)
    color_channels = 4
    # print(i)
    # tmpArr = topl_botr_dither(img, 2, FS_mat)
    # img1 = Image.fromarray(tmpArr)
    # # print("topl_botr_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # # print("topl_botr_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img1.show()
    # # tmp = './TestingImg/' + img_name.split('.')[0] + '_FS_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # # img1.save(tmp)
    
    # tmpArr = palette_reduce(img, 2)
    # img2 = Image.fromarray(tmpArr)
    # img2.show()
    # tmp = img_name.split('.')[0] + '_palette_reduce_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img2.save(tmp)
    
    # tmpArr = botr_topl_dither(img, 2, FS_botr_topl_mat)
    # img3 = Image.fromarray(tmpArr)
    # print("botr_topl_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # print("botr_topl_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img3.show()
    # tmp = img_name.split('.')[0] + '_FS_reversed_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img3.save(tmp)
    
    # tmpArr = topl_botr_dither(img, 2, FS_mod_mat)
    # img4 = Image.fromarray(tmpArr)
    # print("topl_botr_dither FS_mod_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # print("topl_botr_dither FS_mod_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img4.show()
    # tmp = img_name.split('.')[0] + '_FS_modified_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img4.save(tmp)
    
    # tmpArr = topl_botr_dither(img, 2, JJN_mat)
    # img5 = Image.fromarray(tmpArr)
    # print("topl_botr_dither JJN_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # print("topl_botr_dither JJN_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img5.show()
    # tmp  =img_name.split('.')[0] + '_JJN_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img5.save(tmp)
    
    # tmpArr = topl_serpentine_dither(img, 2, FS_mat, FS_r_l_mat)
    # img6 = Image.fromarray(tmpArr)
    # print("topl_serpentine_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # print("topl_serpentine_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img6.show()
    # tmp = img_name.split('.')[0] + '_FS_topl_serpentine_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img6.save(tmp)

    # tmpArr = brick_dither(img, color_channels, left_brick_dist_mat, right_brick_dist_mat)
    # img7 = Image.fromarray(tmpArr)
    # # print("topl_botr_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # # print("topl_botr_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img7.show()
    # # tmp = './TestingImg/frankenstein_Brick_Dither_64x64.jpg'
    # # img7.save(tmp)
    
    
    # tmpArr = brick_dither(img, color_channels, left_brick_dist_mat_2, right_brick_dist_mat_2)
    # img8 = Image.fromarray(tmpArr)
    # # print("topl_botr_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # # print("topl_botr_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    # img8.show()
    # # tmp = './TestingImg/Frankenstein_Brick_Dither_32x32.PNG' #+ img_name.split('.')[-1]
    # # img8.save(tmp)
    
    tmpArr = topl_botr_dither_half(img, 2, FS_mod_mat)
    img9 = Image.fromarray(tmpArr)
    # print("topl_botr_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # print("topl_botr_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    img9.show()
    # tmp = './TestingImg/frankenstein_Brick_Dither_64x64.jpg'
    # img7.save(tmp)