/*
   Code for rendering a target image as a mosaic of zig-zag tiles.
   Written by R. Bosch in 2023 after conversations with Dung (Brian) Do.

   The target image is described in the file

     image.pgm

   and the final artwork is stored in the file

     zzm.eps
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define ROWS_P 75                  /* # of rows of pixels in the target image */
#define COLS_P 75                  /* # of columns of pixels in the target image */
#define K 1                        /* The pixels are grouped in KxK blocks */

/* Note: ROWS_P and COLS_P should be divisible by K */

#define ROWS_M ROWS_P/K            /* # of rows of squares in the mosaic */
#define COLS_M COLS_P/K            /* # of columns of squares in the mosaic */
#define BW 10                      /* border width (measured in squares) */

#define LW 2.50                    /* linewidth of the lines in the mosaic */
#define SW 10.00                   /* width of the square tiles in the mosaic */
#define TMAX 0.50                  /* largest value of t */

#define RBACK 1.0                  /* RGB values for the background */
#define GBACK 1.0
#define BBACK 1.0
#define RLINE 0.0                  /* RGB values for the lines */
#define GLINE 0.0
#define BLINE 0.0

#define ONE_LINE 1                 /* 1 = yes, 0 = no */

int brightness[ROWS_P][COLS_P];    /* brightness of pixel (i,j) on a */
                                   /*  0-to-255 black-to-white scale */
double b[ROWS_M][COLS_M];          /* avg. brightness of square (i,j) on */
                                   /*  a 0.0-to-1.0 black-to-white scale */
double x, y; 
double l, lmax, t;

int main ()
{
int i, j, ip, jp, trash_int; 
     
FILE *image, *eps;
     
char trash_string[25];
     
/* 
   Read the PGM file that describes the target image.
 */

if ((image=fopen("image.pgm", "r")) == NULL) 
  {
    printf("Couldn't open image.pgm!\n");
    exit(0);
  }

fscanf(image, "%s", trash_string);

fscanf(image, "%d", &trash_int);
fscanf(image, "%d", &trash_int);
fscanf(image, "%d", &trash_int);

for (i = 0; i < ROWS_P; i++)
  for (j = 0; j < COLS_P; j++)
    fscanf(image, "%d", &brightness[i][j]);

fclose(image);

/* 
   Use the pixel brightness values (on a 0-to-255 black-to-white scale) 
   to compute block brightness values (on a 0.0-to-1.0 black-to-white scale). 
 */

for (i = 0; i < ROWS_M; i++)
  for (j = 0; j < COLS_M; j++)
    {
      b[i][j] = 0.0;
      for (ip = 0; ip < K; ip++)
        for (jp = 0; jp < K; jp++)
          b[i][j] = b[i][j] + brightness[i*K+ip][j*K+jp];
      b[i][j] = b[i][j]/(K*K);
      b[i][j] = b[i][j]/255.0;
      if (b[i][j] < 0.0)
        b[i][j] = 0.0;
      if (b[i][j] > 1.0)
        b[i][j] = 1.0;
    }

/*
   Open the PostScript file.  Assign values to setlinecap, setlinejoin, and 
   setlinewidth. Compute lmax.
 */

if ((eps=fopen("zzm.eps", "w")) == NULL)
  {
    printf("Couldn't open zzm.eps!\n");
    exit(0);
  }

fprintf(eps, "%%!PS-Adobe-3.0 EPSF-3.0\n");
fprintf(eps, "%%%%BoundingBox: 0 0 %d %d\n\n", 
  (int) ((COLS_M+2*BW)*SW), (int) ((ROWS_M+2*BW)*SW));

fprintf(eps, "1 setlinecap\n");
fprintf(eps, "1 setlinejoin\n");
fprintf(eps, "%.2f setlinewidth\n", LW);

lmax = sqrt(1.0 + 16.0*TMAX*TMAX);

/* Draw background */

fprintf(eps, "%.3f %.3f %.3f setrgbcolor\n\n", RBACK, GBACK, BBACK);
  
fprintf(eps, "newpath\n");
fprintf(eps, "%.6f %.6f moveto\n", 0.0, 0.0);
fprintf(eps, "%.6f %.6f lineto\n", 0.0, SW*(ROWS_M+2*BW));
fprintf(eps, "%.6f %.6f lineto\n", SW*(COLS_M+2*BW), SW*(ROWS_M+2*BW));
fprintf(eps, "%.6f %.6f lineto\n", SW*(COLS_M+2*BW), 0.0);
fprintf(eps, "closepath\n");
fprintf(eps, "fill\n\n");

/*  
   Draw the tiles. Tile (i,j) is centered at 

       (x,y) = (SW*BW + SW*0.5 + SW*j, SW*BW + SW*0.5 + SW*(ROWS_M-1-i)).  
 */

fprintf(eps, "%.3f %.3f %.3f setrgbcolor\n\n", RLINE, GLINE, BLINE);

if (ONE_LINE == 0)
  for (i = 0; i < ROWS_M; i++)
    for (j = 0; j < COLS_M; j++)
      {
        x = SW*BW + SW*0.5 + SW*j;
        y = SW*BW + SW*0.5 + SW*(ROWS_M-1-i);
        l = lmax + (1.0-lmax)*b[i][j];
        t = 0.25*sqrt(l*l - 1.0);

        if (j == 0)
          {
            fprintf(eps, "newpath\n");
            fprintf(eps, "%.3f %.3f moveto\n", x - SW*0.5, y);
          }
        fprintf(eps, "%.3f %.3f lineto\n", x - SW*0.25, y + t*SW);
        fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.25, y - t*SW);
        fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.5, y);
        if (j == COLS_M-1)
          fprintf(eps, "stroke\n\n");
      }
