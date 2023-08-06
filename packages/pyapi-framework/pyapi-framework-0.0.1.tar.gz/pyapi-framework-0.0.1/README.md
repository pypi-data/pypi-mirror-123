# pyapi Framework

A simple python REST api framework.

## Requirements

- python >= 3
- pip

## How to Run pyapi

Navigate to project folder and run the following to start the server:

    python3 main.py

## Default pyapi architecture

- main.py: <br/>
    Includes http server where server url and port are set.

- routes.py: <br/>
    Includes methods for routes set in service_handler.py.

- service_handler.py: <br/>
    Services required for headers, routes dictionary and GET/POST/PUT/DELETE methods.

