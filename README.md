# Education Platform

A modern educational platform built with Django that enables online learning and course management.

## Features

- User Authentication (Login/Register)
- Course Management
- Student Dashboard
- Modern UI with Bootstrap
- Responsive Design

## Tech Stack

- Django 5.1.7
- Python 3.x
- Bootstrap 5
- SQLite (Development) / PostgreSQL (Production)

## Team

- **Team Name:** INNOVATIVE STARS
- **Team Lead:** Naveen Kumar S
- **Members:**
  - Lakshmikanth S
  - Tamilarasan R
  - Pranesh S

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd education_platform
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
Create a `.env` file in the root directory and add:
```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
```

4. Run migrations
```bash
python manage.py migrate
```

5. Start the development server
```bash
python manage.py runserver
```

## Deployment

This project is configured for deployment on Render.com with the following features:
- Production-grade PostgreSQL database
- WhiteNoise for static files
- Security settings for production
- Gunicorn as the production server

## License

This project is licensed under the MIT License. 