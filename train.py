from pycaret.classification import *
import pandas as pd
from sklearn.model_selection import train_test_split
from RCS import RCS

data = pd.read_csv('./data.csv', encoding="cp949")
data = RCS(data)

X = data.drop('category', axis=1)
y = data['category']
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
train_data = pd.concat([train_X, train_y], axis=1)

def custom_accuracy(y_true, y_pred_top_3):
    correct = 0
    for true, pred in zip(y_true, y_pred_top_3.itertuples(index=False, name=None)):
        if true in pred:
            correct += 1
    return correct / len(y_true)


clf1 = setup(data=train_data, target='category', fold=5, n_jobs=16)

# 사용할 모델 리스트
models = ['catboost']

for model_name in models:
    # 모델 생성 및 학습
    model = create_model(model_name)
    
    predictions = predict_model(model, data=test_X, raw_score=True)
    
    score_columns = [f'prediction_score_{i}' for i in range(20)]  # 20개의 클래스에 대한 열 이름
    top_3_predictions = predictions[score_columns].apply(lambda x: x.argsort()[-3:][::-1], axis=1)

    # 정확도 계산
    accuracy = custom_accuracy(test_y, top_3_predictions)
    print("accuracy: {:.4f}".format(accuracy))
    # 모델 저장
    save_model(model, f'./weights/{model_name}')

