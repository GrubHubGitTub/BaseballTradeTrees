FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

# add user (change to whatever you want)
# prevents running sudo commands
RUN useradd -r -s /bin/bash aidan

# set current env
ENV HOME /app
ENV PATH="/app/.local/bin:${PATH}"

RUN chown -R aidan:aidan /app
USER aidan

RUN pip install --no-cache-dir -r ./requirements.txt --user

# set app config option
ENV FLASK_ENV=production

# set argument vars in docker-run command
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# Add the rest of the files
COPY . .

# start web server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]