virtualenv -p python3.4 .   (마지막에 점이나 디렉토리 선정)
pip install django==1.10
pip install psycopg2

pip install awsebcli

pip freeze > requirements.txt
pip freeze -r requirements.txt

django-admin startproject mysite .
python manage.py createsuperuser

Ubuntu Xenial (16.04) 에서 postgresql 9.6 설치 

sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6

<postgresql 사용설명 >
http://acpi.tistory.com/69

sudo -u postgres psql

<아마존 RDS> 
http://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html


ssh -i "RemannKeyPairAws.pem" ubuntu@ec2-13-124-52-53.ap-northeast-2.compute.amazonaws.com

sudo service nginx restart
sudo service mysite restart 

sudo tail -f ./uwsgi/mysite.log

sudo service nginx restart 
sudo service mysite restart && sudo tail -f ./uwsgi/mysite.log

http://13.124.52.53/

http://ec2-13-124-52-53.ap-northeast-2.compute.amazonaws.com:8000/

<rds:>    
remannrds.czgkyfidohea.ap-northeast-2.rds.amazonaws.com


git push -u origin master