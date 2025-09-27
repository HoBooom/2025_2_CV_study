import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#cv.IMREAD_UNCHANGED : 원본 이미지 그대로 읽기
img=cv.imread('./image/grandma5.jpeg', cv.IMREAD_UNCHANGED)

t,bin_img=cv.threshold(img[:,:,2],0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
#xticks : x축 눈금 제거
#yticks : y축 눈금 제거
plt.imshow(bin_img,cmap='gray'),plt.xticks([]),plt.yticks([])
plt.show()

b=bin_img[bin_img.shape[0]//2:bin_img.shape[0],0:bin_img.shape[0]//2+1]
plt.imshow(b,cmap='gray'),plt.xticks([]),plt.yticks([])
plt.show()

se=np.uint8([[0,0,1,0,0],
             [0,1,1,1,0],
             [1,1,1,1,1],
             [0,1,1,1,0],
             [0,0,1,0,0]])

#팽창
b_dilation = cv.dilate(b,se,iterations=1)
plt.imshow(b_dilation,cmap='gray'),plt.xticks([]),plt.yticks([])
plt.show()

#침식
b_erosion = cv.erode(b,se,iterations=1)
plt.imshow(b_erosion,cmap='gray'),plt.xticks([]),plt.yticks([])
plt.show()

#닫기(팽창 후 침식)
b_opening = cv.erode(cv.dilate(b,se,iterations=1),se,iterations=1)
plt.imshow(b_opening,cmap='gray'),plt.xticks([]),plt.yticks([])
plt.show()
