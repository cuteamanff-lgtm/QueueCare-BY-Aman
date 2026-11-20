# QueueCare — Smart Queue & Token Management

A fresh Django project with four connected screens:
- Home / landing page
- Visitor token registration
- Live queue status
- Staff dashboard with queue actions

## Setup (Windows PowerShell)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Staff dashboard: http://127.0.0.1:8000/staff/login/

## Notes
- This is a new project with a new SQLite database created by `migrate`.
- It does not contain your earlier database or admin account. Since you said no database had been created yet, the database will be created on your computer during setup.
- The four screens use the same purple/white visual style and animated 3D-inspired reception illustration.
- Token registration, live queue data, staff login, and queue actions are connected to Django.
- Create a staff user with `createsuperuser`, then use those credentials on the Staff Login page.
- For production deployment, configure `DEBUG`, `ALLOWED_HOSTS`, HTTPS, and a secure `SECRET_KEY`.
