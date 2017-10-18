## 참조책 
![](./assets/book.jpg)

--- 

![](./assets/book.jpg)

---

## 마크다운 문법 
- https://namu.wiki/w/%EB%A7%88%ED%81%AC%EB%8B%A4%EC%9A%B4
* ~~test~~

## 파이썬 설치 
- [ 점프 투 파이썬 ](https://wikidocs.net/8)
- [ pip 설치 ] (http://blog.colab.kr/11)
- [ virtualenv 가상환경 구축 ](http://pythoninreal.blogspot.kr/2013/12/virtualenv.html)

## 파이썬 install
- [파이썬 가상환경 설치](https://www.holaxprogramming.com/2017/07/15/python-virtual-environments/)
- virtualenv -p python3.4 .
---
<br/>

- pip install django==1.10
- pip install --upgrade selenium
    - /dev_testdriven_django/안에 아래와 같은 파일이 생성 
        - selenium/webdriver/firefox/..
        - selenium/webdriver/remote/..
    - source 안에 webdriver 생성 후 chromedriver 복사 
    - 샘플코드 : /source/install_test/functional_test.py
---
- /dev_tstdriven_django/
    - django-admin.py startproject superlists 하여 메인프로젝트 생성
    - superlists를 source 로 프로젝트 이름 변경 
    
---
### Django settings.py
- 템플릿 
    - TEMPLATES = [
        - 'DIRS': [os.path.join(BASE_DIR, 'templates')],
    - 디렉토리 생성 
        - templates
- static 
    - STATICFILES_DIRS = ( os.path.join(BASE_DIR, "static"), )
    - 디렉토리 생성 
        - static 
---     

### git (page8)
 - [ Git 간편 안내 ](https://rogerdudler.github.io/git-guide/index.ko.html)
- echo "# dev_testdriven_django" >> README.md
- git init
- git add README.md
- git commit -m "first commit"
- git remote add origin git@github.com:lux600/dev_testdriven_django.git
- git push -u origin master

<br/>

- git log --oneline  (한줄씩 보기)
- git rm -r --cached superlists/__pycache__
- echo "__pycache__" >> .gitignore

<br/>

- git status
- git add .
- git diff --staged # 커밋 수정내역 확인 
- git commit -m "커밋내용"
 
---
- db 삭제 
    - rm db.sqlite3
    - python manage.py migrate --noinput
---
- http://www.nltk.org/install.html
    - pip install -U nltk
    - pip install -U numpy 


# 가상환경 
- source bin/activate

## logging 설정 
http://ourcstory.tistory.com/97

## nltk
- https://stackoverflow.com/questions/26570944/resource-utokenizers-punkt-english-pickle-not-found/26578793

---

## server 222.239.249.69
- ssh root@222.239.249.69
- sj\*\*84\*\*
- /home/elsepeth
- /home/remann
- /home/exampleapp 
- su - remann 

---
- 새로운 사용자 생성하기 
    - root@server:$ useradd -m -s /bin/bash tdd_django 
        - tdd_django 사용자 추가 
        - -m 은 /home 폴더안에 tdd_django 를 생성 
        - -s 는 tdd_django 가 bash를 사용하도록 설정 
    - root@server:$ usermod -a -G sudo tdd_django
        - tdd_django를 sudoers 그룹에 추가 
    - root@server:$ passwd tdd_django # 패스워드 설정 
        - sj\*\*84\*\*
    - root@server:$ su - tdd_django # tdd_django로 사용자 변경 
    - tdd_django@server:$ 
    
<br/>

- 도메인 연동(카페24)
    - 도메인부가서비스 >  DNS 관리 > 
        - 해당도메인 선택 singsns.com > DNS(네임서버) 관리 >
            - 호스트IP(A 레코드) 관리 > 222.239.249.69
- nginx 설치 
    - tdd_django@server:$ sudo apt-get install nginx 
    - tdd_django@server:$ sudo service nginx start 

<br/>

- 폴더 구조 
    - /home/tdd_django
        - sites
            - live.tdd_django.com
                - database
                    - db.sqlite3
                - source
                    - manage.py
                    - superlists
                - static 
                    - base.css
                - virtualenv
                    - lib
            - staging.tdd_django.com
                - database
                - source
                - static
                - virtualenv 
- export 
    - tdd_django@server:$ export SITENAME=staging.tdd_django.com
    - tdd_django@server:$ mkdir -p ~/sites/$SITENAME/database
    - tdd_django@server:$ mkdir -p ~/sites/$SITENAME/static
    - tdd_django@server:$ mkdir -p ~/sites/$SITENAME/virtualenv
    - tdd_django@server:$
    - tdd_django@server:$ git clone https://github.com/lux600/dev_testdriven_django ~/sites/$SITENAME/source
                                         
- virtualenv 생성 
    - $ pip3 install virtualenv 
    - tdd_django@server:~/sites/staging.tdd_django.com/virtualenv$ virtualenv --python=python3 . 
    - tdd_django@server:~/sites/staging.tdd_django.com/virtualenv$ cd bin
    - tdd_django@server:~/sites/staging.tdd_django.com/virtualenv/bin$ ls
        - 파이썬 버전 확인 가능 
        - which python3 (파이썬 경로)
            - /usr/bin/python3
    - tdd_django@server:~/sites/staging.tdd_django.com/source $ source ../virtualenv/bin/activate
        - (virtualenv) tdd_django@server:~/sites/staging.tdd_django.com/source$
        - which python
            - /home/tdd_django/sites/staging.tdd_django.com/virtualenv/bin/python
    - pip freeze > requirements.txt
        - git add requirements.txt
        - git commit - m "requirements.txt 추가 "
        - git push -u origin master
    - server 
        - pull 
        - source ../virtualenv/activate
        - pip install -r requirements.txt 
        
### Nginx 설정 
~~~
server {
        listen 80;
        server_name www.singsns.com;

        location / {
                proxy_pass http://localhost:8000;
        }
}  
~~~      

~~~
(virtualenv) tdd_django@ommath:/etc/nginx/sites-available$ echo $SITENAME
    - staging.tdd_django.com
tdd_django@ommath:/etc/nginx/sites-available$ sudo ln -s ../sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME
tdd_django@ommath:/etc/nginx/sites-available$ ls -l /etc/nginx/sites-enabled/
    - lrwxrwxrwx 1 root root 34 Sep 22  2016 default -> /etc/nginx/sites-available/default
    - lrwxrwxrwx 1 root root 41 Oct 18 18:04 staging.tdd_django.com -> ../sites-available/staging.tdd_django.com
    - lrwxrwxrwx 1 root root 41 Sep 24  2016 www.staging.remann.com -> ../sites-available/www.staging.remann.com
~~~

- tdd_django@ommath:/etc/nginx/sites-available$ sudo rm www.staging.remann.com      
~~~
server {
        listen 80;
        server_name www.staging.remann.com;

        location / {
                proxy_pass http://localhost:8000;
        }
}
~~~   
- nginx 
    - sudo nginx start
    - sudo nginx stop 
- su - remann : remann7297

- 502 Bad gateway 나올 때, python manage.py runserver 실행여부 확인 
 
            
               
                                         