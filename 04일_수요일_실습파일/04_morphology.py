# from pathlib import Path
# import os
# import cv2
# import numpy as np

# # 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# # OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
# os.chdir(Path(__file__).resolve().parent)

# image = cv2.imread("objects.png")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# threshold_value, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# kernel = np.ones((3, 3), dtype=np.uint8)
# # >>> TODO B04
# # binary에 3×3 kernel을 사용한 Opening을 적용하세요. 결과 이름은 opened입니다.
# opened = binary.copy()
# # <<< TODO B04
# cv2.imwrite("p04_gray.png", gray)
# cv2.imwrite("p04_binary.png", binary)
# cv2.imwrite("p04_open.png", opened)
# print("임계값:", threshold_value)
# print("전경 픽셀:", int(np.count_nonzero(binary)), "->", int(np.count_nonzero(opened)))
# print("결과 값:", np.unique(opened).tolist())

from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

# 1. 원본 이미지 불러오기 및 흑백 변환
image = cv2.imread("objects.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. 임계처리 (이진화, Thresholding)
# - 127을 기준으로 이보다 밝으면 255(흰색), 어두우면 0(검은색)으로 픽셀을 이분법적으로 분리합니다.
# - binary 변수에는 이진화된 이미지 데이터가, threshold_value에는 사용된 임계값(127)이 저장됩니다.
threshold_value, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 3. 모폴로지 연산에 사용할 커널(필터) 생성
# - np.ones((3, 3)): 모든 원소가 1로 채워진 3x3 크기의 행렬을 만듭니다. 이 커널이 이미지를 훑으며 노이즈를 찾아냅니다.
kernel = np.ones((3, 3), dtype=np.uint8)

# >>> TODO B04
# binary에 3×3 kernel을 사용한 Opening을 적용하세요. 결과 이름은 opened입니다.

# [❌ 오답 분석]
# opened = binary.copy()
# 💡 이유: 이전 실습들과 마찬가지로 `.copy()`는 단순히 이미지를 복사하는 함수입니다. 
#          노이즈를 제거하는 '오프닝(Opening)' 연산이 전혀 적용되지 않은 채 이진화 이미지가 그대로 복사됩니다.

# [⭕ 정답 설명]
# - cv2.morphologyEx(): OpenCV의 고급 모폴로지 연산 함수입니다.
# - cv2.MORPH_OPEN: 침식(Erosion) 연산 후 팽창(Dilation) 연산을 연속으로 수행하는 '오프닝' 모드를 지정합니다.
#   (오프닝은 배경에 흰색 점처럼 흩어져 있는 미세한 노이즈나 돌기를 깔끔하게 깎아내어 지워주는 역할을 합니다.)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
# <<< TODO B04

# 4. 가공된 이미지 파일 저장
cv2.imwrite("p04_gray.png", gray)
cv2.imwrite("p04_binary.png", binary)
cv2.imwrite("p04_open.png", opened)

# 5. 결과 검증 출력
print("임계값:", threshold_value)

print("전경 픽셀:", int(np.count_nonzero(binary)), "->", int(np.count_nonzero(opened)))
# np.count_nonzero(): 0이 아닌 픽셀(즉, 흰색 전경 픽셀)의 개수를 세어줍니다.
# 오프닝 연산으로 인해 자잘한 흰색 잡음들이 사라지면서, 흰색 픽셀 수가 줄어든 것(`binary` -> `opened`)을 확인할 수 있습니다.

print("결과 값:", np.unique(opened).tolist())
# np.unique(): 이미지에 사용된 고유한 픽셀 값을 중복 없이 보여줍니다. 이진화와 모폴로지를 거쳤기 때문에 [0, 255]만 깨끗하게 남습니다.

""" 출력 결과 값
임계값: 127.0
전경 픽셀: 14142 -> 14133
결과 값: [0, 255]   """