# from pathlib import Path
# import os
# import cv2
# import numpy as np

# # 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# # OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
# os.chdir(Path(__file__).resolve().parent)

# # 색상 이미지: 한 픽셀의 값 순서는 B, G, R입니다.
# # >>> TODO B01
# # scene.png를 cv2.imread로 읽어 image에 저장하세요. flags를 생략하면 BGR 컬러로 읽습니다.
# image = None
# # <<< TODO B01
# print("shape:", image.shape)
# print("dtype:", image.dtype)
# print("min/max:", int(image.min()), int(image.max()))
# print("빨강 패치의 BGR:", image[30, 30].tolist())
# saved = cv2.imwrite("p01_copy.png", image)
# print("PNG 저장:", saved)

from pathlib import Path
import os
import cv2
import numpy as np

# 1. 작업 디렉토리(실행 위치) 자동 정렬
# 코드를 어느 폴더에서 실행하더라도, 현재 이 파이썬 파일(main.py 등)이 있는 폴더를 
# 기준으로 삼도록 작업 디렉토리를 변경합니다. (scene.png 파일과 같은 위치로 강제 이동)
os.chdir(Path(__file__).resolve().parent)

# 색상 이미지: OpenCV로 이미지를 읽으면 한 픽셀의 색상 값 순서가 R-G-B가 아니라 B(파랑), G(초록), R(빨강) 순서가 됩니다.
# >>> TODO B01
# 2. 이미지 파일 읽기
# 현재 폴더에 있는 "scene.png" 파일을 cv2.imread 함수를 사용해 읽어와 image 변수에 저장합니다.
image = cv2.imread("scene.png")
# <<< TODO B01

# 3. 불러온 이미지의 데이터 속성(메타데이터) 확인하기
print("shape:", image.shape)       
# 이미지의 크기를 출력합니다. 결과는 (세로 픽셀 수, 가로 픽셀 수, 색상 채널 수) 형태입니다.
# 색상 채널 수는 BGR 3개이므로 마지막 숫자는 항상 3이 나옵니다. 예: (480, 640, 3)

print("dtype:", image.dtype)       
# 이미지 데이터의 자료형을 출력합니다. 컴퓨터 비전에서 이미지는 일반적으로 0~255 사이의 정수를 사용하는 `uint8`(8비트 부호없는 정수)입니다.

print("min/max:", int(image.min()), int(image.max()))
# 이미지 전체에서 가장 어두운 픽셀 값(최솟값, 0에 가까움)과 가장 밝은 픽셀 값(최댓값, 255에 가까움)을 찾아 출력합니다.

print("빨강 패치의 BGR:", image[30, 30].tolist())
# 이미지의 세로 30번째, 가로 30번째 위치(좌측 상단 구역)에 있는 픽셀 1개의 색상 값을 [B, G, R] 리스트 형태로 변환하여 출력합니다.
# 만약 그 자리가 빨간색(Red)이라면, B와 G는 0에 가깝고 R은 255에 가까운 값(예: [0, 0, 255])이 나옵니다.

# 4. 이미지 복사본 저장하기
# 불러온 image 데이터를 "p01_copy.png"라는 새로운 이름의 파일로 현재 폴더에 저장합니다.
saved = cv2.imwrite("p01_copy.png", image)

print("PNG 저장:", saved)
# 이미지 저장이 성공하면 True, 실패하면 False가 출력됩니다. 원본 파일은 건드리지 않고 그대로 유지됩니다.

""" 출력 결과 값
shape: (240, 320, 3)
dtype: uint8
min/max: 0 255
빨강 패치의 BGR: [0, 0, 255]
PNG 저장: True  """