import numpy as np
from PIL import Image
from Dithering import *

#Set GREYSCALE to True if expect the output to be greyscale image
GREYSCALE = False
# img_name = './OriginalImg/Ddo_Ava.png'
img_name = './OriginalImg/Di-choi-cover-image.png'
# img_name = './OriginalImg/Girl_with_a_Pearl_Earring.jpeg'
# img_name = './OriginalImg/Starry_Night_Vincent_van_Gogh.webp'
# img_name = './OriginalImg/The_Kiss_Gustav_Klimt.jpeg'
# img_name = './OriginalImg/The_Lovers_II_Rene_Magritte.jpeg'


img = Image.open(img_name)


img.show()


# Change the image into greyscale if wanted
if GREYSCALE:
    img = img.convert(mode="L")
    


#Testing
w, h = img.size
# print(w,h)
for i in [50]:
    # Resize the original image or, in other word, reduce number of pixels
    new_w = i
    new_h = int(h * new_w / w)
    img = img.resize(size = (new_w, new_h))
    # img.show()
    og_arr = np.array(img, dtype=float)

    # print(i)
    tmpArr = topl_botr_dither(img, 2, FS_mat)
    img1 = Image.fromarray(tmpArr)
    # print("topl_botr_dither FS_mat 1 by 1 error value: ", MSE_1by1(tmpArr, og_arr))
    # print("topl_botr_dither FS_mat 2 by 2 error value: ", MSE_2by2(tmpArr, og_arr))
    img1.show()
    # tmp = './TestingImg/' + img_name.split('.')[0] + '_FS_GS_width=' + str(i) + '.' + img_name.split('.')[1]
    # img1.save(tmp)
    
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

               