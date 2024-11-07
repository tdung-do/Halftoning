import numpy as np
from PIL import Image
from Dithering import *

# Define linewidth, tile width, and max t value
LW = 2.50                      # Linewidth of the lines in the mosaic
SW = 10.00                     # Width of the square tiles in the mosaic
TMAX = 0.50                    # Largest value of t

# RGB values for the background
RBACK = 1.0
GBACK = 1.0
BBACK = 1.0

# RGB values for the lines
RLINE = 0.0
GLINE = 0.0
BLINE = 0.0

# Set ONE_LINE to True or False 
ONE_LINE = False

# Set GREYSCALE to True if expect the output to be greyscale image
GREYSCALE = True

# Number of color channel for each R B G if GREYSCALE is False
# Otherwise the number of shades of grey (including black and white)
COL_CHANNEL = 2

# List of original images
img_list = [ './OriginalImg/Ddo_Ava.png',
            './OriginalImg/Di-choi-cover-image.png',
            './OriginalImg/Girl_with_a_Pearl_Earring.jpg',
            './OriginalImg/Starry_Night_Vincent_van_Gogh.webp',
            './OriginalImg/The_Kiss_Gustav_Klimt.jpeg',
            './OriginalImg/The_Lovers_II_Rene_Magritte.jpeg',
            './OriginalImg/Frankenstein_Tom_Carlton.jpeg',
            './OriginalImg/frankenstein300x300.jpg',
            './OriginalImg/Marilyn_Monroe_Laughing.webp',
            './OriginalImg/Albert_Einstein.webp',
            './OriginalImg/IMG_0058.jpg',
            './OriginalImg/IMG_5388.jpg',
            './OriginalImg/IMG_5389.jpg',
            './OriginalImg/IMG_5390.jpg',
            './OriginalImg/IMG_5391.jpg']

img_name = img_list[3]

img = Image.open(img_name)

img_name = img_name.split('/')[-1]


# img.show()


# Change the image into greyscale if wanted
if GREYSCALE:
    img = img.convert(mode="L")
    
# print(len(palette_reduce(img, 2)[0]))

# Number of rows and columns of pixels in the target image
ROWS_P = img.size[1]                       # Number of rows of pixels in the target image
COLS_P = img.size[0]                       # Number of columns of pixels in the target image
K = 1                             # Pixels are grouped in KxK blocks

# Note: ROWS_P and COLS_P should be divisible by K

# Calculate rows and columns of squares in the mosaic
# ROWS_M = ROWS_P // K              # Number of rows of squares in the mosaic
# COLS_M = COLS_P // K              # Number of columns of squares in the mosaic
ROWS_M = 80
COLS_M = (COLS_P * ROWS_M) // ROWS_P
BW = 10                           # Border width (measured in squares)

# print(img.size[0], img.size[1])

# Resize the original image or, in other word, reduce number of pixels
img = img.resize(size = (COLS_M, ROWS_M))
# w, h = img.size
# new_w = 75
# # new_w = w
# new_h = (h * new_w) // w
# img = img.resize(size = (new_w, new_h))


# print(w, h)
# print(new_w, new_h)

# print(len(palette_reduce(img, 2)[0]))

# Brightness of pixel (i,j) on a 0-to-255 scale
# brightness = palette_reduce(img, COL_CHANNEL)
brightness = np.array(img, dtype= float) 

# avg. brightness of square (i,j) on a 0.0-to-1.0 scale */
b = brightness / 255

# print(len(brightness[0]))
# print(b[0])

# Name of PostScript file
f_name = './zzTestImg/' + img_name.split('.')[0] + '_height=' + str(ROWS_M) + '.eps'

# List of lines will be written in PostScript file
ll = []

# Assign values to setlinecap, setlinejoin, and  setlinewidth. Compute lmax.
ll.append("%!PS-Adobe-3.0 EPSF-3.0")
ll.append(f"%%BoundingBox: 0 0 {((COLS_M+2*BW)*SW):.0f} {((ROWS_M+2*BW)*SW):.0f}\n")

ll.append("1 setlinecap")
ll.append("1 setlinejoin")
ll.append(f"{LW:.2f} setlinewidth")

lmax = np.sqrt(1.0 + 16.0*TMAX*TMAX)

# Draw background
ll.append(f"{RBACK:.3f} {GBACK:.3f} {BBACK:.3f} setrgbcolor\n")

