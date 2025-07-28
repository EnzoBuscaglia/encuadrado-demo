# Encuadrado: Demo for "La Vitrina"

## Backend

### Setup

In order to start the Docker services simply run the up files in a terminal: `./up`. When that's ready, migrate the models by attaching the container shell and running `python manage.py migrate`. Then, to obtain a minimal database setup, simply run `python manage.py load_db` which will already have the admin credentials for the `/admin` endpoint.

To actually use the product, *cd* into the frontend directory and then run `npm run dev`. If for any reason Vite is not porting to *5173*, just remember to modify the port in _backend/showcase/settings.py_ `CSRF_TRUSTED_ORIGINS` and `CORS_ALLOWED_ORIGINS` to whatever Vite ported.

The endpoints will be available at ``http://localhost:5173/admin`` and ``http://localhost:5173/store``.

### CI/CD

- Format using Black and isort.
- Check logic patterns using prospector. [Click here to check pylint documentation.](https://pylint.pycqa.org/en/latest/user_guide/messages/index.html).

## Frontend

This project requires Node.js **v20.19.0 or higher** (Vite 7+ compatibility).

We recommend using the latest stable Node.js version (e.g. v22.x).

### Install dependencies

```bash
cd frontend
npm install
```

## Assumptions

- We'll use the Django admin panel as the `/admin` endpoint since its essentially the same as creating an API endpoint that will perform the same operations and visually present the same information.
- We assume that the professional (admin) understands English and can navigate the model fields in the admin panel in order to create/modify/delete Events, Digital Contents, and Discount Codes.
- We also assume that there's only one admin, so there's no need to include a "professional_id" field for any Model app models (Event, DigitalContent, DiscountCode).
- **For this demo, we assume no authentication is required for the API endpoints, and that CSRF and CORS protections are either disabled or configured permissively for ease of local development.**
