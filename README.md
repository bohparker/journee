# Journee
A simple journal app made with Flask

# Setup
Create a python virtual environment named venv: 
$ `python3 -m venv venv

Activate the virtual environment:   
$ `source venv/bin/activate

Install the required packages:  
$ `pip install -r requirements.txt

### Environment Variables
Create a .env file in the project and enter the following environment variables:    
`SECRET_KEY
`DATABASE_URL

### Database Initialization
Initialize the database with flask-migrate: 
$ `flask db init

This will create a folder called 'migrations'. Inside the migrations folder, there
is a file called 'env.py'. At the top of this file, add the following import:   
`import app.models

Now a database migrations can be created:   
$ `flask db migrate -m "initial migration"
$ `flask db upgrade

That's it! Now the database is created and you can run the app: 
$ `flask run