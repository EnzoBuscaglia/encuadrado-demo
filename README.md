# Encuadrado: Demo for "La Vitrina"

## Setup

In order to start the Docker services run the up files in terminal: `./up`

## CI/CD

- Format using Black and isort.
- Check logic patterns using prospector. [Click here to check pylint documentation.](https://pylint.pycqa.org/en/latest/user_guide/messages/index.html).

## Assumptions

We only have one admin, so there's no need to include a "professional" field for any Model app models (Event, DigitalContent, DiscountCode).
