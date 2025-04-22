# 🖥️ PC-Webshop – Seitenstruktur & Frontend-Konzept

## 🌐 Hauptseiten (pages/)

| Seite               | Zweck |
|--------------------|-------|
| **Home.jsx**            | Startseite mit Begrüßung, Highlights, Einstieg in den AI-Konfigurator |
| **PCBuilds.jsx**        | Liste aller gespeicherten/angebotenen PC-Builds |
| **PCBuildDetail.jsx**   | Detailansicht eines PC-Builds (Komponenten + Preis) |
| **Components.jsx**      | Katalog aller PC-Komponenten, filterbar nach Typ |
| **ComponentDetail.jsx** | Einzelanzeige einer Komponente (optional) |
| **Configurator.jsx**    | AI-Konfigurator: Budget + Zweck → PC-Build |
| **Cart.jsx**            | Warenkorb mit ausgewählten Produkten |
| **Checkout.jsx**        | Übersicht + Zahlungs-Button (später implementieren) |
| **Profile.jsx**         | Eigene Userdaten anzeigen |
| **Login.jsx**           | Anmelden |
| **Register.jsx**        | Registrieren |
| **NotFound.jsx**        | Fehlerseite für ungültige URLs |

---

## 🧩 Komponenten (components/)

| Komponente            | Zweck |
|-----------------------|-------|
| **Header.jsx**        | Navigation oben auf allen Seiten |
| **Footer.jsx**        | Seitenende, z. B. mit Links & Impressum |
| **PCBuildCard.jsx**   | Darstellung eines PC-Builds als Box |
| **ComponentCard.jsx** | Darstellung einer Komponente als Box |
| **ComponentFilter.jsx** | Filter-Elemente für den Katalog |
| **Button.jsx**        | Wiederverwendbarer Button |
| **Input.jsx**         | Wiederverwendbare Input-Felder oder Formularelemente |

---

## 📦 Struktur im Projekt

```plaintext
frontend/
└─ src/
   ├─ pages/
   │   ├─ Home.jsx
   │   ├─ PCBuilds.jsx
   │   ├─ PCBuildDetail.jsx
   │   ├─ Components.jsx
   │   ├─ ComponentDetail.jsx
   │   ├─ Configurator.jsx
   │   ├─ Cart.jsx
   │   ├─ Checkout.jsx
   │   ├─ Profile.jsx
   │   ├─ Login.jsx
   │   ├─ Register.jsx
   │   └─ NotFound.jsx
   ├─ components/
   │   ├─ Header.jsx
   │   ├─ Footer.jsx
   │   ├─ PCBuildCard.jsx
   │   ├─ ComponentCard.jsx
   │   ├─ ComponentFilter.jsx
   │   ├─ Button.jsx
   │   └─ Input.jsx
   ├─ styles/
   │   └─ global.css
   ├─ App.jsx
   └─ main.jsx
```
