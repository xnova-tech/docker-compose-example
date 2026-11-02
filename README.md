# Docker Compose: минимальный пример

Проект XNova поднимает одну статическую HTML-страницу в Nginx через Docker Compose. Он соответствует примеру из статьи о базовой модели Compose: один сервис, публикация порта только на loopback-интерфейсе и bind mount только для чтения.

## Запуск

Понадобятся Docker Engine или Docker Desktop с командой `docker compose`. После клонирования выполните:

```bash
git clone https://github.com/xnova-tech/docker-compose-example.git
cd docker-compose-example
docker compose config -q
docker compose up -d
docker compose ps
curl -fsS http://127.0.0.1:8080/
```

В ответе должна появиться строка `<h1>Compose работает</h1>`. Образ Nginx закреплён по digest, а порт `8080` доступен только через `127.0.0.1`. Если порт занят, остановите использующий его процесс или временно измените левую часть mapping в `compose.yaml`.

После проверки удалите контейнер и сеть проекта:

```bash
docker compose down
```

## Проверка файлов

Контрактные тесты сверяют проверенный Compose-файл и разбирают HTML без запуска браузера. Нужен Python 3.12 или новее:

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Тесты не заменяют `docker compose config -q` и HTTP-проверку: эти команды отдельно проверяются в GitHub Actions на Linux.

Исходники распространяются по Apache-2.0; условия находятся в `LICENSE`.
