from PIL import Image
from ultralytics import YOLO
import io
import boto3
import my_settings  # my_settings 파일은 해당 프로젝트의 설정 파일이어야 합니다.

# S3 클라이언트 생성
s3_client = boto3.client('s3', aws_access_key_id=my_settings.AWS_ACCESS_ID, aws_secret_access_key=my_settings.AWS_SECRET_KEY)

# 모델 로드
car_determination_model = YOLO('ai_models/yolov8s.pt')
damage_detection_model = YOLO('ai_models/car_damage_detection_model.pt')

def car_determination_and_damage_detection(img):
    if img:
        try:
            # 이미지 처리
            file_name = img.name
            image_data = img.read()
            processed_img = Image.open(io.BytesIO(image_data))
            
            # 차량 탐지
            results1 = car_determination_model(processed_img)
            
            # 차량 파손 탐지
            results2 = damage_detection_model(processed_img)
            print("results2:", results2)
            
            # 결과 처리
            determination_list = [str(int(r.boxes.cls[0])) for r in results1] if results1 else None
            detection_class = str(int(results2[0].boxes.cls[0])) if results2 else None

            print('determination_list:', determination_list)
            print('detection_class:', detection_class)
            
            # S3에 이미지 업로드
            if determination_list and detection_class:
                for r in results2:
                    im_array = r.plot()  # plot a BGR numpy array of predictions
                    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                    s3_key = f'detection_results/detec_result_{file_name}'
                    
                    # 이미지 데이터를 메모리에서 직접 업로드
                    with io.BytesIO() as output:
                        im.save(output, format='JPEG')  # 이미지를 BytesIO에 저장
                        output.seek(0)  # BytesIO 포인터를 시작으로 되돌림
                        s3_client.upload_fileobj(output, 'ourcar-bucket', s3_key)  # S3에 업로드
                    
                    detection_results = f'detection_results/detec_result_{file_name}'
            else:
                detection_results = None
                
            return determination_list, detection_results
        
        except Exception as e:
            print('에러 발생', e)
            return None, None
            
    else:
        return None, None
