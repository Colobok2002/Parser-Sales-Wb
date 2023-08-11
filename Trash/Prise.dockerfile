
FROM python:3.9

USER root

# Установка дополнительных зависимостей
RUN apt-get update && \
    apt-get install -y wget gnupg ca-certificates && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Установка дополнительных инструментов (по вашему выбору)
RUN apt-get install -y curl

# Установка Python и зависимостей

WORKDIR /.
RUN pip install --upgrade pip
COPY requments.txt .
RUN pip install -r requments.txt
ENV TZ=Europe/Moscow

# Копирование файлов
COPY . .

# Команда для запуска вашего скрипта

CMD ["python", "prise.py"]


