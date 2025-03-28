# Django PC Webshop API

Eine RESTful API für einen PC-Komponenten Webshop, entwickelt mit Django REST Framework.

## 🚀 Features

- RESTful API mit Django REST Framework
- JWT-Authentifizierung
- PostgreSQL Datenbank
- Swagger/OpenAPI Dokumentation
- CORS-Unterstützung
- Automatische API-Dokumentation mit drf-spectacular
- Deployment-ready für Render.com

## 📋 Voraussetzungen

- Python 3.12 oder höher
- PostgreSQL (für Produktion)
- pip (Python Package Manager)

## 🛠️ Installation

1. **Repository klonen**
```bash
git clone https://github.com/IhrUsername/django_pc_webshop_api.git
cd django_pc_webshop_api
```

2. **Virtuelle Umgebung erstellen und aktivieren**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Abhängigkeiten installieren**
```bash
pip install -r requirements.txt
```

4. **Umgebungsvariablen einrichten**
Erstellen Sie eine `.env` Datei im Hauptverzeichnis:
```env
DATABASE_ADMIN_PASSWORD_LOCAL="IhrLokalesPasswort"
DATABASE_ADMIN_PASSWORD_RENDER="IhrRenderPasswort"
PYTHONPATH=D:\Python Projects\django_pc_webshop_api
```

5. **Datenbank-Migrationen ausführen**
```bash
python app/manage.py migrate
```

6. **Statische Dateien sammeln**
```bash
python app/manage.py collectstatic --noinput
```

## 🚀 Entwicklungsserver starten

1. **Virtuelle Umgebung aktivieren** (falls noch nicht geschehen)
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Server starten**
```bash
python app/manage.py runserver
```

Der Server ist dann unter `http://127.0.0.1:8000` erreichbar.

## 📚 API-Dokumentation

Die API-Dokumentation ist unter folgenden URLs verfügbar:
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## 🏗️ Projektstruktur

```
django_pc_webshop_api/
├── app/                    # Hauptanwendungsverzeichnis
│   ├── app/               # Django-Projektkonfiguration
│   ├── users/             # Benutzer-Management
│   ├── pc_components/     # PC-Komponenten
│   ├── orders/           # Bestellungen
│   └── static/           # Statische Dateien
├── venv/                  # Virtuelle Umgebung
├── requirements.txt       # Python-Abhängigkeiten
├── .env                   # Umgebungsvariablen
├── build.sh              # Build-Skript für Render
├── Procfile              # Prozess-Konfiguration für Render
└── render.yaml           # Render.com Konfiguration
```

## 🔧 Konfiguration

### Lokale Entwicklung
- SQLite wird als Datenbank verwendet
- Debug-Modus ist aktiviert
- Statische Dateien werden lokal bereitgestellt

### Produktion (Render.com)
- PostgreSQL als Datenbank
- Debug-Modus ist deaktiviert
- Statische Dateien werden über WhiteNoise bereitgestellt
- Gunicorn als WSGI-Server

## 🚀 Deployment auf Render.com

1. **Repository auf GitHub pushen**
```bash
git add .
git commit -m "Deployment vorbereitet"
git push origin main
```

2. **Render.com Konfiguration**
- Neue Web Service erstellen
- GitHub Repository verbinden
- Umgebungsvariablen setzen:
  - `SECRET_KEY`
  - `DEBUG=False`
  - `ALLOWED_HOSTS`
  - `DATABASE_URL` (wird automatisch von Render gesetzt)

3. **Deployment**
- Render wird automatisch deployen
- Build-Skript wird ausgeführt
- Datenbank-Migrationen werden angewendet
- Statische Dateien werden gesammelt

## 🔒 Sicherheit

- JWT-Authentifizierung für API-Endpunkte
- CORS-Konfiguration für sichere Cross-Origin Requests
- Sichere Passwort-Handhabung
- Umgebungsvariablen für sensible Daten

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## 👥 Autoren

- **Ihr Name** - *Initiale Arbeit* - [IhrGitHub](https://github.com/IhrUsername)

## 🙏 Danksagungen

- Django REST Framework Team
- Render.com für das Hosting
- Alle Mitwirkenden und Unterstützer
