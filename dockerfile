FROM python:3.8-buster

ADD importcsv.py .
ADD tablecreate.py .

#RUN mkdir /var/lib/postgresql/data/data
#ADD data /var/lib/postgresql/data/data
RUN mkdir -p /app/data
ADD ./data /app/data
#ADD create_tables.sql ./sql

#RUN pip install --upgrade cython
RUN pip install --upgrade pip
ADD Requirements.txt .
RUN pip install -r Requirements.txt 

#CMD ["python", "./tablecreate.py"]
CMD ["python", "./importcsv.py"]