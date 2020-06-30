# client-portal
Sparkfish Client Portal

# Requirements
This project is in development
-explore login to django site using Google or Linkedin - done
-create a space for invoices
-create a space for documents (contracts, NDA, etc.)
-create a dashboard
-google drive link

# Set Up Virtual Environment
```
conda create --name client-portal python=3.8
```
# Secrets
Obtain the file config.yml from a team member and place it in the env folder


# Activate Virtual Environment
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
trigger azure