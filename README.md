# foodgram-project-react

[![foodgram_workflow](https://github.com/rume73/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/rume73/foodgram-project-react/actions/workflows/foodgram_workflow.yml)


## Описание
«Продуктовый помощник»
Сайт является - базой кулинарных рецептов. Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в pdf формате. Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx

## Как запустить
Клонируем проект: 
```
git clone https://github.com/rume73/foodgram-project-react.git
```
Для добавления файла .env с настройками базы данных на сервер необходимо:

Установить соединение с сервером по протоколу ssh:

  ```
  ssh username@server_address
  ```

Где username - имя пользователя, под которым будет выполнено подключение к серверу.

server_address - IP-адрес сервера или доменное имя.

Например:

  ```
  ssh praktikum@62.84.114.196
  ```

Также необходимо добавить Action secrets в репозитории на GitHub в разделе settings -> Secrets:

* DOCKER_PASSWORD - пароль от DockerHub;
* DOCKER_USERNAME - имя пользователя на DockerHub;
* HOST - ip-адрес сервера;
* SSH_KEY - приватный ssh ключ (публичный должен быть на сервере);
* Опционно:
   ```
  * TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
  * TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
   ```
## Проверка работоспособности
Теперь если внести любые изменения в проект и выполнить:

  ```
  git add .
  git commit -m "..."
  git push
  ```


Комманда git push является триггером workflow проекта. При выполнении команды git push запустится набор блоков комманд jobs (см. файл foodgram_workflow.yml). Последовательно будут выполнены следующие блоки:
  
  * tests - тестирование проекта на соответствие PEP8 и тестам pytest.

  * build_and_push_to_docker_hub - при успешном прохождении тестов собирается образ (image) для docker контейнера и отправлятеся в DockerHub

  * deploy - после отправки образа на DockerHub начинается деплой проекта на сервере. Происходит копирование следующих файлов с репозитория на сервер:
  
    ```
    1 docker-compose.yaml, необходимый для сборки четырех контейнеров:
      1.1 postgres - контейнер базы данных
      1.2 backend - контейнер Django приложения + wsgi-сервер gunicorn
      1.2 frontend - контейнер JS-React, который будет работать через nginx
      1.4 nginx - веб-сервер
    2 nginx/nginx.conf - файл кофигурации nginx сервера
    3 static - папка со статическими файлами проекта
    ```

После копировния происходит установка docker и docker-compose на сервере и начинается сборка и запуск контейнеров.

* send_message - после сборки и запуска контейнеров происходит отправка сообщения в телеграм об успешном окончании workflow

После выполнения вышеуказанных процедур необходимо установить соединение с сервером:

  ```
  ssh username@server_address
  ```

Отобразить список работающих контейнеров:

  ```
  sudo docker container ls
  ```

В списке контейнеров копировать CONTAINER ID контейнера username/foodgram-backend:latest (username - имя пользователя на DockerHub):

  ```
  CONTAINER ID   IMAGE                                COMMAND                  CREATED         STATUS                       PORTS     NAMES
8021345d9138   nginx:1.19.3                         "/docker-entrypoint.…"   7 minutes ago   Exited (0) 2 minutes ago               rume73_nginx_1
d3eb395676c6   rume73/foodgram_backend:latest       "/entrypoint.sh /bin…"   7 minutes ago   Exited (137) 2 minutes ago             rume73_backend_1
2a0bf05071ba   postgres:12.4                        "docker-entrypoint.s…"   8 minutes ago   Exited (137) 2 minutes ago             rume73_db_1
7caa47e8ad7e   rume73/foodgram_frontend:v1.0        "docker-entrypoint.s…"   8 minutes ago   Exited (0) 7 minutes ago               rume73_frontend_1
  ```

Выполнить вход в контейнер:

  ```
  sudo docker exec -it d3eb395676c6 bash
  ```

Также можно наполнить базу данных начальными тестовыми данными:

  ```
  python3 manage.py shell
  >>> from django.contrib.contenttypes.models import ContentType
  >>> ContentType.objects.all().delete()
  >>> quit()
  python manage.py loaddata dump.json
  ```
Теперь проекту доступна статика. В админке Django (http://<server_address>/admin) доступно управление данными. Если загрузить фикструры, то будет доступен superuser:

```
  user: Admin
  password: admin
  email: admin@admin.com
```

Для создания нового суперпользователя можно выполнить команду:

  ```
  $ python manage.py createsuperuser
  ```
  
Для остановки и удаления контейнеров и образов на сервере:

  ```
  sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -q)
  ```

## Автор:

* [Владимир Логинов](https://github.com/rume73)
* [Рабочий сайт Foodgram](http://62.84.114.196) http://infoodgram.ml
