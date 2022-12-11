FROM python:3.9-slim

WORKDIR /src

COPY requirements.txt ./

COPY src ./src

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "src/main.py"]