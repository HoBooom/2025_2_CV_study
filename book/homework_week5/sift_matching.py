import cv2 as cv
import numpy as np
import time

img1=cv.imread('./book/homework_week5/image/cushion1.jpeg')
img2=cv.imread('./book/homework_week5/image/cushion2.jpeg')
gray1=cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
gray2=cv.cvtColor(img2,cv.COLOR_BGR2GRAY)

sift=cv.SIFT_create()
kp1,des1=sift.detectAndCompute(gray1,None)
kp2,des2=sift.detectAndCompute(gray2,None)

start=time.time()
flann_matcher=cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
knn_match=flann_matcher.knnMatch(des1,des2,k=2)

T=0.7
good_matches=[]
for nearest1,nearest2 in knn_match:
    if (nearest1.distance/nearest2.distance) < T:
        good_matches.append(nearest1)

print(f"매칭에 걸린 시간 : {time.time()-start} seconds")

img_match=np.empty((max(img1.shape[0],img2.shape[0]),img1.shape[1]+img2.shape[1],3),dtype=np.uint8)
cv.drawMatches(img1,kp1,img2,kp2,good_matches,img_match,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imshow("good_matches",img_match)

#Homography 행렬 계산
points1=np.float32([kp1[m.queryIdx].pt for m in good_matches])
points2=np.float32([kp2[m.trainIdx].pt for m in good_matches])
H,_=cv.findHomography(points1,points2,cv.RANSAC)

h1,w1=img1.shape[0],img1.shape[1]
h2,w2=img2.shape[0],img2.shape[1]
img_match2=np.empty((max(h1,h2),w1+w2,3),dtype=np.uint8)
cv.drawMatches(img1,kp1,img2,kp2,good_matches,img_match2,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv.imshow("after Homography",img_match2)


cv.imwrite('./book/homework_week5/sift_matching.png',img_match)
cv.imwrite('./book/homework_week5/sift_matching_after_Homography.png',img_match2)
k=cv.waitKey(0)
cv.destroyAllWindows()

