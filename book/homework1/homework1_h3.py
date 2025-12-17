import cv2 as cv
import numpy as np
import sys
import matplotlib.pyplot as plt

img = cv.imread('./image/grandma3.jpeg')

if img is None:
    sys.exit('can not find file')

r_channel = img[:,:,2]
g_channel = img[:,:,1]
b_channel = img[:,:,0]

#R -> 반전
r_reversed = 255 - r_channel
#cv.imshow('reversed_r_channel',r_reversed)

#G -> Gamma Correction
#gamma=1.0 -> 선형 
#gamma<1.0 -> 밝음
#gamma>1.0 -> 어두움
def gamma(f,gamma=1.0):
     f1=f/255.0 #0~1사이로 정규화
     return np.uint8(255*(f1**gamma))

#hstack : 옆으로 붙여서 한번에 보여주기
gc=np.hstack((gamma(g_channel,0.5),gamma(g_channel,1.0),gamma(g_channel,1.5)))
g_gamma = gamma(g_channel,1.5)
#cv.imshow('gamma_correction',gc)

#B -> 히스토그램평활화(histogram equalization)
b_equalized=cv.equalizeHist(b_channel)
#cv.imshow('b_equalized',b_equalized)

#다시 합치기
final_img=cv.merge((b_equalized,g_gamma,r_reversed))

#출력
check_img=np.hstack((r_reversed,g_gamma,b_equalized))
cv.imshow('r_reversed,g_gamma,b_equalized__img',check_img)
cv.imshow('final_img',final_img)




cv.waitKey(0)
cv.destroyAllWindows()