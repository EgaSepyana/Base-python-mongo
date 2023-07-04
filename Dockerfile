FROM python:slim-buster

WORKDIR /app

COPY requirements.txt ./
COPY /src src
COPY /public public
COPY main.py ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]