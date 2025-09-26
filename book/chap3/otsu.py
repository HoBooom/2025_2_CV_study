import cv2 as cv
import sys

#otsu알고리즘
#목적함수 최소화
#목적함수 -> 이진화 했을때 0이 되는 화소의 분산과 1이되는 화소의 분산의 가중치(해당 화소의 개수) 합
#목적함수가 최소화된다 -> 각 화소별 분산이 작다 -> 즉 이진화 처리가 잘 되었다.
img=cv.imread('./image/grandma1.jpeg')

#cv.threshold : 이진화 처리
#첫번째 인수 : 이미지
#두번째 인수 : 초기 임계값, 현재 otsu 알고리즘 사용이므로 무시
#세번째 인수 : 임계값을 초과하는 픽실에 해당할 값 
# cv.THRESH_BINARY (이진 임계값): 가장 일반적인 이진화 방식입니다. 
# 픽셀 값이 임계값보다 크면 maxval (255)로, 작거나 같으면 0으로 만듭니다.
# cv.THRESH_OTSU (오츠 방법): 이진화에 사용할 최적의 임계값을 이미지의 
# 히스토그램을 분석하여 자동으로 찾아내는 알고리즘입니다. 
# 이 플래그가 cv.THRESH_BINARY와 함께 사용되면, 초기 thresh 값(0)을 무시하고 오츠 방법으로 계산된 최적 임계값을 사용합니다
t, bin_img = cv.threshold(img[:,:,2],0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

print(f'Otsu Threshold: {t}')

cv.imshow("R channel",img[:,:,2])
cv.imshow("Binary Image",bin_img)

cv.waitKey(0)
cv.destroyAllWindows()