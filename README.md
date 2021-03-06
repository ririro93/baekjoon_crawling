# 백준 크롤링

## 실행방법
1. 로컬에서 db를 sqlite로
    - `python manage.py runserver
2. docker-compose로 db를 postgresql로
    - docker-desktop 설치
    - `docker-compose up -d --build` 실행
    - 앱 : `localhost:8000`
    - pgadmin(postgresql 정보 보는 곳) : `localhost:80`
        - id: user@gmail.com
        - pw: password
    - flower(celery worker status 보는 곳): `localhost:5555`

<br>

## Todos
- [x] model design
- [ ] front-end design
    - [x] 3d look
        - [ ] 애니메이션 끄는 기능
    - [x] refresh 버튼 hover 하면 튀어나오게
    - [x] refresh 버튼에 클릭하면 돌아가게
    - [x] 밑에 버튼들에 마우스 올리면 튀어나오게
    - [ ] 제목 더 멋있게
    - [ ] refresh 하는 동안 last updated 약간 매트릭스 느낌나게ㅎㅎ
    - [ ] 새로고침 쿨 다운 5분 정도 설정해두기 -> 그냥 이 정보만 저장할 model 하나 더 만들어보기
    - [ ] 밑으로 쭉 내리면 상세정보 볼 수 있게 하기
    - [ ] *오른쪽 반에 달력(보류: 엄청 어려울듯)* 
        - [x] 거기 마우스 올리면 커지게
        - [x] 거기서 범위 고르면 왼쪽에서 보여주기
        - [ ] 화살표에 역동적인 애니메이션 적용해보기
- [x] 크롤링한 데이터 db에 자동 저장
    - [x] 저장
    - [x] 날짜 데이터, 티어 데이터 사이트 데이터 추가로 필요
- [x] 크롤링 결과를 직접보여주는게 아니라 db에서 데이터 가져와서 보여주기
- [x] 그래프, 차트 등 사용해서 푼 문제 수 표시하기
- [ ] 자동으로 몇 시간에 한번씩 자동으로 업데이트 되게 하기(background periodic tasks) **질문**
    - socket.io 느낌도 원하는데..
    - 검색하니깐 celery?추천하는데 윈도우는 지원안한대ㅎㅎ....어떡할까
        -> celery + redis 해보기
            -> redis 쓸려면 docker 써야된대..
- [x] refresh 버튼으로 수동 업데이트 가능하게 하기
    - [x] refresh 버트 생성
    - [x] 현재 시각도 같이 보여주기(얘는 실시간으로 바뀌게)
    - [x] 그냥 접속만 한 경우에는 전에 업데이트 된 시간 보여주기
    - [x] 위에 alert로 refreshed! 이런 메세지 보여주기 bootstrap alert
- [x] 크롤링 결과를 딕셔너리 형태로 가져와서 바로 해당 object 생성할 수 있는 flow 만들기
    - 이런식으로
        ```python
        # create instance of model
        m = MyModel(**data_dict)
        # don't forget to save to database!ㅍ
        m.save()
        ```
    - ~~지금 테스트로 푼 문제 사람마다 6개씩만 가져오는 중~~
- [x] 다른 사이트 결과 추가할 수 있게 하기
    - [x] 예쁜 form 만들기
    - [x] db에 데이터 넘기기
    - [ ] 팝업으로 하고 제출하면 위로 날아가게 -> single page application 적용?
    - [x] hackerrank랑 swea도 추가
- [ ] html 파일에 css js 까지 쓰면 너무 길어지니깐 statics 폴더에 따로 저장하고 싶은데 js에서 django에서 주는 변수를 사용해서 어떻게 처리해야될지 모르겠다
    - [x] css파일 따로 보관 -> 
        - [ ] 근데 css 파일을 그냥 한꺼번에 base.html 에서 load 하고 있음-> 각 view에 해당하는 html 파일에서 load 할 수 있도록 바꾸기
    - [ ] js파일 따로 보관 (**질문해보기**) -> 아마 안될듯
- [ ] 벌금 페이지 만들기
- [ ] 자기 아이디도 넣어달라고 요청할 수 있기
- [ ] 각자 로그인 해서 자기 정보만 따로 모아서 볼 수 있게 하기
    -[ ] 로그인 가능하게 하기
- [ ] 사람 이름 누르면 상세정보 보이게 
- [x] 크롤링 더 빠르게
- [ ] ajax request 실패 했을 때 코드 추가하기
- [ ] django message framework 써보기
    - [ ] 애니메이션 추가
    - [x] 두개 쌓이면 안 없어지는 버그 고치기 (crawl_home -> removeAlerts() 잘 모름)
    - [x] ajax request 보냈을 때 messages 발동 안되니깐 별도 처리
- [x] dockerize 해서 heroku 배포 해보기
    - [ ] 이러면 db 관리는 어떻게 하는거지? **질문** -> heroku postgres addon 써보기
- [x] logging 기능 추가 해야겠다 -> heroku에서 django log가 안보임 -> logdna addon 써보기
- [x] 모든 멤버가 푼 모든 과거 문제들도 추가 가능하게 하기
    - [ ] 진행바로 얼마나 진행됐는지 표시하는 기능도 추가
        


## 문제
- [x] 데이터를 받을 때 푼 문제가 해당 멤버가 아닌 모든 멤버랑 연결됨
    - 그런줄 알았는데 그게 아니라 내가 admin에서 수동으로 추가할 수도 있었던거ㅎㅎ
    - 추가된 문제들이 admin에서 보이게 따로 설정을 해줘야 될듯
- [x] many to many field로 멤버와 문제를 연결하니까 각 멤버가 그 문제를 며칠에 풀었는지 정보를 어디에 저장해야될지 모르겠다
    - 어쩌면 그냥 문제번호랑 푼 날짜를 tuple로 저장하고 출력할 때는 해당 문제번호 object 정보를 보여주는게 좋을수도...
        - [참고](https://stackoverflow.com/questions/31776586/how-to-add-a-timestamp-to-a-manytomany-record)
        [참고2](https://docs.djangoproject.com/en/3.1/topics/db/models/)
        여기 링크처럼 through keyword 랑 intermediate model을 만들어서 여기에 timestamp정보를 추가해보면 될듯?
- [x] scraping 할 때 티어 정보를 못 가져옴
    - <img> 태그가 안 긁혀! -> 이게 로그인 해서 설정에서 바꿔야 보이게 되어있어서 그런듯 한데 어뜩할까
        - 그냥 solved.ac가서 가져오기
- [x] Solve 에 푼 문제가 푼 시간만 다르게 중복 저장된다 -> solved_time 값만 바뀌게 짜야됨
    - `Solve.objects.update_or_create` 사용해서 해결 -> tuple로 (새로 생성, bool) 반환해줌
        - **해결된줄 알았는데 아직도 중복되네 이거 고쳐야됨**
        - defaults 부분이 바꿔주고 싶은 부분이었음
            - 예전게 나중에 나와서 전에 푼 기록으로 업데이트 됨-> 순서 역순으로 바꿔야됨
- [x] 새로고침 했을 때 페이지 로딩 속도가 너어무 느리다..이거 어떻게 고칠지 생각해보기(**질문**) 
    - -> 멀티쓰레딩 쓰니까 1분 -> 10초
- [ ] leetcode 랑 programmers 새 문제 제출 템플릿이 달라야 되는데

[02-08]
- [x] last crawl 시간이 업데이트 되지 않는다 -> 로직 실수

[02-11]
- [ ] 배포용 서버에서는 윈도욱 개발때랑 다르게 현재 시간이 미국시간으로 적용됨.. -> `datetime.datetime.now()` 가 아니라 `django.utils.timezone.now()` 쓰면됨
    -> 된줄 알았는데 base linux 자체 TZ를 KST로 바꿨어서 된거였음 <br>
    -> [블로그](https://forgiveall.tistory.com/591)
- [x] 내 db랑 예은님 백준 프로필이랑 푼 문제 개수가 다르다
    - -> 백준이 푼 문제수 표기한게 틀린듯..?

[02-13]
- 도커로 로컬에서 작업하면 celery랑 celery-beat를 다 다른 컨테이너에서 돌리면 되는데 heroku에 배포할 때는 어떻게 할지 생각해보기
    - dockerfile애서 CMD 지정해서 shell을 3개를 쓸 수 있으면 각각에서 서버돌리고, celery, celery-beat를 돌리면 되는데 이게 한번에 가능한가?해보기
        - -> 요런게 있었네.. [heroku docs](https://devcenter.heroku.com/articles/dyno-types#default-scaling-limits)
    - 안되면 linux 환경에서 자주 쓰는 daemonization 방식을 쓸수도 있대 [celery docs:daemonization](https://docs.celeryproject.org/en/latest/userguide/daemonizing.html#daemonizing)
- celery beat로 periodic task를 실행하려면 scheduler 가 있어야되는데 이 scheduler는 인자로 non-naive datetime값을 넣어줘야된다. 하지만 장고에서 한국시간으로 보여주기 위해 
    ```python
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Asia/Seoul'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = False
    ```
을 사용하고 있다. `USE_TZ=True`로 설정하면 celery beat는 작동하지만 앱 내부에서 보여주는 current time이 안맞게 된다 vice-versa...............................................난관이다...........
[나랑 비슷한 문제를 겪은듯](https://daeguowl.tistory.com/159)
[블로그](https://daeguowl.tistory.com/159)
    - -> 이거 따라해도 작동안함..

<br>

## 해볼거
- Model.objects.create_or_get : 이거 쓰면 데이터가 db에 존재하는지 if문으로 확인하고 있으면 뭐하고 없으면 더해주고가 아니라 저절로 판별하고 없으면 바로 생성해주는듯
- **kwargs 써서 dictionary 통째로 Model object 에 넣어주기 [참고링크](https://stackoverflow.com/questions/1571570/can-a-dictionary-be-passed-to-django-models-on-create)
- Django REST framework 로 json 데이터 보내기 
    - 지금 내가 보내고 있는건 그냥 str 인건가? -> template이 알아서 django model 데이터 해석해서 보여주는거래(아마?)
    - serializer로 json 형식으로 바꿔서 보내줘보자
- Figma로 애니메이션 만들어보기
- 창 줄였을 때 버튼들이 카드 밖으로 삐져나옴
    - -> overflow 방지 해서 그냥 scroll 생기게 해보기
- CSS SASS로 바꿔보기
- Single Page Application -> Vue 겉핥기 해보기
- typescript도 써보기

<br>

## 배운거
### Django
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

- css, js, 이미지 파일 등 static 파일을 쓰려면
    1. `settings.py`에 아래 코드 추가해줘야되고
        ```
        STATICFILES_DIRS = [
           BASE_DIR / 'static'
        ]
        ```
    2. html 파일에서 `{% load static %}` 이라고 적어줘야 된다
    3. 불러오는 파일에는 `static` 이라는 키워드를 붙여서 부른다

- `HttprResponseRedirect(reverse(<url-name>))`: 를 사용해서 form 제출후에 원하는 곳으로 보낼 수 있다.
- [rendering forms manually](https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html) : 엄청 좋은 사이트

<br>

### JS
- `document.querySelectorAll('.button, .refresh-button');` : 이런식으로 한번에 여러 클래스의 노드들을 하나의 `NodeList`로 묶을 수 있다

<br>

### django <-> js 통신

<br>

#### js -> django
- `var data = {{ data|safe }}` 이런식으로 js에서 django 데이터를 받을 수 있다 [django +  chart.js](https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html)

- ajax request로 get이나 post request를 장고에게 보내는 것
    - csrf_token?라는게 필요해서 아래 코드처럼 넣어주면 된다
    - `headers: { "X-CSRFToken": "{{ csrf_token }}"},`
- django 쪽에서 받는 법:
    - `data = json.loads(request.POST.get('data'))`

<br>

#### django -> js
- `return HttpResponse(json.dumps(context), content_type='application/json)`
    - 이런식으로 content_type을 명시해줘야됨 -> 안 그러면 한글이 깨져서 도착한다


### CSS
- `transform-style: preserve-3d` -> Let the transformed child elements preserve the 3D transformations

<br>

### Django REST Framework
- 나중에 이걸로 텔레그램 메세지 보내는 거 만들어보기
- serializers.py : 얘를 사용한 view를 통해서 어떤 데이터를 어떤 형식으로 넘겨줄지 정하는 곳
    - serializers.Modelserializer : [참고공문](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects)
        - `fields =__all__` 사용하면 모든 field에 대한 정보 한번에 보낼 수 있음
        - `exclude` 로 필요 없는 field 지정 가능
        - `depth` 옵션 사용하면 many-to-many field 의 안쪽 정보도 다 보낼 수 있음

## 참고
[testdriven.io](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)