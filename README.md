# Easy Events API

Django app that handles the API and the end-users

For client-side, take a look at [easyevents_spa](https://github.com/Data5tream/easyevents_spa).

## Environment

```
ALLOWED_HOSTS = space separated lists of allowed hosts
DEBUG = pass something to enable debug mode
SECRET_KEY = [Django secret key](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECRET_KEY)
USER_WEBROOT = The base URL for the API and the pages the participants visit
DEFAULT_FROM_EMAIL = Used in notification emails
```

## Deployment

```bash
docker run \
  -p 8000:8000 \
  -e SECRET_KEY=SEE_ABOVE \
  -e USER_WEBROOT=SEE_ABOVE \
  -e DEFAULT_FROM_EMAIL=SEE_ABOVE \
  easyevents-api
```
