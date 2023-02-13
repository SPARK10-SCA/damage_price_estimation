import joblib
import numpy as np
import functions

# 모델 input 전처리
def get_model_input(FIRSTDAY, REPAIRDAY, HQ, COMPANY, PART, METHOD) : 
    ohe_company = joblib.load('./preprocessing/ohe_COMPANY.save') 
    ohe_repairmethod = joblib.load('./preprocessing/ohe_REPAIRMETHOD.save') 
    ohe_repairpart = joblib.load('./preprocessing/ohe_REPAIRPART.save') 
    # categorical feature 전처리
    PART = functions.get_parts(PART)
    METHOD = functions.get_severity(METHOD)
    COMPANY = functions.get_company(COMPANY)
    COMPANY = ohe_company.transform([[COMPANY]])[0]
    PART = ohe_repairpart.transform([[PART]])[0]
    METHOD = ohe_repairmethod.transform([[METHOD]])[0]
    MinmaxScaler = joblib.load('./preprocessing/scaler.save') 
    # integer feature 전처리
    scaledData = MinmaxScaler.transform([[FIRSTDAY, REPAIRDAY, HQ]])
    modelinput = np.r_[scaledData[0], COMPANY, PART,METHOD]
    return modelinput

### GradientBoosting Model ###
# Traindata : [240000 rows x 24 columns]
# Train data Accuracy :  0.9774661302004374
# Test data Accuracy :  0.9728243928165342
# 정답, 예측값 평균 오차 :  5615.994414286496원
GradientBoostingModel = joblib.load('./model/GradientBoostingRegressor.pkl')

### BMW 5시리즈 55440원
modelinput = get_model_input(20141119,20180512,1.68,"BMW",'뒤범퍼(단독작업)','탈착')

### 벤츠 G350 350000원
modelinput2 = get_model_input(20170601,20180425,100.0,"벤츠",'본네트(보수)','도장')


print("정답 값 : ",'55440원')
print("GradientBoostingModel 예측값 : ",GradientBoostingModel.predict([modelinput])[0])


print("정답 값 : ",'350000원')
print("GradientBoostingModel 예측값 : ",GradientBoostingModel.predict([modelinput2])[0])


