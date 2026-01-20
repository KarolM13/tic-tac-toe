# 🎮 Kółko-Krzyżyk - REST API + PostgreSQL + Docker

Kompletny projekt spełniający wymagania:
- ✅ **REST API z pełnym CRUD** (Create, Read, Update, Delete)
- ✅ **Baza danych PostgreSQL** (przez Docker Compose)
- ✅ **Integracja z zewnętrznym API** (Advice Slip - cytaty wyświetlane na stronie)

---

## 🚀 Szybki Start - 1 Komenda!

```powershell
docker-compose up -d
```

**Gotowe!** Otwórz: **http://localhost:5555** 🎉

---

## 📋 Co Oferuje Projekt?

### 1. REST API z pełnym CRUD
- **POST** `/api/games` - Utwórz nową grę
- **GET** `/api/games` - Pobierz wszystkie gry (z paginacją)
- **GET** `/api/games/<id>` - Pobierz grę po ID
- **PUT** `/api/games/<id>` - Aktualizuj grę
- **DELETE** `/api/games/<id>` - Usuń grę
- **GET** `/api/games/stats` - Statystyki (wygrane, remisy)

### 2. Baza Danych PostgreSQL
- **PostgreSQL 15** przez Docker Compose
- **SQLAlchemy ORM** - mapowanie obiektowo-relacyjne
- **Automatyczne tworzenie tabel** przy starcie
- **Persistent volumes** - dane są zachowane po restarcie
- **Health checks** - aplikacja czeka na bazę

### 3. Zewnętrzne API + Wizualizacja
- **Advice Slip API** - losowe cytaty/porady
- **Endpoint:** `GET /api/quote`
- **🆕 Automatyczne wyświetlanie** na stronie po zakończeniu gry
- **Elegancki design** - animowane pudełko z cytatem
- **Obsługa błędów** - timeout, fallback messages

### 4. Gra Kółko-Krzyżyk
- **Multiplayer** - 2 graczy przez przeglądarkę
- **Real-time** - automatyczna synchronizacja
- **Zapisywanie** - każda gra trafia do bazy
- **Cytaty** - motywacyjna rada po każdej grze

---

## 🐳 Docker - Uruchomienie

> **💡 Nie musisz robić `docker build`!** Docker Compose automatycznie zbuduje obraz przy pierwszym uruchomieniu.

### Podstawowe komendy

```powershell
# Start (pierwszy raz: buduje obraz + pobiera PostgreSQL)
docker-compose up -d

# Jeśli zmieniłeś Dockerfile - przebuduj i uruchom
docker-compose up -d --build

# Ręczny build (opcjonalnie)
docker-compose build

# Sprawdź status
docker-compose ps

# Zobacz logi aplikacji
docker-compose logs -f app

# Zobacz logi bazy danych
docker-compose logs -f postgres

# Restart
docker-compose restart

# Stop
docker-compose down

# Stop + usuń dane (UWAGA!)
docker-compose down -v
```

### Co się uruchamia?

1. **PostgreSQL** (port 5432) - baza danych
2. **Flask App** (port 5555) - aplikacja
3. **Volume** - trwałe przechowywanie danych

**Aplikacja czeka** na bazę dzięki health check!

---

## 💻 Instalacja Lokalna (bez Dockera)

```powershell
# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom serwer (używa SQLite zamiast PostgreSQL)
python server.py
```

Aplikacja: **http://localhost:5555**

---

## 🧪 Testowanie

### Automatyczne testy
```powershell
python test_api.py
```

### Testy ręczne - PowerShell

```powershell
# Utwórz grę
$body = @{
    player_x_email = "test@example.com"
    player_x_nick = "Gracz1"
    player_o_email = "test2@example.com"
    player_o_nick = "Gracz2"
    board = @("X", "O", "X", "O", "X", "O", " ", " ", " ")
    winner = "X"
    status = "completed"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5555/api/games" -Method POST -Body $body -ContentType "application/json"

# Pobierz wszystkie gry
Invoke-RestMethod http://localhost:5555/api/games

# Statystyki
Invoke-RestMethod http://localhost:5555/api/games/stats

# Losowy cytat
Invoke-RestMethod http://localhost:5555/api/quote
```

---

## 📚 Dokumentacja

| Plik | Opis |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | ⚡ Szybki start (1 minuta) |
| [DOCKER_README.md](DOCKER_README.md) | 🐳 Pełna instrukcja Docker |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | 📚 Dokumentacja REST API z przykładami |
| [TEST_POWERSHELL.md](TEST_POWERSHELL.md) | 🧪 Testy w PowerShell |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 🏗️ Architektura systemu |
| [SUMMARY.md](SUMMARY.md) | 📋 Szczegółowe podsumowanie |

---

## 🗄️ Struktura Bazy Danych

### Tabela: `games`

| Kolumna | Typ | Opis |
|---------|-----|------|
| id | Integer | Primary Key |
| player_x_email | String(120) | Email gracza X |
| player_x_nick | String(80) | Nick gracza X |
| player_o_email | String(120) | Email gracza O |
| player_o_nick | String(80) | Nick gracza O |
| board | String(200) | Plansza jako JSON |
| winner | String(10) | 'X', 'O', 'DRAW', NULL |
| status | String(20) | 'completed', 'ongoing' |
| created_at | DateTime | Data utworzenia |
| updated_at | DateTime | Data aktualizacji |

---

## 🌐 Zewnętrzne API - Advice Slip

