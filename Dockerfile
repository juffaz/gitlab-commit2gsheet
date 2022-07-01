FROM python:3.9-slim

WORKDIR /app

COPY gitlab_commits2telegram.py .

COPY req.txt .
COPY cred.json .

RUN python -m pip install --upgrade pip

RUN pip install -r req.txt

CMD [ "python", "./gitlab_commits2telegram.py" ]
