FROM python:3-slim

RUN mkdir -p /tmp
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /usr/src/app
COPY . .

CMD [ "python", "./main_loop.py" ]