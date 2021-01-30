# 백준 크롤링

## Todos
- [x] model design
- [ ] front-end design (3d look)
- [x] 크롤링한 데이터 db에 자동 저장
    - [x] 저장
    - [x] 날짜 데이터, 티어 데이터 사이트 데이터 추가로 필요
- [x]] 크롤링 결과를 직접보여주는게 아니라 db에서 데이터 가져와서 보여주기
- [ ] 벌금 페이지 만들기
- [ ] 그래프, 차트 등 사용해서 푼 문제 수 표시하기
- [ ] 자동으로 몇 시간에 한번씩 자동으로 업데이트 되게 하기
- [x] refresh 버튼으로 수동 업데이트 가능하게 하기
    - [x] refresh 버트 생성
    - [ ] 현재 시각도 같이 보여주기(얘는 실시간으로 바뀌게)
- [x] 크롤링 결과를 딕셔너리 형태로 가져와서 바로 해당 object 생성할 수 있는 flow 만들기
    - 이런식으로
        ```python
        # create instance of model
        m = MyModel(**data_dict)
        # don't forget to save to database!ㅍ
        m.save()
        ```
    - 지금 테스트로 푼 문제 사람마다 6개씩만 가져오는 중
        

생각보다 할꺼 겁나 많네ㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷㄷ

## 문제
- 데이터를 받을 때 푼 문제가 해당 멤버가 아닌 모든 멤버랑 연결됨
    - 그런줄 알았는데 그게 아니라 내가 admin에서 수동으로 추가할 수도 있었던거ㅎㅎ
    - 추가된 문제들이 admin에서 보이게 따로 설정을 해줘야 될듯
- many to many field로 멤버와 문제를 연결하니까 각 멤버가 그 문제를 며칠에 풀었는지 정보를 어디에 저장해야될지 모르겠다
    - 어쩌면 그냥 문제번호랑 푼 날짜를 tuple로 저장하고 출력할 때는 해당 문제번호 object 정보를 보여주는게 좋을수도...
        - [참고](https://stackoverflow.com/questions/31776586/how-to-add-a-timestamp-to-a-manytomany-record)
        [참고2](https://docs.djangoproject.com/en/3.1/topics/db/models/)
        여기 링크처럼 through keyword 랑 intermediate model을 만들어서 여기에 timestamp정보를 추가해보면 될듯?
- scraping 할 때 티어 정보를 못 가져옴
    - <img> 태그가 안 긁혀!이게 설정에서 바꿔야 보이게 되어있어서 그런듯 한데 어뜩할까
- Solve 에 푼 문제가 푼 시간만 다르게 중복 저장된다 -> solved_time 값만 바뀌게 짜야됨
    - `Solve.objects.update_or_create` 사용해서 해결 -> tuple로 (새로 생성, bool) 반환해줌
        - **해결된줄 알았는데 아직도 중복되네 이거 고쳐야됨**
        - defaults 부분이 바꿔주고 싶은 부분이었음
            - 예전게 나중에 나와서 전에 푼 기록으로 업데이트 됨-> 순서 역순으로 바꿔야됨
## 해볼거
- Model.objects.create_or_get : 이거 쓰면 데이터가 db에 존재하는지 if문으로 확인하고 있으면 뭐하고 없으면 더해주고가 아니라 저절로 판별하고 없으면 바로 생성해주는듯
- dictionary 통째로 Model object 에 넣어주기 [참고링크](https://stackoverflow.com/questions/1571570/can-a-dictionary-be-passed-to-django-models-on-create)


## 배운거
- db에 특정 object 있나 확인 : `Question.objects.filter(question_number=question[0]).exists():`
- `python manage.py flush` 하면 db 초기화 가능
- `update_or_create` -> tuple로 (새로 생성된 object, bool) 반환해줌
    - defaults 부분이 업데이트 하고 싶은 값!