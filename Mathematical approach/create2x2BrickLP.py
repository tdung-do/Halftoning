import numpy as np
from PIL import Image

#Set GREYSCALE to True if expect the output to be greyscale image
GREYSCALE = True
img_list = [ './OriginalImg/Ddo_Ava.png',
            './OriginalImg/Di-choi-cover-image.png',
            './OriginalImg/Girl_with_a_Pearl_Earring.jpeg',
            './OriginalImg/Starry_Night_Vincent_van_Gogh.webp',
            './OriginalImg/The_Kiss_Gustav_Klimt.jpeg',
            './OriginalImg/The_Lovers_II_Rene_Magritte.jpeg',
            './OriginalImg/Frankenstein_Tom_Carlton.jpeg',
            './OriginalImg/frank300x300.jpg',
            './OriginalImg/Marilyn_Monroe_Laughing.webp',
            './OriginalImg/Albert_Einstein.webp']

img_name = img_list[-3]
name = img_name.split('/')[-1].split('.')[0]

img = Image.open(img_name)


# img.show()


# Change the image into greyscale if wanted
if GREYSCALE:
    img = img.convert(mode="L")
    

#RESIZE ORIGINAL IMAGE
new_w = 64
w, h = img.size
new_h = int(h * new_w / w)
img = img.resize(size = (new_w, new_h))

arr = np.array(img, dtype= float) / 255 * 3

nc = 4              #Number of color channel

bound1 = nc - 1
bound2 = 4*nc - 4

    

#Write into a .lp file
fname = './Mathematical approach/LP_files/' + name + '_' + str(new_w) + '_2x2_brick.lp'
f = open(fname, 'w')



#OBJECTIVE FUNCTION
f.write('minimize\n')

tmp = ' + 0 Height\n + 0 Width\n'
f.write(tmp)

for i in range(new_h):
    for j in range(1, new_w + 1):
        tmp = ' + 0 Y' + str(i) + ',' + str(j) + '\n'           # ' + 0 Yi,j '
        f.write(tmp)

for i in range(new_h - 1):  # i from 0 to (m - 2)
    for j in range(1, new_w):   # j from 1 to (n - 1)
        beta = arr[i, j - 1] + arr[i, j] + arr[i+1, j-1] + arr[i+1, j]
        for h in range(bound2 + 1):
            coeff = round((h - beta) * (h - beta), 3)
            tmp = ' + ' + str(coeff) + ' Z' + str(i) + ',' + str(j) + ',' + str(h) + '\n'    # ' + coeff Zi,j,h ' 
            f.write(tmp)
        # if (i + j) % 2 == 1:
        #     for k in range(nc):
        #         coeff = (k - arr[i, j-1]) * (k - arr[i, j-1])
        #         tmp = ' + ' + str(coeff) + ' X' + str(i) + ',' + str(j) + ',' + str(k) + '\n'    # ' + coeff Xi,j,k ' 
        #         f.write(tmp)
        # else:
        #     for k in range(nc):
        #         coeff = (k - arr[i, j-1]) * (k - arr[i, j-1])
        #         tmp = ' + ' + str(coeff) + ' X' + str(i) + ',' + str(j-1) + ',' + str(k) + '\n'  # ' + coeff Xi,j-1,k ' 
        #         f.write(tmp)



#CONSTRAINTS
f.write('subject to\n')

tmp = ' Height = ' + str(new_h) + '\n' + ' Width = ' + str(new_w) + '\n'
f.write(tmp)

