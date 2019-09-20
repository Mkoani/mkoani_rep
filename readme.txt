to run this application unzip the folder and delete the migrations folder and the virtual folder
if you are on windows then open windows power shell(or commandprompt) and make sure the current working directory
is this folder(Mkoani),then create the virtual enviroment and activate it:
    ....\Mkoani> python -m venv virtual
    .....\Mkoani>virtual\activate
    (virtual)....\Mkoani>pip install -r 'requirements.txt'
the second line above installs all the necessary extensions and the flask framework
after activating the virtualenviroment and installing all necessary packages,create a migration repository:
    be sure to look in the config.py to match the SQLALCHEMY_DATABASE_URI with the path to your created database for mkoani
    (virtual)....\Mkoani> $env:FLASK_APP='application.py' or set FLASK_APP=application.py if you are using commandprompt
    (virtual)....\Mkoani> flask db init ......here you are setting up a migration repository
    (virtual)....\Mkoani> flask db migrate -m 'new_schema'
    (virtual)....\Mkoani> flask db upgrade
    please note that you will need to create an entirely new database first before pointing to it
    using SQLALCHEMY_DATABASE_URI forexample if you are using postgresql;
    SQLALCHEMY_DATABSE_URI=postgresql://postgres:yourpassword@localhost/name of database...just follow format in config.py
if no error encountered then you have succesfully set up the databse and can run your app
but first enable debug mode
    (virtual).....\Mkoani> $env:FLASK_DEBUG=1 or set FLASK_DEBUG=1 for commnadprompt
    (virtual).....\Mkoani>python -m flask run.......here you are running the app
    
please note:
make sure you run the commandpropmpt as an adminstrator should you decide to use the cmd
to see the owner functionality you have to insert the login credentials into the database
first and then login as that user
to do that you will need a hashed password for your password to do that:
    run python in the terminal
    (virtual).....\Mkoani>python
    (virtual)....\Mkoani>python3.7(or your particular version)............
    .......>>>from werkzeug.security import generate_password_hash
    .......>>>generate_password_hash('chichi')........the password you want to hash
    .......>>>some hashed password...........now copy this hashed password and insert it with other credentials into owner table
    .......>>>exit()
    (virtual)......\Mkoani>python -m flask run
the owner functionality is now accessible via urls forexample .../owner,/owner/customers,/profile,etc as depicted in the owner package for the app
to access the login page go to .../login
... here stands for localhost as shown when you execute python -m flask run
the seats and booking functionality have not been implemented in this demo,booking is basically what the app is doing on the customer part
and seats we need a seat layout for the bus
a note on seats whenever a user adds a bus into the database seats are automatically populated which are distinct for each bus
please do check the seats table in the database when you add a bus and any other functionality

if you are using MacOs,all procedures thus far remain the same except
to create a virtual environment you do
    ...../Mkoani$ python3 virtualenv -m virtual
    ..../Mkoani$source/bin/activate.....to activate your virtual enviroment
    ..../Mkoani$(virtual)....everything else remains the same
    
when you will be modifying the frontend please take note of the code in the skeletal templates

Thanks you.


##### Update ######
- To add a new owner simply visit localhost:5000/register and input the details. The owner will then be sent an email with their password.
- After a customer books the ticket, they will be sent an email with their particulars.
- The email configuration needs to be set on the config file for email to work.
