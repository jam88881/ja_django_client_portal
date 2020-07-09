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