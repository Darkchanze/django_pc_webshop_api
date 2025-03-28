# Django PC Webshop API - Lokale Entwicklung

Eine RESTful API für einen PC-Komponenten Webshop, entwickelt mit Django REST Framework. Diese Version ist für die lokale Entwicklung optimiert.

## 🚀 Features

- RESTful API mit Django REST Framework
- JWT-Authentifizierung
- SQLite Datenbank (für lokale Entwicklung)
- Swagger/OpenAPI Dokumentation
- CORS-Unterstützung
- Automatische API-Dokumentation mit drf-spectacular
- Hot-Reload für schnelle Entwicklung

## 📋 Voraussetzungen

- Python 3.12 oder höher
- pip (Python Package Manager)
- Git (optional, für Versionskontrolle)

## 🛠️ Installation

1. **Repository klonen** (falls Sie Git verwenden)
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
PYTHONPATH=D:\Python Projects\django_pc_webshop_api
```

5. **Datenbank-Migrationen ausführen**
```bash
python app/manage.py migrate
```

6. **Superuser erstellen**
```bash
python app/manage.py createsuperuser
```

7. **Statische Dateien sammeln**
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
└── .gitignore            # Git Ignore-Datei
```

## 🔧 Entwicklungskonfiguration

### Datenbank
- SQLite wird als lokale Datenbank verwendet
- Datenbankdatei: `db.sqlite3`
- Migrationen: `python app/manage.py makemigrations`
- Anwenden: `python app/manage.py migrate`

### Debug-Modus
- Debug ist standardmäßig aktiviert
- Detaillierte Fehlermeldungen
- Hot-Reload für Code-Änderungen

### Statische Dateien
- Lokale Entwicklung: `python app/manage.py collectstatic`
- Statische Dateien werden in `app/staticfiles` gespeichert

## 🔒 Sicherheit

### Lokale Entwicklung
- JWT-Authentifizierung für API-Endpunkte
- CORS-Konfiguration für lokale Entwicklung
- Sichere Passwort-Handhabung
- Umgebungsvariablen für sensible Daten

### API-Tests
```bash
# Tests ausführen
python app/manage.py test

# Spezifische App testen
python app/manage.py test users
python app/manage.py test pc_components
python app/manage.py test orders
```

## 🛠️ Nützliche Befehle

```bash
# Datenbank zurücksetzen
python app/manage.py flush

# Neuen Superuser erstellen
python app/manage.py createsuperuser

# Shell öffnen
python app/manage.py shell

# Migrationen zurücksetzen
python app/manage.py migrate --fake zero
python app/manage.py migrate
```

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
- Alle Mitwirkenden und Unterstützer
