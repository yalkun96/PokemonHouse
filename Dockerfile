# Dockerfile
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установим рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . /app/

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]