# from pathlib import Path
# import os
# import cv2
# import numpy as np

# # 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# # OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
# os.chdir(Path(__file__).resolve().parent)

# image = cv2.imread("noisy.png")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # >>> TODO B03
# # gray를 (5,5), sigmaX=0으로 흐리게 하여 blur를 만드세요. blur에 Canny 80,160을 적용하여 edge를 만드세요.
# blur = gray.copy()
# edge = gray.copy()
# # <<< TODO B03
# cv2.imwrite("p03_blur.png", blur)
# cv2.imwrite("p03_edge.png", edge)
# print("설정: Gaussian (5,5), sigmaX=0, Canny 80/160")
# print("Shape:", blur.shape, edge.shape)
# print("Edge 픽셀:", int(np.count_nonzero(edge)))


from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

# 1. 노이즈가 있는 원본 이미지를 읽어와서 흑백(Gray)으로 변환합니다.
image = cv2.imread("noisy.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# >>> TODO B03
# gray를 (5,5), sigmaX=0으로 흐리게 하여 blur를 만드세요. blur에 Canny 80,160을 적용하여 edge를 만드세요.

# [❌ 오답 분석]
# blur = cv2.GaussianBlur(gray,size=5,5, sigmaX=0)
# 💡 이유: 파이썬에서 함수를 호출할 때는 반드시 이름 뒤에 괄호 `()`를 열고 인자들을 쉼표로 구분해야 합니다. 
#          또한 커널 크기는 `(5, 5)`처럼 튜플 형태로 묶어서 전달해야 합니다.
# edge = cv2.Canny, threshold1=80, threshold2=160
# 💡 이유: 함수 이름 뒤에 괄호를 열지 않고 쉼표를 찍으면 연산이 아니라 잘못된 문법 오류(SyntaxError)가 발생합니다.

# [⭕ 정답 설명]
# 2. 가우시안 블러를 적용하여 지저분한 자잘한 노이즈를 부드럽게 뭉갭니다.
# - (5, 5): 블러링을 적용할 필터의 가로세로 크기 (반드시 홀수여야 합니다)
# - 0: 가우시안 커널의 표준 편차(sigmaX)를 0으로 주면, 커널 크기에 맞춰 자동으로 계산됩니다.
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. 노이즈가 제거된 깨끗한 블러 이미지에서 캐니 알고리즘으로 경계선(Edge)을 검출합니다.
# - 80: 하위 임계값 (이 값보다 낮으면 확실히 에지가 아니라고 판단)
# - 160: 상위 임계값 (이 값보다 높으면 확실한 에지로 판단)
edge = cv2.Canny(blur, 80, 160)
# <<< TODO B03

# 4. 가공된 블러 이미지와 에지 이미지 결과를 각각 파일로 저장합니다.
cv2.imwrite("p03_blur.png", blur)
cv2.imwrite("p03_edge.png", edge)

# 5. 결과 검증 출력
print("설정: Gaussian (5,5), sigmaX=0, Canny 80/160")
print("Shape:", blur.shape, edge.shape) # 두 이미지 모두 흑백 단일 채널이므로 크기가 (세로, 가로) 형태로 동일합니다.

# 검출된 에지 선(흰색 픽셀, 255)의 총 개수를 세어 출력합니다.
print("Edge 픽셀:", int(np.count_nonzero(edge)))

""" 출력 결과 값
설정: Gaussian (5,5), sigmaX=0, Canny 80/160
Shape: (240, 320) (240, 320)
Edge 픽셀: 3234 """