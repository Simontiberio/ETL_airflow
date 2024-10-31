FROM apache/airflow:2.10.1

COPY  requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

ARG AIRFLOW_UID=1000
ENV AIRFLOW_UID=${AIRFLOW_UID}


#USER airflow
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt 