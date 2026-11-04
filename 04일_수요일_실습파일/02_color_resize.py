# from pathlib import Path
# import os
# import cv2
# import numpy as np

# # 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# # OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
# os.chdir(Path(__file__).resolve().parent)

# image = cv2.imread("scene.png")
# # >>> TODO B02
# # image를 Gray와 RGB로 각각 변환하여 gray, rgb에 넣으세요. 두 번째 인자는 변환 코드입니다.
# gray = image.copy()
# rgb = image.copy()
# # <<< TODO B02
# small = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
# cv2.imwrite("p02_gray.png", gray)
# cv2.imwrite("p02_small.png", small)
# # RGB 배열은 화면 표시용입니다. imwrite에 그대로 넣지 않습니다.
# print("Gray shape:", gray.shape)
# print("RGB 빨강:", rgb[30, 30].tolist())
# print("Resize shape:", small.shape)

from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

# 원본 이미지를 BGR 형태로 불러옵니다.
image = cv2.imread("scene.png")

# >>> TODO B02
# image를 Gray와 RGB로 각각 변환하여 gray, rgb에 넣으세요. 두 번째 인자는 변환 코드입니다.

# [❌ 과거 오답 주석 처리 부분 해석]
# gray = cv2.imread("p02_gray.png")
# 💡 이유: 아직 아래에서 저장(imwrite)하기도 전인 결과 파일("p02_gray.png")을 미리 읽으려고 해서 파일 없음 오류(None)가 발생했습니다.
# rgb = cv2.imread("image")
# 💡 이유: 파일 이름 자리에 문자열 "image"를 넣으면, 파이썬은 진짜 이름이 'image'인 이미지 파일을 찾으려고 합니다. 
#          그런 파일이 없으므로 빈 값(None)이 들어가서 아랫줄에서 'NoneType' 에러를 일으켰습니다.

# [설명] 이미 cv2.imread로 읽어온 메모리 상의 'image' 데이터를 다룰 때는 새로운 파일 읽기(imread)가 아니라 색상 변환(cvtColor)을 사용해야 합니다.

# [⭕ 현재 정답 수정 완료 부분 해석]
# 원본 image(BGR)를 흑백(GRAY)으로 색상 공간을 변환하여 gray 변수에 담습니다.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 원본 image(BGR)를 표준 컬러(RGB)로 색상 공간을 변환하여 rgb 변수에 담습니다.
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# <<< TODO B02

# 원본 이미지의 크기를 224x224로 축소(Resize)합니다. 축소할 때는 화질 손실을 줄이는 INTER_AREA 보간법을 씁니다.
small = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

# 변환 및 가공이 끝난 이미지(gray, small)를 각각 파일로 컴퓨터에 저장합니다.
cv2.imwrite("p02_gray.png", gray)
cv2.imwrite("p02_small.png", small)

# ⚠️ RGB 배열은 화면 표시용(예: Matplotlib, 웹 페이지 띄우기용)입니다. 
# OpenCV의 imwrite 함수는 무조건 BGR 순서로 저장하려 하기 때문에, 여기에 rgb 변수를 그대로 넣으면 색상이 파랗게/빨갛게 뒤틀려 저장됩니다.

# 결과 출력 확인
print("Gray shape:", gray.shape)       
# 흑백 이미지가 되면서 3차원(BGR)이었던 채널이 사라지고, (세로, 가로) 형태의 2차원 배열 크기가 출력됩니다.

print("RGB 빨강:", rgb[30, 30].tolist()) 
# 정답 코드로 수정되면서 rgb 변수에 실제 데이터가 존재하므로, (30, 30) 좌표의 픽셀 값이 [R, G, B] 리스트로 에러 없이 완벽하게 출력됩니다!

print("Resize shape:", small.shape)    
# 축소된 이미지의 크기인 (224, 224, 3)이 출력됩니다.

""" 출력 결과 값
Gray shape: (240, 320)
RGB 빨강: [255, 0, 0]
Resize shape: (224, 224, 3) """