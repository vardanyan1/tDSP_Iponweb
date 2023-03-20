"""
WSGI config for image_server project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

from app import app

if __name__ == "__main__":
    app.run()