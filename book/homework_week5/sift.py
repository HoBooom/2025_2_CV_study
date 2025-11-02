import cv2 as cv
import numpy as np

img1=cv.imread('./book/homework_week5/image/bed1.jpeg')
img2=cv.imread('./book/homework_week5/image/bed2.jpeg')
gray1=cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
gray2=cv.cvtColor(img2,cv.COLOR_BGR2GRAY)

#sift_create : SIFT 객체 생성
sift=cv.SIFT_create()
#kp : 키 포인트(특징점)
#des : 기술자(특징벡터)
kp1,des1=sift.detectAndCompute(gray1,None)
kp2,des2=sift.detectAndCompute(gray2,None)


gray1=cv.drawKeypoints(gray1,kp1,None,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
gray2=cv.drawKeypoints(gray2,kp2,None,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

result=np.hstack((gray1,gray2))
cv.imshow('sift',result)
cv.imwrite('./book/homework_week5/sift_result.png',result)



k=cv.waitKey(0)
cv.destroyAllWindows()

