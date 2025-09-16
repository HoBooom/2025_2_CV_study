import cv2 as cv
import matplotlib.pyplot as plt

img=cv.imread('./image/grandma3.jpeg')

#히스토그램을 통해 각 화소마다 빈도수를 계산해서 시각화
#첫번째 인수 : img위치
#두번째 인수 : 채널 번호
#세번째 인수 : mask(히스토그램을 구할 영역, 현재 None으로 전체 영역)
#네번째 인수 : 히스토그램 빈도수 계산 범위
#다섯번째 인수 : 세어볼 명암 값의 범위
h_r=cv.calcHist([img],[2],None,[256],[0,256])
h_g=cv.calcHist([img],[1],None,[256],[0,256])
h_b=cv.calcHist([img],[0],None,[256],[0,256])

plt.plot(h_r,color='r',label='Red',linewidth=1)
plt.plot(h_g,color='g',label='Green',linewidth=1)
plt.plot(h_b,color='b',label='Blue',linewidth=1)
plt.legend()
plt.show()