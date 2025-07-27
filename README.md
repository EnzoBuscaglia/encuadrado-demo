# Encuadrado: Demo for "La Vitrina"

## Setup

In order to start the Docker services run the up files in terminal: `./up`

## CI/CD

- Format using Black and isort.
- Check logic patterns using prospector. [Click here to check pylint documentation.](https://pylint.pycqa.org/en/latest/user_guide/messages/index.html).

## Assumptions

We'll use the Django admin panel as the /admin endpoint since its essentially the same as creating an API endpoint that will perform the same operations and visually present the same information.
We only have one admin, so there's no need to include a "professional_id" field for any Model app models (Event, DigitalContent, DiscountCode).
