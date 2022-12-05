import numpy as np
import sys
from PIL import Image

# fname = './Mathematical approach/Frank_64.sol'

fname =  './SOL_files/' + sys.argv[1]
f = open(fname, 'r')

# print(fname)
print(f.readline().rstrip())
# exit()

height = int(f.readline().rstrip().split(' ')[-1])
width = int(f.readline().rstrip().split(' ')[-1])

arr = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        arr[i, j] = int(f.readline().rstrip().split(' ')[-1])
        
arr = np.array(arr / 3 * 255, dtype=np.uint8)



img = Image.fromarray(arr)

img.show()

# save_addr = '../OptimalImg/Frank_64_2x2_brick.PNG'
# img.save(save_addr)
        
        
        

# def MSE_1by1(arr, og_arr):
#     arr = arr / 255
#     og_arr = og_arr / 255
#     diff = np.square(arr - og_arr)
#     return np.sum(diff) #/ len(arr) / len(arr[0])


# def MSE_2by2(arr, og_arr):
#     arr = arr / 255
#     og_arr = og_arr / 255
#     diff = arr[:-1, :-1]
#     r, c = len(diff), len(diff[0])
#     for row in range(r):
#         for col in range(c):
#             diff[row, col] = (arr[row, col] + arr[row+1, col] + arr[row, col+1] + arr[row+1, col+1]
#                               - og_arr[row, col] - og_arr[row+1, col] - og_arr[row, col+1] - og_arr[row+1, col+1])
#     diff = np.square(diff) #/ 16
#     return np.sum(diff) #/ r / c




# GREYSCALE = True
# img_list = [ './OriginalImg/Ddo_Ava.png',
#             './OriginalImg/Di-choi-cover-image.png',
#             './OriginalImg/Girl_with_a_Pearl_Earring.jpeg',
#             './OriginalImg/Starry_Night_Vincent_van_Gogh.webp',
#             './OriginalImg/The_Kiss_Gustav_Klimt.jpeg',
#             './OriginalImg/The_Lovers_II_Rene_Magritte.jpeg',
#             './OriginalImg/Frankenstein_Tom_Carlton.jpeg',
#             '../OriginalImg/frank300x300.jpg',
#             './OriginalImg/Marilyn_Monroe_Laughing.webp',
#             './OriginalImg/Albert_Einstein.webp']

# img_name = img_list[-3]

# img = Image.open(img_name)


# img.show()


# Change the image into greyscale if wanted
# if GREYSCALE:
#     img = img.convert(mode="L")

# w, h = img.size
# # print(w,h)
# for i in [32]:
#     # Resize the original image or, in other word, reduce number of pixels
#     new_w = i
#     new_h = int(h * new_w / w)
#     img = img.resize(size = (new_w, new_h))
#     # img.show()
#     og_arr = np.array(img, dtype=float)
#     color_channels = 4
    
#     print(MSE_1by1(arr, og_arr))