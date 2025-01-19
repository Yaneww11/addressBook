### Project Documentation
[https://docs.google.com/document/d/1IL8xgpp-KMa1CkxTJG1lMVPZhwinh4rkEnirxwvwNW4/edit?usp=sharing](https://drive.google.com/file/d/1A7uBCbuJ_R2rmugplISZsY95HjACYiO0/view?usp=drive_link)

### ⚙️ Setup

Clone the repository into a workdir.

1. Create virtualenv dir, using python3.12 as executable, and activate it.

2. Inside the virtual environment run pip install -r requirements.txt.

3. Create and configure .env file inside project root. You can use .env.sample as an example.

4. In console run these commands:
   - python manage.py makemigrations
   - python manage.py migrate

5. Run server with the command:
   - python manage.py runserver

