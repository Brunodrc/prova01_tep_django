FROM bitnami/python:3.11

WORKDIR /app

COPY . /app

# COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]