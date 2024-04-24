from ..models import Car
import pickle
import csv
import pandas as pd

def load_data(car):
    data = {
        'MYEAR': [2024 - car.MYERAR + 1],
        'MILEAGE': [car.MILEAGE],
        'DISP': [car.DISP],         
        'CU_HIS': [car.CU_HIS],
        'MVD_HIS': [car.MVD_HIS],
        'AVD_HIS': [car.AVD_HIS],
        'TL_HIS': [1],
        'FD_HIS': [car.FD_HIS],
        'VT_HIS': [car.VT_HIS],
        'US_HIS': [car.US_HIS],
        'TLHIS' : [1],

        'TRANS_CVT' : [(car.TRANS == 'CVT')],
        'TRANS_SAT' : [(car.TRANS == 'SAT')],
        'TRANS_기타': [(car.TRANS == '기타')],
        'TRANS_수동': [(car.TRANS == '수동')],
        'TRANS_오토' : [(car.TRANS == '오토')],
        'TRANS_자동': [(car.TRANS == '자동')],

        'F_TYPE_0': [(car.F_TYPE == '0')],
        'F_TYPE_CNG': [(car.F_TYPE == 'CNG')],
        'F_TYPE_LPG': [(car.F_TYPE == 'LPG')],
        'F_TYPE_가솔린': [(car.F_TYPE == '가솔린')],
        'F_TYPE_가솔린 하이브리드': [(car.F_TYPE == '가솔린 하이브리드')],
        'F_TYPE_가솔린+LPG': [(car.F_TYPE == '가솔린+LPG')],
        'F_TYPE_가솔린/LPG겸용': [(car.F_TYPE == '가솔린/LPG겸용')],
        'F_TYPE_기타': [(car.F_TYPE == '기타')],
        'F_TYPE_디젤': [(car.F_TYPE == '디젤')],
        'F_TYPE_전기': [(car.F_TYPE == '전기')],
        'F_TYPE_하이브리드': [(car.F_TYPE == '하이브리드')],
        'F_TYPE_하이브리드(LPG)': [(car.F_TYPE == '하이브리드(LPG)')],
        'F_TYPE_하이브리드(가솔린)': [(car.F_TYPE == '하이브리드(가솔린)')],
        'F_TYPE_하이브리드(가솔린/전기)': [(car.F_TYPE == '하이브리드(가솔린/전기)')],
        'F_TYPE_하이브리드(디젤)': [(car.F_TYPE == '하이브리드(디젤)')],
    }
    return data

