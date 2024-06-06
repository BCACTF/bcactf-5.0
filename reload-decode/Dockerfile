FROM python:3.12-bookworm

RUN apt update && apt install python3-pip -y \
    && pip3 install flask \
    && pip3 install python-dotenv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

EXPOSE 3000
CMD ["python3", "main.py"]