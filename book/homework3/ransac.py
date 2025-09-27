import cv2 as cv
import numpy as np
import math

"""
RANSAC 알고리즘
line = []
for i in range(MaxIterations):
    엣지 화소 임의의 두개 선택
    이 두 점으로 직선의 방정식 l 계산
    이 두 점으로 inlier 초기화
    for 이 두 점을 제외한 모든 포인트:
        만약 p가 직선 l에 허용오차 이내에 속한다면 -> inlier에 추가
    if inlier의 개수가 MinInliers 이상이면 -> 직선 업데이트
line에 있는 직선 중 가장 많은 inlier를 가지고 있는 직선 선택 -> 최종 직선
"""

"""
Parameters
* Points - 엣지 검출을 통해 얻은 모든 2D 좌표 ({(xi,yi)})들의 집합
* MaxIterations -	알고리즘의 최대 반복 횟수
* SampleSize - 모델(직선)을 정의하는 데 필요한 최소 샘플 수 (직선의 경우 2)
* Threshold -	점이 직선에 속한다고 판단하는 최대 거리 (허용 오차), 
        너무 작으면 노이즈가 없는 완벽한 엣지포인트만 인정 -> 유효한 직선도 놓칠 수 있음
        너무 크면 노이즈 까지도 인정 -> 잘못된 직선 찾을 수 있음
* MinInliers - 유효한 직선으로 인정하기 위한 최소 인라이어(Inlier) 수
"""

# --- RANSAC 파라미터 ---
MAX_ITERATIONS = 1000      # 최대 반복 횟수 (직선을 시도할 횟수)
SAMPLE_SIZE = 2          # 직선을 정의하는 데 필요한 최소 포인트 수
INLIER_THRESHOLD = 5.0   # 점이 직선에 속한다고 판단하는 최대 거리 (픽셀)
MIN_INLIERS = 10         # 유효한 직선으로 인정하기 위한 최소 인라이어 수 (절대 개수)

def ransac(points):
    global MAX_ITERATIONS, SAMPLE_SIZE, INLIER_THRESHOLD, MIN_INLIERS

    best_line_params = None
    max_inliers_count = 0
    
    # 엣지 포인트가 충분하지 않으면 종료
    if len(points) < SAMPLE_SIZE:
        return None

    # 모든 엣지 포인트의 인덱스 리스트 생성
    all_indices = np.arange(len(points))

    for i in range(MAX_ITERATIONS):
        # 1. 무작위 샘플링 (Hypothesize): 2개의 점 선택
        sample_indices = np.random.choice(all_indices, SAMPLE_SIZE, replace=False)
        p1, p2 = points[sample_indices]
        
        # 2. 모델 생성: y = mx + c 또는 x = c (직선의 기울기 m과 y/x 절편 c 계산)
        
        # 분모 (x2 - x1)가 0인 경우: 수직선 (기울기 무한대)
        if p2[0] - p1[0] == 0:
            m = float('inf')
            c = p1[0]  # 수직선의 x 좌표
        else:
            m = (p2[1] - p1[1]) / (p2[0] - p1[0])
            c = p1[1] - m * p1[0]
            
        # 3. 인라이어(Inlier) 계산
        current_inliers_indices = []
        
        for j in all_indices:
            x, y = points[j]
            
            if m == float('inf'): # 수직선 (x = c)
                # 점과 수직선 사이의 거리
                dist = abs(x - c)
            else: # 일반 직선 (mx - y + c = 0)
                # 점과 직선 사이의 거리 공식: |Ax + By + C| / sqrt(A^2 + B^2)
                dist = abs(m * x - 1 * y + c) / math.sqrt(m**2 + 1)
            
            # 임계값 이내이면 인라이어로 간주
            if dist < INLIER_THRESHOLD:
                current_inliers_indices.append(j)
        
        # 4. 최적 모델 업데이트
        current_inliers_count = len(current_inliers_indices)
        if current_inliers_count > max_inliers_count:
            max_inliers_count = current_inliers_count
            # 현재 모델의 인라이어 인덱스 저장
            best_inlier_indices = current_inliers_indices

    # 5. 최종 결과 확인 및 정제 (Refinement)
    if max_inliers_count >= MIN_INLIERS:
        
        # 최종 인라이어 포인트들만 추출
        final_inliers = points[best_inlier_indices]
        inlier_x = final_inliers[:, 0]
        inlier_y = final_inliers[:, 1]
        
        # NumPy의 polyfit을 사용하여 인라이어에 가장 잘 맞는 최종 직선 피팅 (최소 제곱법)
        # polyfit(x_data, y_data, degree=1) 반환: [기울기 m, y절편 c]
        if len(inlier_x) >= 2:
            final_m, final_c = np.polyfit(inlier_x, inlier_y, 1)
            
            # 직선을 그릴 영역의 경계 설정
            x_min, x_max = inlier_x.min(), inlier_x.max()
            
            return (final_m, final_c, x_min, x_max)

    
    return None

img=cv.imread('./image/grandma2.jpeg')
# 전처리 과정 -> Canny edge 검출
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges=cv.Canny(image=gray,threshold1=50,threshold2=150,apertureSize=3,L2gradient=False)

# 엣지 이미지에서 (x, y) 엣지 픽셀의 좌표를 추출
# np.where : 조건에 맞는 인덱스를 반환
edge_y, edge_x = np.where(edges > 0)
# (x, y) 좌표 쌍으로 배열을 재구성: (N, 2) 형태, np.column_stack : 좌표 쌍으로 배열을 재구성
edge_points = np.column_stack((edge_x, edge_y))

# RANSAC 실행
print(f"총 엣지 포인트 수: {len(edge_points)}")
print(f"RANSAC 시작 (반복 횟수: {MAX_ITERATIONS}, 최소 인라이어: {MIN_INLIERS})...")
best_line_params = ransac(edge_points)


# 시각화
ransac_result = np.copy(img)

if best_line_params:
    m, c, x_min, x_max = best_line_params
    
    x1 = int(x_min)
    y1 = int(m * x1 + c)
    x2 = int(x_max)
    y2 = int(m * x2 + c)
    
    # 검출된 직선 그리기
    cv.line(img=ransac_result, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 0), thickness=3)
    
    print(f"RANSAC 검출 성공: 기울기 m={m:.2f}, Y절편 c={c:.2f}")
else:
    print("RANSAC 조건을 만족하는 유효한 직선을 찾지 못했습니다.")

# 결과 출력
cv.imshow("Canny Edges", edges)
cv.imshow("RANSAC Line Detection Result", ransac_result)
cv.imwrite('./book/homework3/ransac_result.png', ransac_result)

cv.waitKey(0)
cv.destroyAllWindows()
