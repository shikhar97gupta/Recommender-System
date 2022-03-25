FROM python:3.8.8

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN conda create --name new_env --file requirements.txt

COPY . .

CMD ["python", "app.py"]