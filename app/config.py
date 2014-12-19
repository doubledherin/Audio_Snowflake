import os

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")
