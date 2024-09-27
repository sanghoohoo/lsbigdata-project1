import streamlit as st
from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np

# YOLOv8 모델 불러오기
model = YOLO('yolov8n.pt')

# Streamlit 타이틀
st.title("YOLOv8 Object Detection")

# 이미지 업로드
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# 이미지가 업로드되면 처리
if uploaded_file is not None:
    # PIL 이미지를 열기
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # 이미지를 numpy 배열로 변환
    image_np = np.array(image)

    # YOLOv8을 사용하여 객체 감지 수행
    results = model(image_np)

    # 감지된 객체가 있는 이미지 표시
    for result in results:
        result_img = result.plot()  # 결과 이미지를 가져오기

        # 결과 이미지를 화면에 출력
        st.image(result_img, caption='Detected Objects', use_column_width=True)