

# Краткое описание #
Скрипт переводит xprt/xml проекты SimInTech на английский

---

# Принцип работы #
1. Cоздается словарь на основе базового словаря (**базовый словарь - dictionaries/base_translations.csv**, **создаваемый словарь - translations.db**).
2. Скрипт берет структуру исходной директории, создает ее копию в директории вывода.
3. Скрипт ищет русский текст в xprt/xml документе **по тегам 'plot'/'title', 'bottomaxis'/'title', 'leftaxis'/'title', 'series'/'title', 'data'/'value'** (выбор нужного тега он выполняет с дополнительными условиями).
4. Ищет текст в словаре dictionaries/translations.db.
5. Если текст отсутствует в словарe dictionaries/translations.db, то выполняется процедура перевода.
6. Исходная строка текста подменяется на переведенную с полным сохранением кажого служебного символа - логика работы проекта не должна быть нарушена.
7. Каждый файл формата xprt/xml подвергается процедуре перевода на выбранный пользователем язык, затем переведенная копия попадает в то место скопированной структуры, где был ее оригинал.
8. Каждый файл иного формата просто копируется в то же место скопированной структуры в папке вывода.
 
---

# Как пользоваться? #
Установка виртуального окужения, активация, установка зависимостей (все делается внутри папки с проектом):

**MacOS/Linux**
```Bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```
**Windows**
```PowerShell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```
Есть вероятность что Windows откажет в исполнении файла `.\venv\Scripts\activate` - так происходит, потому что в вашем Windows по-умолчанию стоит запрет на выполнение стрёмных скриптов. Я не настаиваю, но его можно снять, если ввести:
```PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```
После снятия запрета просто повторите в папке проекта команду `.\venv\Scripts\Activate` и все дальнейшие действия.

Когда все будет установлено - можно закинуть в `main.py` в переменные `input_path` (ваши изначальные файлы) и `output_path` (папка для хранения переводов) абсолютные пути до папок с файлами.

**ИЛИ**

Вы можете просто запустить программу и передать пути к уже существующим папкам, как аргументы:
```Bash
python main.py '/example/path/to/input' 'example/path/to/output'
```


---

# А переводы можно менять? #
Да, можно. Прямо в файле `dictionaries/base_translations.csv`. Все, что нужно - написать строчку `<русское слово>;<английское слово>;`. А еще там же можно удалять слова.
Логи можно посмотреть в файле `trans_support_files_dirs/sim_log.log`.

---

# Brief description #
Script translates SimInTech's xprt/xml projects into English/Chinese.

---

# Working principle #
1. Create a dictionary based on the base dictionary (**base dictionary - dictionaries/base_translations.csv**, **create dictionary - translations.db**).
2. The script takes the structure of the source directory, creates a copy of it in the output directory.
3. The script searches for Russian text in xprt/xml document ** by tags 'plot'/'title', 'bottomaxis'/'title', 'leftaxis'/'title', 'series'/'title', 'data'/'value'** (it selects the necessary tag with additional conditions).
4. searches for text in dictionaries/translations.db.
5. If the text does not exist in the dictionaries/translations.db dictionary, it performs a translation procedure.
6. The original text string is replaced by the translated one with full preservation of each service character - the logic of the project should not be broken.
7. Each xprt/xml file is subjected to the procedure of translation into the language chosen by the user, then the translated copy falls into the place of the copied structure where the original was.
8. Each file of a different format is simply copied to the same location of the copied structure in the output folder.

 ---

 # How to use it? #
Virtual environment installation, activation, dependency installation (all done inside the project folder):

**MacOS/Linux**
```Bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```
**Windows**
```PowerShell
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```
There is a chance that Windows will refuse to execute the `.\venv\Scripts\activate` file - this happens because your Windows default setting is to disallow the execution of creepy scripts. I don't insist, but you can remove it by typing:
```PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```
After unbanning, just repeat the `.\venv\Scripts\Activate` command in the project folder and all further actions will be performed.

When everything is installed - you can throw in `main.py` in the variables `input_path` (your original files) and `output_path` (folder for storing translations) absolute paths to the file folders.

**OR**.

You can simply run the program and pass the paths to your existing folders as arguments:
```Bash
python main.py '/example/path/to/input' 'example/path/to/output'
```

---

# Can you change the translations? #
Yes, you can. Right in the `dictionaries/base_translations.csv` file. All you have to do is write the line `<Russian word>;<English word>;`. You can also delete words there.
Logs can be viewed in the `trans_support_files_dirs/sim_log.log` file.