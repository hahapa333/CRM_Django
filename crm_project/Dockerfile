FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем линтер (не обязательно падать при ошибках)
RUN pylint crm || true
CMD ["gunicorn", "crm_project.wsgi:application", "--bind", "0.0.0.0:8000"]
