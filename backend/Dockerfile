FROM python:3.8.5
WORKDIR /code
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
COPY . /code
RUN chmod +x ./start.sh
CMD ["./start.sh"]