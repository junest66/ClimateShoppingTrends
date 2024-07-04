<h1> 인공지능 기반 업종 추천 서비스 '이거 어때요' </h1>

<img src="https://img.shields.io/badge/Python-3776AB?style=square&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Flask-white?style=square&logo=Flask&logoColor=black"/>&nbsp;<img src = "https://img.shields.io/badge/HTML5-E34F26?style=square&logo=HTML5&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/CSS3-1572B6?style=square&logo=CSS3&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Javascript-F7DF1E?style=square&logo=Javascript&logoColor=black"/> 
</p>

<img  width="800" src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/948b3169-e468-4318-be1c-e4039b79146e">


<br>

> 이거 어때요?는 날씨 기반 추천 업종을 제공합니다. 인공지능 모델의 학습된 정보를 바탕으로 입력한 사용자 정보에 가장 최적화된 업종을 제공합니다.

<br>

## ⌘ Project BackGround

### 기획 의도 및 기대효과 

<img width="1407" alt="Screenshot 2023-07-31 at 11 36 29 AM" src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/46f5a619-c8de-4250-a617-d6866138423e">

<br>

* **`배경`** : 디지털 결제 시장의 확장과 데이터 분석의 진보가 소비자의 개인화된 서비스 요구를 증폭시키고 있습니다. 이에 대응하여, 기존의 서비스들은 주로 결제 이력에 기반한 추천을 제공하지만, 복잡해지는 소비자의 생활 패턴과 다양한 특성을 반영할 필요성을 느꼈습니다.

* **`목표`**: 카드결제 데이터와 날씨 데이터를 기반으로 사용자 맞춤형 카드 혜택을 추천해주는 인공지능 모델 개발하고 더 나아가 카드 혜택을 누릴 수 있는 가맹점까지 추천을 제공하며 이를 웹서비스로 확장하는게 목표입니다.

<br>

### '이거 어때요?' 의 차별점

- 기존 서비스들은 주로 사용자의 소비 패턴만을 분석하여 해당하는 카드와 혜택을 제안하거나, 사용자가 직접 원하는 혜택을 찾아야 하는데, 이로 인해 다양하고 자동화된 추천이 어려웠습니다. 반면, '이거 어때요'는 금융데이터 뿐만 아니라 사용자의 복합적인 요인, 현재 시간, 현재 위치, 그리고 날씨 정보를 인공지능을 활용하여 철저하게 분석하여, 고객들이 다양한 카드 혜택과 가맹점을 자동으로 누릴 수 있는 추천 서비스를 제공합니다. 이는 우리 서비스의 차별점 중 하나입니다.

<br>