else /* ONE_LINE == 1 */
  {
    x = SW*BW + SW*0.5 + SW*0 - SW;       /* The path starts in the top left */
    y = SW*BW + SW*0.5 + SW*(ROWS_M-1);   /* (one square left of square (0,0) */
    fprintf(eps, "newpath\n");
    fprintf(eps, "%.3f %.3f moveto\n", x - SW*0.5, y);

    for (i = 0; i < ROWS_M; i++)
      {
        if (i%2 == 0)  /* Even numbered rows are drawn from left to right */
          {
            if (i != 0)
              {
                x = SW*BW + SW*0.5 + SW*0 - SW;
                y = SW*BW + SW*0.5 + SW*(ROWS_M-1-i);
                fprintf(eps, "%.3f %.3f lineto\n", x - SW*0.5, y);
              }
            for (j = 0; j < COLS_M; j++)
              {
                x = SW*BW + SW*0.5 + SW*j;
                y = SW*BW + SW*0.5 + SW*(ROWS_M-1-i);
                l = lmax + (1.0-lmax)*b[i][j];
                t = 0.25*sqrt(l*l - 1.0);
                fprintf(eps, "%.3f %.3f lineto\n", x - SW*0.5, y);
                fprintf(eps, "%.3f %.3f lineto\n", x - SW*0.25, y + t*SW);
                fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.25, y - t*SW);
                fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.5, y);
              }
            x = SW*BW + SW*0.5 + SW*(COLS_M-1) + SW; 
            y = SW*BW + SW*0.5 + SW*(ROWS_M-1-i);
            fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.5, y);
          }
        else           /* Odd numbered rows are drawn from right to left */
          {
            x = SW*BW + SW*0.5 + SW*(COLS_M-1) + SW;
            y = SW*BW + SW*0.5 + SW*(ROWS_M-1-i);
            fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.5, y);

            for (j = COLS_M-1; j >= 0; j--)
              {
                x = SW*BW + SW*0.5 + SW*j;
                y = SW*BW + SW*0.5 + SW*(ROWS_M-1-i);
                l = lmax + (1.0-lmax)*b[i][j];
                t = 0.25*sqrt(l*l - 1.0);
                fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.5, y);
                fprintf(eps, "%.3f %.3f lineto\n", x + SW*0.25, y - t*SW);
                fprintf(eps, "%.3f %.3f lineto\n", x - SW*0.25, y + t*SW);
                fprintf(eps, "%.3f %.3f lineto\n", x - SW*0.5, y);
              }

            x = SW*BW + SW*0.5 + SW*0 - SW;
            y = SW*BW + SW*0.5 + SW*(ROWS_M-1-i);
            fprintf(eps, "%.3f %.3f lineto\n", x - SW*0.5, y);
          }
      }
    fprintf(eps, "stroke\n\n");
  }

fprintf(eps, "showpage\n");                                                
fprintf(eps, "%%EOF\n");

fclose(eps);

}

