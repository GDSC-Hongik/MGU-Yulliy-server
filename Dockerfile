# BUILDER #
###########

# pull official base image
FROM python:3.12 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential && pip install mysqlclient

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# FINAL #
#########

# pull official base image
FROM python:3.12

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --ingroup app app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/static $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev musl-dev \
    && apt-get install -y default-libmysqlclient-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install mysqlclient
RUN pip install --no-cache /wheels/*
RUN apt-get remove -y gcc python3-dev musl-dev && apt-get autoremove -y

# copy entrypoint.sh
COPY ./config/docker/entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# set entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

# default command
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
