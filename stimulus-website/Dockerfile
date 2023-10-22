FROM python:3.10
RUN mkdir stimulus-website
WORKDIR /stimulus-website
RUN pip install gunicorn
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY assets/ assets/
COPY .env .env
COPY mongo_connector.py mongo_connector.py
COPY main.py main.py
CMD [ "gunicorn", "--bind", "0.0.0.0:8050", "main:server" ]
