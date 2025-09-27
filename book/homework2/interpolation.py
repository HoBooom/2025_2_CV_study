import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma2.jpeg')
patch=img[50:150,220:320]

# cv.imshow('ori_img',img)
# cv.imshow('patch',patch)
#cv.rectangle(img,(x1,y1),(x2,y2),(color),thickness)
img=cv.rectangle(img,(220,50),(320,150),(0,0,255),2)
cv.imshow('ori_img',img)

#INTER_NEAREST : 가장 가까운 픽셀 값을 사용
#INTER_LINEAR : 선형 보간법을 사용
#INTER_CUBIC : 큐빅 보간법을 사용
patch1=cv.resize(patch,dsize=(0,0),fx=8,fy=8,interpolation=cv.INTER_NEAREST)
patch2=cv.resize(patch,dsize=(0,0),fx=8,fy=8,interpolation=cv.INTER_LINEAR)
patch3=cv.resize(patch,dsize=(0,0),fx=8,fy=8,interpolation=cv.INTER_CUBIC)

patchs=np.hstack((patch1,patch2,patch3))
cv.imshow('INTER_NEAREST,INTER_LINEAR,INTER_CUBIC',patchs)
cv.imwrite('./book/homework2/interpolation_original.png',img)
cv.imwrite('./book/homework2/interpolation_INTER_NEAREST,INTER_LINEAR,INTER_CUBIC.png',patchs)

cv.waitKey(0)
cv.destroyAllWindows()