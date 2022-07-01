FROM python:3.9-slim

WORKDIR /app

COPY gitlab-commit2gsheet.py .

COPY req.txt .
COPY cred.json .

RUN python -m pip install --upgrade pip

RUN pip install -r req.txt

CMD [ "python", "./gitlab-commit2gsheet.py" ]
