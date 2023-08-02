FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN sudo su
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN exit
RUN apt-get update 
RUN apt-get install libssl-dev libcurl4-openssl-dev 
RUN apt-get install nano iputils-ping unixodbc-dev -y 
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 unixodbc-dev -y





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
