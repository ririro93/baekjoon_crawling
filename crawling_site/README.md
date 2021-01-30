# 백준 크롤링

## Todos
- [x] model design
- [ ] front-end design (3d look)
- [ ] 크롤링한 데이터 db에 자동 저장
    - [x] 저장
    - [ ] 날짜 데이터, 티어 데이터 사이트 데이터 추가로 필요
- [ ] 벌금 페이지 만들기
- [ ] 그래프, 차트 등 사용해서 푼 문제 수 표시하기
- [ ] 자동으로 몇 시간에 한번씩 자동으로 업데이트 되게 하기
- [x] refresh 버튼으로 수동 업데이트 가능하게 하기
- [ ] 크롤링 결과를 딕셔너리 형태로 가져와서 바로 해당 object 생성할 수 있는 flow 만들기
    - 이런식으로
        ```python
        # create instance of model
        m = MyModel(**data_dict)
        # don't forget to save to database!ㅍ
        m.save()
        ```

생각보다 할꺼 겁나 많네ㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷ

## 해볼거
- Mode.objects.create_or_get : 이거 쓰면 데이터가 db에 존재하는지 if문으로 확인하고 있으면 뭐하고 없으면 더해주고가 아니라 저절로 판별하고 없으면 바로 생성해주는듯


## 배운거
- db에 특정 object 있나 확인 : `Question.objects.filter(question_number=question[0]).exists():`
