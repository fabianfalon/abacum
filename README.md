# ABACUM TEST

### Local Setup

### 1 Run with docker
    $ docker-compose build
    $ docker-compose up

### Access to swagger
    http://localhost:8000/swagger/

### RUN Tests
    $ docker-compose -f local.yml run --rm django pytest

### You can access shell in a container
    $ docker-compose run django sh


### USES CASES:

| Test case | Endpoint |
| ---------- |--------- |
| Get a full year balance by account  | http://localhost:8000/api/balance/full-year/by-account/ |
| Get a full year balance for a specific account | http://localhost:8000/api/balance/46000000/?frequency=year |
| Get monthly balances by account | http://localhost:8000/api/balance/46000000/?frequency=monthly |
| Get monthly balance for a specific account | http://localhost:8000/api/balance/77800000/?frequency=monthly |
| Get the monthly balance for a specific month by account | http://localhost:8000/api/balance/monthly/12/account/ |
| Get the monthly balance for a specific month and a specific account | http://localhost:8000/api/balance/monthly/12/account/68100000/ |


### Run test
    $ docker-compose run --rm django pytest