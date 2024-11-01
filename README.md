[![Maintainability](https://api.codeclimate.com/v1/badges/d95789b672a970f73666/maintainability)](https://codeclimate.com/github/Myakot/test_DjangoRest/maintainability)

# Project Overview
================

This project is a RESTful API built with FastAPI, PostgreSQL, and Alembic. It provides endpoints for wallet operations, including deposit, withdrawal, and balance retrieval.

## Table of Contents
---------------

* [Project Structure](#project-structure)
* [Endpoints](#endpoints)
* [Database](#database)
* [Testing](#testing)
* [Environment Variables](#environment variables)
* [Dockerization](#dockerization)

## Project Structure
-----------------

The project is organized into the following directories:

* `app`: contains the main application code
* [alembic](cci:4:///home/myakot/PycharmProjects/test_DjangoRest/requirements.txt:0:0-36:0): contains database migration scripts
* `tests`: contains unit tests and integration tests
* [config](cci:4:///home/myakot/PycharmProjects/test_DjangoRest/alembic/env.py:0:0-37:0): contains configuration files

## Endpoints
------------

The API provides the following endpoints:

* `POST /api/v1/wallets/<WALLET_UUID>/operation`: performs a deposit or withdrawal operation on a wallet
* `GET /api/v1/wallets/<WALLET_UUID>`: retrieves the balance of a wallet

## Database
------------

The project uses PostgreSQL as the database management system. The database schema is defined using Alembic migration scripts.

## Testing
------------

The project includes unit tests and integration tests written using Pytest.

## Environment Variables
------------

This project requires a single environment variable, `DB_URL`, to connect to the database.
This, you have to setup manually, by creating an '.env' file in the root directory and adding said variable there, i.e.:
```
DB_URL=postgresql://postgres:password@localhost:5432/postgres
```

## Dockerization
--------------

The project is dockerized using Docker Compose. To run the application, use the following command:

```bash
docker-compose up
```
This will start the application and database containers.

## API Documentation
------------

The API documentation is automatically generated using FastAPI's built-in documentation features. To access the documentation, navigate to `http://localhost:8000/docs` after starting the application.

The documentation includes information about available endpoints, request and response bodies, and other relevant details.


# Benchmark Results
### Summary

| Name | Min (ms) | Max (ms) | Mean (ms) | StdDev (ms) | Median (ms) | IQR (ms) | Outliers | OPS | Rounds | Iterations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| test_perform_operation_1000_rps | 723.43 | 2509.04 | 960.15 | 162.92 | 935.80 | 231.46 | 322;9 | 1.04 | 1000 | 1 |

### Legend

* Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
* OPS: Operations Per Second, computed as 1 / Mean

### Test Summary

* **Passed:** 1
* **Skipped:** 8
* **Warnings:** 1
* **Total Time:** 965.53s (0:16:05)