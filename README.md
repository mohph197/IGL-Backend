# Real Estate Web App Backend (TP IGL)

## Requirements

1. To run the project you need to have **[Python 3.x](https://www.python.org/downloads/)**
1. To host the database install mysql in your machine and import/run **[This File](./db_structure.sql)**
1. For google authentication you need to download the file **client_secret.json** associated to your google app and place it in the following path:
   > /app/auth/client_secret.json
1. To run functional tests you need the following:
   1. Make sure you have **[Google Chrome Browser](https://www.google.com/chrome/)** installed in your environment
   1. Download the chrome driver with a version similar to your chrome version\
      Download link: **[Chrome Drivers](https://chromedriver.chromium.org/downloads)**

## Environement Variables

1. Create the **.env** file:
   ```bash
   cp .env.example .env
   ```
1. Add the following variables to your **.env** file:
   - **GOOGLE_CLIENT_ID**: The client id of your google app (for google login)
   - **HOST_URL**: The url where your backend app is hosted
   - **DATABASE_URL**: The url of your database
   - **SECRET_KEY**: A secret key of your choice
   - **JWT_ALGORITHM**: The algorithm used to encode the jwt token (HS256, RS256, etc...)
   - **CHROME_WEB_DRIVER_PATH**: The path to the chrome driver we downloaded earlier
   - **FRONTEND_URL**: The url of your frontend app
   - **TEST_TOKEN**: A valid jwt token to be used in functional tests (you can generate one using the **/auth** endpoint)

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run The App

```bash
python run.py
```

## Run Tests

- Make sure your backend and frontend apps are running (for functional tests)
- This command will run all the tests (unit and functional):

```bash
pytest -v
```
