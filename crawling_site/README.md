# 백준 크롤링

## Todos
- [x] model design
- [ ] front-end design (3d look)
- [x] 크롤링한 데이터 db에 자동 저장
    - [x] 저장
    - [x] 날짜 데이터, 티어 데이터 사이트 데이터 추가로 필요
- [x]] 크롤링 결과를 직접보여주는게 아니라 db에서 데이터 가져와서 보여주기
- [ ] 벌금 페이지 만들기
- [x] 그래프, 차트 등 사용해서 푼 문제 수 표시하기
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
- [ ] 다른 사이트 결과 수동으로 추가할 수 있게 하기
- [ ] html 파일에 css js 까지 쓰면 너무 길어지니깐 statics 폴더에 따로 저장하고 싶은데 js에서 django에서 주는 변수를 사용해서 어떻게 처리해야될지 모르겠다
    - [x] css파일 따로 보관 -> 
        - [ ] 근데 css 파일을 그냥 한꺼번에 base.html 에서 load 하고 있음-> 각 view에 해당하는 html 파일에서 load 할 수 있도록 바꾸기
    - [ ] js파일 따로 보관 (**질문해보기**)
        

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
- 새로고침 했을 때 페이지 로딩 속도가 너어무 느리다..이거 어떻게 고칠지 생각해보기(**질문**)

<br>

## 해볼거
- Model.objects.create_or_get : 이거 쓰면 데이터가 db에 존재하는지 if문으로 확인하고 있으면 뭐하고 없으면 더해주고가 아니라 저절로 판별하고 없으면 바로 생성해주는듯
- **kwargs 써서 dictionary 통째로 Model object 에 넣어주기 [참고링크](https://stackoverflow.com/questions/1571570/can-a-dictionary-be-passed-to-django-models-on-create)
- Django REST framework 로 json 데이터 보내기 
    - 지금 내가 보내고 있는건 그냥 str 인건가? -> template이 알아서 django model 데이터 해석해서 보여주는거래(아마?)
    - serializer로 json 형식으로 바꿔서 보내줘보자

<br>

## 배운거
- db에 특정 object 있나 확인 : `Question.objects.filter(question_number=question[0]).exists():`
- `python manage.py flush` 하면 db 초기화 가능
- `update_or_create` -> tuple로 (새로 생성된 object, bool) 반환해줌
    - defaults 부분이 업데이트 하고 싶은 값!

- 데이터를 보여주는 view 와 데이터를 front 로 보내는 function은 분리하는게 좋대 -> 담엔 나눠서 해보기
- `class Meta` Field가 아닌 모든 정보를 보관하는 공간, 정렬 순서 등
    - -> Solve Class를 최근에 푼 것부터 위에 보이게 정렬해봤다 
    - [옵션 목록](https://docs.djangoproject.com/en/3.1/ref/models/options/)

- migrations 파일을 보면 자동으로 `id` field를 생성해주는 걸 볼 수 있다
    - 이 값은 auto-increment 하는 값으로 각 object의 고유값이다

- `var data = {{ data|safe }}` 이런식으로 js에서 django 데이터를 받을 수 있다 [django +  chart.js](https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html)

<br>

### Django REST Framework
- 나중에 이걸로 텔레그램 메세지 보내는 거 만들어보기
- serializers.py : 얘를 사용한 view를 통해서 어떤 데이터를 어떤 형식으로 넘겨줄지 정하는 곳
    - serializers.Modelserializer : [참고공문](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects)
        - `fields =__all__` 사용하면 모든 field에 대한 정보 한번에 보낼 수 있음
        - `exclude` 로 필요 없는 field 지정 가능
        - `depth` 옵션 사용하면 many-to-many field 의 안쪽 정보도 다 보낼 수 있음