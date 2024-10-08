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

## Functionalities and Snippets
### 1: Home Page
<img src="mugiwara images/h1.png" width="750">
<img src="mugiwara images/h2.png" width="750">
<img src="mugiwara images/h3.png" width="750">

### 2: Customer/Banking User

* Account Request and Management: Users can request a new checking or savings account if they do not already have an account. Once an account is created, additional options become available in the navigation menu.

  <img src="mugiwara images/c2.png" width="750">
  
  <img src="mugiwara images/c3.png" width="750">
  
* Account Maintenance: Users can view their existing accounts or request the deletion of an account.
  
  <img src="mugiwara images/c4.png" width="750">
  
* Deposits and Withdrawals: Users can deposit funds into their account, with transactions requiring a One-Time Password (OTP) verification to confirm their identity. Users can also request to debit money from their account, following the same OTP verification process.
  
  <img src="mugiwara images/c5.png" width="750">
  <img src="mugiwara images/c6.png" width="750">
  <img src="mugiwara images/c8.png" width="750">
  
* Transaction Management: Users can view their transaction history, including the status of each transaction. All transactions are initially marked as pending and are completed only upon approval by authorized personnel, such as bank employees or managers.
  
  <img src="mugiwara images/c13.png" width="750">
  
* Fund Transfers: Users can send money to other accounts, with OTP verification required to ensure the authenticity of the transaction.
  
  <img src="mugiwara images/c11.png" width="750">
  
* Profile Management: Users can check, request updates, or request the deletion of their profile details.
  
  <img src="mugiwara images/c15.png" width="750">
  <img src="mugiwara images/c16.png" width="750">


### 3. Bank Employee

* Transaction Approval and Management: Employees have the authority to approve, decline, or modify user transactions. To ensure the authenticity of transactions, employees can verify whether the user has successfully completed the One-Time Password (OTP) verification process.
  
  <img src="mugiwara images/e2.png" width="750">
  
* Transaction Modification: Employees can modify transactions upon the user's request, ensuring that any changes align with the bank's policies and procedures.
  
  <img src="mugiwara images/e3.png" width="750">
  
* Transaction Monitoring: Employees can access and review a comprehensive list of all transactions made by a user, allowing them to monitor and manage user activity effectively.
  
  <img src="mugiwara images/e4.png" width="750">

### 4. Bank Manager

* Transaction Oversight: Bank managers have the authority to view and monitor transactions, specifically those above a threshold amount of $10,000.
  
  <img src="mugiwara images/man3.png" width="750">
  
* Transaction Approval and Management: Managers can approve, decline, or modify high-value transactions, ensuring compliance with the bank’s policies and regulatory requirements. To verify the authenticity of high-value transactions, managers can check if the user has completed the One-Time Password (OTP) verification process.
  
  <img src="mugiwara images/man1.png" width="750">
  
* Transaction Modification: Managers can modify high-value transactions upon the user’s request, provided the changes adhere to bank regulations and policies.
  
  <img src="mugiwara images/man2.png" width="750">

### 5. Merchants

* Payment Request Submission: Merchants can submit payment requests for processing. Each request requires One-Time Password (OTP) verification to ensure authenticity.
  
  <img src="mugiwara images/merch2.png" width="750">
  
* Request Modification: Merchants have the ability to modify the requested payment amount as needed before it is processed.

  <img src="mugiwara images/merch4.png" width="750">
  
* Request Approval: Submitted payment requests are subject to approval or rejection by bank employees or managers, depending on the transaction's nature and value.

  <img src="mugiwara images/merch.png" width="750">
  
* User Details Modification: Merchants can modify specific user details, ensuring the information is accurate and up-to-date for transaction processing.
  
  <img src="mugiwara images/merch5.png" width="750">
  <img src="mugiwara images/merch6.png" width="750">

### 6. Admin

* User and Account Management: Administrators have the authority to approve or reject user registration requests, user profile update requests, and user deletion requests.
They also manage account-related activities, including approving or rejecting requests for creating new accounts or deleting existing ones.

  <img src="mugiwara images/a3.png" width="750">
  <img src="mugiwara images/a2.png" width="750">
  <img src="mugiwara images/a4.png" width="750">
  <img src="mugiwara images/a5.png" width="750">
  
* Transaction Oversight: Administrators have full visibility of all transactions within the database, allowing them to monitor and audit activities across the platform.


## Developers
Jignesh Nagda | Chinmay Lotankar | Nikhil Kulkarni | Sagar Sahu | Mihir Vaidya
