import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# jb_df_original = pd.read_csv("./data.csv", encoding="cp949")

def RCS(jb_df_original):
    # Min-Max 정규화
    scaler = MinMaxScaler()
    df_no_category = jb_df_original.drop('category', axis=1)
    df_no_category_normalized = pd.DataFrame(scaler.fit_transform(df_no_category), columns=df_no_category.columns)

    # NearestNeighbors 모델 생성 및 훈련
    nearest_neighbors = NearestNeighbors(n_neighbors=1001, n_jobs=16)  
    nearest_neighbors.fit(df_no_category_normalized)

    # 여러 rare classes에 대한 처리
    rare_classes = [1, 5, 13, 17]  # 원하는 rare classes 리스트
    final_df = jb_df_original.copy()

    def process_data(combined_data_df):
    # 대부분의 열에서 가장 많이 나타난 값 또는 랜덤 샘플링
        mode_or_random_columns = ['time', 'area', 'gender', 'age', 'married', 'alien', 'main']
        new_data = {}

        for col in mode_or_random_columns:
            mode_values = combined_data_df[col].mode()
            if len(mode_values) > 1:
                # 여러 최빈값이 있는 경우, 랜덤하게 하나 선택
                new_data[col] = np.random.choice(mode_values)
            else:
                new_data[col] = mode_values[0]

        # 나머지 열의 평균값 계산
        mean_columns = ['child', 'amount', 'count', 'temp', 'feels_like', 'rain_1h', 'snow_1h', 'category']
        for col in mean_columns:
            new_data[col] = combined_data_df[col].mean()

        # 'count' 열은 반올림
        new_data['count'] = round(new_data['count'])
        new_data['amount'] = round(new_data['amount'])

        # 'temp'와 'feels_like' 열은 소수 둘째자리 미만을 버림
        new_data['temp'] = np.floor(new_data['temp'] * 100) / 100
        new_data['feels_like'] = np.floor(new_data['feels_like'] * 100) / 100


        new_data['category'] = rare_class
        new_data_df = pd.DataFrame([new_data])
        new_data_df
        return new_data

    for rare_class in rare_classes:
        # rare_class에 해당하는 데이터 추출
        df_rare_class = jb_df_original[jb_df_original['category'] == rare_class]

        for index, row in df_rare_class.iterrows():
            selected_data = row.drop('category')
            selected_data_normalized = scaler.transform([selected_data.values])

            # 가장 가까운 이웃 찾기
            distances, indices = nearest_neighbors.kneighbors(selected_data_normalized)
            if(rare_class == 1 or rare_class==5 or rare_class==8):
            # 가장 가까운 k개의 데이터 찾기 및 처리 (k=100부터 1000까지 25씩 증가)
                for k in range(100, 1001, 25):
                    closest_indices = indices[0][1:k+1]  # 자기 자신을 제외
                    closest_data_normalized = df_no_category_normalized.iloc[closest_indices]

                    # 정규화 해제 및 데이터 프레임 변환
                    closest_data_restored = scaler.inverse_transform(closest_data_normalized)
                    closest_data_df = pd.DataFrame(closest_data_restored, columns=df_no_category.columns)
                    closest_data_df['category'] = jb_df_original['category'].iloc[closest_indices].values

                    # 데이터 처리 및 final_df에 추가
                    new_data = process_data(closest_data_df)
                    new_data_df = pd.DataFrame([new_data])
                    final_df = final_df.append(new_data_df, ignore_index=True)

            else:
            # 가장 가까운 k개의 데이터 찾기 및 처리 (k=100부터 1000까지 100씩 증가)
                for k in range(100, 1001, 100):
                    closest_indices = indices[0][1:k+1]  # 자기 자신을 제외
                    closest_data_normalized = df_no_category_normalized.iloc[closest_indices]

                    # 정규화 해제 및 데이터 프레임 변환
                    closest_data_restored = scaler.inverse_transform(closest_data_normalized)
                    closest_data_df = pd.DataFrame(closest_data_restored, columns=df_no_category.columns)
                    closest_data_df['category'] = jb_df_original['category'].iloc[closest_indices].values

                    # 데이터 처리 및 final_df에 추가
                    new_data = process_data(closest_data_df)
                    new_data_df = pd.DataFrame([new_data])
                    final_df = final_df.append(new_data_df, ignore_index=True)     

    return final_df    


