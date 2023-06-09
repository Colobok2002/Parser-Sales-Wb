FROM python:3.9

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Установка переменных среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ Europe/Moscow

# Установка рабочей директории
WORKDIR /riche

# Обновление pip и установка зависимостей Python
RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip3 install -r req.txt

# Копирование проекта
COPY . .

# Запуск команды по умолчанию
CMD python main.py
