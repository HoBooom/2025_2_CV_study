import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma3.jpeg')

gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#Canny : 캐니 필터
#image : 이미지
#threshold1 : 첫번째 임계값
#threshold2 : 두번째 임계값
#apertureSize : 커널 크기
#L2gradient : 라플라시안 연산 사용 여부
canny1=cv.Canny(image=gray,threshold1=50,threshold2=150,apertureSize=3,L2gradient=False)
canny2=cv.Canny(image=gray,threshold1=100,threshold2=200,apertureSize=3,L2gradient=False)


#임계값이 높을 수록 더 확실한 엣지만을 추적하기 때문에 더욱 적은 엣지가 발생함
result=np.hstack((canny1,canny2))
cv.imshow('ori_img',img)
cv.imshow('canny1,canny2',result)

cv.waitKey(0)
cv.destroyAllWindows()