for i in range(new_h):
    for j in range(1, new_w + 1):
        if (i + j) % 2 == 1:
            #cons1 = ' sum k=0->(nc-1) of Xi,j,k = 1'
            #cons2 = ' sum k=0->(nc-1) of k * Xi,j,k - Yi,j = 0'
            #cons3 = ' Yi,j+1 - Yi,j = 0 '
            cons1 = ' '
            cons2 = ' '
            cons3 = ' Y' + str(i) + ',' + str(j+1) + ' - Y' + str(i) + ',' + str(j) + ' = 0\n'
            for k in range(bound1 + 1):
                if k != bound1:
                    cons1 += 'X' + str(i) + ',' + str(j) + ',' + str(k) + ' + '
                    cons2 += str(k) + ' X' + str(i) + ',' + str(j) + ',' + str(k) + ' + '
                else:
                    cons1 += 'X' + str(i) + ',' + str(j) + ',' + str(k)
                    cons2 += str(k) + ' X' + str(i) + ',' + str(j) + ',' + str(k)
            cons1 += ' = 1\n'
            cons2 += ' - Y' + str(i) + ',' + str(j) + ' = 0\n'
            
            f.write(cons1)
            f.write(cons2)
            f.write(cons3)
            
        if j == 1 and i % 2 == 1:
            # Special pixels on the left edge
            cons4 = ' Y' + str(i) + ',' + str(j) + ' = ' + str(round(arr[i, j-1])) + '\n'
            f.write(cons4)
        
        if (0 <= i <= (new_h - 2)) and (1 <= j <= (new_w - 1)):
            # cons5 = ' sum h=0->(4nc-4) of Zi,j,h = 1'
            # cons6 = ' sum h=0->(4nc-4) of h * Zi,j,h - Yi,j - Yi,j+1 - Yi+1,j - Yi+1,j+1 = 0'
            cons5 = ' '
            cons6 = ' '
            for h in range(bound2 + 1):
                if h != bound2:
                    cons5 += 'Z' + str(i) + ',' + str(j) + ',' + str(h) + ' + '
                    cons6 += str(h) + ' Z' + str(i) + ',' + str(j) + ',' + str(h) + ' + '
                else:
                    cons5 += 'Z' + str(i) + ',' + str(j) + ',' + str(h)
                    cons6 += str(h) + ' Z' + str(i) + ',' + str(j) + ',' + str(h)
            
            cons5 += ' = 1\n'
            cons6 += ' - Y' + str(i) + ',' + str(j) + ' - Y' + str(i) + ',' + str(j+1) + ' - Y' + str(i+1) + ',' + str(j) + ' - Y' + str(i+1) + ',' + str(j+1) + ' = 0\n'
            
            f.write(cons5)
            f.write(cons6)
            

#BOUNDS of each variable
f.write('bounds\n')

for i in range(new_h):
    for j in range(1, new_w + 1):
        tmp = ' 0 <= Y' + str(i) + ',' + str(j) + ' <= ' + str(bound1) + '\n'       # ' 0 <= Yi,j <= (nc-1) '
        f.write(tmp)
        if (i + j) % 2 == 1:
            for k in range(nc):
                tmp = ' 0 <= X' + str(i) + ',' + str(j) + ',' + str(k) + ' <= 1\n'  # ' 0 <= Xi,j,k <= 1 '
                f.write(tmp)
    
        if (0 <= i <= (new_h - 2)) and (1 <= j <= (new_w - 1)):
            for h in range(bound2 + 1):
                tmp = ' 0 <= Z' + str(i) + ',' + str(j) + ',' + str(h) + ' <= 1\n'    # ' 0 <= Zi,j,h <= 1 '
                f.write(tmp)
        
        



#INTEGERS
f.write('integers\n')

for i in range(new_h):
    for j in range(1, new_w + 1):
        tmp = ' Y' + str(i) + ',' + str(j) + '\n'                           # ' Yi,j '
        f.write(tmp)
        if (i + j) % 2 == 1:
            for k in range(bound1 + 1):
                tmp = ' X' + str(i) + ',' + str(j) + ',' + str(k) + '\n'    # ' Xi,j,k '
                f.write(tmp)
        
        if (0 <= i <= (new_h - 2)) and (1 <= j <= (new_w - 1)):
            for h in range(bound2 + 1):
                tmp = ' Z' + str(i) + ',' + str(j) + ',' + str(h) + '\n'    # ' Zi,j,h '
                f.write(tmp)

#END
f.write('end')
f.close()


