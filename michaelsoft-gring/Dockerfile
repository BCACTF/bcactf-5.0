FROM python:3.12

RUN useradd -m -d /home/bcactf bcactf && chown -R bcactf:bcactf /home/bcactf

USER bcactf

WORKDIR /home/bcactf

ENV PATH $PATH:/home/bcactf/.local/bin

RUN pip install flask

COPY --chown=bcactf:bcactf . .

EXPOSE 5000
CMD ["python", "server.py"]