import joblib
import numpy as np
import functions

# 모델 input 전처리
def get_model_input(FIRSTDAY, REPAIRDAY, COMPANY, PART, METHOD) : 
    ohe_company = joblib.load('./preprocessing/ohe_COMPANY.save') 
    ohe_repairmethod = joblib.load('./preprocessing/ohe_REPAIRMETHOD.save') 
    ohe_repairpart = joblib.load('./preprocessing/ohe_REPAIRPART.save') 
    # categorical feature 전처리
    PART = functions.get_parts(PART)
    METHOD = functions.get_severity(METHOD)
    COMPANY = functions.get_company(COMPANY)
    # 만약 교체일 경우 차 부품 비용 추가
    replace_price = 0
    if METHOD == "교환" :
        if PART == "Bonnet" :
            replace_price = 300000
        elif PART == "FrontWheel" :
            replace_price = 150000
        elif PART == "Frontbumper" :
            replace_price = 150000
        elif PART == "Frontdoor" :
            replace_price = 450000
        elif PART == "Frontfender" :
            replace_price = 300000
        elif PART == "Rearbumper" :
            replace_price = 500000
        elif PART == "Reardoor" :
            replace_price = 450000
        elif PART == "Rearfender" :
            replace_price = 300000
        elif PART == "Sidemirror" :
            replace_price = 150000
        elif PART == "Trunklid" :
            replace_price = 650000
        elif PART == "Headlights" :
            replace_price = 15000
        else :
            replace_price = 0

    HQ = get_mean_HQ(METHOD)
    COMPANY = ohe_company.transform([[COMPANY]])[0]
    PART = ohe_repairpart.transform([[PART]])[0]
    METHOD = ohe_repairmethod.transform([[METHOD]])[0]
    MinmaxScaler = joblib.load('./preprocessing/scaler.save') 
    # integer feature 전처리
    scaledData = MinmaxScaler.transform([[FIRSTDAY, REPAIRDAY, HQ]])
    modelinput = np.r_[scaledData[0], COMPANY, PART,METHOD]
    
    return modelinput,replace_price

def get_mean_HQ(method) :
    if method == "오버홀" :
        return 1.87
    elif method == "교환" : # 도장 HQ 중간 값으로 설정함 부품 가격 반영해야함
        return 1.95
    elif method == "탈착" :
        return 2.27
    else :
        return 2.58

### GradientBoosting Model ###
# Traindata : [240000 rows x 24 columns]
# Train data Accuracy :  0.9774661302004374
# Test data Accuracy :  0.9728243928165342
# 정답, 예측값 평균 오차 :  5615.994414286496원

### 사용법 ###
# 1. get_model_input 함수에 인자로 firstday, repairday, company, repairpart, repairmethod 넘겨주면 modelinput,replace_price 리턴 받음
# 2. replace_price += GradientBoostingModel.predict([modelinput])[0] 이 코드를 작동 시키면 replace_price가 최종 예측 가격

GradientBoostingModel = joblib.load('./model/GradientBoostingRegressor.pkl')

### BMW 5시리즈 55440원
modelinput,replace_price = get_model_input(20141119,20180512,"BMW",'뒤범퍼(단독작업)','탈착')
replace_price += GradientBoostingModel.predict([modelinput])[0]

print("정답 값 : ",'55440원')
print("GradientBoostingModel 예측값 : ",replace_price)

### 벤츠 G350 350000원
modelinput2,replace_price = get_model_input(20170601,20180425,"벤츠",'본네트(보수)','도장')
replace_price += GradientBoostingModel.predict([modelinput2])[0]

print("정답 값 : ",'350000원')
print("GradientBoostingModel 예측값 : ",replace_price)