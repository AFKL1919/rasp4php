FROM python:stretch

RUN mkdir /code
WORKDIR /code
COPY . /code

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pipenv install --system

# RUN apt update
# RUN apt-get install -y apt-transport-https curl
# RUN curl -v -k https://packages.sury.org/php/apt.gpg | apt-key add -
# RUN echo "deb https://packages.sury.org/php/ stretch main" | tee /etc/apt/sources.list.d/php5.list
RUN sed -i 's#http://deb.debian.org#http://mirrors.aliyun.com#g' /etc/apt/sources.list &&\
    sed -i 's|security.debian.org/debian-security|mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list &&\
    apt-get update &&\
    apt-get install -y php7.0-fpm &&\
    mkdir /run/php &&\
    cp /code/docker/rasp4php/www.conf /etc/php/7.0/fpm/pool.d/www.conf
