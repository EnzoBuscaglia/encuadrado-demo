FROM python:3.13-slim

WORKDIR /app/
COPY . /app/

RUN pip install --upgrade pip && \
  pip install poetry && \
  poetry config virtualenvs.create false
RUN poetry install

# RUN poetry run python manage.py collectstatic --noinput
# RUN poetry run python manage.py compilemessages

RUN apt-get -qq update && \
  apt-get install --fix-missing --install-recommends -y \
  gettext && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

EXPOSE 6000
