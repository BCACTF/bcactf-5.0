FROM python:3.12

RUN useradd -m -d /home/bcactf bcactf && chown -R bcactf:bcactf /home/bcactf

RUN chown bcactf:bcactf ./search_results.db
RUN chmod +rw ./search_results.db

USER bcactf

WORKDIR /home/bcactf

ENV PATH $PATH:/home/bcactf/.local/bin

RUN pip install flask

COPY . .

EXPOSE 5000
CMD ["python", "server.py"]