"""
엣지만을 추출한 엣지맵에는 연결관계가 암시적으로 나타나 있을 뿐
명시적으로 표현되어 있지 않음, 이러한 엣지들을 연결해 경계선으로 변환하고
경계선을 직선으로 변환하면 이후 단계인 물체 표현이나 인식에 무척 유리함
"""

import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma5.jpeg')

gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#edge map구하기 canny이용
canny=cv.Canny(image=gray,threshold1=50,threshold2=150,apertureSize=3,L2gradient=False)

#경계선 찾기
#findContours : 경계선 찾기
#image : 이미지
#mode : 경계선 찾기 모드 cv.RETR_EXTERNAL : 외곽선만 찾기, cv.RETR_LIST : 모든 경계선 찾기, cv.RETR_CCOMP : 두 단계 계층 구조로 찾기, cv.RETR_TREE : 모든 경계선을 포함하는 계층 구조로 찾기
#method : 경계선 찾기 방법 cv.CHAIN_APPROX_NONE : 모든 점을 포함하는 경계선 찾기, cv.CHAIN_APPROX_SIMPLE : 경계선을 줄이는 방법
#contours : 윤곽선 목록 리스트, 리스트 각 요소는 numpy array로 구성되어 있음 ex) coutour[0] : 첫번째 윤곽선, coutour[0][0] : 첫번째 윤곽선의 첫번째 점
#hierarchy : 각 윤곽선의 계층 구조 정보를 담고 있는 numpy array, 각 윤곽선 i에 대해 hierarchy[0, i]는 [다음 윤곽선 인덱스, 이전 윤곽선 인덱스, 자식 윤곽선 인덱스, 부모 윤곽선 인덱스]의 4개 값을 가집니다. 윤곽선이 없는 경우 -1이 기록됩니다.
contour,hierarchy=cv.findContours(image=canny,mode=cv.RETR_LIST,method=cv.CHAIN_APPROX_NONE)

#lcontour : 윤곽선 목록 리스트
lcontour=[]


for i in range(len(contour)):
    #윤곽선의 점의 개수가 50개 이상인 경우 윤곽선 목록에 추가
    if contour[i].shape[0] > 150:
        lcontour.append(contour[i])

#drawContours : 윤곽선 그리기
#image : 이미지
#contours : 윤곽선 목록 리스트
#contourIdx : 그릴 윤곽선 인덱스 -1은 모든 윤곽선을 그림
#color : 윤곽선 색상
#thickness : 윤곽선 두께
cv.drawContours(image=img,contours=lcontour,contourIdx=-1,color=(0,255,0),thickness=2)

cv.imshow('ori_img',img)
cv.imshow('canny',canny)

cv.waitKey(0)
cv.destroyAllWindows()