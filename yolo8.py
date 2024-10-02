from ultralytics import YOLO

# 모델 불러오기 (YOLOv8n: 가장 작은 모델, YOLOv8s: 작은 모델, YOLOv8m: 중간 모델, YOLOv8l: 큰 모델, YOLOv8x: 가장 큰 모델)
model = YOLO('yolov8n.pt')

# 이미지에 대한 객체 감지 수행
results = model('C:/Users/USER/Desktop/사진/증사.jpg')

# 결과 시각화
for result in results:
    result.show()

