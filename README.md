# Для чего нужен проект #
Перевод отдельных тегов в .xprt-файлах с сохранением структуры и функционала изначального .xprt-файла. Создание копии изначального файла на китайском/английском языках и создание перечня всех сделанных переводов в процессе работы программы.

# Технологии #
Python

# Как развернуть проект #
Проект может быть развернут на любой системе с установленным программным обеспечением Python и pip. Чтобы активировать проект следует, находясь в корневой папке проекта, последовательно исполнить в терминале команды:

Попасть в корневую папку проекта можно с помощью команды:
+ cd <путь>
+ когда формируете путь используйте клавишу Tab

Для macOS:
+ python3 -m venv venv
+ source venv/bin/activate
+ pip3 install -r requirements.txt
Или одну команду:
+ python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt

Для Windows:
+ python3 -m venv venv
+ source venv/Scripts/activate
+ pip3 install -r requirements.txt
Или одну команду:
+ python3 -m venv venv && source venv/Scripts/activate && pip3 install -r requirements.txt
