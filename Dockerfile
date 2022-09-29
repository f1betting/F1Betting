FROM python:3.10.7-bullseye
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
ENV PYTHONPATH /code
CMD ["python", "app/main.py"]