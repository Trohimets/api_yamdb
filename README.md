# api_yamdb
api_yamdb

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в основную папку и выполнить миграции:

```
cd api_yamdb
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
