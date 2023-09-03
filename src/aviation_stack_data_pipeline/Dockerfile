FROM python:3

WORKDIR /usr/src/app

ARG AVIATION_STACK_API_KEY

COPY requirements.txt .

COPY ./include/ ./include/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pytest -m build

CMD [ "python", "./main.py" ]
