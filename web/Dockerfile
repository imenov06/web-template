FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /web

COPY requirements.txt .
COPY start_web.sh .

RUN chmod +x ./start_web.sh

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["./start_web.sh"]
