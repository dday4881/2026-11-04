from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

# 1. 원본 동영상 파일 열기
cap = cv2.VideoCapture("sample.avi")

# 2. 동영상의 메타데이터(정보) 가져오기
fps = cap.get(cv2.CAP_PROP_FPS)                              # 초당 프레임 수 (예: 30.0 FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))               # 동영상 가로 해상도 크기
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             # 동영상 세로 해상도 크기

# 3. 저장할 새로운 동영상 파일 설정
# - "p05_gray.avi": 저장할 파일명
# - cv2.VideoWriter_fourcc(*"MJPG"): 동영상을 압축할 코덱 포맷 (Motion JPEG)
# - fps, (width, height): 원본과 동일한 배속 및 크기로 설정
writer = cv2.VideoWriter("p05_gray.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height))

print("열림(입력/출력):", cap.isOpened(), writer.isOpened())  # 두 파일이 모두 에러 없이 정상적으로 열렸는지 확인 (True, True)
print("입력 FPS/크기:", fps, (width, height))

# 4. 프레임별 비디오 처리 반복문
count = 0
while cap.isOpened() and writer.isOpened():
    ok, frame = cap.read() # 동영상에서 프레임(이미지)을 1장씩 순서대로 읽어옵니다.
    if not ok:  # 영상이 끝나서 더 이상 읽을 프레임이 없으면 반복문을 탈출합니다.
        break
        
    # >>> TODO B05
    # 현재 frame을 Gray로 변환하여 gray에 넣으세요. VideoCapture는 반복문 밖에서 이미 열었습니다.
    
    # [❌ 오답 분석]
    # gray = frame[:, :, 0]
    # 💡 이유: 컬러 동영상 프레임에서 B(Blue) 채널 데이터 한 장만 통째로 슬라이싱해 온 것입니다. 
    #          눈으로 보기에는 흑백처럼 보일지 몰라도, 정확한 명도 공식이 반영된 표준 '그레이스케일'이 아닙니다.
    
    # [⭕ 정답 설명]
    # OpenCV 공식 함수를 사용하여 컬러(BGR) 프레임을 표준 흑백(GRAY)으로 완벽하게 변환합니다.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # <<< TODO B05
    
    # 5. 변환된 프레임 저장하기
    # 중요: 위에서 정의한 VideoWriter는 기본적으로 컬러(3채널) 저장이 기본값입니다.
    # 단일 채널인 gray 변수를 그대로 넣으면 파일이 깨지거나 저장되지 않으므로, 
    # cv2.COLOR_GRAY2BGR를 통해 모양만 다시 3채널 구조로 채워서 저장해야 안정적으로 기록됩니다.
    writer.write(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))
    count += 1

# 6. 사용이 끝난 동영상 객체 및 장치 메모리 해제 (필수)
cap.release()
writer.release()

# 7. 저장 완료된 동영상을 다시 열어서 검증하기
check = cv2.VideoCapture("p05_gray.avi")
print("처리/재읽기 Frame:", count, int(check.get(cv2.CAP_PROP_FRAME_COUNT))) # 처리한 프레임 총 개수와 저장된 비디오의 총 프레임 수가 일치하는지 확인
print("재읽기 FPS:", check.get(cv2.CAP_PROP_FPS))                             # 저장된 비디오의 FPS 정보가 손실 없이 들어갔는지 확인
check.release()

""" 출력 결과 값
열림(입력/출력): True True
입력 FPS/크기: 12.0 (320, 240)
처리/재읽기 Frame: 48 48
재읽기 FPS: 12.0    """