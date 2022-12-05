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
new_w = 1000
w, h = img.size
new_h = int(h * new_w / w)
img = img.resize(size = (new_w, new_h))

arr = np.array(img, dtype= float) / 255 * 3

nc = 4              #Number of color channel


    

#Write into a .lp file
fname = './Mathematical approach/LP_files/' + name + '_' + str(new_w) + '_1x1_brick.lp'
f = open(fname, 'w')



#OBJECTIVE FUNCTION
f.write('minimize\n')

tmp = ' + 0 Height\n + 0 Width\n'
f.write(tmp)

for i in range(new_h):
    for j in range(1, new_w + 1):
        tmp = ' + 0 Y' + str(i) + ',' + str(j) + '\n'           # ' + 0 Yi,j '
        f.write(tmp)

for i in range(new_h):
    for j in range(1, new_w + 1):
        if (i + j) % 2 == 1:
            for k in range(nc):
                coeff = (k - arr[i, j-1]) * (k - arr[i, j-1])
                tmp = ' + ' + str(coeff) + ' X' + str(i) + ',' + str(j) + ',' + str(k) + '\n'    # ' + coeff Xi,j,k ' 
                f.write(tmp)
        else:
            for k in range(nc):
                coeff = (k - arr[i, j-1]) * (k - arr[i, j-1])
                tmp = ' + ' + str(coeff) + ' X' + str(i) + ',' + str(j-1) + ',' + str(k) + '\n'  # ' + coeff Xi,j-1,k ' 
                f.write(tmp)



#CONSTRAINTS
f.write('subject to\n')

tmp = ' Height = ' + str(new_h) + '\n' + ' Width = ' + str(new_w) + '\n'
f.write(tmp)

for i in range(new_h):
    for j in range(1, new_w + 1):
        if (i + j) % 2 == 1:
            #cons1 = ' sum k=0->3 of Xi,j,k = 1'
            #cons2 = ' sum k=0->3 of k * Xi,j,k - Yi,j = 0'
            #cons3 = ' Yi,j+1 - Yi,j = 0 '
            cons1 = ' '
            cons2 = ' '
            cons3 = ' Y' + str(i) + ',' + str(j+1) + ' - Y' + str(i) + ',' + str(j) + ' = 0\n'
            for k in range(nc):
                if k != 3:
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
        elif j == 1 and i % 2 == 1:
            cons = ' Y' + str(i) + ',' + str(j) + ' = ' + str(round(arr[i, j-1])) + '\n'
            f.write(cons)
            
            

#BOUNDS of each variable
f.write('bounds\n')

for i in range(new_h):
    for j in range(1, new_w + 1):
        tmp = ' 0 <= Y' + str(i) + ',' + str(j) + ' <= 3\n'                         # ' 0 <= Yi,j <= 3 '
        f.write(tmp)
        if (i + j) % 2 == 1:
            for k in range(nc):
                tmp = ' 0 <= X' + str(i) + ',' + str(j) + ',' + str(k) + ' <= 1\n'  # ' 0 <= Xi,j,k <= 1 '
                f.write(tmp)



#INTEGERS
f.write('integers\n')

for i in range(new_h):
    for j in range(1, new_w + 1):
        tmp = ' Y' + str(i) + ',' + str(j) + '\n'                           # ' Yi,j '
        f.write(tmp)
        if (i + j) % 2 == 1:
            for k in range(nc):
                tmp = ' X' + str(i) + ',' + str(j) + ',' + str(k) + '\n'    # ' Xi,j,k '
                f.write(tmp)

#END
f.write('end')
f.close()


