@echo off

:: Активируем виртуальное окружение
call venv\Scripts\activate

:: Запускаем script.py
python prise.py

:: Деактивируем виртуальное окружение после выполнения
deactivate
