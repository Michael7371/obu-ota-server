FROM python:3.12-alpine

WORKDIR /code

COPY requirements.txt .

COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]