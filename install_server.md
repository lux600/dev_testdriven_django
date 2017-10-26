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

- nginx log 
~~~
singsns@server:~/sites/staging.singsns.com/source$ sudo tail -F /var/log/nginx/error.log
~~~

## 참고자료 
- ubuntu, nginx, django, postgresql 
    - [설치내용](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
        - [ufw 방화벽 설치](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)
        - [https 설치](http://wp.raonworks.com/?p=482)
            
## fabric 
~~~
# (dev_testdriven_django) sang-ui-MacBook-Air:deploy_tools sangjunpark$ fab deploy:host=singsns@staging.singsns.com
            
            
[singsns@staging.singsns.com] Executing task 'deploy'
[singsns@staging.singsns.com] run: mkdir -p /home/singsns/sites/staging.singsns.com/database
[singsns@staging.singsns.com] Login password for 'singsns': 
[singsns@staging.singsns.com] run: mkdir -p /home/singsns/sites/staging.singsns.com/virtualenv
[singsns@staging.singsns.com] run: mkdir -p /home/singsns/sites/staging.singsns.com/source
[singsns@staging.singsns.com] run: cd /home/singsns/sites/staging.singsns.com/source && git fetch
[singsns@staging.singsns.com] out: remote: Counting objects: 8, done.
[singsns@staging.singsns.com] out: remote: Compressing objects:  33% (1/3)   
[singsns@staging.singsns.com] out: remote: Compressing objects:  66% (2/3)   
[singsns@staging.singsns.com] out: remote: Compressing objects: 100% (3/3)   
[singsns@staging.singsns.com] out: remote: Compressing objects: 100% (3/3), done.
[singsns@staging.singsns.com] out: remote: Total 8 (delta 5), reused 8 (delta 5), pack-reused 0
[singsns@staging.singsns.com] out: Unpacking objects:  12% (1/8)   
[singsns@staging.singsns.com] out: Unpacking objects:  25% (2/8)   
[singsns@staging.singsns.com] out: Unpacking objects:  37% (3/8)   
[singsns@staging.singsns.com] out: Unpacking objects:  50% (4/8)   
[singsns@staging.singsns.com] out: Unpacking objects:  62% (5/8)   
[singsns@staging.singsns.com] out: Unpacking objects:  75% (6/8)   
[singsns@staging.singsns.com] out: Unpacking objects:  87% (7/8)   
[singsns@staging.singsns.com] out: Unpacking objects: 100% (8/8)   
[singsns@staging.singsns.com] out: Unpacking objects: 100% (8/8), done.
[singsns@staging.singsns.com] out: From https://github.com/lux600/dev_testdriven_django
[singsns@staging.singsns.com] out:    f24d267..2fd9673  master     -> origin/master
[singsns@staging.singsns.com] out: 

[localhost] local: git log -n 1 --format=%H
[singsns@staging.singsns.com] run: cd /home/singsns/sites/staging.singsns.com/source && git reset --hard 2fd967338db0a29e860c566f59d1cdce9ff9b66c
[singsns@staging.singsns.com] out: HEAD is now at 2fd9673 테스트 서버 설정하는법
[singsns@staging.singsns.com] out: 

[singsns@staging.singsns.com] run: sed -i.bak -r -e 's/DEBUG = True/DEBUG = False/g' "$(echo /home/singsns/sites/staging.singsns.com/source/superlists/settings.py)"
[singsns@staging.singsns.com] run: sed -i.bak -r -e 's/ALLOWED_HOSTS =.+$/ALLOWD_HOSTS = ["staging.singsns.com"]/g' "$(echo /home/singsns/sites/staging.singsns.com/source/superlists/settings.py)"
[singsns@staging.singsns.com] run: echo 'SECRET_KEY ='\\''nx=d7n5lsmt(5$ulirf_sl=7fnnn48d(e33mnnrix%r=s_$88m'\\''' >> "$(echo /home/singsns/sites/staging.singsns.com/source/superlists/secret_key.py)"
[singsns@staging.singsns.com] run: echo '
from .secret_key import SECRET_KEY' >> "$(echo /home/singsns/sites/staging.singsns.com/source/superlists/settings.py)"
[singsns@staging.singsns.com] run: /home/singsns/sites/staging.singsns.com/source/../virtualenv/bin/pip install -r /home/singsns/sites/staging.singsns.com/source/requirements.txt
[singsns@staging.singsns.com] out: Requirement already satisfied: Django==1.10 in ./sites/staging.singsns.com/virtualenv/lib/python3.5/site-packages (from -r /home/singsns/sites/staging.singsns.com/source/requirements.txt (line 1))
[singsns@staging.singsns.com] out: Collecting selenium==3.6.0 (from -r /home/singsns/sites/staging.singsns.com/source/requirements.txt (line 2))
[singsns@staging.singsns.com] out:   Downloading selenium-3.6.0-py2.py3-none-any.whl (924kB)
[singsns@staging.singsns.com] out: 
[singsns@staging.singsns.com] out:     1% |▍                               | 10kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     2% |▊                               | 20kB 620kB/s eta 0:00:02
[singsns@staging.singsns.com] out:     3% |█                               | 30kB 922kB/s eta 0:00:01
[singsns@staging.singsns.com] out:     4% |█▍                              | 40kB 969kB/s eta 0:00:01
[singsns@staging.singsns.com] out:     5% |█▊                              | 51kB 1.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     6% |██▏                             | 61kB 1.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     7% |██▌                             | 71kB 1.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     8% |██▉                             | 81kB 1.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     9% |███▏                            | 92kB 1.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     11% |███▌                            | 102kB 1.4MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     12% |████                            | 112kB 1.5MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     13% |████▎                           | 122kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     14% |████▋                           | 133kB 2.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     15% |█████                           | 143kB 2.6MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     16% |█████▎                          | 153kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     17% |█████▊                          | 163kB 2.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     18% |██████                          | 174kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     19% |██████▍                         | 184kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     21% |██████▊                         | 194kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     22% |███████                         | 204kB 2.7MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     23% |███████▍                        | 215kB 1.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     24% |███████▉                        | 225kB 2.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     25% |████████▏                       | 235kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     26% |████████▌                       | 245kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     27% |████████▉                       | 256kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     28% |█████████▏                      | 266kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     29% |█████████▋                      | 276kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     31% |██████████                      | 286kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     32% |██████████▎                     | 296kB 2.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     33% |██████████▋                     | 307kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     34% |███████████                     | 317kB 2.7MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     35% |███████████▍                    | 327kB 2.4MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     36% |███████████▊                    | 337kB 2.5MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     37% |████████████                    | 348kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     38% |████████████▍                   | 358kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     39% |████████████▊                   | 368kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     40% |█████████████▏                  | 378kB 1.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     42% |█████████████▌                  | 389kB 2.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     43% |█████████████▉                  | 399kB 2.8MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     44% |██████████████▏                 | 409kB 2.5MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     45% |██████████████▌                 | 419kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     46% |██████████████▉                 | 430kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     47% |███████████████▎                | 440kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     48% |███████████████▋                | 450kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     49% |████████████████                | 460kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     50% |████████████████▎               | 471kB 2.4MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     52% |████████████████▋               | 481kB 2.7MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     53% |█████████████████               | 491kB 2.5MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     54% |█████████████████▍              | 501kB 2.8MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     55% |█████████████████▊              | 512kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     56% |██████████████████              | 522kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     57% |██████████████████▍             | 532kB 2.8MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     58% |██████████████████▉             | 542kB 1.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     59% |███████████████████▏            | 552kB 2.6MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     60% |███████████████████▌            | 563kB 2.4MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     62% |███████████████████▉            | 573kB 2.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     63% |████████████████████▏           | 583kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     64% |████████████████████▌           | 593kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     65% |█████████████████████           | 604kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     66% |█████████████████████▎          | 614kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     67% |█████████████████████▋          | 624kB 1.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     68% |██████████████████████          | 634kB 2.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     69% |██████████████████████▎         | 645kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     70% |██████████████████████▊         | 655kB 2.6MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     71% |███████████████████████         | 665kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     73% |███████████████████████▍        | 675kB 3.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     74% |███████████████████████▊        | 686kB 3.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     75% |████████████████████████        | 696kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     76% |████████████████████████▌       | 706kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     77% |████████████████████████▉       | 716kB 2.5MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     78% |█████████████████████████▏      | 727kB 3.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     79% |█████████████████████████▌      | 737kB 2.7MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     80% |█████████████████████████▉      | 747kB 3.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     81% |██████████████████████████▎     | 757kB 3.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     83% |██████████████████████████▋     | 768kB 3.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     84% |███████████████████████████     | 778kB 2.1MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     85% |███████████████████████████▎    | 788kB 1.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     86% |███████████████████████████▋    | 798kB 2.7MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     87% |████████████████████████████    | 808kB 2.5MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     88% |████████████████████████████▍   | 819kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     89% |████████████████████████████▊   | 829kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     90% |█████████████████████████████   | 839kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     91% |█████████████████████████████▍  | 849kB 2.2MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     93% |█████████████████████████████▊  | 860kB 2.3MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     94% |██████████████████████████████▏ | 870kB 1.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     95% |██████████████████████████████▌ | 880kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     96% |██████████████████████████████▉ | 890kB 3.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     97% |███████████████████████████████▏| 901kB 2.6MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     98% |███████████████████████████████▌| 911kB 2.9MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     99% |████████████████████████████████| 921kB 2.0MB/s eta 0:00:01
[singsns@staging.singsns.com] out:     100% |████████████████████████████████| 931kB 644kB/s 
[singsns@staging.singsns.com] out: Installing collected packages: selenium
[singsns@staging.singsns.com] out: Successfully installed selenium-3.6.0
[singsns@staging.singsns.com] out: 

[singsns@staging.singsns.com] run: cd /home/singsns/sites/staging.singsns.com/source && ../virtualenv/bin/python3 manage.py migrate --noinput
[singsns@staging.singsns.com] out: Operations to perform:
[singsns@staging.singsns.com] out:   Apply all migrations: admin, auth, contenttypes, lists, sessions
[singsns@staging.singsns.com] out: Running migrations:
[singsns@staging.singsns.com] out:   No migrations to apply.
[singsns@staging.singsns.com] out: 


Done.
Disconnecting from singsns@staging.singsns.com... done.
~~~            

- Bad Request (400) django setting.py debug =false
    - ALLOWED_HOSTS 의 값이 존재하면 bad request 400 에러 남 
    - [참고자료](http://yujuwon.tistory.com/entry/Django-DEBUG-False-%EC%84%A4%EC%A0%95-%EC%8B%9C-Bad-Request-%EB%B0%9C%EC%83%9D)
 
~~~
DEBUG = True

ALLOWED_HOSTS = ['*']
~~~

- /source/deploy_tools/fabfile.py
~~~
def _update_settings(source_folder, site_name):
    settings_path = source_folder+'/superlists/settings.py'
    sed(settings_path,"DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        # 'ALLOWED_HOSTS = ["%s"]' % (site_name,)
        'ALLOWED_HOSTS = ["*"]'
    )
~~~

## 실서버 배포 

- 서버에 소스 생성 
~~~
$ fab deploy:host=singsns@singsns.com 


[singsns@singsns.com] Executing task 'deploy'
[singsns@singsns.com] run: mkdir -p /home/singsns/sites/singsns.com/database
[singsns@singsns.com] Login password for 'singsns': 
[singsns@singsns.com] run: mkdir -p /home/singsns/sites/singsns.com/virtualenv
[singsns@singsns.com] run: mkdir -p /home/singsns/sites/singsns.com/source
[singsns@singsns.com] run: git clone https://github.com/lux600/dev_testdriven_django /home/singsns/sites/singsns.com/source
[singsns@singsns.com] out: Cloning into '/home/singsns/sites/singsns.com/source'...
[singsns@singsns.com] out: remote: Counting objects: 307, done.
[singsns@singsns.com] out: remote: Compressing objects:   0% (1/166)   
[singsns@singsns.com] out: remote: Compressing objects:   1% (2/166)   
[singsns@singsns.com] out: remote: Compressing objects:   2% (4/166)   
[singsns@singsns.com] out: remote: Compressing objects:   3% (5/166)   
[singsns@singsns.com] out: remote: Compressing objects:   4% (7/166)   
[singsns@singsns.com] out: remote: Compressing objects:   5% (9/166)   
[singsns@singsns.com] out: remote: Compressing objects:   6% (10/166)   
[singsns@singsns.com] out: remote: Compressing objects:   7% (12/166)   
[singsns@singsns.com] out: remote: Compressing objects:   8% (14/166)   
[singsns@singsns.com] out: remote: Compressing objects:   9% (15/166)   
[singsns@singsns.com] out: remote: Compressing objects:  10% (17/166)   
[singsns@singsns.com] out: remote: Compressing objects:  11% (19/166)   
[singsns@singsns.com] out: remote: Compressing objects:  12% (20/166)   
[singsns@singsns.com] out: remote: Compressing objects:  13% (22/166)   
[singsns@singsns.com] out: remote: Compressing objects:  14% (24/166)   
[singsns@singsns.com] out: remote: Compressing objects:  15% (25/166)   
[singsns@singsns.com] out: remote: Compressing objects:  16% (27/166)   
[singsns@singsns.com] out: remote: Compressing objects:  17% (29/166)   
[singsns@singsns.com] out: remote: Compressing objects:  18% (30/166)   
[singsns@singsns.com] out: remote: Compressing objects:  19% (32/166)   
[singsns@singsns.com] out: remote: Compressing objects:  20% (34/166)   
[singsns@singsns.com] out: remote: Compressing objects:  21% (35/166)   
[singsns@singsns.com] out: remote: Compressing objects:  22% (37/166)   
[singsns@singsns.com] out: remote: Compressing objects:  23% (39/166)   
[singsns@singsns.com] out: remote: Compressing objects:  24% (40/166)   
[singsns@singsns.com] out: remote: Compressing objects:  25% (42/166)   
[singsns@singsns.com] out: remote: Compressing objects:  26% (44/166)   
[singsns@singsns.com] out: remote: Compressing objects:  27% (45/166)   
[singsns@singsns.com] out: remote: Compressing objects:  28% (47/166)   
[singsns@singsns.com] out: remote: Compressing objects:  29% (49/166)   
[singsns@singsns.com] out: remote: Compressing objects:  30% (50/166)   
[singsns@singsns.com] out: remote: Compressing objects:  31% (52/166)   
[singsns@singsns.com] out: remote: Compressing objects:  32% (54/166)   
[singsns@singsns.com] out: remote: Compressing objects:  33% (55/166)   
[singsns@singsns.com] out: remote: Compressing objects:  34% (57/166)   
[singsns@singsns.com] out: remote: Compressing objects:  35% (59/166)   
[singsns@singsns.com] out: remote: Compressing objects:  36% (60/166)   
[singsns@singsns.com] out: remote: Compressing objects:  37% (62/166)   
[singsns@singsns.com] out: remote: Compressing objects:  38% (64/166)   
[singsns@singsns.com] out: remote: Compressing objects:  39% (65/166)   
[singsns@singsns.com] out: remote: Compressing objects:  40% (67/166)   
[singsns@singsns.com] out: remote: Compressing objects:  41% (69/166)   
[singsns@singsns.com] out: remote: Compressing objects:  42% (70/166)   
[singsns@singsns.com] out: remote: Compressing objects:  43% (72/166)   
[singsns@singsns.com] out: remote: Compressing objects:  44% (74/166)   
[singsns@singsns.com] out: remote: Compressing objects:  45% (75/166)   
[singsns@singsns.com] out: remote: Compressing objects:  46% (77/166)   
[singsns@singsns.com] out: remote: Compressing objects:  47% (79/166)   
[singsns@singsns.com] out: remote: Compressing objects:  48% (80/166)   
[singsns@singsns.com] out: remote: Compressing objects:  49% (82/166)   
[singsns@singsns.com] out: remote: Compressing objects:  50% (83/166)   
[singsns@singsns.com] out: remote: Compressing objects:  51% (85/166)   
[singsns@singsns.com] out: remote: Compressing objects:  52% (87/166)   
[singsns@singsns.com] out: remote: Compressing objects:  53% (88/166)   
[singsns@singsns.com] out: remote: Compressing objects:  54% (90/166)   
[singsns@singsns.com] out: remote: Compressing objects:  55% (92/166)   
[singsns@singsns.com] out: remote: Compressing objects:  56% (93/166)   
[singsns@singsns.com] out: remote: Compressing objects:  57% (95/166)   
[singsns@singsns.com] out: remote: Compressing objects:  58% (97/166)   
[singsns@singsns.com] out: remote: Compressing objects:  59% (98/166)   
[singsns@singsns.com] out: remote: Compressing objects:  60% (100/166)   
[singsns@singsns.com] out: remote: Compressing objects:  61% (102/166)   
[singsns@singsns.com] out: remote: Compressing objects:  62% (103/166)   
[singsns@singsns.com] out: remote: Compressing objects:  63% (105/166)   
[singsns@singsns.com] out: remote: Compressing objects:  64% (107/166)   
[singsns@singsns.com] out: remote: Compressing objects:  65% (108/166)   
[singsns@singsns.com] out: remote: Compressing objects:  66% (110/166)   
[singsns@singsns.com] out: remote: Compressing objects:  67% (112/166)   
[singsns@singsns.com] out: remote: Compressing objects:  68% (113/166)   
[singsns@singsns.com] out: remote: Compressing objects:  69% (115/166)   
[singsns@singsns.com] out: remote: Compressing objects:  70% (117/166)   
[singsns@singsns.com] out: remote: Compressing objects:  71% (118/166)   
[singsns@singsns.com] out: remote: Compressing objects:  72% (120/166)   
[singsns@singsns.com] out: remote: Compressing objects:  73% (122/166)   
[singsns@singsns.com] out: remote: Compressing objects:  74% (123/166)   
[singsns@singsns.com] out: remote: Compressing objects:  75% (125/166)   
[singsns@singsns.com] out: remote: Compressing objects:  76% (127/166)   
[singsns@singsns.com] out: remote: Compressing objects:  77% (128/166)   
[singsns@singsns.com] out: remote: Compressing objects:  78% (130/166)   
[singsns@singsns.com] out: remote: Compressing objects:  79% (132/166)   
[singsns@singsns.com] out: remote: Compressing objects:  80% (133/166)   
[singsns@singsns.com] out: remote: Compressing objects:  81% (135/166)   
[singsns@singsns.com] out: remote: Compressing objects:  82% (137/166)   
[singsns@singsns.com] out: remote: Compressing objects:  83% (138/166)   
[singsns@singsns.com] out: remote: Compressing objects:  84% (140/166)   
[singsns@singsns.com] out: remote: Compressing objects:  85% (142/166)   
[singsns@singsns.com] out: remote: Compressing objects:  86% (143/166)   
[singsns@singsns.com] out: remote: Compressing objects:  87% (145/166)   
[singsns@singsns.com] out: remote: Compressing objects:  88% (147/166)   
[singsns@singsns.com] out: remote: Compressing objects:  89% (148/166)   
[singsns@singsns.com] out: remote: Compressing objects:  90% (150/166)   
[singsns@singsns.com] out: remote: Compressing objects:  91% (152/166)   
[singsns@singsns.com] out: remote: Compressing objects:  92% (153/166)   
[singsns@singsns.com] out: remote: Compressing objects:  93% (155/166)   
[singsns@singsns.com] out: remote: Compressing objects:  94% (157/166)   
[singsns@singsns.com] out: remote: Compressing objects:  95% (158/166)   
[singsns@singsns.com] out: remote: Compressing objects:  96% (160/166)   
[singsns@singsns.com] out: remote: Compressing objects:  97% (162/166)   
[singsns@singsns.com] out: remote: Compressing objects:  98% (163/166)   
[singsns@singsns.com] out: remote: Compressing objects:  99% (165/166)   
[singsns@singsns.com] out: remote: Compressing objects: 100% (166/166)   
[singsns@singsns.com] out: remote: Compressing objects: 100% (166/166), done.
[singsns@singsns.com] out: Receiving objects:   0% (1/307)   
[singsns@singsns.com] out: Receiving objects:   1% (4/307)   
[singsns@singsns.com] out: Receiving objects:   2% (7/307)   
[singsns@singsns.com] out: Receiving objects:   3% (10/307)   
[singsns@singsns.com] out: Receiving objects:   4% (13/307)   
[singsns@singsns.com] out: Receiving objects:   5% (16/307)   
[singsns@singsns.com] out: Receiving objects:   6% (19/307)   
[singsns@singsns.com] out: Receiving objects:   7% (22/307)   
[singsns@singsns.com] out: Receiving objects:   8% (25/307)   
[singsns@singsns.com] out: Receiving objects:   9% (28/307)   
[singsns@singsns.com] out: Receiving objects:  10% (31/307)   
[singsns@singsns.com] out: Receiving objects:  11% (34/307)   
[singsns@singsns.com] out: Receiving objects:  12% (37/307)   
[singsns@singsns.com] out: Receiving objects:  13% (40/307)   
[singsns@singsns.com] out: Receiving objects:  14% (43/307)   
[singsns@singsns.com] out: Receiving objects:  15% (47/307)   
[singsns@singsns.com] out: Receiving objects:  16% (50/307)   
[singsns@singsns.com] out: Receiving objects:  17% (53/307)   
[singsns@singsns.com] out: Receiving objects:  18% (56/307)   
[singsns@singsns.com] out: Receiving objects:  19% (59/307)   
[singsns@singsns.com] out: Receiving objects:  20% (62/307)   
[singsns@singsns.com] out: Receiving objects:  21% (65/307)   
[singsns@singsns.com] out: Receiving objects:  22% (68/307)   
[singsns@singsns.com] out: Receiving objects:  23% (71/307)   
[singsns@singsns.com] out: Receiving objects:  24% (74/307)   
[singsns@singsns.com] out: Receiving objects:  25% (77/307)   
[singsns@singsns.com] out: Receiving objects:  26% (80/307)   
[singsns@singsns.com] out: Receiving objects:  27% (83/307)   
[singsns@singsns.com] out: Receiving objects:  28% (86/307)   
[singsns@singsns.com] out: Receiving objects:  29% (90/307)   
[singsns@singsns.com] out: Receiving objects:  30% (93/307)   
[singsns@singsns.com] out: Receiving objects:  31% (96/307)   
[singsns@singsns.com] out: Receiving objects:  32% (99/307)   
[singsns@singsns.com] out: Receiving objects:  33% (102/307)   
[singsns@singsns.com] out: Receiving objects:  34% (105/307)   
[singsns@singsns.com] out: Receiving objects:  35% (108/307)   
[singsns@singsns.com] out: Receiving objects:  36% (111/307)   
[singsns@singsns.com] out: Receiving objects:  37% (114/307)   
[singsns@singsns.com] out: Receiving objects:  38% (117/307)   
[singsns@singsns.com] out: Receiving objects:  39% (120/307)   
[singsns@singsns.com] out: Receiving objects:  40% (123/307)   
[singsns@singsns.com] out: Receiving objects:  41% (126/307)   
[singsns@singsns.com] out: Receiving objects:  42% (129/307)   
[singsns@singsns.com] out: Receiving objects:  43% (133/307)   
[singsns@singsns.com] out: Receiving objects:  44% (136/307)   
[singsns@singsns.com] out: Receiving objects:  45% (139/307)   
[singsns@singsns.com] out: Receiving objects:  46% (142/307)   
[singsns@singsns.com] out: Receiving objects:  47% (145/307)   
[singsns@singsns.com] out: Receiving objects:  48% (148/307)   
[singsns@singsns.com] out: Receiving objects:  49% (151/307)   
[singsns@singsns.com] out: Receiving objects:  50% (154/307)   
[singsns@singsns.com] out: Receiving objects:  51% (157/307)   
[singsns@singsns.com] out: Receiving objects:  52% (160/307)   
[singsns@singsns.com] out: Receiving objects:  53% (163/307)   
[singsns@singsns.com] out: Receiving objects:  54% (166/307)   
[singsns@singsns.com] out: Receiving objects:  55% (169/307)   
[singsns@singsns.com] out: Receiving objects:  56% (172/307)   
[singsns@singsns.com] out: Receiving objects:  57% (175/307)   
[singsns@singsns.com] out: Receiving objects:  58% (179/307)   
[singsns@singsns.com] out: Receiving objects:  59% (182/307)   
[singsns@singsns.com] out: Receiving objects:  60% (185/307)   
[singsns@singsns.com] out: Receiving objects:  61% (188/307)   
[singsns@singsns.com] out: Receiving objects:  62% (191/307)   
[singsns@singsns.com] out: Receiving objects:  62% (193/307), 6.42 MiB | 6.41 MiB/s   
[singsns@singsns.com] out: Receiving objects:  62% (193/307), 16.62 MiB | 8.16 MiB/s   
[singsns@singsns.com] out: Receiving objects:  62% (193/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: remote: Total 307 (delta 173), reused 264 (delta 130), pack-reused 0
[singsns@singsns.com] out: Receiving objects:  63% (194/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  64% (197/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  65% (200/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  66% (203/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  67% (206/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  68% (209/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  69% (212/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  70% (215/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  71% (218/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  72% (222/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  73% (225/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  74% (228/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  75% (231/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  76% (234/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  77% (237/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  78% (240/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  79% (243/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  80% (246/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  81% (249/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  82% (252/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  83% (255/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  84% (258/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  85% (261/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  86% (265/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  87% (268/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  88% (271/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  89% (274/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  90% (277/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  91% (280/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  92% (283/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  93% (286/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  94% (289/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  95% (292/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  96% (295/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  97% (298/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  98% (301/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects:  99% (304/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects: 100% (307/307), 20.69 MiB | 6.81 MiB/s   
[singsns@singsns.com] out: Receiving objects: 100% (307/307), 21.14 MiB | 6.81 MiB/s, done.
[singsns@singsns.com] out: Resolving deltas:   0% (0/173)   
[singsns@singsns.com] out: Resolving deltas:  15% (27/173)   
[singsns@singsns.com] out: Resolving deltas:  16% (28/173)   
[singsns@singsns.com] out: Resolving deltas:  22% (39/173)   
[singsns@singsns.com] out: Resolving deltas:  23% (40/173)   
[singsns@singsns.com] out: Resolving deltas:  24% (43/173)   
[singsns@singsns.com] out: Resolving deltas:  25% (44/173)   
[singsns@singsns.com] out: Resolving deltas:  26% (45/173)   
[singsns@singsns.com] out: Resolving deltas:  27% (47/173)   
[singsns@singsns.com] out: Resolving deltas:  30% (52/173)   
[singsns@singsns.com] out: Resolving deltas:  34% (59/173)   
[singsns@singsns.com] out: Resolving deltas:  39% (69/173)   
[singsns@singsns.com] out: Resolving deltas:  40% (70/173)   
[singsns@singsns.com] out: Resolving deltas:  47% (82/173)   
[singsns@singsns.com] out: Resolving deltas:  48% (84/173)   
[singsns@singsns.com] out: Resolving deltas:  49% (86/173)   
[singsns@singsns.com] out: Resolving deltas:  62% (108/173)   
[singsns@singsns.com] out: Resolving deltas:  64% (112/173)   
[singsns@singsns.com] out: Resolving deltas:  73% (128/173)   
[singsns@singsns.com] out: Resolving deltas:  74% (129/173)   
[singsns@singsns.com] out: Resolving deltas:  75% (130/173)   
[singsns@singsns.com] out: Resolving deltas:  78% (136/173)   
[singsns@singsns.com] out: Resolving deltas:  79% (138/173)   
[singsns@singsns.com] out: Resolving deltas:  82% (142/173)   
[singsns@singsns.com] out: Resolving deltas:  83% (145/173)   
[singsns@singsns.com] out: Resolving deltas:  89% (155/173)   
[singsns@singsns.com] out: Resolving deltas:  92% (160/173)   
[singsns@singsns.com] out: Resolving deltas:  94% (163/173)   
[singsns@singsns.com] out: Resolving deltas:  95% (165/173)   
[singsns@singsns.com] out: Resolving deltas:  96% (167/173)   
[singsns@singsns.com] out: Resolving deltas:  97% (168/173)   
[singsns@singsns.com] out: Resolving deltas:  99% (172/173)   
[singsns@singsns.com] out: Resolving deltas: 100% (173/173)   
[singsns@singsns.com] out: Resolving deltas: 100% (173/173), done.
[singsns@singsns.com] out: Checking connectivity... done.
[singsns@singsns.com] out: 

[localhost] local: git log -n 1 --format=%H
[singsns@singsns.com] run: cd /home/singsns/sites/singsns.com/source && git reset --hard c69f596fb2fa9a435f57f04cb5aca899e649c96c
[singsns@singsns.com] out: HEAD is now at c69f596 deploy_tools/fabpile.py 설정
[singsns@singsns.com] out: 

[singsns@singsns.com] run: sed -i.bak -r -e 's/DEBUG = True/DEBUG = False/g' "$(echo /home/singsns/sites/singsns.com/source/superlists/settings.py)"
[singsns@singsns.com] run: sed -i.bak -r -e 's/ALLOWED_HOSTS =.+$/ALLOWED_HOSTS = ["*"]/g' "$(echo /home/singsns/sites/singsns.com/source/superlists/settings.py)"
[singsns@singsns.com] run: echo 'SECRET_KEY ='\\''_k79kz(n3u%l(_+)k8re+)(7u(5j)t84r9%l$ltf8%$+(zeind'\\''' >> "$(echo /home/singsns/sites/singsns.com/source/superlists/secret_key.py)"
[singsns@singsns.com] run: echo '
from .secret_key import SECRET_KEY' >> "$(echo /home/singsns/sites/singsns.com/source/superlists/settings.py)"
[singsns@singsns.com] run: virtualenv --python=python3 /home/singsns/sites/singsns.com/source/../virtualenv
[singsns@singsns.com] out: Already using interpreter /usr/bin/python3
[singsns@singsns.com] out: Using base prefix '/usr'
[singsns@singsns.com] out: New python executable in /home/singsns/sites/singsns.com/virtualenv/bin/python3
[singsns@singsns.com] out: Also creating executable in /home/singsns/sites/singsns.com/virtualenv/bin/python
[singsns@singsns.com] out: Installing setuptools, pip, wheel...done.
[singsns@singsns.com] out: 

[singsns@singsns.com] run: /home/singsns/sites/singsns.com/source/../virtualenv/bin/pip install -r /home/singsns/sites/singsns.com/source/requirements.txt
[singsns@singsns.com] out: Collecting Django==1.10 (from -r /home/singsns/sites/singsns.com/source/requirements.txt (line 1))
[singsns@singsns.com] out:   Using cached Django-1.10-py2.py3-none-any.whl
[singsns@singsns.com] out: Collecting selenium==3.6.0 (from -r /home/singsns/sites/singsns.com/source/requirements.txt (line 2))
[singsns@singsns.com] out:   Using cached selenium-3.6.0-py2.py3-none-any.whl
[singsns@singsns.com] out: Installing collected packages: Django, selenium
[singsns@singsns.com] out: Successfully installed Django-1.10 selenium-3.6.0
[singsns@singsns.com] out: 

[singsns@singsns.com] run: cd /home/singsns/sites/singsns.com/source && ../virtualenv/bin/python3 manage.py migrate --noinput
[singsns@singsns.com] out: Operations to perform:
[singsns@singsns.com] out:   Apply all migrations: admin, auth, contenttypes, lists, sessions
[singsns@singsns.com] out: Running migrations:
[singsns@singsns.com] out:   Rendering model states... DONE
[singsns@singsns.com] out:   Applying contenttypes.0001_initial... OK
[singsns@singsns.com] out:   Applying auth.0001_initial... OK
[singsns@singsns.com] out:   Applying admin.0001_initial... OK
[singsns@singsns.com] out:   Applying admin.0002_logentry_remove_auto_add... OK
[singsns@singsns.com] out:   Applying contenttypes.0002_remove_content_type_name... OK
[singsns@singsns.com] out:   Applying auth.0002_alter_permission_name_max_length... OK
[singsns@singsns.com] out:   Applying auth.0003_alter_user_email_max_length... OK
[singsns@singsns.com] out:   Applying auth.0004_alter_user_username_opts... OK
[singsns@singsns.com] out:   Applying auth.0005_alter_user_last_login_null... OK
[singsns@singsns.com] out:   Applying auth.0006_require_contenttypes_0002... OK
[singsns@singsns.com] out:   Applying auth.0007_alter_validators_add_error_messages... OK
[singsns@singsns.com] out:   Applying auth.0008_alter_user_username_max_length... OK
[singsns@singsns.com] out:   Applying lists.0001_initial... OK
[singsns@singsns.com] out:   Applying lists.0002_item_text... OK
[singsns@singsns.com] out:   Applying lists.0003_auto_20171016_0235... OK
[singsns@singsns.com] out:   Applying sessions.0001_initial... OK
[singsns@singsns.com] out: 


Done.
Disconnecting from singsns@singsns.com... done.
~~~

- /etc/nginx/sites-available/singsns.com 파일 만들기 
~~~
signsns@server:~/sites/singsns.com/source$ sed "s/SITENAME/singsns.com/g" \ 
deploy_tools/nginx.template.conf | sudo tee \
/etc/nginx/sites-available/singsns.com
~~~
        
- 위의 설정파일 활성화, link 만들기 
~~~
singsns@server:/etc/nginx/sites-available$ sudo ln -s ../sites-available/singsns.com \ 
    /etc/nginx/sites-enabled/singsns.com
~~~    

- systemd 스크립트 파일 작성 
    - multiple gunicorn.service 
    - [참조](http://codejaxy.com/q/261541/django-server-gunicorn-systemd-how-to-run-multiple-django-app-gunicorn-systemd)
~~~
singsns@server:~/sites/singsns.com/source$ sed "s/SITENAME/singsns.com/g" \
        deploy_tools/gunicorn-systemd.template.conf | sudo tee \
        /etc/systemd/system/gunicorn_singsns.service
~~~      

- gunicorn 생성 파일 
~~~
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=singsns
Group=www-data
WorkingDirectory=/home/singsns/sites/singsns.com/source
ExecStart=/home/singsns/sites/singsns.com/virtualenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/tmp/singsns.com
.socket superlists.wsgi:application

[Install]
WantedBy=multi-user.target
~~~  
                
## Nginx , gunicorn 재시작 
~~~
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
                                         
$ sudo systemctl restart nginx
# $ sudo nginx -t && sudo systemctl restart nginx
~~~                                         
                    
    
                        
                                        
                                                            
    