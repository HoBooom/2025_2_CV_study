import cv2 as cv
import sys

img=cv.imread('./image/grandma3.jpeg')

if img is None:
    sys.exit('can not find file')

cv.imshow('ori_rgb',img)

cv.imshow('r_channel',img[:,:,2])
cv.imshow('g_channel',img[:,:,1])
cv.imshow('b_channel',img[:,:,0])

cv.waitKey(0)
cv.destroyAllWindows()