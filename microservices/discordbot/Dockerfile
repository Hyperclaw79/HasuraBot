FROM python:3.6.4-alpine3.7

# install requirements
RUN apk update && apk upgrade && \
    apk add --no-cache bash git && \
    apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev	

                       		
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN apk del .pynacl_deps

# copy current directory to /bot
COPY . /bot

# set app/src as the working directory
WORKDIR /bot/src

# Run the python file
CMD ["python","-u","bot.py"]
