⚙️ Setup (Linux only)

Clone the repository into a workdir.

1.Create virtualenv dir, using python3.12 as executable, and activate it.
2.Inside the virtual environment run pip install -r requirements.txt.
3.Create and configure .env file inside project root. You can use .env.sample as an example.
4.In console run this commands:
- python manage.py makemigraions
- python manage.py migrate
5.Run server witch command:
- python manage.py runserver
