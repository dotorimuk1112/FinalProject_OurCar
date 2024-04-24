from PIL import Image
from ultralytics import YOLO
import io

# 1. 차인지 아닌지 판단하는
car_determination_model = YOLO('yolov8s.pt')

# 2. 차량 파손 탐지
damage_detection_model = YOLO('best.pt')

def car_determination_and_damage_detection(img):
    if img:
        file_name = img.name
        image_data = img.read()
        processed_img = Image.open(io.BytesIO(image_data))
        try:
            results1 = car_determination_model(processed_img)
            results2 = damage_detection_model(processed_img)
            print("results2:", results2)
            if results1 and results2:  # 처리된 결과가 있을 경우
                for r in results1:
                    determination_result = str(int(r.boxes.cls[0])) # 탐지 결과 None이면 여기서 에러 발생
                
                try:
                    for dr in results2:
                        detection_class = str(int(dr.boxes.cls[0]))
                except Exception as e:
                    print("results2가 Nonetype입니다.")
                    detection_class = None

                # 사진 판독 결과가 차량이고, 파손이 감지됐을 경우
                if (determination_result == '2') and detection_class:
                    for r in results2:
                        im_array = r.plot()  # plot a BGR numpy array of predictions
                        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                        # im.show()  # show image
                        im.save(f'_media/detection_results/{file_name}_results.jpg')  # save image
                        detection_results = f'detection_results/{file_name}_results.jpg'
                else:
                    detection_results = None
                    return determination_result, detection_results

                return determination_result, detection_results
            else:
                return None, None  # 처리된 결과가 없을 경우 None 반환
        # 아무것도 탐지 안됐을 때 에러 처리
        except Exception as e:
            print('에러 발생', e)
            # 전체 이미지 경로를 반환
            return None, None
    else:
        return None, None