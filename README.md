# Thimble

## 프로젝트 소개

<img src="https://user-images.githubusercontent.com/32920566/147911895-e18f3222-d85b-4191-922d-167c60f0ad0f.png" width="900">

<br>

> 사진, gif, 비디오 파일에서 지문 정보가 노출되는 경우 해당 위치를 블러 처리하는 서비스입니다.


## 방법

1. 왼손과 오른손을 구분합니다.

2. 손 skeleton 구조를 파악한 것을 토대로 다각도에서 들어오는 뼈대 좌표를 토대로 손의 방향을 판단합니다.

3. 이를 토대로 손바닥과 손등을 구분합니다.

4. 손바닥일 경우 skeleton을 토대로 지문 영역을 구합니다.

5. 손가락이 접혀있는지 판단하여 지문이 보인다고 판단되는 경우 블러 처리를 적용합니다.

## 😱 issue

- 사진과 영상 속에서 손을 `detection,tracking` 하기 까지는 문제가 없었습니다.

- 지문을 지우는 방식 : 손의 skeleton 구조를 파악하여 손끝과 다음 마디를 타원형으로 블러 처리해주는 방식을 고안했습니다.

- 하지만, 이런 방식은 손등이 보이는 경우(손톱이 화면에 노출되는 경우)에 대해서도 블러를 처리하기 때문에 원하지 않는 블러가 처리될 수 밖에 없는 로직입니다.

- 손등과 손바닥을 탐지하기 위한 방법을 고안했습니다.

## Demo

- `thimble.py` 을 실행하면 바로 확인하실 수 있습니다.

## 사용 예시

<img src="https://user-images.githubusercontent.com/32920566/147912402-12e7e124-46be-451d-91b4-a7ee7993e3bd.png" width="900">

<br>

<img src="https://user-images.githubusercontent.com/32920566/147912451-797812bf-fcdb-4113-92cb-ee329c66eae9.png" width="900">

<br>
<br>

## 블러 처리 후의 모습

<img src="https://user-images.githubusercontent.com/32920566/147912552-c62f03c8-d2ca-49f5-bf50-9dc164c1fea0.png" width="900">

## 앞으로 해결해야할 사항 

- ~~get_label 함수 리팩토링~~

- ~~왼손과 오른손을 판단하는 로직 정확도 높이기~~
  - Mediapipe보다 Cvzone을 사용했을 때 left,right 판단 정확도가 훨씬 
  높고 코드 가독성도 좋음. (2021-10-11)

- ~~손바닥, 손등 구분 로직 정확도 높이기~~
  - 랜드마크 특정 지점을 내적하여 각도를 기준으로 손등, 손바닥 정확도를 높임.(손목, 엄지손가락, 새끼손가락이 이루는 각도)

- input으로 들어오는 확장자를 parsing하여 input에 정확히 맞는 코덱 적용하기 (2022.01.03)
  - Map table을 만들어 맞춤형 코덱 제작 필요

- 추가 사항
  <img src="https://user-images.githubusercontent.com/32920566/147912620-1697ca6c-9f74-474b-b763-277da7c376b7.png">
  
