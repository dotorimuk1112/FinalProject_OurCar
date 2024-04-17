from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import numpy as np
from ultralytics import YOLO
import io
import os
from django.contrib import messages

model = YOLO('yolov8s.pt')

def car_determination(img):
    if img:
        image_data = img.read()
        processed_img = Image.open(io.BytesIO(image_data))
        try:
            results = model(processed_img)
            if results:  # 처리된 결과가 있을 경우
                for r in results:
                    determination_result = str(int(r.boxes.cls[0])) # 여기서 에러 발생

                return determination_result
            else:
                return None  # 처리된 결과가 없을 경우 None 반환
        except Exception as e:
            determination_result = None

            # 전체 이미지 경로를 반환
            return determination_result
    else:
        pass