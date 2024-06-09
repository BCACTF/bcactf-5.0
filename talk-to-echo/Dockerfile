FROM python:3.12-bookworm

WORKDIR /app

RUN wget -O ynetd.c \
        https://raw.githubusercontent.com/johnsonjh/ynetd/e6fd08f8f5d0c6b8c18d645957e30ce012536ed4/ynetd.c \
    && echo "ec7509dec7737da54f8b18e1b5ba935d657f9f016c36cfc9ac08f9952373226f  ynetd.c" | sha256sum -c \
    && gcc -o ynetd ynetd.c

RUN pip install pycryptodome

COPY ./flag.txt .

COPY ./echo.py .
EXPOSE 3000
ENTRYPOINT ["./ynetd", "-p", "3000", "python3 ./echo.py"]