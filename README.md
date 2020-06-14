# Run project

To run project locally, you should do the next simple steps:

1. Clone the repo `git clone git@github.com:shaggy7202/sendcloud-test.git`
2. Move to the project directory `cd sendcloud-test`
3. Build docker containers `docker-compose build`
4. Run the migrations `docker-compose run web python manage.py migrate`
5. Start the project `docker-compose up -d` 

Project will be available at `http://0.0.0.0:8000/`


# Run Tests

Tests were written using [pytest](https://docs.pytest.org/en/latest/).
To run the tests, you should use the next command: `docker-compose run web pytest`


# Run PEP8 Checks

You can check code for PEP8 requirements with [flake8](https://flake8.pycqa.org/en/latest/).
To check the code, you should use the next command: `docker-compose run web flake8`
