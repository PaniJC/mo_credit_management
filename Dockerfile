FROM python:3

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /Virtualizations

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /Virtualizations/.aws

COPY . .

CMD ["python","MO_Credit_Management\BackendTechnicalTest\BackendTechnicalTest\__init__.py"]
