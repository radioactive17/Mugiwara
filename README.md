# Mugiwara - A Secure Banking System

Introducing Mugiwara, a secure and versatile banking system designed to cater to the diverse needs of its users. With Mugiwara, every user has a unique role and set of functionalities—customers can manage their accounts, transfer funds, and access a variety of banking services; employees can handle day-to-day operations and assist customers; system managers ensure the seamless functioning of the banking system; merchants can process transactions and manage payments; and administrators maintain overall system security and compliance.

Mugiwara not only prioritizes security and efficiency but also provides a user-friendly interface for all its users. Whether you're a customer looking for a reliable banking experience, an employee ensuring excellent service, or an admin managing system-wide operations, Mugiwara is your trusted partner in modern banking. Experience the future of secure banking with Mugiwara today!

## Install Dependencies
Go to the directory containing requirements.txt 
```bash
pip install -r requirements.txt
```

## Setup Database
For this project, we are using Django's default database setup i.e., SQLite. However, it is recommended to use a more robust setup.
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```
Note: Different Databases require different setups. Please setup your database accordingly.

To create the necessary database tables and prepare your database, run the following commands in your terminal:
```python
python manage.py makemigrations
python manage.py migrate
```

To access the Django admin interface, you'll need to create a superuser:
```python
python manage.py createsuperuser
```

## Run the program
After installing the dependencies and setting up the database you should be good to go and execute the program.  
Make sure you are in the directory containing the manage.py file and Run the following command line to bring up the server 
```bash
python manage.py runserver
```
If everything went smoothly, you should see the below screen.   
<img src="mugiwara images/terminal.png" width="750">

If you encounter any errors, please search online for solutions or feel free to reach out to me at jigsshah.97@gmail.com.

## Few Snippets of the application  


## Developers
Jignesh Nagda | Chinmay Lotankar | Nikhil Kulkarni | Sagar Sahu | Mihir Vaidya
