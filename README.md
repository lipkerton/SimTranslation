

# Краткое описание #
Скрипт переводит xprt/xml проекты SimInTech на английский/китайский язык.

---

# Принцип работы #
+ Запуск:
    1. Cоздается словарь на основе базового словаря (**базовый словарь - dictionaries/base_translations.csv**, **создаваемый словарь - translations.db**).
    2. Создаются файлы, которые отражают **текущее состояние словаря в двух форматах (csv, txt) - dictionaries/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt**.
    3. Включается интерфейс.
    4. Пользователь выставляет настройки для папки ввода и папки вывода.
    5. Нажимает кнопку перевода.
+ Процесс перевода:
    1. Скрипт берет структуру исходной директории, создает ее копию в директории вывода.
    2. Скрипт ищет русский текст в xprt/xml документе **по тегам 'plot'/'title', 'bottomaxis'/'title', 'leftaxis'/'title', 'series'/'title', 'data'/'value'** (выбор нужного тега он выполняет с дополнительными условиями).
    3. Ищет текст в словаре dictionaries/translations.db.
    4. Если текст отсутствует в словарe dictionaries/translations.db, то выполняется процедура перевода.
    5. Исходная строка текста подменяется на переведенную с полным сохранением кажого служебного символа - логика работы проекта не должна быть нарушена.
    6. Каждый файл формата xprt/xml подвергается процедуре перевода на выбранный пользователем язык, затем переведенная копия попадает в то место скопированной структуры, где был ее оригинал.
    7. Каждый файл иного формата просто копируется в то же место скопированной структуры в папке вывода.
+ Окончание работы:
    1. Когда работа над выбранной директорией завершена в окне вывода появятся все переводы, которые были сделаны именно с помощью машинного перевода - это означает, что они отсутствуют в словаре dictionaries/decoded_dictionary.pkl.
    2. Пользователь имеет возможность коректировать переводы прямо в окне вывода (в формате <русское слово>;<английский перевод>;<китайский перевод>) и имеет возможность сразу же их сохранить в словарь dictionaries/decoded_dictionary.pkl.
    3. Пользователь имеет возможность открыть текущее состояние словаря dictionaries/translations.db (документы dictionaries/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt) и выполнить корректировку словаря прямо там, с последующим сохранением изменений в интерфейсе скрипта с помощью кнопок.

---

# Кнопки интерфейса #
+ **'Open...'** - кнопка активирует процесс поиска папки ввода/вывода
+ **Кнопки выбора языка** - точка на определенном языке означает, что он выбран для перевода (после нажатия кнопки 'Translate' и до окончания процедуры перевода выбор языка ни на что не повлияет).
+ **'Translate'** - запускает выбранную папку и xprt/xml файлы в ней на перевод.
    + Пока процесс перевода не завершен изменить словарь dictionaries/translations.db невозможно.
    + Кнопка 'Translate' будет заблокирована до окончания перевода.
+ **'Quick save changes'** - все переводы в окне вывода будут сохранены в словарь dictionaries/translations.db
    + Если для перевода указан верный формат - он исчезнет из окна; это значит, что он попал в словарь и будет использован.
    + Если для перевода указан неверный формат - он останется в окне; это значит, что он не сохранен, не попал в словарь и не будет использован.
    + До сохранения в словарь ни один из переводов не будет использован - все случаи несохраненных переводов будут переводиться машинным способом (программа будет дольше работать).
+ **Кнопки выбора формата** - точка на определенном формате означает, что он был выбран для демонстрации и для выполнения обновлений словаря.
+ **'Update dictionary'** - все изменения, которые были внесены в документы dictionaries/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt, будут сохранены в словарь.
+ **'Open full dictionary'** - будет открыто **текущее состояние** словаря dictionaries/translations.db
    + Если какие-то изменения вносились в документы dictionaries/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt и не были сохранены с помощью 'Update dictionary' - они будут удалены.

---

# Файлы и папки программы #
+ **'dictionaries'** - папка, которая хранит все словари.
    + 'base_translations.csv' - русско-англйиско-китайский словарь; является копией встроенного словаря SimInTech с добавлением китайских переводов - он никогда не будет изменяться, если только встроенный в SimInTech словарь не будет изменен.
    + 'translations.db' - центральный словарь скрипта, используется для хранения базовых переводов, новых переводов и т.д.
    + 'dictionary_current_state.txt' - словарь, который описывает текущее состояние словаря 'decoded_dictionary.pkl' в формате txt.
    + 'dictionary_current_state.csv' - словарь, который описывает текущее состояние словаря 'decoded_dictionary.pkl' в формате csv.
+ **'launcher_windows'** - папка, которая содержит исполняющий файл.
+ **'methods'** - папка, которая содержит основные py-файлы программы.
    + '__pycache__' - оно вам не надо.
    + '__init__.py' - пустой файл, но он нужен, чтобы папка 'methods' для python считалась пакетом и чтобы из нее можно было импортировать фукнции с использованием относительного пути.
    + 'classes.py' - файл, который содержит три класса Word, RunSettings, DictionaryInit.
    + 'constants.py' - здесь хранятся пути проекта.
    + 'test_interface.py' - код интерфейса + пуск программы с помощью функции 'core_pattern'.
    + 'test_xml_line_parsing.py' - логика перевода реализуется здесь с момента взятия файла из исходной папки: файл попадает сюда и начинается парсинг файла.
