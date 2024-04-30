FROM python:3.12

WORKDIR /app

RUN useradd -m bcactf && chown -R bcactf:bcactf /app

USER bcactf
ENV PATH $PATH:/home/bcactf/.local/bin
RUN pip install flask

COPY . . 

EXPOSE 5000
ENTRYPOINT ["flask", "--app", "server","run", "--host", "0.0.0.0", "--port", "5000"]