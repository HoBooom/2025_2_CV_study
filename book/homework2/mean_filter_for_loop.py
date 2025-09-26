import cv2 as cv
import numpy as np

img=cv.imread('./image/grandma3.jpeg')
img_size_r = img.shape[0]
img_size_c = img.shape[1]

#결과 이미지
#padding을 위해 2칸 추가
#padding_img = np.pad(img,((1,1),(1,1),(0,0)),'constant') 이 코드는 원본에 패딩을 추가하는 코드임
padding_img = np.zeros((img_size_r + 2,img_size_c + 2, 3),dtype=np.uint8) #그냥 새로운 빈 이미지
padding = 1

for r in range(padding,img_size_r + padding):
    for c in range(padding,img_size_c + padding):
        for k in range(3):
            padding_img[r,c,k] = np.sum(img[r-padding:r+padding+1,c-padding:c+padding+1,k]) / 9


output_img = padding_img[padding:img_size_r + padding,padding:img_size_c + padding,:]
result = np.hstack((img,output_img))
cv.imshow('ori_img,output_img',result)

cv.imwrite('mean_filter_for_loop.png', result) 

cv.waitKey(0)
cv.destroyAllWindows()


