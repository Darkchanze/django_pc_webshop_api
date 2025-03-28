# Django PC Webshop API - Local Development

A RESTful API for a PC Components Webshop, developed with Django REST Framework. This version is optimized for local development.

## 🚀 Features

- RESTful API with Django REST Framework
- JWT Authentication
- SQLite Database (for local development)
- Swagger/OpenAPI Documentation
- CORS Support
- Automatic API Documentation with drf-spectacular
- Hot-Reload for fast development

## 📋 Prerequisites

- Python 3.12 or higher
- pip (Python Package Manager)
- Git (optional, for version control)

## 🛠️ Installation

1. **Clone Repository** (if using Git)
```bash
git clone https://github.com/IhrUsername/django_pc_webshop_api.git
cd django_pc_webshop_api
```

2. **Create and Activate Virtual Environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
Create a `.env` file in the root directory:
```env
DATABASE_ADMIN_PASSWORD_LOCAL="YourLocalPassword"
PYTHONPATH=D:\Python Projects\django_pc_webshop_api
```

5. **Run Database Migrations**
```bash
python app/manage.py migrate
```

6. **Create Superuser**
```bash
python app/manage.py createsuperuser
```

7. **Collect Static Files**
```bash
python app/manage.py collectstatic --noinput
```

## 🚀 Start Development Server

1. **Activate Virtual Environment** (if not already done)
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Start Server**
```bash
python app/manage.py runserver
```

The server will be available at `http://127.0.0.1:8000`.

## 📚 API Documentation

The API documentation is available at the following URLs:
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## 🏗️ Project Structure

```
django_pc_webshop_api/
├── app/                    # Main application directory
│   ├── app/               # Django project configuration
│   ├── users/             # User management
│   ├── pc_components/     # PC components
│   ├── orders/           # Orders
│   └── static/           # Static files
├── venv/                  # Virtual environment
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── .gitignore            # Git ignore file
```

## 🔧 Development Configuration

### Database
- SQLite is used as local database
- Database file: `db.sqlite3`
- Migrations: `python app/manage.py makemigrations`
- Apply: `python app/manage.py migrate`

### Debug Mode
- Debug is enabled by default
- Detailed error messages
- Hot-Reload for code changes

### Static Files
- Local development: `python app/manage.py collectstatic`
- Static files are stored in `app/staticfiles`

## 🔒 Security

### Local Development
- JWT Authentication for API endpoints
- CORS configuration for local development
- Secure password handling
- Environment variables for sensitive data

### API Tests
```bash
# Run tests
python app/manage.py test

# Test specific app
python app/manage.py test users
python app/manage.py test pc_components
python app/manage.py test orders
```

## 🛠️ Useful Commands

```bash
# Reset database
python app/manage.py flush

# Create new superuser
python app/manage.py createsuperuser

# Open shell
python app/manage.py shell

# Reset migrations
python app/manage.py migrate --fake zero
python app/manage.py migrate
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Nico Wittemann** - [https://github.com/Darkchanze/django_pc_webshop_api](https://github.com/Darkchanze/django_pc_webshop_api)

## 🙏 Acknowledgments

- Django REST Framework Team
- All contributors and supporters
