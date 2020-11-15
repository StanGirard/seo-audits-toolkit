FROM ubuntu:18.04
WORKDIR .
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    python3-pip \
    python-psycopg2 \
    && pip3 install psycopg2-binary \
    && pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3" ,"run.py"]