# Скачивание фотоснимков с сайтов NASA и SpaceX

Данная программа позволяет, используя API, скачивать фотографии с сайтов SpaceX и NASA и 
публиковать их в телеграм-канале с заданной периодичностью

## Как работает

По умолчанию, в директории, где расположен скрипт, создается папка "images", куда загружаются 
медиафайлы. Если используете скрипт для загрузки с сайтов NASA, SpaceX - директория будет 
создана автоматически, иначе - создайте его вручную и добавьте в нее медиафайлы 
(форматы: png, jpg, jpeg). 

Загрузка файлов:
* Чтобы скачать фотографии, сделанных при пуске кораблей SpaceX, необходимо в командной строке указать id пуска. 
По умолчанию будут загружены фотоснимки с последнего доступного пуска.
* Чтобы скачать мадиаматериалы с сайта NASA из раздела [APOD](https://apod.nasa.gov/apod/astropix.html) (Astronomy Picture of the Day),
необходимо в командной строке указать количество файлов. По умолчанию скачается 1 медиафайл.
* Чтобы скачать мадиаматериалы с сайта NASA из раздела [EPIC](https://epic.gsfc.nasa.gov/) (Earth Polychromatic Imaging Camera),
необходимо в командной строке указать дату. По умолчанию будут скачаны файлы с последней доступной даты.

Запуск телеграм-бота:
* Чтобы выполнить запуск бота, в командной строке в качестве опциональных аргументов укажите:
периодичность публикации в секундах, файл для публикации в канале. 
* По умолчанию - бот публикует файлы каждые 4 часа (14400 секунд) и выбирает случайный файл для публикации. 
* Публикация файлов продолжится с заданной периодичностью, в случайном порядке в бесконечном цикле.


### Как установить

* Python3 должен уже быть установлен.
* Для изоляции проекта рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html).
* Чтобы развернуть зависимости используйте **`pip`** (или **`pip3`**, если есть конфликт с Python2):

```bash
pip install -r requirements.txt
```

### Авторизация

#### Получения API-KEY на сайте NASA:

1. Зарегистрируйтесь на сайте [https://api.nasa.gov/](https://api.nasa.gov/), получите api-key, 
например такой: **Zg8r1mb4mPl0PegSGPdac1977542fecf00231da7**.
2. Полученный ключ запишите в переменную окружения .env, например:
**```NASA_API_KEY=Zg8r1mb4mPl0PegSGPdac1977542fecf00231da7```**

#### Создание бота в Телеграме:

1. Перейдите в диалог с инструментом для разработки чатов — [https://telegram.me/BotFather](https://telegram.me/BotFather).
2. Нажмите кнопку "Start" или введите в диалоге команду /start.
3. Далее введите команду /newbot, чтобы сделать новый бот.
4. Укажите название — как будет отображаться чат в списке контактов.
5. Последнее — системное имя: это то, что будет ником после знака @. 
Cистемное имя обязательно должно быть уникальным. Если имя уже занято, вы увидите подсказку: "Sorry, this username is already taken. 
Please try something different".

![image](https://developers.sber.ru/help/assets/ideal-img/telegram-chat-bot.32e2f94.941.png)

6. После успешного создания вы получите токен HTTP API. 

![image](https://developers.sber.ru/help/assets/ideal-img/ti1.12da233.939.png)

7. Сохраните его в переменной окружения .env, например:
**```TG_TOKEN=5928746033:AAE3Ex1sGrTQCdFXXXXPgmfON8d2L85dVJQ```**.

#### Создание канала в Телеграме:

1. В основном меню приложения Телеграм выбрать "Создать канал".

![image](https://smmplanner.com/blog/content/images/size/w1000/2022/09/7-sozdanie-kanala.jpg)

2. Укажите название, добавьте описание, выберите тип канала.

![image](https://smmplanner.com/blog/content/images/size/w1000/2022/09/9-finalnaya-nastrojka.jpg)

3. Добавьте свой бот в администраторы канала, укажите разрешения.
4. Системное имя телеграм-канала (начинается со знака @) сохраните в переменной окружения .env, 
например:
**```CHANNEL_CHAT_ID=@mychannel```**

### Примеры

Для получения справки используйте аргумент ```-h``` или ```--help```.

1. Загрузка с сайта SpaceX:\
В терминале запустите файл **```fetch_spacex_images.py```** введите необязательный 
параметр **```-l```**  или **```--launch_id```** в качестве позиционного аргумента
```bash
python fetch_spacex_images.py -l 5eb87d42ffd86e000604b384
```

2. Загрузка с сайта NASA APOD:\
В терминале запустите файл **```fetch_nasa_apod_images.py```** введите необязательный 
параметр **```-c```**  или **```--count```** в качестве позиционного аргумента.
```bash
python fetch_nasa_apod_images.py -c 10
```

3. Загрузка с сайта NASA EPIC:\
В терминале запустите файл **```fetch_nasa_epic_images.py```** введите необязательный 
параметр **```-ed```**  или **```--epic_date```** в качестве позиционного аргумента.
```bash
python fetch_nasa_epic_images.py -ed 2023-01-17
```

4. Запуск бота:\
В терминале запустите файл **```tg_bot.py```** введите один или все необязательные позиционные аргументы:
* число после флага **```-rs```**  или **```--rotation_seconds```** (секунды).\
К примеру, публикация фото каждые 10 минут (10 * 60 = 600 секунд) будет выглядеть так:
```bash
python tg_bot.py -rs 600
```
* название файла после флага **```-f```**  или **```--file```**, например:
```bash
python tg_bot.py -f spacex_1.jpeg
```
* или оба параметра сразу:
```bash
python tg_bot.py -rs 600 -f spacex_1.jpeg
```

Для остановки бота нажмите сочетание клавиш **```CTRL```** + **```С```** для вызова **```KeyboardInterrupt```**.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.prg).

### Лицензия

Этот проект лицензирован по лицензии MIT - подробности см. в файле [ЛИЦЕНЗИЯ](LICENSE).
