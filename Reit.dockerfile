FROM python:3.9

# Установка рабочей директории
WORKDIR /.


RUN pip install --upgrade pip
COPY ./requments.txt .
RUN pip3 install -r requments.txt
ENV TZ=Europe/Moscow
COPY reit.py .

COPY . .

CMD ["python","-u", "./reit.py"]
