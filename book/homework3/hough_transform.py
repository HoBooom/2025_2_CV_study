import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma5.jpeg')
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#GaussianBlur : 가우시안 블러 처리를 통해 노이즈 감소
#cv.GaussianBlur(src,ksize,sigmaX)
#src : 이미지
#ksize : 커널 크기
#sigmaX : 표준 편차 -> 0으로 설정시 자동으로 계산, 커질 수록 더 넓고 부드럽게 블러처리됨
blur = cv.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)

edges=cv.Canny(image=blur,threshold1=40,threshold2=120,apertureSize=3,L2gradient=False)

"""
기본적으로 현재 코드에서 Hough 변환은 Canny edge후 edge라고 판단한 픽셀들에 한해서 이루어지기 때문에
Canny edge 임계값을 높여서 edge를 더 적게 추출하면 Hough 변환 결과도 더 적게 검출됨
"""

#houghLinesP : 확률적 Hough 변환 return numpy.array([[x1,y1,x2,y2]]) (N,1,4) N : 검출된 직선의 개수, 4 : 직선의 양 끝 좌표(x1,y1,x2,y2)
#rho : 거리 해상도, 원점에서 직선까지의 거리를 얼마나 세밀하게 측정할지 결정, Hough transform -> 이미지 공간의 점을 Hough 공간의 p(rho,theta) 형태로 변환
#rho = 1 : 1픽셀 단위로 거리를 측정, 값이 커질 수록 정확도는 떨어지지만 연산속도 빨라짐(정확도와 연산속도 반비례)
#theta : 각도 해상도, 각도를 얼마나 세밀하게 측정할지 결정, theta = np.pi / 180 : 1도 단위로 각도를 측정
#threshold : 임계값
#minLineLength : 최소 직선 길이
#maxLineGap : 최대 허용 간격
lines1 = cv.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)
lines2 = cv.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=75, maxLineGap=10)
lines3 = cv.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=100, maxLineGap=10)
lines4 = cv.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=125, maxLineGap=10)
lines5 = cv.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=50, minLineLength=150, maxLineGap=10)

# 3. 검출된 직선 그리기
hough_result1 = np.copy(img)
hough_result2 = np.copy(img)
hough_result3 = np.copy(img)
hough_result4 = np.copy(img)
hough_result5 = np.copy(img)

def draw_lines(lines,hough_result):
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(img=hough_result, pt1=(x1, y1), pt2=(x2, y2), color=(0, 0, 255), thickness=3) 

draw_lines(lines1,hough_result1)
draw_lines(lines2,hough_result2)
draw_lines(lines3,hough_result3)
draw_lines(lines4,hough_result4)
draw_lines(lines5,hough_result5)

# 결과 출력
result=np.hstack((img,hough_result1,hough_result2,hough_result3,hough_result4,hough_result5))
cv.imshow('result',result)
cv.imwrite('./book/homework3/hough_transform_minlineLength_50,75,100,125,150.png',result)




cv.waitKey(0)
cv.destroyAllWindows()