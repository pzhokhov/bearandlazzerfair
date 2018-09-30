FROM python:3.6

COPY . /root/code
WORKDIR /root/code

RUN pip install -r requirements.txt
CMD python app.py
