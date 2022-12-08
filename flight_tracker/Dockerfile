FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    build-essential

RUN useradd -ms /bin/bash user
USER user

WORKDIR /app
COPY . /app

RUN python3 -m pip install -r requirements.txt

#CMD ["yes"]
#   RUN python3 manage.py makemigrations website
#   RUN python3 manage.py migrate

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
