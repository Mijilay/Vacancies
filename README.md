# Сравниваем вакансии программистов
## Описание
Проект создан для загрузки данных о зарплатах различных программистов, в зависимости от языка программирования. Поиск производится по [hh.ru](https://hh.ru/) и [superjob](https://www.superjob.ru/).

## Устанавка
Скачайте необходимые файлы, затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей. Для этого запустите файл и передайте команду:
```
pip install -r requirements.txt
```
## Пример запуска
Для запуска скрипта у вас должен быть установлен Python3.

Для получения таблиц с вакансиями и заработной платой напишите команду:
```
python main.py
```
## Переменные окружения
Часть настроек проекта берётся из переменных окружения. Переменные окружения - данные, передаваемые програмаме через внешние структуры. Чтобы их определить, вывполните пункты:
1. Создайте файл без названия с расширением `.env` в одной папке с `main.py`.
2. Запишите данные (API-ключ Superjob) в этом формате:
```
  'SUPERJOB_SECRET_KEY' = 'Ваш ключ Superjob'
```
  Токен можно получить на сайте [API_superjob](https://api.superjob.ru/).

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-резроботчиков [dvmn.org](https://dvmn.org/).
