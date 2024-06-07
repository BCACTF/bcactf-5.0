FROM python:3.12-bookworm

RUN wget -O ynetd.c \
        https://raw.githubusercontent.com/johnsonjh/ynetd/e6fd08f8f5d0c6b8c18d645957e30ce012536ed4/ynetd.c \
    && echo "ec7509dec7737da54f8b18e1b5ba935d657f9f016c36cfc9ac08f9952373226f  ynetd.c" | sha256sum -c \
    && gcc -o ynetd ynetd.c

RUN pip3 install flask
RUN pip3 install python-dotenv

COPY ./error_pattern.txt .
COPY ./flag_gen.py .
COPY ./flag.txt .

EXPOSE 1337
ENTRYPOINT ["./ynetd", "-p", "1337", "python3 ./flag_gen.py"]