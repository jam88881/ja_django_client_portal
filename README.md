# client-portal
Sparkfish Client Portal

# Requirements
This project is in development
-explore login to django site using Google or Linkedin - done
-create a space for invoices
-create a space for documents (contracts, NDA, etc.)
-create a dashboard
-google drive link
-the status  reports page (see mockup from Ross Hughes)

# Set Up Virtual Environment

```
conda create --name client-portal python=3.8
```

# Secrets
obtain from a team member (see below list) the chunk of code that gets placed at the bottom of \core\settings.py. 

People who have the secrets:
John Amarante
Patrick Watson

If you have the secret then please add yourself to the list.

# Activate Conda Virtual Environment

```
activate client-portal
```

# Requirements

```
pip3 install -r requirements.txt
```

# Install Django and Create Project 

```
pip install django
django-admin startproject sparkfishclientportal
cd sparkfishclientportal
python manage.py runserver
python manage.py migrate
python manage.py runserver
pip install django-allauth
```

# Run the website
```
python manage.py runserver
```

# Give yourself permission to see stuff
Go to the Django admin page and give yourselfpermission to see EXACTLY ONE trello board. At the time of writing this the application is not going to support a user having access to more than one trello board at a time. 
Here are the steps: 
1. in the browser go to http://127.0.0.1:8000/admin/ and login
2. Click on Users
3. Click on the user name to give permission to (probably yourself)
4. Add ONLY 1 Trello permission (based on what board you want to see)
5. Save
6. check the dashboard to make sure it is getting cards from the right board
