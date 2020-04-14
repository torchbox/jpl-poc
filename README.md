# JPL Wagtail

## Local dev setup

```
# Spin up the server accessible at http://localhost:8000/
$ docker-compose up

# Run on-off commands inside docker
$ docker-compose run web bash

docker$ dj migrate
docker$ dj createsuperuser
```

## Deployments

Deployments are triggered when new code is pushed to origin master on Github.
