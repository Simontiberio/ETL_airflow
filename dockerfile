FROM apache/airflow:2.10.1

COPY  requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

#USER ROOT
#RUN apt-get update

#USER airflow
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt 