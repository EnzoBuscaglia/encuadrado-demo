FROM python:3.13-slim

WORKDIR /app/
COPY backend/ /app/

RUN apt-get -qq update && \
  apt-get install --fix-missing --install-recommends -y \
  gettext && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
  pip install "poetry==2.1.0" && \
  poetry config virtualenvs.create false
RUN poetry install

# RUN poetry run python manage.py collectstatic --noinput
# RUN poetry run python manage.py compilemessages

EXPOSE 6000