## ⚙️ Use Case
![예시-케이스](https://github.com/junest66/ClimateShoppingTrends/assets/101254480/d7449ede-0e06-4707-8324-1ccce6a20b4c)

>1. http://127.0.0.1:5000 에 접속합니다
>2. 본인의 정보를 입력합니다. 선호도, 분위기 선호도, 자차 유무는 음식관련 추천에 적용되는 항목입니다.
>3. AI 모델이 사용자 입력 정보를 분석하여 관련 업종을 3가지 추천해줍니다.
>4. 1순위 ~ 3순위에 해당하는 업종에 대해서 자세히 보기를 클릭하면 해당 업종과 관련된 장소 및 카드혜택을 제공합니다.

<br>

### 👨🏼‍💻 Members
이승한|최준|편지승|채나정|
:-:|:-:|:-:|:-:|
<img src="https://avatars.githubusercontent.com/u/127590055?v=4" height=130 width=130></img>|<img src="https://avatars.githubusercontent.com/u/121853214?v=4" height=130 width=130></img>|<img src="https://avatars.githubusercontent.com/u/101254480?v=4" height=130 width=130></img>|<img src="https://avatars.githubusercontent.com/u/97399807?v=4" height=130 width=130></img>|
<a href="https://github.com/juajua56" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a>|<a href="https://github.com/junest66" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a>|<a href="https://github.com/vuswltmd" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a>|<a href="https://github.com/iltdm" target="_blank"><img src="https://img.shields.io/badge/GitHub-black.svg?&style=round&logo=github"/></a>|
<a href="mailto:juajua56@gmail.com" target="_blank"><img src="https://img.shields.io/badge/Gmail-EA4335?style&logo=Gmail&logoColor=white"/></a>|<a href="mailto:chlwndks33@naver.com" target="_blank"><img src="https://img.shields.io/badge/Gmail-EA4335?style&logo=Gmail&logoColor=white"/></a>|<a href="mailto:pyun2007@naver.com" target="_blank"><img src="https://img.shields.io/badge/Gmail-EA4335?style&logo=Gmail&logoColor=white"/></a>|<a href="mailto:coskwjd1356@gmail.com" target="_blank"><img src="https://img.shields.io/badge/Gmail-EA4335?style&logo=Gmail&logoColor=white"/></a>|

### 👨🏼‍💻 역할 분담
![구현업무](https://github.com/junest66/ClimateShoppingTrends/assets/121853214/2444cb71-cf21-4faf-aef5-445fb059749e)

## 💿 Data
### 1️⃣ 데이터 수집
#### 1. 금융데이터
![금융데이터](https://github.com/junest66/ClimateShoppingTrends/assets/121853214/541e27c6-f901-4f53-baec-64138d4e6ed3)
#### 2. 비금융데이터 
![비금융데이터](https://github.com/junest66/ClimateShoppingTrends/assets/121853214/9ecc6a64-a069-467c-8d62-170f760620b6)

<hr>

### 2️⃣ EDA 및 데이터 전처리
<img src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/6a3b39a6-ef81-4984-b012-e14a50f72d8a" alt="결제데이터 전처리" width="940">
<br><br>
<img src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/ee6cc9a4-0fd7-465e-9c36-539456a31fe7" alt="날씨데이터 전처리" width="940">
<br><br>
<img src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/7427c6b4-63eb-4d6b-949a-456215df2129" alt="카테고리빈도수" width="940">

### RCS
<img src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/2a928c91-c2e3-464d-a649-84c7da04f848" alt="Rare Class Sampling" width="940">
<img src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/d19b12a4-963c-43e1-ab30-05c62a4ed356" alt="RCS벡터" width="940">

### RCS 성능 비교
<img src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/e1709869-5c38-41bc-a8d0-4c000966495b" alt="RCS 성능 비교 1">
<img src="https://github.com/junest66/ClimateShoppingTrends/assets/121853214/66cc112a-5ffb-4b92-8f21-3f7684fc8ad8" alt="RCS 성능 비교 2">
<hr>

### 3️⃣ 결합된 최종 데이터
![최종데이터](https://github.com/junest66/ClimateShoppingTrends/assets/121853214/3cb9b9e1-048d-48a1-945a-fa4c1b33f40c)


## 📊 Model
### 1️⃣ 실험결과
![실험결과](https://github.com/junest66/ClimateShoppingTrends/assets/121853214/723ae2b4-2d9b-461b-9681-ac557bb8133e)
### 2️⃣ 최종 모델 및 파이프라인
![파이프라인](https://github.com/junest66/ClimateShoppingTrends/assets/121853214/a81eb350-66d9-4c46-bcb2-1b7f2378bb54)


## 📚 Further Information
### 1️⃣ 개발 스택 및 개발 환경
![기술스택](https://github.com/junest66/ClimateShoppingTrends/assets/121853214/2414c5b7-ad06-4d10-b8c7-f2b72e6049b6)

### 2️⃣ Usage
### 1. 라이브러리 설치
---
`requirements.txt` 파일을 다운로드합니다:  
[requirements.txt](https://github.com/junest66/ClimateShoppingTrends/files/13695645/requirements.txt)

다운로드한 파일에는 다음과 같은 라이브러리들이 포함되어 있습니다:
- pycaret==3.2.0
- pandas==1.5.3
- numpy==1.25.2
- selenium==4.16.0
- flask==3.0.0
- python-dotenv==1.0.0
- chromedriver-autoinstaller==0.6.3
- Flask-Session==0.5.0
- markupsafe==2.1.3
- catboost==1.2.2

아래 명령어를 사용하여 이 파일에 명시된 라이브러리들을 설치합니다.

```bash
pip install -r requirements.txt
```
### 2. 환경 설정
<hr>
<br>

프로젝트 실행을 위해 먼저 `.env` 파일을 생성하고 아래의 두 가지 키를 설정합니다:

1. `OPENWEATHER_API_KEY`: [OpenWeatherMap](https://openweathermap.org/current)에서 API 키를 발급받아 입력합니다.
2. `FLASK_SECRET_KEY`: Flask 세션 관리를 위해 사용자가 직접 생성한 시크릿 키를 입력합니다.

```python
OPENWEATHER_API_KEY='여기에_OpenWeather_API_키를_입력하세요'
FLASK_SECRET_KEY='여기에_생성한_Flask_시크릿_키를_입력하세요'
```
### 3. 실행 방법
---
`form_processor.py` 파일을 실행하고 다음 단계에 따라 진행하세요:
1. 웹 브라우저에서 `http://127.0.0.1:5000`로 접속합니다.
2. 본인의 정보를 입력합니다. 선호도, 분위기 선호도, 자차 유무는 음식관련 추천에 사용합니다.
3. AI 모델이 입력 정보를 분석해 관련 업종 3가지를 추천합니다.
4. 추천된 업종에 대해 자세히 보기를 클릭하면 해당 업종과 관련된 장소 및 카드 혜택 정보를 볼 수 있습니다.

#### ❗️ 주의사항
- 음식 관련 가맹점 추천은 사용자의 추가 정보로 필터를 적용하여 실시간 웹 크롤링을 통해 제공됩니다. 이후 네이버 웹사이트의 업데이트로 인해 코드의 수정이 필요할 수도 있습니다.
- 다른 업종 가맹점 추천은 미리 수집된 데이터를 사용합니다. 데이터는 항상 최신 상태를 반영하지 않을 수 있으므로, 최신 정보를 확인하는 것이 좋습니다.

