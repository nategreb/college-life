## Introduction

The College Life is an all-in-one app that you need for your college. We provide course reviews, professor reviews and
many more.

For now, we only have the following functionalities:
- Login/Logout
- Course Review
- Professor Review

## Requirements

To run this app, you will need the following softwares:

- [Python](https://realpython.com/installing-python/)
- [Django](https://docs.djangoproject.com/en/4.1/topics/install/#installing-official-release)
- [Docker](https://docs.docker.com/get-docker/)

## Installation

- Check that you have python\
`python --version`

- Check that you have Django\
`django-admin --version`

1. Clone our [repository](https://github.com/nategreb/college-life.git) into your machine
2. Create `env.sh` shell script and fill it with your credentials and run the shell script\
`export EMAIL=""`\
`export PASSWORD=""`\
`export SECRET_KEY=""`\
`export DB_HOST="0.0.0.0"`\
`export DB_NAME="test_db"`\
`export DB_USER="root"`\
`export DB_PASSWORD="root"`
3. In your terminal, run docker compose\
`docker compose up -d`
4. Go into `college_living` folder
5. Install requirements packages\
`pip install -r requirements.txt`
6. Migrate model into database\
`python manage.py migrate`
7. Load initial data\
`python manage.py loadata colleges/fixtures/*.json`
8. Start server\
`python manage.py runserver`
9. Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and start exploring!
