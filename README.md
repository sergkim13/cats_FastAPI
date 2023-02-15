# Тестовое задание от Wargaming.net

__________

### Тестовое задание WG Forge (Backend)

Тестовое задание можно выполнить на любом языке программирования из списка:
- Python 3
- Ruby
- Go
- Erlang
- Elixir
- Java
- Scala
- C#
- F#

За выбор функционального языка — дополнительный плюс кандидату.

Для выполнения задания нужен [PostgreSQL](https://postgrespro.ru/docs/postgresql/11/index) с базой данных, таблицами и данными. Если вы умеете пользоваться [Docker](https://docs.docker.com/), то можете взять подготовленый нами докер-контейнер, где все необходимое уже есть. Инструкции по установке Docker для вашей ОС смотрите [здесь](./docker_instructions.md).

Или вы можете подготовить окружение вручную, установив и настроив PostgreSQL. Инструкции смотрите [здесь](./manual_instructions.md). Схему и данные возьмите [здесь](./wg_forge_init.sql).

Подключившись к базе с помощью [любого клиента, который умеет работать с PostgreSQL](https://wiki.postgresql.org/wiki/PostgreSQL_Clients), вы можете изучить имеющиеся там таблицы и данные:
```
wg_forge_backend=# \d
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | cat_colors_info | table | postgres
 public | cats            | table | postgres
 public | cats_stat       | table | postgres
(3 rows)

wg_forge_backend=# select * from cats limit 2;
 name  |     color     | tail_length | whiskers_length
-------+---------------+-------------+-----------------
 Tihon | red & white   |          15 |              12
 Marfa | black & white |          13 |              11
(2 rows)
```

Первые два задания требуют написать программу, которая подключится к базе данных и выполнит там некоторые запросы на чтение и запись. Задания с 3-го по 6-е потребуют от вас реализовать веб-сервис с неким HTTP API.

Как вы уже догадались, сложность заданий возрастает. Мало того, чем дальше, тем менее четко сформулированы требования. Так что вам понадобятся навыки не только программирования, но и проектирования. Например, вам нужно будет самим придумать, как именно обрабатывать невалидные данные. Возможно, вы не сделаете все. Но сделайте столько, сколько сможете.

Разумеется, вашей программе нужны библиотеки: драйвер для работы с базой, веб-сервер, JSON-сериализатор. Возможно что-то еще. Вы сами решаете, какие взять библиотеки.

Задание вы можете выполнить в своем github аккаунте, либо присылать zip-архив с вашим кодом и документацией по нему. Имейте в виду, что выбранных вами библиотек может не быть на компьютере проверяющего. Поэтому в документации должно быть описано, как установить все, что необходимо для работы программы, как ее собрать и запустить. Желательно, чтобы все это делал пакетный менеджер для вашего языка.

Если вы достаточно хорошо знакомы с Docker, то можете прислать свой докер-контейнер, где все необходимое (язык и библиотеки) уже будет установлено, а ваш код собран и готов к запуску. Это идеальный вариант, так как если проверяющий не сможет собрать и запустить вашу программу, то это будет оценено как "не выполнено ни одного задания".


# 1-е задание - ✅

В базе данных есть таблица **cats** с такой схемой:
```
Table "public.cats"
     Column      |       Type
-----------------+-------------------
 name            | character varying
 color           | cat_color
 tail_length     | integer
 whiskers_length | integer
```

И она заполнена некоторыми данными, примерно такими:
```
 name  |     color     | tail_length | whiskers_length
-------+---------------+-------------+-----------------
 Tihon | red & white   |          15 |              12
 Marfa | black & white |          13 |              11
```

Про котов мы знаем некоторую важную информацию, например имя, цвет, длину хвоста и усов.

Цвет котов определен как перечисляемый тип данных:
```
CREATE TYPE cat_color AS ENUM (
    'black',
    'white',
    'black & white',
    'red',
    'red & white',
    'red & black & white'
);
```

Нужно выяснить, сколько котов каждого цвета есть в базe и записать эту информацию в таблицу **cat_colors_info**:
```
Table "public.cat_colors_info"
 Column |   Type
--------+-----------
 color  | cat_color
 count  | integer
Indexes:
    "cat_colors_info_color_key" UNIQUE CONSTRAINT, btree (color)
```

Должно получиться примерно так:
```
        color        | count
---------------------+-------
 black & white       |    1
 red & white         |    1
```


# 2-е задание - ✅

Продолжим анализ наших котов.

Нужно вычислить некоторые статистические данные о котах:
- средняя длина хвоста,
- медиана длин хвостов,
- мода длин хвостов,
- средняя длина усов,
- медиана длин усов,
- мода длин усов.

И сохранить эту информацию в таблицу **cats_stat**:
```
Table "public.cats_stat"
         Column         |   Type
------------------------+-----------
 tail_length_mean       | numeric
 tail_length_median     | numeric
 tail_length_mode       | integer[]
 whiskers_length_mean   | numeric
 whiskers_length_median | numeric
 whiskers_length_mode   | integer[]
```

Должно получиться примерно так:
```
 tail_length_mean | tail_length_median | tail_length_mode
------------------+--------------------+------------------
             14.0 |               14.0 | {13,15}

 whiskers_length_mean | whiskers_length_median | whiskers_length_mode
----------------------+------------------------+----------------------
                 11.5 |                   11.5 | {11,12}
```

Если вы не знаете, что такое среднее значение (mean), медиана (median) и мода (mode), вы без труда найдете информацию об этих базовых величинах статистики в интернете.


# 3-е задание - ✅

Хорошо иметь данные, но еще лучше иметь сервис, который с этими данными работает. Нам понадобится HTTP API.

Для начала нужно реализовать метод ping.

Напишите программу, которая будет работать как веб-сервер на порту 8080. И на запрос:
```
curl -X GET http://localhost:8080/ping
```

будет отвечать строкой:
```
"Cats Service. Version 0.1"
```

Здесь в примерах используется HTTP-клиент [curl](https://curl.haxx.se/), но вы можете использовать любой другой HTTP-клиент для тестирования вашего сервиса.


# 4-е задание

Теперь нужен метод для получения списка котов. На запрос:
```
curl -X GET http://localhost:8080/cats
```

Должен возвращаться список котов в формате JSON:
```
[
  {"name": "Tihon", "color": "red & white", "tail_length": 15, "whiskers_length": 12},
  {"name": "Marfa", "color": "black & white", "tail_length": 13, "whiskers_length": 11}
]
```

Должна работать сортировка по заданному атрибуту, по возрастанию или убыванию:
```
curl -X GET http://localhost:8080/cats?attribute=name&order=asc
curl -X GET http://localhost:8080/cats?attribute=tail_length&order=desc
```

Так же клиент должен иметь возможность запросить подмножество данных, указав offset и limit:
```
curl -X GET http://localhost:8080/cats?offset=10&limit=10
```

Разумеется, клиент может указать и сортировку, и лимит одновременно:
```
curl -X GET http://localhost:8080/cats?attribute=color&order=asc&offset=5&limit=2
```

Подумайте, что должен возвращать сервер, если указан несуществующий атрибут? Неправильный order? Offset больший, чем имеется данных в базе? Какие еще могут быть варианты невалидных запросов?

Обработайте такие запросы так, как считаете правильным.

В этом задании не лишними будут юнит-тесты, проверяющие, что ваша программа корректно обрабатывает валидные и невалидные входящие данные.


# 5-е задание

Конечно, наш сервис должен поддерживать добавление новых котов.

Запрос на добавление выглядит так:
```
curl -X POST http://localhost:8080/cat \
-d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"
```

Получив такой запрос сервис должен сохранить в базе нового кота.

Здесь тоже может быть много интересных ситуаций. Что, если кот с указнным именем уже есть в базе? А если длина хвоста задана как отрицательное число? Или это вообще не число? А если данные не являются валидным JSON-объектом?

Подумайте, какие еще возможны ситуации. Обработайте их так, как считаете правильным. Не забудьте про юнит-тесты.


# 6-е задание

Хороший сервис должен быть готов к нештатным ситуациям. Допустим, некая группа клиентов случайно или намеренно посылает больше запросов к сервису, чем сервис может обслужить.

Если сервис будет пытаться обслужить все запросы, то в какой-то момент он упадет. Но умный сервис знает свои возможности и работает в их пределах. Лишние запросы сервис должен отвергать.

У сервиса должна быть настройка, какое количество запросов он может обслужить. Допустим, это будет 600 запросов в минуту. Если количество запросов от клиентов превышает этот лимит, то часть запросов сервер должен отвергнуть с HTTP-статусом "429 Too Many Requests".

```
curl -X GET http://localhost:8080/cats
429 Too Many Requests
```

Как это протестировать?
