from pathlib import Path
import os
import cv2
import numpy as np

# [ 시스템 설정 ] 
# 어떤 작업 폴더(Terminal 경로)에서 파이썬을 실행하더라도, 
# 현재 이 스크립트 파일이 저장된 폴더를 기준(Root)으로 강제 고정합니다.
# 이렇게 해야 옆에 있는 "scene.png", "sample.avi" 같은 파일들을 경로 에러(NoneType) 없이 바로 읽을 수 있습니다.
os.chdir(Path(__file__).resolve().parent)

import csv

# 엑셀 파일(CSV)에 차곡차곡 기록해 둘 데이터 행(Rows)들을 임시 저장할 텅 빈 리스트를 만듭니다.
rows = []

# =========================================================================
#  PART 1: 3개의 이미지 파일들을 반복문을 돌며 일괄 변환 처리하기
# =========================================================================
for filename in ["scene.png", "noisy.png", "objects.png"]:
    # 하드디스크에서 이미지 파일을 하나씩 [세로, 가로, 3(BGR)] 형태의 넘파이 배열로 읽어옵니다.
    image = cv2.imread(filename)
    
    # >>> TODO B07: 흑백 변환 및 160x120 해상도 축소
    
    # [❌ 내 오답 집중 분석 1]
    # gray = image[:160, :120, 0]
    # 💡 이유 A: 대괄호와 콜론을 쓰는 슬라이싱은 이미지 크기를 조절하는 게 아니라, 좌측 상단 꼭짓점부터 
    #            가로 120, 세로 160만큼 칼로 두부 자르듯 '가위질(Crop)'을 하는 연산입니다. (축소가 아님)
    # 💡 이유 B: 맨 마지막의 `, 0`은 BGR 색상 중 0번째 채널인 '파란색(Blue) 빛의 밝기'만 똑 떼어온 것입니다.
    #            진짜 흑백(Gray)은 RGB 전반의 가중치를 계산해야 하므로, 파란색 채널만 가져오면 붉은색 사물이 새까맣게 타버리는 왜곡이 생깁니다.
    
    # small = gray.copy()
    # 💡 이유: 위의 잘라낸 영역을 단순히 복사만 했을 뿐이므로, 사물 전체를 온전하게 압축하는 '축소(Resize)'가 되지 않았습니다.
    
    # [⭕ 완벽 정답 해설 1]
    # cv2.cvtColor: 수학적 공식(0.299*R + 0.587*G + 0.114*B)을 완벽히 적용하여 인간의 눈이 보기에 가장 자연스러운 흑백(Single Channel)으로 변환합니다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    
    # cv2.resize(원본, (너비, 높이)): 이미지 전체 형체를 유지한 채 가로 160, 세로 120 픽셀 크기로 꾹 압축합니다.
    # interpolation=cv2.INTER_AREA: 이미지를 '축소'할 때 픽셀이 뭉개지거나 깨지는 계단 현상을 방지하고 화질을 가장 부드럽고 깨끗하게 유지해 주는 전용 옵션입니다.
    small = cv2.resize(gray, (160, 120), interpolation=cv2.INTER_AREA) 
    # <<< TODO B07
    
    # >>> TODO B08: 가우시안 노이즈 필터링이 반영된 캐니 에지 검출
    
    # [❌ 내 오답 집중 분석 2]
    # edge = small.copy(80, 160)
    # 💡 이유: 넘파이의 `.copy()` 함수는 인자(매개변수)를 절대 받지 않는 '단순 복제 인간 제조기'입니다. 
    #          괄호 안에 숫자(80, 160)를 억지로 쑤셔 넣었기 때문에 "함수가 요구하는 인자의 개수가 틀렸다"며 문법 에러(TypeError)를 뿜고 멈춥니다.
    
    # [⭕ 완벽 정답 해설 2]
    # cv2.Canny(이미지, 하위임계값, 상위임계값): 픽셀 값의 변화도를 분석해 외곽선을 땁니다.
    # 변화량이 160을 넘으면 '확실한 선'으로 등록하고, 80보다 작으면 '노이즈'로 버리며, 그 사이(80~160) 값은 확실한 선과 이어져 있을 때만 최종 에지로 살려둡니다.
    edge = cv2.Canny(small, 80, 160) 
    # <<< TODO B08
    
    # 확장자를 제외한 순수 파일 이름(예: "scene")만 쏙 추출합니다.
    stem = Path(filename).stem
    
    # 가공이 완료된 각 단계별 이미지 결과물들을 중복되지 않게 독자적인 이름으로 저장합니다.
    cv2.imwrite(f"p07_{stem}_gray.png", gray)
    cv2.imwrite(f"p07_{stem}_small.png", small)
    cv2.imwrite(f"p07_{stem}_edge.png", edge)
    
    # 엑셀 보고서에 집계할 정보를 한 행씩 추가합니다.
    # [파일명, 원본너비(shape[1]), 원본높이(shape[0]), 결과너비(shape[1]), 결과높이(shape[0]), 에지 선으로 판명된 흰색 픽셀의 총 개수]
    # ⚠️ np.count_nonzero(edge)는 검은 배경(0) 속에서 에지 선으로 판명된 흰색 픽셀(255, 즉 0이 아닌 값)이 몇 개나 살아남았는지 카운트합니다.
    rows.append([filename, image.shape[1], image.shape[0], small.shape[1], small.shape[0], int(np.count_nonzero(edge))])