**URL:** https://api.adviceslip.com/advice

**Endpoint projektu:** `GET /api/quote`

**Przykład odpowiedzi:**
```json
{
  "ok": true,
  "quote": "The best time to plant a tree was 20 years ago. The second best time is now.",
  "author": "Advice Slip"
}
```

**Funkcje:**
- ✅ Automatyczne pobieranie po zakończeniu gry
- ✅ Wyświetlanie w eleganckim pudełku
- ✅ Animacja ładowania "💭 Ładowanie..."
- ✅ Obsługa błędów i timeoutów

---

## 📁 Struktura Projektu

```
tic-tac-toe/
├── server.py              # Główny serwer Flask + REST API
├── database.py            # Model SQLAlchemy + inicjalizacja
├── game_logic.py          # Logika gry kółko-krzyżyk
├── test_api.py            # Automatyczne testy
├── requirements.txt       # Zależności Python
├── Dockerfile             # Obraz Docker aplikacji
├── docker-compose.yml     # Orkiestracja (app + PostgreSQL)
├── .dockerignore          # Ignorowane pliki
├── .gitignore             # Git ignore
├── make.ps1               # Skrypty pomocnicze
├── templates/
│   └── index.html         # Frontend gry (HTML/CSS/JS)
├── README.md              # Ten plik
├── QUICKSTART.md          # Szybki start
├── DOCKER_README.md       # Instrukcja Docker
├── API_DOCUMENTATION.md   # Dokumentacja API
├── TEST_POWERSHELL.md     # Testy
├── ARCHITECTURE.md        # Architektura
└── SUMMARY.md             # Podsumowanie
```

---

## 🎯 Główne Endpointy API

### Gra
```
GET  /                     - Frontend gry
POST /api/join             - Dołącz do gry
POST /api/move             - Wykonaj ruch
GET  /api/state            - Pobierz stan gry
POST /api/reset            - Resetuj grę
```

### CRUD - Zarządzanie Grami
```
POST   /api/games          - Utwórz grę
GET    /api/games          - Lista gier (z paginacją)
GET    /api/games/<id>     - Pobierz grę
PUT    /api/games/<id>     - Aktualizuj grę
DELETE /api/games/<id>     - Usuń grę
GET    /api/games/stats    - Statystyki
```

### Zewnętrzne API
```
GET  /api/quote            - Losowy cytat/rada
```

---

## 💡 Szybkie Komendy (make.ps1)

```powershell
.\make.ps1 docker-up       # Start Docker
.\make.ps1 docker-down     # Stop Docker
.\make.ps1 docker-logs     # Logi
.\make.ps1 docker-rebuild  # Rebuild + restart
.\make.ps1 run             # Uruchom lokalnie
.\make.ps1 test            # Testy API
.\make.ps1 help            # Pomoc
```

---

## 📊 Funkcje Projektu

✅ **Gra multiplayer** - Kółko-krzyżyk przez przeglądarkę  
✅ **REST API CRUD** - Pełne zarządzanie grami  
✅ **PostgreSQL** - Baza produkcyjna w Docker  
✅ **Zewnętrzne API** - Advice Slip (cytaty)  
✅ **Cytaty na stronie** - Automatyczne wyświetlanie po grze  
✅ **Docker Compose** - Pełna orkiestracja  
✅ **Testy automatyczne** - test_api.py  
✅ **8 plików dokumentacji** - Kompletny opis  
✅ **Gotowe do produkcji** - Railway, Render, Heroku  

---

## 🚀 Deployment

### Railway / Render / Fly.io
Automatycznie wykrywają `Dockerfile`:
1. Podłącz repo GitHub
2. Ustaw zmienną `DATABASE_URL` na PostgreSQL
3. Deploy!

### Docker Hub
```powershell
docker build -t username/tictactoe:latest .
docker push username/tictactoe:latest
```

---

## 📦 Technologie

- **Backend:** Flask (Python)
- **Baza danych:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Frontend:** HTML/CSS/JavaScript
- **Konteneryzacja:** Docker + Docker Compose
- **Zewnętrzne API:** Advice Slip API
- **Testing:** Python requests library

---

## 🎯 Wymagania - Status

| Wymaganie | Status | Implementacja |
|-----------|--------|---------------|
| REST API z CRUD | ✅ DONE | POST, GET, PUT, DELETE w `/api/games` |
| Baza danych | ✅ DONE | PostgreSQL przez Docker Compose |
| Zewnętrzne API | ✅ DONE | Advice Slip API + wyświetlanie na stronie |

**Wszystkie wymagania spełnione!** 🎉

---

## 🆘 Troubleshooting

### Port 5555 zajęty?
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5555).OwningProcess | Stop-Process -Force
```

### Docker nie działa?
```powershell
docker-compose logs app
docker-compose logs postgres
```

### Baza nie łączy się?
```powershell
docker-compose down -v
docker-compose up -d
```

### Cytaty się nie ładują?
Sprawdź konsolę przeglądarki (F12) - może być problem z DNS w Docker.

---

## 👨‍💻 Autor

Projekt Kółko-Krzyżyk z REST API, PostgreSQL i integracją zewnętrznego API.

**Technologie:** Flask, PostgreSQL, Docker, SQLAlchemy, Advice Slip API

**GitHub:** KarolM13/tic-tac-toe

---

## 📄 Licencja

MIT

---

**Gotowe? Uruchom:** `docker-compose up -d` 🚀
