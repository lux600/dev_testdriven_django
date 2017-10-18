## 소개

## aws.amazon.com
- jjoljjollee@gmail.com
- rema\*\*72\*\*
- keypair : purchase-keypair
    - chmode 400 purchase-keypair
    - http://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
- security group : purchase_security_group
    - inbound
        - HTTP TCP 80 0.0.0/0 (anywhere)
        - PostgreSQL TCP 5432 0.0.0/0 (anywhere)
        - Custom TCP 8000 0.0.0/0 (anywhere)
        - SMTP TCP 25 0.0.0/0 (anywhere)
        - HTTPS TCP 443 0.0.0/0 (anywhere)
- vpc : purchase_vpc
- EC2 : Ubuntu Server 16.04 LTS(HVM), SSE Valume Type- ami-66e33108 (64bit)
    - Type : t2.micros
    - vCPUS : 1
    - Memory(GiB) : 1
    - Instance Storage(GB): EBS only
    - Configure Instance Details
        - Network : vpc-c43a5ead(default)
```        
- ssh -i "purchase-keypair.pem" ubuntu@13.124.141.252
    - (위와 동일) ssh -i "purchase-keypair.pem" ubuntu@ec2-13-124-141-252.ap-northeast-2.compute.amazonaws.com
```

## aws.db 
- 아마존 로그인 
    - jjoljjollee@gmail.com
    - rema\*\*72\*\*
- RDS 
    - PostgreSQL9.6.2-R1
    - DB instance identifier : purchasedb
    - master username : rema\*\*  
    - master password : rema\*\*72\*\*
    - database name ; purchase_db
    
--- 
## 아마존 서버 Git identity
- remann@ip-10-0-0-173.ap-northeast-2.compute.internal
- git config --global user.email "woo@remann.co.kr"
- git config --global user.name "rema\*\*"

## smtp (메일서버)
- smtp.cafe24.com
- pop3 : webmail.remann.co.kr
- rema\*\*7
- @kcrc72\*\*
- port : 110
---
### 우분투 내의 작업 
```
- 사용자 추가 : sudo useradd -m -s /bin/bash rema**
- remann 사용자를 sudoers 그룹 추가 : sudo usermod -a -G sudo rema**
- remann 사용자 비밀번호 : sudo passwd rema** 
    - rema**72**
    
- rema** 으로 사용자 변경 : su - rema**
- ngix 서버 설치 
    - remann@server:$ sudo apt-get update
    - remann@server:$ sudo apt-get install nginx 
    - remann@server:$ sudo service nginx start (서버실행)
    - remann@server:$ sudo service nginx stop (서버종료)
```    
### 파이썬 설치 
```
- rema** 으로 사용자 변경 : su - rema**
- remann@server:$ sudo apt-get install git python3.4 python3-pip
- remann@server:$ sudo pip3 install virtualenv
```
### 파이썬 개발환경 설정 
```
root@server:$ su - rema**
remann@server:$ pwd
/home/remann

remann@server:$ mkdir website
remann@server:$ cd website

remann@server:~/website$ mkdir source
remann@server:~/website$ mkdir static_cdn
remann@server:~/website$ mkdir media_cdn
remann@server:~/website$ mkdir virtualenv
```
### 파이썬 가상환경 설정 
```
root@server:$ su - remann
/home/rema**

remann@server:$ cd website/virtualenv
/home/remann/website/virtualenv

remann@server:~/website/virtualenv:$ vitualenv -p python3 . (현재 디렉토리에 3.x 버전 파이썬)
현재 python3.5 버전 (2017-06-07)
 
remann@server:~/website/virtualenv:$ source ./bin/activate
(virtualenv)remann@server:~/website/virtualenv:$

```
---

### Django 설치 
```
(virtualenv)remann@server:~/website/virtualenv:$ pip install django==1.10  ( 장고 1.10 버전 설치) 
(virtualenv)remann@server:~/website/virtualenv:$ pip install psycopg2 (DB 는 Postgresql ) 
```