def car_price_pred_model(car):
    with open('car_price_prediction_models_RF.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    try:
        data = load_data(car=car)
        data_df = pd.DataFrame(data)
        target_model_name = car.L_NAME
        target_model = None

        for model_name, model in loaded_model:
            if model_name == 'model_' + target_model_name:
                target_model = model
                break
        
        if target_model:
            # 예측을 위한 입력 데이터 준비
            # 예를 들어, 입력 데이터는 DataFrame 형태여야 하며, 모델을 훈련할 때와 동일한 특성을 가져야 합니다.
            input_data = data_df

            # 모델을 사용하여 예측 수행
            # predictions = target_model.predict(input_data)
            predicted_price = int(round(float(target_model.predict(input_data)), 1))

            # 딕셔너리로 데이터를 저장할 변수 초기화
            target_model_mae = None

            csv_file_path = 'common/static/car_price_pred_mae.csv'

            print(target_model_name)

            # CSV 파일 열기
            with open(csv_file_path, newline='', encoding='cp949') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # 헤더 스킵
                for row in reader:
                    if row[0] == target_model_name:
                        target_model_mae = row[1]
                        break
                else:
                    print(f"{target_model_name}에 해당하는 값이 없습니다.")
                    target_model_mae = None
            return predicted_price, target_model_mae

        else:
            # 해당 모델을 찾을 수 없는 경우 처리
            predicted_price = "모델을 못 찾았습니다."
            return predicted_price
        
    except Car.DoesNotExist:
        error_message = "해당하는 차량 정보가 없습니다."
        return error_message
    
def car_price_pred_model_10000(car):
    with open('car_price_prediction_models_RF.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    try:
        # 입력된 차량 정보를 기반으로 데이터 구성
        data = load_data(car=car)
        data_df = pd.DataFrame(data)
        prediction_list = []
        target_model_name = car.L_NAME
        target_model = None 


        for model_name, model in loaded_model:
            if model_name == 'model_' + target_model_name:
                target_model = model
                break
        
        csv_file_path = 'common/static/car_price_pred_mae.csv'
        
        with open(csv_file_path, newline='', encoding='cp949') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 헤더 스킵
            for row in reader:
                if row[0] == target_model_name:
                    target_model_mae = row[1]
                    break
            else:
                print(f"{target_model_name}에 해당하는 값이 없습니다.")
                target_model_mae = None

        if target_model:
            print("☆car_price_pred_model_10000 모델 작동")
            input_data = data_df
            init_year = data_df['MYEAR'].iloc[0]
            init_mil = data_df['MILEAGE'].iloc[0]
            mil = []
            year = []
            for i in range(6):
                input_data['MYEAR'] = init_year + i
                input_data['MILEAGE'] = init_mil + (i * 10000)
                year.append(input_data['MYEAR'])
                mil.append(input_data['MILEAGE'])
                # 모델을 사용하여 예측 수행
                # predictions = target_model.predict(input_data)
                print(f"{i}회차 예측 데이터:", input_data['MYEAR'], input_data['MILEAGE'])

                predicted_price = int(round(float(target_model.predict(input_data)), 1))

                if len(prediction_list) > 0 and predicted_price < prediction_list[-1]:
                    prediction_list.append(predicted_price)
                elif len(prediction_list) == 0:
                    prediction_list.append(predicted_price)
                else:
                    prediction_list.append(prediction_list[-1])

            print('mil, year:', mil, year)
                
            print('prediction_list', prediction_list)
            
            return prediction_list, target_model_mae

        else:
            # 해당 모델을 찾을 수 없는 경우 처리
            return prediction_list
        
    except Car.DoesNotExist:
        error_message = "해당하는 차량 정보가 없습니다."
        return error_message

def car_price_pred_model_20000(car):
    with open('car_price_prediction_models_RF.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    try:
        # 입력된 차량 정보를 기반으로 데이터 구성
        data = load_data(car=car)
        prediction_list = []
        data_df = pd.DataFrame(data)
        target_model_name = car.L_NAME
        target_model = None 


        for model_name, model in loaded_model:
            if model_name == 'model_' + target_model_name:
                target_model = model
                break
        
        csv_file_path = 'common/static/car_price_pred_mae.csv'
        
        with open(csv_file_path, newline='', encoding='cp949') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 헤더 스킵
            for row in reader:
                if row[0] == target_model_name:
                    target_model_mae = row[1]
                    break
            else:
                print(f"{target_model_name}에 해당하는 값이 없습니다.")
                target_model_mae = None

        if target_model:
            print("☆car_price_pred_model_10000 모델 작동")
            input_data = data_df
            init_year = data_df['MYEAR'].iloc[0]
            init_mil = data_df['MILEAGE'].iloc[0]
            mil = []
            year = []
            for i in range(6):
                input_data['MYEAR'] = init_year + i
                input_data['MILEAGE'] = init_mil + (i * 20000)
                year.append(input_data['MYEAR'])
                mil.append(input_data['MILEAGE'])
                # 모델을 사용하여 예측 수행
                # predictions = target_model.predict(input_data)
                print(f"{i}회차 예측 데이터:", input_data['MYEAR'], input_data['MILEAGE'])

                predicted_price = int(round(float(target_model.predict(input_data)), 1))

                if len(prediction_list) > 0 and predicted_price < prediction_list[-1]:
                    prediction_list.append(predicted_price)
                elif len(prediction_list) == 0:
                    prediction_list.append(predicted_price)
                else:
                    prediction_list.append(prediction_list[-1])

            print('mil, year:', mil, year)
                
            print('prediction_list', prediction_list)
            
            return prediction_list, target_model_mae

        else:
            # 해당 모델을 찾을 수 없는 경우 처리
            return prediction_list
        
    except Car.DoesNotExist:
        error_message = "해당하는 차량 정보가 없습니다."
        return error_message

def car_price_pred_model_30000(car):
    with open('car_price_prediction_models_RF.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    try:
        data = load_data(car=car)
        prediction_list = []
        data_df = pd.DataFrame(data)
        target_model_name = car.L_NAME
        target_model = None 


        for model_name, model in loaded_model:
            if model_name == 'model_' + target_model_name:
                target_model = model
                break
        
        csv_file_path = 'common/static/car_price_pred_mae.csv'
        
        with open(csv_file_path, newline='', encoding='cp949') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 헤더 스킵
            for row in reader:
                if row[0] == target_model_name:
                    target_model_mae = row[1]
                    break
            else:
                print(f"{target_model_name}에 해당하는 값이 없습니다.")
                target_model_mae = None

        if target_model:
            print("☆car_price_pred_model_10000 모델 작동")
            input_data = data_df
            init_year = data_df['MYEAR'].iloc[0]
            init_mil = data_df['MILEAGE'].iloc[0]
            mil = []
            year = []
            for i in range(6):
                input_data['MYEAR'] = init_year + i
                input_data['MILEAGE'] = init_mil + (i * 30000)
                year.append(input_data['MYEAR'])
                mil.append(input_data['MILEAGE'])
                # 모델을 사용하여 예측 수행
                # predictions = target_model.predict(input_data)
                print(f"{i}회차 예측 데이터:", input_data['MYEAR'], input_data['MILEAGE'])

                predicted_price = int(round(float(target_model.predict(input_data)), 1))

                if len(prediction_list) > 0 and predicted_price < prediction_list[-1]:
                    prediction_list.append(predicted_price)
                elif len(prediction_list) == 0:
                    prediction_list.append(predicted_price)
                else:
                    prediction_list.append(prediction_list[-1])

            print('mil, year:', mil, year)
                
            print('prediction_list', prediction_list)
            
            return prediction_list, target_model_mae

        else:
            # 해당 모델을 찾을 수 없는 경우 처리
            return prediction_list
        
    except Car.DoesNotExist:
        error_message = "해당하는 차량 정보가 없습니다."
        return error_message
