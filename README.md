Выполнить тестовое задание:
SQLAlchemy - создать локальную базу скриптами питона. База должна содержать 2 таблицы(users, geo_locations) со связью много-ко-многим;
Requests - Заполнить таблицу используя скрипты питона, и The Google Maps Geocoding API. Для запросов на гугл использовать requests;
Flask - сделать локальное приложение. Создать 2 массива (один с юзерами, второй с названиями городов, которые распознает Geocoding API). На каждый запрос localhost/get_users_location приложение выбирает 5 рандомных юзеров и 5 рандомных городов, делает запросы на Geocoding API для получения координат, после получения координат переформировывает данные в junction таблице для 5 юзеров, после чего отображает сформированные данные на странице в виде json объекта.