### Django 프로젝트 생성 
```
(virtualenv)remann@server:~/website/:$ pwd
/home/remann/wetsite/

(virtualenv)remann@server:~/website/:$ django-admin startproject mysite

(virtualenv)remann@server:~/website/:$ cd mysite
(virtualenv)remann@server:~/website/:$ python manage.py runserver

```
### Ubuntu + Django + nginx
- [Ubuntu + Django + nginx 설치 예제](http://astronaut94.tistory.com/entry/Django-%EC%82%AC%EC%9D%B4%ED%8A%B8-%EA%B5%AC%EC%B6%95-1-%EA%B0%84%EB%8B%A8%ED%95%9C-Nginx-uWSGI-Django-%EC%82%AC%EC%9D%B4%ED%8A%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0)
```
(virtualenv)remann@server:~/website/:$ pwd
/home/remann/wetsite/

(virtualenv)remann@server:~/website/:$ pip install uwsgi
(virtualenv)remann@server:~/website/:$ mkdir uwsgi
(virtualenv)remann@server:~/website/:$ cd uwsgi
```

- /home/remann/website/uwsgi/uwsgi.ini
```
(virtualenv)remann@server:~/website/:$ sudo vi uwsgi.ini

[uwsgi]
chdir           = /home/remann/website/source
module          = mysite.wsgi
virtualenv      = /home/remann/website/virtualenv
processes       = 2
pidfile         = /home/remann/website/uwsgi/mysite.pid
socket          = /home/remann/website/uwsgi/mysite.sock
chmod-socket    = 666
daemonize       = /home/remann/website/uwsgi/mysite.log
master          = true
```

- /etc/init.d
```
(virtualenv)remann@server:~/website/:$ sudo vi /etc/init.d/mysite  (mysite 파일생성)

#!/bin/bash
### BEGIN INIT INFO
# Provides:           mysite
# Required-Start:    
# Required-Stop:     
# Default-Start:      2 3 4 5
# Default-Stop:       0 1 6
# Short-Description:  Start/Stop uwsgi in virtual environment to serve myproject app.
# Description:        Start/Stop uwsgi in virtual environment to serve myproject app.
### END INIT INFO
MYPROJECT_HOME=/home/remann/website/
case $1 in
    start) $MYPROJECT_HOME/virtualenv/bin/uwsgi --ini $MYPROJECT_HOME/uwsgi/uwsgi.ini;;
    stop) $MYPROJECT_HOME/virtualenv/bin/uwsgi --stop $MYPROJECT_HOME/uwsgi/mysite.pid;;
    restart) $MYPROJECT_HOME/virtualenv/bin/uwsgi --reload $MYPROJECT_HOME/uwsgi/mysite.pid;;
    *) echo "Usage: $0 {start|stop|restart}" >&2; exit 1;;
esac
exit 0
```
- mysite 에 연결된 uWSGI 가 자동실행된다 
```
sudo service mysite start
sudo service mysite stop
sudo service mysite restart
```

####  Nginx 설정 
- /etc/nginx/sites-available/mysite  ( mysite 파일생성 )
```
server {
	listen 80;
	server_name 13.124.141.252;  # 현재서버, 도메인으로 변경가능 
	charset utf-8;

	location / {
		uwsgi_pass unix:///home/remann/website/uwsgi/mysite.sock;
		include uwsgi_params;
	}
}

```
- sites-enabled 에 있는 default 사이트를 삭제한 후 방금 만든 mysite 를 링크 
```
cd /etc/nginx/sites-enabled
$ sudo rm default
$ sudo ln -s /etc/nginx/sites-available/mysite ./mysite

```
### 최종 결과 확인 및 변경시 
```
$ sudo service nginx restart
$ sudo service mysite restart 
```

---
### django 슈퍼 관리자 설정 
```
$ python manage.py cratesuperuser
admin 
remann7297

remann
reman7297  (비밀번호 similiar 에러나서 n을 1개 제외 )
```

### mysite.settings
#### Django-allouth : 회원가입, 로그인, 소셜 로그인
- http://django-allauth.readthedocs.io/en/latest/index.html
- urls
    - url(r'^accounts/', include('allauth.urls')),
    1. accounts/signup/$ [name='account_signup']
    2. accounts/login/$ [name='account_login']
    3. accounts/logout/$ [name='account_logout']
    4. accounts/password/change/$ [name='account_change_password']
    5. accounts/password/set/$ [name='account_set_password']
    6. accounts/inactive/$ [name='account_inactive']
    7. accounts/email/$ [name='account_email']
    8. accounts/confirm-email/$ [name='account_email_verification_sent']
    9. accounts/confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']
    10. accounts/password/reset/$ [name='account_reset_password']
    11. accounts/password/reset/done/$ [name='account_reset_password_done']
    12. accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']
    13. accounts/password/reset/key/done/$ [name='account_reset_password_from_key_done']
    14. accounts/social/

- SMTP
    - http://sendgrid.com/
    - EMAIL_HOST = 'smtp.sendgrid.net'
    - EMAIL_HOST_USER = 'user id ****'
    - EMAIL_MAIN = 'email address @****.net'
    - EMAIL_HOST_PASSWORD = '*******'
    - EMAIL_PORT = 587
    - EMAIL_USER_TLS = True
- Facebook Login
    - https://developers.facebook.com/apps/

#### Django Crisp Forms
- http://django-crispy-forms.readthedocs.io/en/latest/

#### Facebook Login
    - 새 앱 추가 (create app)
    - Dashboard
        - Provider = Facebook
        - client id = 앱 ID
        - Secrete key = 앱 시크릿 코드
        - Sites = Django sites
    - http://django-allauth.readthedocs.io/en/latest/providers.html#facebook
    ```
    {% load socialaccount %}
    <a href="{% provider_login_url "facebook" method="oauth2" %}">Facebook OAuth2</a>
    ```
    ```
    SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable', ==> 변경 lambda request: 'en_US'
        'VERIFIED_EMAIL': False, ==> True
        'VERSION': 'v2.4',
        }
    }
    ```
    - LOCALE_FUNC
    ```
    SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'LOCALE_FUNC': lambda request: 'en_US'
        }
    }
    ```
    - VERIFIED_EMAIL
    - Development callback URL
        - 페이스북 > app > 설정 >
            - 앱 도메인 : localhost
            - 웹사이트 : (테스트) http://localhost:8000/ ==> (실제) 실도메인
        - 페이스북 > app > 제품 > Facebook 로그인 > 설정
            - 유효한 OAuth 리디렉션 URI
                - http://localhost:8000/accounts/facebook/login/callback/
                - http://127.0.0.1:8000/accounts/facebook/login/callback/
                - http://13.124.52.53/accounts/facebook/login/callback/


#### kakao Login
    - https://github.com/askdjango/django-allauth-providers-ko
    
## 언론보도 편집기 WYSIWYG editor 
    - http://summernote.org/
## 통계 그래프 
    - http://www.chartjs.org/
    
## django template math 
- https://pypi.python.org/pypi/django-mathfilters
- https://stackoverflow.com/questions/9948095/variable-subtraction-in-django-templates
- mysite > utils.py > def pageDivideUtility(count, paginate_by, page):
```
settings.py INSTALLED_APPS = [ 'mathfilters', ]
templates file(.html)  {% load mathfilters %} 
{{ num_pages|sub:forloop.counter }}
```

## 로그인 체크 
- https://docs.djangoproject.com/en/1.10/topics/auth/default/
```
from django.contrib.auth.mixins import LoginRequiredMixin

class DeviceFactoryListView(LoginRequiredMixin,ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

```
## 다양한 Mixin 
- https://gist.github.com/robgolding/3092600


## To-Do
- 첫째 화면 슬라이드 
- 모델에 대한 선택변경 
- 회원가입 에러 
- template 파일들 정리
- 패키지 정리 