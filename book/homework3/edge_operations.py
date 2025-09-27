import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma4.jpeg')
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

#TODO : prewitt filter
#prewitt x : 수직엣지 검출 
kernel_prewitt_x = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
], dtype=np.float32)

#prewitt y : 수평엣지 검출
kernel_prewitt_y = np.array([
    [-1, -1, -1],
    [ 0,  0,  0],
    [ 1,  1,  1]
], dtype=np.float32)

#filter2D : 컨볼루션 연산
prewitt_x = cv.filter2D(src=gray, ddepth=cv.CV_32F, kernel=kernel_prewitt_x)
prewitt_y = cv.filter2D(src=gray, ddepth=cv.CV_32F, kernel=kernel_prewitt_y)
prewitt_x_abs = cv.convertScaleAbs(prewitt_x)
prewitt_y_abs = cv.convertScaleAbs(prewitt_y)
prewitt_combined = cv.addWeighted(src1=prewitt_x_abs, alpha=0.5, src2=prewitt_y_abs, beta=0.5, gamma=0)

prewitt_result=np.hstack((gray,prewitt_x_abs,prewitt_y_abs,prewitt_combined))
cv.imshow('prewitt_x,prewitt_y,prewitt_combined',prewitt_result)
cv.imwrite('./book/homework3/prewitt_x,prewitt_y,prewitt_combined.png',prewitt_result)


#TODO : sobel filter
kernel_sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
], dtype=np.float32)
kernel_sobel_y = np.array([
    [-1, -2, -1],
    [ 0,  0,  0],
    [ 1,  2,  1]
], dtype=np.float32)
sobel_x = cv.filter2D(src=gray, ddepth=cv.CV_32F, kernel=kernel_sobel_x)
sobel_y = cv.filter2D(src=gray, ddepth=cv.CV_32F, kernel=kernel_sobel_y)
sobel_x_abs = cv.convertScaleAbs(sobel_x)
sobel_y_abs = cv.convertScaleAbs(sobel_y)
sobel_combined = cv.addWeighted(src1=sobel_x_abs, alpha=0.5, src2=sobel_y_abs, beta=0.5, gamma=0)
sobel_result=np.hstack((gray,sobel_x_abs,sobel_y_abs,sobel_combined))
cv.imshow('sobel_x,sobel_y,sobel_combined',sobel_result)
cv.imwrite('./book/homework3/sobel_x,sobel_y,sobel_combined.png',sobel_result)

#TODO : canny filter
canny1=cv.Canny(image=gray,threshold1=50,threshold2=150,apertureSize=3,L2gradient=False)
canny2=cv.Canny(image=gray,threshold1=150,threshold2=450,apertureSize=3,L2gradient=False)
canny_result=np.hstack((gray,canny1,canny2))
cv.imshow('canny1,canny2',canny_result)
cv.imwrite('./book/homework3/canny1,canny2.png',canny_result)



cv.waitKey(0)
cv.destroyAllWindows()