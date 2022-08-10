FROM python:3.8-slim-buster

ADD importcsv.py .
ADD tablecreate.py .

RUN mkdir data
ADD ./data data
#ADD /data .

#ADD create_tables.sql ./sql

#RUN pip install --upgrade cython
RUN pip install --upgrade pip
ADD Requirements.txt .
RUN pip install -r Requirements.txt 

#CMD ["python", "./tablecreate.py"]
CMD ["python", "./importcsv.py"]