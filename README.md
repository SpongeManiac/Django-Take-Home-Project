# Django Take-Home Project
For this take-home project I was asked to impliment a CRUD system for several model types in Django without using the admin module to generate pages. As security was not apart of the requirements, I did not bother to encrypt password fields. However, this can easily be done with `django-cryptography`.

# Packages
Some packages are required to run this project. A pip compatible list of required packages is included in `requirements.txt`:
```
Django==4.0.5
django_tables2==2.4.1
httplib2==0.20.4
```

# Results
Here are a couple of screenshots to give you a small preview of what the finished project looks like.

## Home Page
![Home Page](https://github.com/SpongeManiac/Django-Take-Home-Project/blob/main/Screenshots/Home.png?raw=true "Home Page")

## Home Page - Authenticated
![Home Page - Authenticated](https://github.com/SpongeManiac/Django-Take-Home-Project/blob/main/Screenshots/Home%20-%20Authenticated.png?raw=true "Home Page - Authenticated")

## Software Table
![Software Table](https://github.com/SpongeManiac/Django-Take-Home-Project/blob/main/Screenshots/Software%20Table.png?raw=true "Software Table")

# Take-Home Project Requirements
In case you wish to replicate this project, here are the requirements I was given:

## Task 1
1. Implement sign-in and sign-up for user accounts with username/email and password.
    - Implementing features such as “forgot password,” etc., are not required.

## Task 2
1. Add the ability to create a customer via an HTML form
    - Only customer name is required
2. HTML page to list customers in the system
3. Button or form to delete a customer
4. Button or form to edit a customer

## Task 3
1. Add the ability to create a software entity via an HTML form
    - Software title
    - Software image (JPG or PNG)
      - This would typically be a logo (ex. PowerPoint logo)
    - Ability to associate a customer with a software
2. HTML page to list software in the system
3. Button or form to delete a software entity
4. Button or form to edit a software entity
    - Edit page should show the associated image, not just a link.

# Give it a try
I learned quite a lot with this assignment. You will become much more familiar with and confident in your Django skills if you can replicate the functionality of the example site.
