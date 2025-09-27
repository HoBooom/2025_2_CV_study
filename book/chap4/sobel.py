import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma3.jpeg')
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#Sobel : 솔베 필터
#src : 이미지
#ddepth : 이미지 타입 현재 cv.CV_32F로 설정 32bit float
#dx : x방향 미분 
#dy: y방향 미분
#ksize : 커널 크기
grad_x=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=1,dy=0,ksize=3)
grad_y=cv.Sobel(src=gray,ddepth=cv.CV_32F,dx=0,dy=1,ksize=3)

#convertScaleAbs : 이미지 타입을 시각화 할 수 있도록 uint8로 변환
sobel_x=cv.convertScaleAbs(grad_x)
sobel_y=cv.convertScaleAbs(grad_y)

#src1 : 첫번째 이미지
#alpha : 첫번째 이미지 가중치
#src2 : 두번째 이미지
#beta : 두번째 이미지 가중치
#gamma : 결과 이미지 오프셋(추가적으로 더해지는 값)
edge_strength=cv.addWeighted(src1=sobel_x,alpha=0.5,src2=sobel_y,beta=0.5,gamma=0)

result=np.hstack((sobel_x,sobel_y,edge_strength))
cv.imshow('ori_img',img)
cv.imshow('sobel_x,sobel_y,edge_strength',result)




cv.waitKey(0)
cv.destroyAllWindows()