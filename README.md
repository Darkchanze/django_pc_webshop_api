# Django PC Webshop API

A RESTful API for a PC Components Webshop, developed with Django REST Framework.

## 🚀 Features

- RESTful API with Django REST Framework
- JWT Authentication
- PostgreSQL Database
- Swagger/OpenAPI Documentation
- CORS Support
- Automatic API Documentation with drf-spectacular
- Deployment-ready for Render.com

## 📋 Prerequisites

- Python 3.12 or higher
- PostgreSQL (for production)
- pip (Python Package Manager)

## 🛠️ Installation

1. **Clone Repository**
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
DATABASE_ADMIN_PASSWORD_RENDER="YourRenderPassword"
PYTHONPATH=D:\Python Projects\django_pc_webshop_api
```

5. **Run Database Migrations**
```bash
python app/manage.py migrate
```

6. **Collect Static Files**
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
├── build.sh              # Build script for Render
├── Procfile              # Process configuration for Render
└── render.yaml           # Render.com configuration
```

## 🔧 Configuration

### Local Development
- SQLite is used as database
- Debug mode is enabled
- Static files are served locally

### Production (Render.com)
- PostgreSQL as database
- Debug mode is disabled
- Static files are served via WhiteNoise
- Gunicorn as WSGI server

## 🚀 Deployment on Render.com

1. **Push Repository to GitHub**
```bash
git add .
git commit -m "Deployment prepared"
git push origin main
```

2. **Render.com Configuration**
- Create new Web Service
- Connect GitHub Repository
- Set environment variables:
  - `SECRET_KEY`
  - `DEBUG=False`
  - `ALLOWED_HOSTS`
  - `DATABASE_URL` (automatically set by Render)

3. **Deployment**
- Render will deploy automatically
- Build script will be executed
- Database migrations will be applied
- Static files will be collected

## 🔒 Security

- JWT Authentication for API endpoints
- CORS configuration for secure Cross-Origin Requests
- Secure password handling
- Environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Nico Wittemann** - [https://github.com/Darkchanze](https://github.com/Darkchanze)

## 🙏 Acknowledgments

- Django REST Framework Team
- Render.com for hosting
- All contributors and supporters
