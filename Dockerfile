FROM python:3.7.4
ADD . app/
WORKDIR app/
RUN pip install --upgrade pip
RUN pip install -r github_loader/requirements.txt
RUN python github_loader/create_tables.py
EXPOSE 5000
ENTRYPOINT ["python", "run.py"]
