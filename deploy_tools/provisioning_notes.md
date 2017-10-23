## 필요 패키지 

- nginx
- Python 3
- Git
- pip 
- virtualenv 

## Ubuntu 실행 
- sudo apt-get install nginx git python3 python3-pip
- sudo pip3 install virtualenv 

## Nginx 가상 호스트 설정 
- nginx.template.conf 참고 
    - /etc/nginx/sites-available/staging.tdd_django.com
    - SITENAME 부분을 staging.my-domain.com 으로 수정 

## systemd Job
- gunicorn-systemd.template.conf 참고  
    - /etc/systemd/system/gunicorn.service
    - SITENAME 부분을 staging.my-domain.com 으로 수정 

## 폴더 구조 
- 사용자 계정의 홈 폴더가 /home/username 이라고 가정 

- /home/username 
    - sites
        - SITENAME
            - database
            - source
            - static
            - virtualenv
            
- [ 전체설치 참고 ](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on
-ubuntu-16-04)            