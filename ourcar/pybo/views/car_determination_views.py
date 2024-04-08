from django.shortcuts import render
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import UploadedImage2
from PIL import Image
import numpy as np
from ultralytics import YOLO
import io
import os
from config.settings import MEDIA_ROOT, MEDIA_URL
import uuid


# YOLOv8 모델 로드
model = YOLO('yolov8s.pt')

def car_determination(request):
    uploaded_image = None
    processed_image = None
    determination_result = None  # 초기화

    if request.method == "POST":
        image = request.FILES["image"]
        try:
            # 업로드된 이미지의 파일명 가져오기
            uploaded_filename = image.name
            # 이미지를 열고 바이너리 모드로 읽습니다.
            image_data = image.read()
            # 이미지를 PIL Image로 열기
            img = Image.open(io.BytesIO(image_data))
            # 처리된 이미지의 파일명 동적으로 생성
            processed_image_filename = f"processed_{uploaded_filename}"
            # 이미지 처리 함수 호출하여 처리된 이미지의 경로와 판별 결과 가져옴
            processed_image_path, determination_result = process_image(img, processed_image_filename)
            
            # 업로드된 이미지와 처리된 이미지를 저장
            # if processed_image_path:  # 처리된 이미지가 있을 경우에만 저장
            uploaded_image = UploadedImage2.objects.create(uploadedimage=image, processedimage=processed_image_filename)  # 파일명만 저장
            processed_image = f"{MEDIA_URL}{processed_image_filename}"  # 이미지의 URL로 설정

        except Exception as e:
            print(f"Error uploading and processing image: {e}")

    return render(request, "pybo/car_determination.html", {"uploaded_image": uploaded_image, "processed_image": processed_image, "determination_result": determination_result})


def process_image(image, processed_image_filename):
    try:
        # 이미지를 YOLOv8로 처리
        results = model(image)
        if results:  # 처리된 결과가 있을 경우

            for r in results:
                determination_result = str(int(r.boxes.cls[0])) # 여기서 에러 발생

            # Plot results image
            im_bgr = results[0].plot()  # 첫 번째 결과 이미지 선택
            im_rgb = Image.fromarray(im_bgr[..., ::-1])  # BGR-order numpy array를 RGB-order PIL 이미지로 변환

            # 파일시스템에 이미지 저장
            processed_image_path = os.path.join(MEDIA_ROOT, processed_image_filename)
            im_rgb.save(processed_image_path)
            print("♣processed_image_path: ",processed_image_path)
            # 전체 이미지 경로를 반환
            return processed_image_path, determination_result
        else:
            return None  # 처리된 결과가 없을 경우 None 반환
    except Exception as e:
        
        determination_result = None

        im_bgr = results[0].plot()  # 첫 번째 결과 이미지 선택
        im_rgb = Image.fromarray(im_bgr[..., ::-1])  # BGR-order numpy array를 RGB-order PIL 이미지로 변환

        processed_image_path = os.path.join(MEDIA_ROOT, processed_image_filename)
        im_rgb.save(processed_image_path) # 이거 처리
        print("♣processed_image_path: ",processed_image_path)
        # 전체 이미지 경로를 반환
        return processed_image_path, determination_result