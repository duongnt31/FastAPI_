# Dockerfile
FROM python:3.10-slim

WORKDIR ${DIR}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "run.py"]
