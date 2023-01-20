# Обрезка ссылок с помощью сервиса Bitly.

Битли - сервис для сокращения длинных ссылок и отслеживания количества переходов по ним, описание размещено на [https://bitly.com/](https://bitly.com/).

## Как работает

* При вводе в программу битлинка выведется сумма кликов по нему.
* При вводе других ссылок выводится битлинк.
* Если ввести в браузер сокращённую ссылку, то он перенаправит на правильный адрес.\
Например, https://bit.ly/3G9s8vL ведет на https://www.google.com/.


### Как установить

* Python3 должен уже быть установлен.
* Для изоляции проекта рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html).
* Чтобы развернуть зависимости используйте **`pip`** (или **`pip3`**, если есть конфликт с Python2):
```python
pip install -r requirements.txt
```

### Авторизация

1. Зарегистрируйтесь на сайте [https://bitly.com/](https://bitly.com/), а по [https://app.bitly.com/settings/api/](https://app.bitly.com/settings/api/) получите токен, например такой: **17c09e20ad155405123ac1977542fecf00231da7**.
2. Полученный токен запишите в переменную окружения .env, например:
**```BITLY_TOKEN=17c09e20ad155405123ac1977542fecf00231da7```**
3. В терминале запустите файл **```main.py```** введите нужную ссылку в качестве позиционного аргумента. 
4. Для получения справки используйте аргумент ```-h``` или ```--help```.

### Примеры.

1. Получение справки:
```python
$ python main.py -h
```
Вывод:
```
$ python main.py -h
usage: main.py [-h] link

Принимает url для проверки

positional arguments:
  link        Ввод URL

options:
  -h, --help  show this help message and exit
```
2. Сокращение ссылки:
```python
$ python main.py https://www.google.com/
```
Вывод
```python
https://bit.ly/3G9s8vL
```
3. Получение информации о переходах по короткой ссылке:
```python
$ python main.py https://bit.ly/3G9s8vL
```
Вывод
```
Количество переходов по ссылке: 6
```
4. Ошибка при вводе ссылки:
```python
$ python main.py google.com
```
Вывод
```
Недействительная ссылка: google.com
400 Client Error: Bad Request for url: https://api-ssl.bitly.com/v4/shorten
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.prg).

### Лицензия

Этот проект лицензирован по лицензии MIT - подробности см. в файле [ЛИЦЕНЗИЯ](LICENSE).
