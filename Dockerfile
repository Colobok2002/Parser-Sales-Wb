FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /riche

# install psycopg2 dependencies
RUN apt update

# install dependencies
RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip3 install -r req.txt
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb 
# copy project
COPY . .

