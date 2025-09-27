import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma3.jpeg')
#img=cv.resize(img,dsize=(0,0),fx=0.5,fy=0.5)
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.putText(gray,'HBC',(10,20),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
cv.imshow('gray',gray)

#GaussianBlur : 가우시안 필터
#첫번째 인수 : 이미지
#두번째 인수 : 커널 크기
#세번째 인수 : 표준 편차 - 0.0으로 설정시 자동으로 계산
smooth=np.hstack((
                cv.GaussianBlur(gray,(5,5),0.0),
                cv.GaussianBlur(gray,(9,9),0.0),
                cv.GaussianBlur(gray,(15,15),0.0)))
cv.imshow('smooth',smooth)

femboss=np.array([[-1.0,0.0,0.0],
                  [0.0,0.0,0.0],
                  [0.0,0.0,1.0]])

gray16=np.int16(gray)
emboss=np.uint8(np.clip(cv.filter2D(gray16,-1,femboss)+128,0,255))
emboss_bad=np.uint8(cv.filter2D(gray16,-1,femboss)+128)


emboss_result=np.hstack((emboss,emboss_bad))
cv.imshow('emboos,emboss_bad',emboss_result)

cv.waitKey(0)
cv.destroyAllWindows()