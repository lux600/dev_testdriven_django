## 파이썬+장고 설치 
- virtualenv -p python3.4 .   (마지막에 점이나 디렉토리 선정)
- pip install django==1.10
- pip install psycopg2

<br/>

- pip install awsebcli

<br/>

- pip freeze > requirements.txt
- pip freeze -r requirements.txt

## 장고 기본 디렉토리 

- django-admin startproject mysite .
- python manage.py createsuperuser

<br/>

- Ubuntu Xenial (16.04) 에서 postgresql 9.6 설치 

<br/>
- sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
- wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
- sudo apt-get update
- sudo apt-get install postgresql-9.6

## < postgresql 사용설명> 
- http://acpi.tistory.com/69

<br/>

-  sudo -u postgres psql

## < 아마존 RDS > 
- http://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html

<br/>

- ssh -i "RemannKeyPairAws.pem" ubuntu@ec2-13-124-52-53.ap-northeast-2.compute.amazonaws.com

<br/>

- sudo service nginx restart
- sudo service mysite restart 

<br/>

- sudo tail -f ./uwsgi/mysite.log

<br/>

- sudo service nginx restart 
- sudo service mysite restart && sudo tail -f ./uwsgi/mysite.log

<br/>
- http://13.124.52.53/

<br/>

- http://ec2-13-124-52-53.ap-northeast-2.compute.amazonaws.com:8000/

<br/>

- <rds:>    
    - remannrds.czgkyfidohea.ap-northeast-2.rds.amazonaws.com

<br/>

- git push -u origin master