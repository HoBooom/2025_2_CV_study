#TODO : 각 알고리즘의 파라미터 비교해보기

import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma3.jpeg')


#TODO : mean
#cv.blur(src,ksize)
#src : 이미지
#ksize : 커널 크기 -> 커질 수록 더 강하게 블러처리됨
mean=np.hstack((cv.blur(src=img,ksize=(3,3)),cv.blur(src=img,ksize=(5,5)),cv.blur(src=img,ksize=(7,7))))
cv.imshow('ori_img,mean_ksize_3,5,7',np.hstack((img, mean)))
cv.imwrite('mean_ksize_3,5,7.png',mean)

#TODO : gaussian
#cv.GaussianBlur(src,ksize,sigmaX)
#src : 이미지
#ksize : 커널 크기
#sigmaX : 표준 편차 -> 0으로 설정시 자동으로 계산, 커질 수록 더 넓고 부드럽게 블러처리됨
gaussian_ksize=np.hstack((img,cv.GaussianBlur(src=img,ksize=(3,3),sigmaX=0),cv.GaussianBlur(src=img,ksize=(5,5),sigmaX=0),cv.GaussianBlur(src=img,ksize=(7,7),sigmaX=0)))
gaussian_sigmaX=np.hstack((img,cv.GaussianBlur(src=img,ksize=(3,3),sigmaX=5),cv.GaussianBlur(src=img,ksize=(3,3),sigmaX=50),cv.GaussianBlur(src=img,ksize=(3,3),sigmaX=100)))
gaussian_result=np.vstack((gaussian_ksize,gaussian_sigmaX))
cv.imshow('row1 : gaussian_ksize_3,5,7, row2 : gaussian_sigmaX_5,50,100(k_size=3)',gaussian_result)
cv.imwrite('row1_gaussian_ksize_3,5,7_row2_gaussian_sigmaX_5,50,100(k_size=3).png',gaussian_result)

#TODO : sobel
#cv.Sobel(src,ddepth,dx,dy,ksize)
#src : 이미지
#ddepth : 이미지 타입 -> sobel 필터(미분) 연산 시 값이 음수가 나올 수 있기에 보통 float로 설정
#dx : x방향 미분
#dy : y방향 미분
#ksize : 커널 크기 -> 커질 수록 엣지 검출 범위가 더 넓어지고 노이즈에 덜 민감해짐
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('gray',gray)

grad_x_3=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=1,dy=0,ksize=3)
grad_y_3=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=0,dy=1,ksize=3)
grad_x_5=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=1,dy=0,ksize=5)
grad_y_5=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=0,dy=1,ksize=5)
grad_x_7=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=1,dy=0,ksize=7)
grad_y_7=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=0,dy=1,ksize=7)

#convertScaleAbs : 이미지 타입을 시각화 할 수 있도록 uint8로 변환
sobel_x_3=cv.convertScaleAbs(grad_x_3)
sobel_y_3=cv.convertScaleAbs(grad_y_3)
sobel_x_5=cv.convertScaleAbs(grad_x_5)
sobel_y_5=cv.convertScaleAbs(grad_y_5)
sobel_x_7=cv.convertScaleAbs(grad_x_7)
sobel_y_7=cv.convertScaleAbs(grad_y_7)

edge_strength_3=cv.addWeighted(src1=sobel_x_3,alpha=0.5,src2=sobel_y_3,beta=0.5,gamma=0)
edge_strength_5=cv.addWeighted(src1=sobel_x_5,alpha=0.5,src2=sobel_y_5,beta=0.5,gamma=0)
edge_strength_7=cv.addWeighted(src1=sobel_x_7,alpha=0.5,src2=sobel_y_7,beta=0.5,gamma=0)

sobel_3=np.hstack((sobel_x_3,sobel_y_3,edge_strength_3))
sobel_5=np.hstack((sobel_x_5,sobel_y_5,edge_strength_5))
sobel_7=np.hstack((sobel_x_7,sobel_y_7,edge_strength_7))

sobel_result=np.vstack((sobel_3,sobel_5,sobel_7))
cv.imshow('row : sobel_ksize_3,5,7, column : sobel_x,sobel_y,edge_strength',sobel_result)
cv.imwrite('row_sobel_ksize_3,5,7_column_sobel_x,sobel_y,edge_strength.png',sobel_result)

cv.waitKey(0)
cv.destroyAllWindows()