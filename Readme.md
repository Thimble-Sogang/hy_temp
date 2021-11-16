# Thimble
---
## handside 판단 

### 😱 issue
- 사진과 영상 속에서 손을 `detection,tracking` 하기 까지는 문제가 없었습니다.
- 지문을 지우는 방식 : 손의 skeleton 구조를 파악하여 손끝과 다음 마디를 타원형으로 블러 처리해주는 방식을 고안했습니다.
- 하지만, 이런 방식은 손등이 보이는 경우(손톱이 화면에 노출되는 경우)에 대해서도 블러를 처리하기 때문에 원하지 않는 블러가 처리될 수 밖에 없는 로직입니다.
- 손등과 손바닥을 탐지하기 위한 방법을 고안했습니다.

### ✋ 방법
1. 왼손과 오른손을 구분합니다.
2. 손 skeleton 구조를 파악한 것을 토대로 다각도에서 들어오는 뼈대 좌표를 토대로 손의 방향을 판단합니다.
3. 이를 토대로 손바닥과 손등을 구분했습니다.


### 🤔 앞으로 해결해야할 사항 
- get_label 함수 리팩토링
- 왼손과 오른손을 판단하는 로직 정확도 높이기
  - ~~Mediapipe보다 Cvzone을 사용했을 때 left,right 판단 정확도가 훨씬 높고 코드 가독성도 좋음. (2021-10-11)~~
- Hand Skeleton Landmark의 x,y좌표 차를 이용하여 손바닥과 손등을 구분하는 방식을 사용하고 있음
  - ~~현재(2021.10.22) 5,9번의 랜드마크를 사용하고 있고 손이 완전한 좌우를 바라보는 경우에 대해서 잘못된 판단을 하고 있음.~~
  - ~~또한, 주먹을 쥔 상태인 경우에는 절반 이상의 경우로 제대로된 판단을 하고 있지 못함.~~
- 손날이 비춰지는 경우에 대해 정확도가 낮음 (2021-11-16)
- 
### 작업
- Cvzone으로 왼손 오른손 구분 정확도 향상 완료
- 새끼와 검지 손가락 정보를 이용해 벡터 내적으로 손의 오므림 유무 판단 예정 -> Code 준비 완료
- 
