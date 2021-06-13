# appts

## python version
Python 3.9

## setup
 - clone repo onto local machine
 - enter `appts` directory
 - create a virtual environment: `python3 -m venv env`
 - activate virtual environment: `. env/bin/activate`
 - install requirements: `pip3 install -r requirements.txt`
 - set initial env variables for flask:
   - `export FLASK_APP=flaskr`
   - `export FLASK_ENV=development`
 - run local server: `flask run`
 
## API endpoints:

### /users/
 - METHODS: GET and POST
  - this allows you to get a list of users created
  - it also allows you to create new users. Currently the only user attribute is a user id (uuid format) which is auto assigned, 
  so POSTs don't need any data in the body of the request

### /users/<user_id>/appointments
 - METHOD: GET
  - this allows you to get a list of appointments for a user
 - METHOD: POST
  - body params:
    - appt_datetime: string in isoformat without seconds, microseconds or timezone: %Y-%m-%dT%H:%M
  - validation: for each post request to appointments, the appt_datetime is checked to make sure that it's a valid format, that the miniutes are on the hour and half hour,
  that the user doesn't have any other appointments that day, and that the user exists.
  
## Usage

- start by creating a user. A post request to `http://127.0.0.1:5000/users/` will return a new user object with an id (in uuid format)
- copy the user's uuid and add it to the url, and then append `appointments`
- your new url should look something like `http://127.0.0.1:5000/users/<user_id>/appointments` where the user_id is your newly created user's id.
- here you can post new appointments for that user. To do this, you'll can add the appt_datetime to the body of your request: `{"appt_datetime": "2021-07-023T14:30"}`
- you can continue to add new appointments with additional post requests, but keep in mind the validation described above
- to see all of the appointments for the user you've added, send a GET request to your current url: `http://127.0.0.1:5000/users/<user_id>/appointments` this will give you a list of the appointments for that user


## Future updates:
 - add a database to store this data to disk
 - add more validation to the appointments: maybe prevent past appointment creation, and limit a user to a certain number of appointments per year
 - add more attributes for the user
 - add tests for users and appointments
