from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

# 원본 이미지를 읽어옵니다.
image = cv2.imread("scene.png")

# >>> TODO B06
# cv2.flip(image, 1)로 좌우 반전한 flipped를 만드세요. 세로 반전은 flipCode=0입니다.

# [❌ 오답 분석]
# flipped = image.copy(cv2.flip(image, 1))
# 💡 이유: 7교시 오답과 마찬가지로 `.copy()` 함수는 안에 다른 변수나 함수를 넣을 수 없습니다. 
#          이미 `cv2.flip(image, 1)` 자체가 반전된 새로운 이미지 배열을 만들어내므로 대입만 해주면 됩니다.

# [⭕ 정답 설명]
# cv2.flip(원본, flipCode): 1은 좌우 반전, 0은 상하(세로) 반전, -1은 상하좌우 모두 반전입니다.
flipped = cv2.flip(image, 1) 
# <<< TODO B06

# [💡 밝기 조절 및 데이터 타입 클리핑(Clip) 연산 중요 설명]
# 1. image.astype(np.float32) + 30: 기본 uint8(0~255) 상태에서 30을 더하면 255를 넘는 순간 0으로 뒤틀리는 현상(Overflow)이 생깁니다. 이를 방지하려 실수형(float)으로 바꾼 뒤 30을 더합니다.
# 2. np.clip(데이터, 최소, 최대): 255를 초과한 값은 255로, 0보다 작은 값은 0으로 강제 고정합니다.
# 3. .astype(np.uint8): 연산이 끝난 후 다시 이미지 표준 데이터 타입인 8비트 정수형으로 되돌립니다.
bright = np.clip(image.astype(np.float32) + 30, 0, 255).astype(np.uint8)

# cv2.hconcat([이미지1, 이미지2, 이미지3]): 리스트 안의 이미지들을 '가로(Horizontal)' 방향으로 나란히 이어 붙입니다.
# 세로로 붙이고 싶을 때는 cv2.vconcat()을 사용합니다.
comparison = cv2.hconcat([image, flipped, bright])

# 하나로 합쳐진 가로 이미지를 파일로 저장합니다.
cv2.imwrite("p06_comparison.png", comparison)

# 터미널 결과 출력
print("왼쪽 원본 / 가운데 좌우반전 / 오른쪽 +30 밝기")
print("비교 그림 Shape:", comparison.shape) 
# 가로로 3장을 붙였기 때문에 세로 크기와 채널(3)은 그대로이고, 가로 픽셀 크기만 원본의 3배로 늘어납니다.

print("밝기 범위:", int(bright.min()), int(bright.max()))
# 최소 밝기 값과 최대 밝기 값(255 제한 보증)을 출력합니다.

""" 출력 결과 값
왼쪽 원본 / 가운데 좌우반전 / 오른쪽 +30 밝기
비교 그림 Shape: (240, 960, 3)
밝기 범위: 30 255   """