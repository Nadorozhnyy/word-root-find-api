# API to find cognate words
Задача: API должно принимать запросы на поиск корней для списка слов и возвращать ответ с соответствующим списком корней для каждого слова.

Входные данные: Запрос на поиск корней должен содержать JSON-объект со списком слов, для которых необходимо найти корни (синонимы, однокоренные слова).

## Использованные технологии:
  * python 3.7
  * Flask 2.2.3
  * Flask-RESTful 0.3.9
  * spacy 3.5.1
  * spacy-wordnet 0.1.0
  * ruwordnet 0.0.6

## Управление

### Запуск
Установить Python версии 3.7 или выше.

Установить необходимые библиотеки, указанные в файле requirements.txt.
```bash
pip install -r requirements.txt
```
Установить базы данных для библиотек spacy и ruwordnet

Для spacy (подробнее в документации https://spacy.io/usage)
```bash
python -m spacy download en_core_web_sm
```

Для ruwordnet (подробнее в документации https://github.com/avidale/python-ruwordnet)
```bash
ruwordnet download
```
Для ruwordnet необходимо отредактировать файл библиотеки venv\Lib\site-packages\ruwordnet\utils.py
в функции "get_default_session" необходимо изменить переменную engine следующим образом приведенным ниже
```bash
engine = create_engine(f'sqlite:///{filename}' +'?check_same_thread=False', echo=False)
```
Без этого изменения запрос с работающим api можно сделать один раз, на повторный выпадает ошибка "SQLite objects created in a thread can only be used in that same thread"

Запустить файл main.py.
```bash
python main.py
```

### Документация

#### Получение однокоренных слов:
* Request method: POST
* URL: http://127.0.0.1:5000/api/v1/word_roots
* Body:
    * raw: JSON with format {"words": ["some_word_1", "some_word_2",... etc]}

### Screenshot

![alt text](/screenshot/Screenshot_1.jpg?raw=true "POST screenshot")

