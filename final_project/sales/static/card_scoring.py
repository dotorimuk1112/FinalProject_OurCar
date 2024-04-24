from common.models import scoring
import pandas as pd
import pickle
import numpy as np
import toad

def load_record(user_id):
    try:
        current_user_record = scoring.objects.get(id=user_id)
        data = [{
            'verification_status' : current_user_record.verification_status,
            'home_ownership' : current_user_record.home_ownership,
            'loan_amnt' : current_user_record.loan_amnt,
            'int_rate' : current_user_record.int_rate,
            'term' : current_user_record.term,
            'purpose' : current_user_record.purpose,
            'annual_inc' : current_user_record.annual_inc,
            'dti' : current_user_record.dti,
            'avg_cur_bal' : current_user_record.avg_cur_bal,
            'acc_open_past_24mths' : current_user_record.acc_open_past_24mths,
            'total_bc_limit' : current_user_record.total_bc_limit,
            'bc_util' : current_user_record.bc_util
        }]

        return data
    
    except scoring.DoesNotExist:
        current_user_record = None

def scoring_data(user_id):    
    with open('credit_scorecard_final.pkl', 'rb') as f:
        scorecard = pickle.load(f) 
    
    try:
        data = load_record(user_id=user_id)
        data_df = pd.DataFrame.from_dict(data)
        result_score = int(round(float(scorecard.predict(data_df))))
        return result_score
    
    except scoring.DoesNotExist:
        error_message = "신용 기록을 불러올 수 없습니다."
        return error_message