+ **'trans_support_files_dirs'** - вспомогательные файлы и папки. Они не используются для реализации основной логики, но здесь храняться логи и список абсолютных путей для выходных файлов.
+ **'main.py'** - центральный файл программы: он запускает все остальные файлы на исполнение (при манульном запуске).

---

# Brief description #
Script translates SimInTech's xprt/xml projects into English/Chinese.

---

# Working principle #
+ Startup:
    1. A dictionary is created based on the base dictionary (**base dictionary - dictionaries/base_translations.csv**, **created dictionary - translations.db**).
    2. Files that reflect the **current state of the dictionary in two formats (csv, txt) are created - dictionaries/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt**.
    3. The interface is enabled.
    4. The user sets the settings for the input folder and output folder.
    5. Presses the translation button.
+ Translation process:
    1. The script takes the structure of the source directory, creates a copy of it in the output directory.
    2. The script searches for Russian text in xprt/xml document ** by tags 'plot'/'title', 'bottomaxis'/'title', 'leftaxis'/'title', 'series'/'title', 'data'/'value'** (it selects the right tag with additional conditions).
    3. searches for text in dictionaries/translations.db.
    4. If the text does not exist in dictionaries/decoded_dictionary.pkl, it performs a translation procedure.
    5. The original text string is replaced by the translated one with full preservation of each service character - the logic of the project should not be broken.
    6. Each xprt/xml file is subjected to the procedure of translation into the language chosen by the user, then the translated copy falls into the place of the copied structure where the original was.
    7. Each file of a different format is simply copied to the same location of the copied structure in the output folder.
+ End of work:
    1. When the work on the selected directory is complete, the output window will show all translations that were done exactly by machine translation - this means that they are missing from dictionaries/translations.db.
    2. The user can correct translations directly in the output window (in the format <Russian word>;<English translation>;<Chinese translation>) and can immediately save them to the dictionaries/translations.db.
    3. The user has an opportunity to open the current state of the dictionary dictionaries/decoded_dictionary.pkl (documents dictionaries/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt) and perform dictionary corrections right there, with subsequent saving of changes in the script interface using the buttons.

---

# Interface buttons #
+ **'Open...'** - the button activates the process of searching for the I/O folder
+ **'Language selection buttons** - a dot on a certain language means that it is selected for translation (after pressing the 'Translate' button and until the end of the translation procedure the language selection will not affect anything).
+ **'Translate'** - starts the selected folder and xprt/xml files in it for translation.
    + Until the translation process is completed, the dictionaries/translations.db cannot be changed.
    + The 'Translate' button will be locked until the translation is complete.
+ **'Quick save changes'** - all translations in the output window will be saved to the dictionaries/translations.db dictionary.
    + If a correct format is specified for a translation - it will disappear from the window; it means that it has been added to the dictionary and will be used.
    + If an incorrect format is specified for the translation, it will remain in the window; this means that it has not been saved, has not entered the dictionary, and will not be used.
    + None of the translations will be used until they are saved to the dictionary - all cases of unsaved translations will be machine translated (the program will work longer).
+ **'Format selection buttons** - a dot on a particular format means that it has been selected for demonstration and for performing dictionary updates.
+ **'Update dictionary'** - all changes that were made to the documents dictionaries/dictionary/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt will be saved to the dictionary.
+ **'Open full dictionary'** - the **current state** of dictionaries/dictionaries/translations.db will be opened.
    + If any changes were made to the documents dictionaries/dictionary/dictionary_current_state.csv, dictionaries/dictionary_current_state.txt and were not saved using 'Update dictionary' - they will be deleted.

---

# Program files and folders #
+ **'dictionaries'** - folder that stores all dictionaries.
    + 'base_translations.csv' - Russian-English-Chinese dictionary; it is a copy of SimInTech built-in dictionary with Chinese translations added - it will never be changed unless SimInTech built-in dictionary is changed.
    + 'translations.db' - central dictionary of the script, used to store basic translations, new translations, etc.
    + 'dictionary_current_state.txt' - dictionary that describes the current state of the 'decoded_dictionary.pkl' dictionary in txt format.
    + 'dictionary_current_state.csv' is a dictionary that describes the current state of the 'decoded_dictionary.pkl' dictionary in csv format.
+ **'launcher_windows'** - folder that contains the executable file.
+ **'methods'** - the folder that contains the main py-files of the program.
+ '__pycache__' - you don't need it.
    + '__init__.py' - an empty file, but it is needed for the 'methods' folder to be considered a package for python and to be able to import functions from it using relative path.
+ 'classes.py' - a file that contains the three classes Word, RunSettings, DictionaryInit.
    + 'constants.py' - this is where the project paths are stored.
+ 'test_interface.py' - interface code + start the program using the 'core_pattern' function.
    + 'test_xml_line_parsing.py' - translation logic is implemented here from the moment the file is taken from the source folder: the file gets here and parsing of the file starts.
+ **'trans_support_files_dirs'** - auxiliary files and folders. They are not used to implement the main logic, but logs and a list of absolute paths for output files are stored here.
+ **'main.py'** - the central file of the program: it starts all other files for execution (at manual startup).