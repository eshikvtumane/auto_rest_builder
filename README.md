# auto_rest_builder

 - Python 3.7.7
 - SQLite

Установите зависимости:
```sh
$ pip install -r requirements.txt
```

Запустите сервер:
```sh
$ manage.py runserver
```

Доступные endpoints:
```sh
$ GET - /api/<app_label>/<model>/get/
$ POST - /api/<app_label>/<model>/add/
$ DELETE - /api/<app_label>/<model>/delete/<pk>
$ PUT - /api/<app_label>/<model>/update/<pk>
```