## 사용자 계정 
- ssh root@222.239.249.69
~~~
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:DDv9b4jCp0we/9jbekNBLXL43h7NPfKrRILTDzs0qlg.
Please contact your system administrator.
Add correct host key in /Users/sangjunpark/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /Users/sangjunpark/.ssh/known_hosts:8
ECDSA host key for 222.239.249.69 has changed and you have requested strict checking.
Host key verification failed.
~~~
- [해결책](https://cpuu.postype.com/post/30065)
    1. 초기화 시키기 ssh-keygen -R 222.239.249.69
    2. ssh root@222.239.249.69
~~~
sang-ui-MacBook-Air:source sangjunpark$ ssh root@222.239.249.69

The authenticity of host '222.239.249.69 (222.239.249.69)' can't be established.
ECDSA key fingerprint is SHA256:DDv9b4jCp0we/9jbekNBLXL43h7NPfKrRILTDzs0qlg.
Are you sure you want to continue connecting (yes/no)? 
~~~
    

- ssh root@222.239.249.69
    - sj\*\*84\*\*
~~~    
root@server:$ useradd -m -s /bin/bash singsns 
root@server:$ usermod -a -G sudo singsns
root@server:$ passwd singsns
    - sj**84**
root@server:$ su - singsns

singsns@server:~$
~~~
    
## Nginx 설치 

- error 
~~~
singsns@server:$ sudo apt-get install nginx

E: dpkg was interrupted, you must manually run 'sudo dpkg --configure -a' to correct the problem.
 
singsns@server:$ sudo dpkg --configure -a
~~~
 
~~~
singsns@server:$ sudo apt-get update
singsns@server:$ sudo apt-get install nginx 
singsns@server:$ sudo service nginx start 
~~~

- ngix 실행여부 확인 
    - http://jojoldu.tistory.com/60
~~~
$ sudo service nginx status
or 
$ ps auxww |grep nginx
~~~

    
- 기본 설치 
~~~
singsns@server:$ sudo apt-get install git python3 python3-pip
singsns@server:$ sudo pip3 install virtualenv 
~~~

- 파이썬 위치 
~~~
$ which python3
/usr/bin/python3
~~~
    
## 스테이징 서버와 운영서버를 위한 도메인 설정 
- 도메인 ip 설정 
    - 도메인 구매처에서 연동 

## 기능테스트 코드를 이용해서 도메인 및 Nginx 가 동작하는지 확인 
~~~
local $ python manage.py test functional_tests -- liveserver=staging.singsns.com
~~~

## 코드 수동 배치 
## 서버에서 export 설정 및 디렉토리 만들기  
~~~
singsns@server:$ export SITENAME=staging.singsns.com
# singsns@server:$ mkdir -p ~/sites/$SITENAME/source
singsns@server:$ mkdir -p ~/sites/$SITENAME/database
singsns@server:$ mkdir -p ~/sites/$SITENAME/static
singsns@server:$ mkdir -p ~/sites/$SITENAME/virtualenv
~~~

- /home/singsns/
    - sites
        - live.singsns.com
            - database
                - db.sqlite3
            - source
                - manage.py 
                - superlists/
                - etc ...
            - static
                - base.css
                - etc ...
            - virtualenv
                - lib
                - etc 
        - staging.singsns.com
            - database
            - source
            - static
            - virtualenv

## 서버에서 export 설정 및 디렉토리 만들기  
~~~
singsns@server:~/sites/staging.singsns.com:$ git clone https://github.com/lux600/dev_testdriven_django
    - rm -rf source 
singsns@server:~/sites/staging.singsns.com:$ mv dev_testdriven_django source
~~~
                                                        
## virtualenv 생성 
~~~
# $ pip3 install virtualenv 
                                                        
singsns@server:~/sites/staging.singsns.com/virtualenv$ virtualenv --python=python3 .
                                 
singsns@server:~/sites/staging.singsns.com/virtualenv$ which python3
- /usr/bin/python3
~~~

## package 설치 (가상환경) 
~~~
singsns@server:~/sites/staging.singsns.com/source$ source ../virtualenv/bin/activate

(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ pip install django==1.10
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ pip install psycopg2
- Postgresql DB 연동 드라이버 
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ pip install gunicorn==18
- wsgi 연동
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ pip install fabric3

(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ pip freeze 

asn1crypto==0.23.0
bcrypt==3.1.4
cffi==1.11.2
cryptography==2.1.2
Django==1.10
Fabric3==1.13.1.post1
gunicorn==18.0
idna==2.6
paramiko==2.3.1
psycopg2==2.7.3.2
pyasn1==0.3.7
pycparser==2.18
PyNaCl==1.1.2
six==1.11.0
~~~

## django 데이터베이스 마이그레이션 
~~~
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ python manage.py makemigrations
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ python manage.py migrate --noinput
~~~

## 간단한 Nginx 설정 
- [설치참조](https://fureweb-com.github.io/blog/2017/08/07/applying-free-ssl-to-your-ubuntu-server-using-nginx-and-let
%27sencrypt-from-scratch.html)
~~~
# /etc/nginx/sites-available/staging.singsns.com

server {
        listen 80;
        server_name staging.singsns.com;

        location / {
    		proxy_pass http://localhost:8000;
        }
}
~~~

- nginx 로그 
~~~
singsns@server:~/sites/staging.singsns.com/source$ sudo tail -F /var/log/nginx/error.log
~~~

~~~
# /etc/nginx/sites-available/staging.singsns.com

server {
        listen 80;
        server_name staging.singsns.com;

	location /static {
		alias /home/singsns/sites/staging.singsns.com/source/static;
	}
        location / {
               	proxy_set_header Host $host;
		proxy_pass http://unix:/tmp/staging.singsns.com.socket;
		#proxy_pass http://localhost:8000;
        }
}
~~~

## symlink 
~~~
singsns@server:$ echo $SITENAME
- staging.singsns.com 

singsns@server:$ sudo ln -s ../sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME
singsns@server:/etc/nginx/sites-available$ ls -l ../sites-enabled/
    total 0
    lrwxrwxrwx 1 root root 34 Sep 22  2016 default -> /etc/nginx/sites-available/default
    lrwxrwxrwx 1 root root 37 Oct 24 20:07 staging.singsns.com -> ../site-available/staging.singsns.com

singsns@server:/etc/nginx/sites-available$ mv /etc/nginx/sites-enabled/default /home/singsns/sites/original_settings
    - 기존 default 이동(or 삭제)     
~~~

## Nginx 와 django 연동 
~~~
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ sudo service nginx reload
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ python manage.py runserver
~~~

## 운영 준비 배포 단계 gunicorn 교체 (manage.py runserver)
~~~
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ pip install gunicorn==18
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ ../virtualenv/bin/gunicorn superlists
.wsgi:application
~~~

## Nginx 정적파일 연동 
~~~
(virtualenv)singsns@server:~/sites/staging.singsns.com/source$ manage.py collecstatic --noinput
~~~

~~~
# /etc/nginx/sites-available/staging.singsns.com

server {
        listen 80;
        server_name staging.singsns.com;

	location /static {
		alias /home/singsns/sites/staging.singsns.com/source/static;
	}
        location / {
               	proxy_set_header Host $host;
		proxy_pass http://unix:/tmp/staging.singsns.com.socket;
		#proxy_pass http://localhost:8000;
        }
}
~~~

## 유닉스 소켓으로 교체하기 
~~~
# /etc/nginx/sites-available/staging.singsns.com

server {
        listen 80;
        server_name staging.singsns.com;

	location /static {
		alias /home/singsns/sites/staging.singsns.com/source/static;
	}
    
    location / {
        proxy_set_header Host $host;
		proxy_pass http://unix:/tmp/staging.singsns.com.socket;
    }
}
~~~
~~~
singsns@server:~/sites/staging.singsns.com/source$ sudo service nginx reload
singsns@server:~/sites/staging.singsns.com/source$ ../virtualenv/bin/gunicorn --bind unix:/tmp/staging.singsns.com
.socket superlists.wsgi:application
~~~

## setting.py DEBUG 변경하기 
~~~
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['staging.singsns.com',']
~~~

## Upstart 대신에 systemd 
~~~
# /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=singsns
Group=www-data
WorkingDirectory=/home/singsns/sites/staging.singsns.com/source
ExecStart=/home/singsns/sites/staging.singsns.com/virtualenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/tmp/staging.singsns.com.socket superlists.wsgi:application

[Install]
WantedBy=multi-user.target
~~~  

- 실시간 로그 분석 
~~~
singsns@server:~/sites/staging.singsns.com/source$ sudo tail -F /var/log/nginx/error.log
~~~

## Nginx , gunicorn 재시작 
~~~
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
                                         
$ sudo systemctl restart nginx
# $ sudo nginx -t && sudo systemctl restart nginx
~~~                                         

- nginx 상태 
~~~
$ sudo service nginx status
~~~

## 참고자료 
- ubuntu, nginx, django, postgresql 
    - [설치내용](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
        - [ufw 방화벽 설치](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)
        - [https 설치](http://wp.raonworks.com/?p=482)    
            

        
                
                    
    
                        
                                        
                                                            
    