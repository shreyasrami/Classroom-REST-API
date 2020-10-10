# Classroom-REST-API

A classroom where teacher can assign quizzes on various topics to students. 
Students can submit the quiz and view their results.
API endpoints created for all these functionalities.

## Installation Instructions

1. Clone the project.
    ```shell
    $ git clone https://github.com/shreyasrami/Classroom-REST-API
    ```
2. `cd` intro the project directory
    ```shell
    $ cd Classroom
    ```
3. Create a new virtual environment activate it.
    ```shell
    $ python3 -m venv env
    $ source env/bin/activate
    ```
4. Install dependencies from requirements.txt:
    ```shell
    (env)$ pip install -r requirements.txt
    ```
5. Usage of python-decouple to hide confidential stuff
   ####In your settings.py :
   1.Simply create a .env text file on your repository's root directory and set the parameters in .env file:
     ```shell
     $ SECRET_KEY=ARANDOMSECRETKEY
     $ DEBUG=True/False
     $ DB_NAME=ARANDOMNAME
     $ DB_USER=DATABASEUSER
     $ DB_PASSWORD=ARANDOMPASSWORD
     $ DB_HOST=127.0.0.1
     ```
   2.Import the config object:
     ```shell
     $ from decouple import config
     ```
     
   3.Retrieve the configuration parameters in settings.py:
     ```shell
     $ SECRET_KEY = config('SECRET_KEY')
     $ DEBUG = config('DEBUG', cast=bool)
     $ DB_NAME=config('DB_NAME')
     $ DB_USER=config('DB_USER')
     $ DB_PASSWORD=config('DB_PASSWORD')
     $ DB_HOST=config('DB_HOST')
     ```
     
6. Migrate the database.
    ```shell
    (env)$ python manage.py migrate
    ```

7. Run the local server via:
    ```shell
    (env)$ python manage.py runserver
    ```

### Done!
The local application will be available at <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>.

## Contributing
Pull requests are welcome. For major
changes, please open an issue first 
to discuss what you would like to change.
