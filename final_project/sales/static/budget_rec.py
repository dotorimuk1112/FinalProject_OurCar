from common.models import TestSangmin
import pickle
import pandas as pd
import numpy as np

with open('budget_recommend_models.pkl', 'rb') as f:
    budget_rec_model = pickle.load(f)

def budget_rec_func(user_id):
    try:
        test_sangmin_instance = TestSangmin.objects.get(id=user_id)
        data = {
            'INTERIOR_AM': [int(test_sangmin_instance.interior_am)],
            'INSUHOS_AM': [int(test_sangmin_instance.insuhos_am)],
            'OFFEDU_AM': [int(test_sangmin_instance.offedu_am)],
            'TRVLEC_AM': [int(test_sangmin_instance.trvlec_am)],
            'FSBZ_AM': [int(test_sangmin_instance.fsbz_am)],
            'SVCARC_AM': [int(test_sangmin_instance.svcarc_am)],
            'DIST_AM': [int(test_sangmin_instance.dist_am)],
            'PLSANIT_AM': [int(test_sangmin_instance.plsanit_am)],
            'CLOTHGDS_AM': [int(test_sangmin_instance.clothgds_am)]
        }

        data_df = pd.DataFrame(data)
        print(data_df)
        
        if budget_rec_model:
            budget_rec_result = budget_rec_model.predict(data_df)
            budget_rec_result = np.squeeze(budget_rec_result)
            budget_rec_result = int(budget_rec_result)
            min_budget = budget_rec_result - 147
            max_budget = budget_rec_result + 147
            print("예측 결과:", "최소 예산-", min_budget, "|", "최대 예산-", max_budget)
            return min_budget, max_budget, budget_rec_result
        else:
            print("budget_rec_model is None")
            budget_rec_result = None
            
    except TestSangmin.DoesNotExist:
        test_sangmin_instance = None
        print('데이터가 존재하지 않습니다.')