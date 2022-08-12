FROM python:3.9-buster

ADD importcsv.py .
ADD tablecreate.py .

RUN mkdir -p /app/data
ADD ./data /app/data

RUN pip install --upgrade pip
ADD requirements.txt .
RUN pip install -r requirements.txt 

#CMD ["python", "./tablecreate.py"]
CMD ["python", "./importcsv.py"]