# 🎮 Kółko-Krzyżyk - REST API + PostgreSQL + Docker

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
##  Instalacja Lokalna (bez Dockera)

```powershell
# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom serwer (używa SQLite zamiast PostgreSQL)
python server.py
```

Aplikacja: **http://localhost:5555**

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
## 📁 Struktura Projektu

```
tic-tac-toe/
├── server.py              # Główny serwer Flask + REST API
├── database.py            # Model SQLAlchemy + inicjalizacja
├── game_logic.py          # Logika gry kółko-krzyżyk
├── requirements.txt       # Zależności Python
├── Dockerfile             # Obraz Docker aplikacji
├── docker-compose.yml     # Orkiestracja (app + PostgreSQL)
├── .dockerignore          # Ignorowane pliki
├── .gitignore             # Git ignore
├── templates/
│   └── index.html         # Frontend gry (HTML/CSS/JS)
├── README.md              # Ten plik
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

## 📊 Funkcje Projektu

✅ **Gra multiplayer** - Kółko-krzyżyk przez przeglądarkę  
✅ **REST API CRUD** - Pełne zarządzanie grami  
✅ **PostgreSQL** - Baza produkcyjna w Docker  
✅ **Zewnętrzne API** - Advice Slip (cytaty)  
✅ **Cytaty na stronie** - Automatyczne wyświetlanie po grze  

---

## 📦 Technologie

- **Backend:** Flask (Python)
- **Baza danych:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Frontend:** HTML/CSS/JavaScript
- **Konteneryzacja:** Docker + Docker Compose
- **Zewnętrzne API:** Advice Slip API

---
## 👨‍💻 Autorzy
Tymoteusz Łach , Karol Mach

## Licencja
Projekt studencki