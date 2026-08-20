# Vercel WSGI entrypoint for the Care Connect Flask app.
# Vercel's Flask runtime imports `app` from this module.
from app import app

__all__ = ["app"]
