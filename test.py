from datetime import datetime

now = datetime.now()
date_str = "2023-06-21T07:29:46Z"
date = datetime.strptime(date_str.split('T')[0], "%Y-%m-%d")

if date.date() == now.date():
    print("Дата сегодняшняя")
else:
    print("Дата не сегодняшняя")
