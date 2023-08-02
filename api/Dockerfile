FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10


WORKDIR /api
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install fastapi uvicorn
RUN pip install python-multipart
RUN pip install python-decouple
RUN pip install pycurl
RUN apt-get install odbc-postgresql

COPY ./requirements.txt /api/requirements.txt
RUN pip install -r /api/requirements.txt

COPY . /api

COPY odbcinst.ini /etc
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
