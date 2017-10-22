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
- /dev_testdriven_django/
    - django-admin.py startproject superlists 하여 메인프로젝트 생성
    - superlists를 source 로 프로젝트 이름 변경 

---
- wsgi 가 무엇인가?
    - http://brownbears.tistory.com/350
    - http://khanrc.tistory.com/entry/WSGI%EB%A1%9C-%EB%B3%B4%EB%8A%94-%EC%9B%B9-%EC%84%9C%EB%B2%84%EC%9D%98-%EA%B0%9C%EB%85%90
    - http://paphopu.tistory.com/37
    - python manage.py runserver 대신 아래를 실시
        - pip install gunicorn==18
        - (virtualenv) tdd_django@ommath:~/sites/staging.tdd_django.com/source$ 
            - ../virtualenv/bin/gunicorn superlists.wsgi:applicationㄴ
    - 서버 tdd (로컬)
        - python manage.py test functional_tests --liveserver=singsns.com
- 유닉스의 도메인 소켓 
    - staging서버와 실서버를 같이 운용하기 위해서 
    - https://www.joinc.co.kr/w/Site/system_programing/IPC/Unix_Domain_Socket
    - http://forum.falinux.com/zbxe/index.php?document_srl=406064&mid=network_programming
    - 재실행 
        - (virtualenv) tdd_django@ommath:~/sites/staging.tdd_django.com/source$
            - sudo service nginx reload
            - ../virtualenv/bin/gunicorn --bind unix:/tmp/staging.tdd_django.com.socket superlists.wsgi:application   
                             
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
- ubuntu 에서 selenium 
    - https://christopher.su/2015/selenium-chromedriver-ubuntu/
~~~
sudo apt-get install unzip

wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
~~~     

- sudo apt-get update

- sudo vi /etc/nginx/sites-available/staging.tdd_django.com 
~~~
server {
        listen 80;
        server_name staging.tdd_django.com;

        location /static {
                alias /home/tdd_django/sites/staging.tdd_django.com/source/static;
        }
        location / {
                proxy_set_header Host $host;
                proxy_pass http://unix:/tmp/staging.tdd_django.com.socket;
                #proxy_pass http://localhost:8000;
        }
}
~~~

### Upstart 를 이용한 부팅 시 Gunicorn 가동 
- 서버 부팅시 Gunicorn를 자동으로 가동시킴 
- (virtualenv) tdd_django@ommath:~/sites/staging.tdd_django.com/source$ 
    - sudo vi /etc/init/gunicorn-superlists-staging.tdd_django.com.conf
~~~
description "Gunicorn server for superlists-staging.tdd_django.com"

start on net-device-up
stop on shutdown

respawn

setuid tdd_django
chdir /home/tdd_django/sites/staging.tdd_django.com/source

exec ../virutalenv/bin/gunicorn --bind unix:/tmp/superlists-staging.tdd_django.com.socket superlists.wsgi:application
~~~    
- sudo apt-get install upstart-sysv
- http://blog.sapzil.org/2014/08/12/upstart/
 
## 설치과정 
- https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

 
## 서버 재기동 
- sudo service nginx reload
- ../virtualenv/bin/gunicorn superlists.wsgi:application
    - python manage.py runserver 보다 위의 것으로 wsgi 가동

<br/>
       
- tdd_django@ommath:/etc/nginx/sites-available$ sudo vi staging.tdd_django.com        
~~~
# page176
server {
        listen 80;
        server_name staging.tdd_django.com;

	location /static {
		alias /home/tdd_django/sites/staging.tdd_django.com/source/static;
	}
        location / {
               	proxy_set_header Host $host;
		proxy_pass http://unix:/tmp/staging.tdd_django.com.socket;
		#proxy_pass http://localhost:8000;
        }
}
~~~

- 서버 재가동 
    - sudo service nginx reload 
    - ../virtualenv/bin/gunicorn --bind unix:/tmp/staging.tdd_django.com.socket superlists.wsgi:application 

## 서버 shutdown 해도 다시 재부팅
sudo vi /etc/systemd/system/gunicorn.service

~~~
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/tdd_django/sites/staging.tdd_django.com/source/
ExecStart=/home/tdd_django/sites/staging.tdd_django.com/source/virtualenv/bin/gunicorn --access-logfile - 
--workers 3 --bind unix:/tmp/staging.tdd_django.com.sock superlists.wsgi:application

[Install]
WantedBy=multi-user.target
~~~       
            
               
~~~
sudo tail -F /var/log/nginx/error.log
~~~               

                                         
~~~
# 재시작 

$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
                                         
$ sudo systemctl restart nginx
# $ sudo nginx -t && sudo systemctl restart nginx
~~~                                         