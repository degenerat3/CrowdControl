FROM alpine:latest

RUN apk add --update  python3 


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN mkdir -p /tmp/cc/hosts
RUN touch /tmp/cc/calls.log

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