# =========================================================================
# PART 2: 동영상(샘플 비디오) 프레임 단위 연속 일괄 가공 처리하기
# =========================================================================
# 컴퓨터에 저장된 영상 파일인 "sample.avi"를 읽어올 준비를 합니다.
cap = cv2.VideoCapture("sample.avi")
fps = cap.get(cv2.CAP_PROP_FPS) # 원본 비디오의 초당 프레임 수(배속)를 그대로 복사해 옵니다.

# 저장용 비디오 출력 객체를 생성합니다.
# - "p07_video.avi": 최종 저장할 비디오 파일명
# - cv2.VideoWriter_fourcc(*"MJPG"): 자막이나 영상 데이터를 압축할 때 표준적으로 쓰이는 Motion JPEG 코덱 양식 지정
# - (160, 120): 우리가 축소할 타겟 크기대로 비디오 도화지 규격을 선언합니다. (여기에 규격이 맞지 않는 크기를 쓰면 영상이 안 구워집니다)
writer = cv2.VideoWriter("p07_video.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps, (160, 120))
print("Writer:", writer.isOpened()) # 저장용 도화지가 문제없이 정상 개설되었는지 상태 확인 (True가 떠야 함)
count = 0

# 영상 파일이 정상적으로 읽히고, 저장 도화지도 준비가 되어있는 동안 무한 반복 작동합니다.
while cap.isOpened() and writer.isOpened():
    ok, frame = cap.read() # 영상에서 영화 필름 1장(프레임)을 읽어와 frame 변수에 넣고, 읽기 성공 여부를 ok(True/False)에 넣습니다.
    if not ok: # 영상이 끝나서 더 이상 읽을 필름이 없다면(False) 반복문을 즉시 깨부수고 탈출합니다.
        break
        
    # >>> TODO B09: 각 비디오 프레임 한 장 한 장마다 이미지와 똑같은 가공 순서 적용하기
    
    # [❌ 내 오답 집중 분석 3]
    # frame_gray = frame[:, :, 0]
    # 💡 이유: 이미지 때와 똑같은 실수입니다. 컬러 영상 프레임에서 단순 블루(B) 채널 레이어 한 장만 분리해 낸 것이므로 왜곡된 야매 흑백입니다.
    # frame_small = cv2.resize(frame_gray, (160, 120))
    # 💡 이유: 보간법 옵션을 생략하면 기본값으로 축소되지만, 축소 연산 시 화질이 깨져 에지가 지저분하게 따지는 것을 막으려면 `INTER_AREA`를 명시하는 훈련이 필요합니다.
    # frame_edge = frame_small.copy()
    # 💡 이유: 가장 중요한 임무인 `cv2.Canny` 선 검출 함수를 아예 호출조차 하지 않고 맹목적으로 복사만 해서 넘겼기 때문에 미션 실패입니다.
    
    # [⭕ 완벽 정답 해설 3]
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 1단계: 컬러 프레임을 정석 흑백으로 변환
    frame_small = cv2.resize(frame_gray, (160, 120), interpolation=cv2.INTER_AREA) # 2단계: 지정 규격인 160x120으로 압축 축소
    frame_edge = cv2.Canny(frame_small, 80, 160)          # 3단계: 축소된 프레임에서 선명한 외곽선(에지) 검출
    # <<< TODO B09
    
    # ⚠️ 초특급 중요 내부 규칙!
    # 위에서 비디오 저장소(`VideoWriter`)를 개설할 때 우리는 컬러 비디오 형태로 세팅을 마쳤습니다.
    # 그런데 우리가 최종 추출한 `frame_edge`는 채널이 1개밖에 없는 흑백 데이터입니다. 이 상태 그대로 쓰면 규격 불일치로 비디오 파일이 박살 납니다.
    # 따라서 `cv2.cvtColor(..., cv2.COLOR_GRAY2BGR)`를 거쳐 속 알맹이는 흑백 선 형태지만, 외형 포맷만 3채널(컬러 구조)로 껍데기를 위장시켜서 비디오에 누적 저장해야 합니다.
    writer.write(cv2.cvtColor(frame_edge, cv2.COLOR_GRAY2BGR))
    count += 1

# 다 사용한 원본 비디오 장치와 저장용 비디오 장치를 안전하게 닫아 메모리를 OS에 반환합니다. (열었으면 반드시 닫아야 파일이 저장됩니다)
cap.release()
writer.release()


# =========================================================================
# PART 3: 분석된 통계 리포트를 표준 CSV(엑셀) 파일로 내보내기
# =========================================================================
# - "p07_summary.csv": 저장할 파일 이름
# - encoding="utf-8-sig": 한글 깨짐을 방지하기 위해 마이크로소프트 엑셀 호환용 특수 코드로 인코딩 설정
# - newline="": 행과 행 사이에 불필요한 빈 줄(공백 라인)이 추가되는 것을 차단
with open("p07_summary.csv", "w", encoding="utf-8-sig", newline="") as f:
    output = csv.writer(f)
    output.writerow(["source", "source_w", "source_h", "output_w", "output_h", "edge_pixels"]) # 엑셀 가장 첫 줄에 컬럼 이름(헤더) 작성
    output.writerows(rows) # 위에서 append로 모아두었던 순수 데이터 행들을 밑으로 통째로 다 부어 넣습니다.


# =========================================================================
# PART 4: 최종 저장물들이 사기 치지 않고 진짜 잘 만들어졌는지 재점검 검증
# =========================================================================
check = cv2.VideoCapture("p07_video.avi") # 우리가 방금 만들어낸 결과물 동영상을 실험용으로 다시 강제 로드해 봅니다.
print("이미지 수/Frame 수:", len(rows), count) # 처리한 이미지 개수(3개)와 비디오 총 프레임 수 출력
print("재읽기 이미지 Shape:", cv2.imread("p07_scene_edge.png", 0).shape) # 저장된 에지 이미지 중 1개를 골라 크기 점검
print("재읽기 영상 Frame/FPS:", int(check.get(cv2.CAP_PROP_FRAME_COUNT)), check.get(cv2.CAP_PROP_FPS)) # 저장된 비디오가 먹통이 아니라 프레임이 제대로 채워졌는지 최종 검증 출력
check.release()

print("결과: p07_ PNG 9개 + AVI 1개 + CSV 1개")

""" 출력 결과 값
Writer: True
이미지 수/Frame 수: 3 48
재읽기 이미지 Shape: (120, 160)
재읽기 영상 Frame/FPS: 48 12.0
결과: p07_ PNG 9개 + AVI 1개 + CSV 1개  """