ll.append("newpath")
ll.append(f"{0.0:.6f} {0.0:.6f} moveto")
ll.append(f"{0.0:.6f} {SW * (ROWS_M + 2 * BW):.6f} lineto")
ll.append(f"{SW * (COLS_M + 2 * BW):.6f} {SW * (ROWS_M + 2 * BW):.6f} lineto")
ll.append(f"{SW * (COLS_M + 2 * BW):.6f} {0.0:.6f} lineto")
ll.append("closepath")
ll.append("fill\n")

# Draw the tiles
# Note: Tile (i,j) is centered at (x,y) = (SW*BW + SW*0.5 + SW*j, SW*BW + SW*0.5 + SW*(ROWS_M-1-i))
ll.append(f"{RLINE:.3f} {GLINE:.3f} {BLINE:.3f} setrgbcolor\n")



# Draw the lines based on ONE_LINE setting
if ONE_LINE == False:
    for i in range(ROWS_M):
        for j in range(COLS_M):
            x = SW * BW + SW * 0.5 + SW * j
            y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1 - i)
            l = lmax + (1.0 - lmax) * b[i, j]
            t = 0.25 * (l * l - 1.0) ** 0.5

            if j == 0:
                ll.append("newpath")
                ll.append(f"{x - SW * 0.5:.3f} {y:.3f} moveto")
            
            ll.append(f"{x - SW * 0.25:.3f} {y + t * SW:.3f} lineto")
            ll.append(f"{x + SW * 0.25:.3f} {y - t * SW:.3f} lineto")
            ll.append(f"{x + SW * 0.5:.3f} {y:.3f} lineto")
            
            if j == COLS_M - 1:
                ll.append("stroke\n")

else:  # ONE_LINE == True
    x = SW * BW + SW * 0.5 + SW * 0 - SW  # Start in top left
    y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1)  # One square left of (0, 0)
    ll.append("newpath")
    ll.append(f"{x - SW * 0.5:.3f} {y:.3f} moveto")

    for i in range(ROWS_M):
        if i % 2 == 0:  # Even rows, left to right
            if i != 0:
                x = SW * BW + SW * 0.5 + SW * 0 - SW
                y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1 - i)
                ll.append(f"{x - SW * 0.5:.3f} {y:.3f} lineto")
            
            for j in range(COLS_M):
                x = SW * BW + SW * 0.5 + SW * j
                y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1 - i)
                l = lmax + (1.0 - lmax) * b[i, j]
                t = 0.25 * (l * l - 1.0) ** 0.5
                
                ll.append(f"{x - SW * 0.5:.3f} {y:.3f} lineto")
                ll.append(f"{x - SW * 0.25:.3f} {y + t * SW:.3f} lineto")
                ll.append(f"{x + SW * 0.25:.3f} {y - t * SW:.3f} lineto")
                ll.append(f"{x + SW * 0.5:.3f} {y:.3f} lineto")
            
            x = SW * BW + SW * 0.5 + SW * (COLS_M - 1) + SW
            y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1 - i)
            ll.append(f"{x + SW * 0.5:.3f} {y:.3f} lineto")
        
        else:  # Odd rows, right to left
            x = SW * BW + SW * 0.5 + SW * (COLS_M - 1) + SW
            y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1 - i)
            ll.append(f"{x + SW * 0.5:.3f} {y:.3f} lineto")
            
            for j in range(COLS_M - 1, -1, -1):
                x = SW * BW + SW * 0.5 + SW * j
                y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1 - i)
                l = lmax + (1.0 - lmax) * b[i, j]
                t = 0.25 * (l * l - 1.0) ** 0.5
                
                ll.append(f"{x + SW * 0.5:.3f} {y:.3f} lineto")
                ll.append(f"{x + SW * 0.25:.3f} {y - t * SW:.3f} lineto")
                ll.append(f"{x - SW * 0.25:.3f} {y + t * SW:.3f} lineto")
                ll.append(f"{x - SW * 0.5:.3f} {y:.3f} lineto")
            
            x = SW * BW + SW * 0.5 + SW * 0 - SW
            y = SW * BW + SW * 0.5 + SW * (ROWS_M - 1 - i)
            ll.append(f"{x - SW * 0.5:.3f} {y:.3f} lineto")

    ll.append("stroke\n")

# Finalize the page
ll.append("showpage")
ll.append("%%EOF")








f = open(f_name, "w")
f.write('\n'.join(ll))
f.close()