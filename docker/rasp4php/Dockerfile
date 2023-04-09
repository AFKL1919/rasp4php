FROM python:stretch

RUN mkdir /code
WORKDIR /code
COPY . /code

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt &&\
    sed -i 's#http://deb.debian.org#http://mirrors.aliyun.com#g' /etc/apt/sources.list &&\
    sed -i 's|security.debian.org/debian-security|mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list &&\
    apt-get update &&\
    apt-get install -y php7.0-fpm &&\
    mkdir /run/php &&\
    cp /code/docker/rasp4php/www.conf /etc/php/7.0/fpm/pool.d/www.conf
